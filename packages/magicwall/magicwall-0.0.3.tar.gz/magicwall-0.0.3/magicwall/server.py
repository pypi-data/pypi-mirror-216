#!/usr/bin/env python3
#                        _                    _ _   _
#  _ __ ___   __ _  __ _(_) _____      ____ _| | | (_) ___
# | '_ ` _ \ / _` |/ _` | |/ __\ \ /\ / / _` | | | | |/ _ \
# | | | | | | (_| | (_| | | (__ \ V  V / (_| | | |_| | (_) |
# |_| |_| |_|\__,_|\__, |_|\___| \_/\_/ \__,_|_|_(_)_|\___/
#                  |___/
#
# magicwall.io - a magic wall
# Copyright (C) 2023 - Frans Fürst
#
# magicwall.io is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# magicwall.io is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details
# at <http://www.gnu.org/licenses/>.
#

"""magicwall.io server implementation
"""

import argparse
import asyncio
import json
import logging
import sys
import tarfile
import tempfile
import threading
import uuid
from argparse import Namespace as Args
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, cast

import exifread
import markdown
import yaml
from PIL import Image, UnidentifiedImageError
from quart import Quart, Response, redirect, render_template, request, send_file
from werkzeug.datastructures import FileStorage

from magicwall.common import GenMap, GenMapArray, MutableGenMap, Tag
from magicwall.utils import fs_changes, setup_logging, watchdog


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("mw.server")


@dataclass
class File:
    """Models a file associated with an Item element"""

    name: str
    safe_name: str
    hovertext: str | None = None
    preview_width: str | None = None

    @staticmethod
    def from_file_storage(wall: str, name: str, fileob: FileStorage) -> "File":
        """Creates File element from what we get from a POST request"""
        safe_name = store_file(name, wall, fileob)
        has_preview = Path(safe_name).suffix.lower() in {".png", ".jpg", ".gif", ".jpeg"}
        return File(name=name, safe_name=safe_name, preview_width="6cm" if has_preview else "1.5cm")

    @staticmethod
    def from_tree(tree: GenMap) -> "File":
        """Creates File element from untyped structure"""
        if isinstance(tree, File):
            return tree
        return File(
            name=str(tree["name"]),
            safe_name=str(tree["safe_name"]),
            hovertext=cast(str | None, tree.get("hovertext")),
            preview_width=cast(str | None, tree.get("preview_width")),
        )


@dataclass
class Item:
    """Models one visible element on a wall"""

    id: str  # pylint: disable=invalid-name
    pos: tuple[int, int]
    files: MutableSequence[File]
    text_plain: str | None = None
    text_html: str | None = None

    @staticmethod
    def from_tree(tree: GenMap) -> "Item":
        """Creates Item from untyped structure"""
        return Item(
            id=str(tree.get("id", uuid.uuid4())),
            pos=cast(tuple[int, int], tree.get("pos", [0, 0])),
            files=[File.from_tree(item) for item in cast(Sequence[GenMap], tree["files"])],
            text_plain=cast(str | None, tree.get("text_plain") or tree.get("text/plain")),
            text_html=cast(str | None, tree.get("text_html") or tree.get("text/html")),
        )


@dataclass
class Model:
    """Stores a magicwall model"""

    items: MutableSequence[Item] = field(default_factory=list)

    @staticmethod
    def from_yaml(filepath: Path) -> "Model":
        """Creates Model from YAML file"""
        with open(filepath, encoding="utf-8") as model_file:
            return Model.from_tree(yaml.load(model_file, Loader=yaml.FullLoader))

    @staticmethod
    def from_json(filepath: Path) -> "Model":
        """Creates Model from JSON file"""
        with open(filepath, encoding="utf-8") as model_file:
            return Model.from_tree(json.load(model_file))

    @staticmethod
    def from_tree(tree: GenMap) -> "Model":
        """Creates Model from untyped structure"""
        return Model(
            items=[Item.from_tree(cast(GenMap, item)) for item in cast(GenMapArray, tree["items"])]
        )


def to_external(data: GenMap) -> GenMap:
    """Makes some corrections to keys of dicts"""
    return {
        {
            "preview_width": "preview-width",
            "text_plain": "text/plain",
            "text_html": "text/html",
        }.get(key, key): value
        for key, value in data.items()
    }


def mw_representer(dumper: yaml.Dumper, data: object) -> yaml.nodes.Node:
    """Makes some corrections to keys of dicts"""
    return dumper.represent_dict(to_external(data.__dict__))


def extract_tags(filename: str) -> Mapping[str, str]:
    """Reads interesting EXIF tags from given file"""
    # for PNG
    #  https://blender.stackexchange.com/questions/35504/read-image-metadata-from-python
    def extract_date(tags: Mapping[str, Tag]) -> str:
        with suppress(KeyError):
            return tags["EXIF DateTimeOriginal"].values  # datetime.strptime(, '%Y:%m:%d %H:%M:%S')
        return "no-date"

    with open(filename, "rb") as file:
        tags = exifread.process_file(file)
        return {"date": extract_date(tags)}


class Wall:
    """Interfaces one specific magicwall."""

    def __init__(self, wall_name: str) -> None:
        self._folder = app.config["UPLOAD_FOLDER"] / wall_name
        self._folder.mkdir(parents=True, exist_ok=True)
        self._model: Model = Model()
        self._lock = threading.Lock()
        self.load()

    def load(self) -> None:
        """Read a wall from disk"""
        with self._lock:
            with suppress(FileNotFoundError):
                try:
                    self._model = Model.from_yaml(self._folder / "model.yaml")
                except FileNotFoundError:
                    self._model = Model.from_json(self._folder / "model.json")
                for i in self._model.items:
                    for file in i.files:
                        if not file.hovertext:
                            tags = extract_tags(self._folder / file.name)
                            file.hovertext = f"{file.name}\n{tags['date']}"
                        if not file.preview_width:
                            file.preview_width = (
                                "6cm"
                                if Path(file.name).suffix.lower()
                                in {".png", ".jpg", ".gif", ".jpeg"}
                                else "1.5cm"
                            )

    def model(self) -> Model:
        """RW access to the model structure"""
        return self._model

    def save(self) -> None:
        """Store to disk"""
        with self._lock:
            path = self._folder / "_model.yaml"
            log().debug("write wall model file %s", path)
            # make sure we don't delete data by stumbling over a failing save
            with open(path, "w", encoding="utf-8") as model_file:
                yaml.dump(self._model, model_file)
            (self._folder / "_model.yaml").rename(self._folder / "model.yaml")

    def add_item(self, item: Item) -> str:
        """Adds a visible item to the wall and saves the wall"""
        self._model.items.append(item)
        self.save()
        return item.id

    def dirty(self) -> None:
        """Does whatever is needed after a file inside a wall directory has been touched"""
        self.load()


class WallStore:
    """Singleton Wall container"""

    _walls: MutableMapping[str, Wall] = {}
    _instance = None

    def __new__(cls) -> "WallStore":
        if cls._instance is None:
            cls._instance = super(WallStore, cls).__new__(cls)
        return cls._instance

    def get(self, name: str) -> Wall:
        """Returns a Wall element identified by its @name. Creates it if it doesn't exist yet."""
        if name not in self._walls:
            self._walls[name] = Wall(name)
        return self._walls[name]

    def loaded(self, name: str) -> bool:
        """Returns True if a wall is already loaded to memory and thus might have to be reloaded"""
        return name in self._walls


def wall_from_name(name: str) -> Wall:
    """Convenience function to avoid manual access to the WallStore singleton"""
    return WallStore().get(name)


def parse_args(argv: Sequence[str]) -> Args:
    """Parses the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8006)
    parser.add_argument("-d", "--debug", action="store_true")
    return parser.parse_args(argv)


def parse_json_value(name: str, json_string: str) -> str | tuple[int, int] | None:
    """Returns an element indicated by @name from JSON mapping parsed from @json_string if
    applicable, the raw input string otherwise"""
    if name in {"pos"}:
        with suppress(json.JSONDecodeError):
            return int((pos := json.loads(json_string))[0]), int(pos[1])
        print(f"XX{json_string}")
        return None
    return json_string


def secure_filename(filename: str) -> str:
    """Creates a valid filename from a string by replacing invalid characters"""
    return filename


def store_file(name: str, wall: str, fileobj: FileStorage) -> str:
    """Stores a file provided via POST on disk"""
    print(f"file: {name} / {fileobj}")
    assert fileobj.filename
    safe_name = secure_filename(fileobj.filename)
    save_path = app.config["UPLOAD_FOLDER"] / wall / safe_name
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fileobj.save(save_path)
    return safe_name


def create_preview(input_file_name: Path, output_file: Path) -> Path | None:
    """Creates a thumbnail of given input file, whatever that means"""
    basewidth = 1000
    with suppress(UnidentifiedImageError):
        input_image = Image.open(input_file_name)
        hsize = int(input_image.size[1] * basewidth / input_image.size[0])
        converted_image = input_image.resize(
            (basewidth, hsize),
            Image.ANTIALIAS,
        ).convert("RGB")

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_file = Path(tmp_dir) / "preview.jpeg"
            print(f"create temp file {temp_file}")
            # this command might fail and nevertheless create a file
            converted_image.save(temp_file, "JPEG", exif=input_image.info.get("exif", b""))
            output_file.write_bytes(temp_file.read_bytes())
            return temp_file
        return Path("static/unknown.jpg")

        # file_object = io.BytesIO()
        # img.resize((basewidth, hsize), Image.ANTIALIAS).save(file_object, 'JPEG')
        # file_object.seek(0)
    return None


@watchdog
async def watch_fs_changes() -> None:
    """Observe changes to filesystem and mark walls dirty"""
    wall_dir = app.config["UPLOAD_FOLDER"]
    async for changed_path in fs_changes(wall_dir, timeout=1, postpone=True):
        log().info("file %s changed", changed_path)
        if not changed_path.is_relative_to(wall_dir):
            continue
        if len(changed_path.parts) <= len(wall_dir.parts):
            continue
        if not WallStore().loaded(wall_name := changed_path.parts[len(wall_dir.parts)]):
            continue
        WallStore().get(wall_name).dirty()


app = Quart(
    __name__,
    # static_url_path="/"
)


@app.route("/")
def root() -> Response:
    """Landing page, creates a dummy site 'first'"""
    # here we might copy some default wall and give it a random name
    return cast(Response, redirect("first"))


@app.route("/<wall_name>/")
async def index(wall_name: str) -> str:  # pylint: disable=unused-argument
    """Returns the (static) magicwalll HTML site"""
    # TODO: use Blueprints:
    # https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
    # return open(app.config["BASE_FOLDER"] / "magicwall.html").read()
    return await render_template("magicwall.html")


@app.route("/<wall_name>/model", methods=["GET"])
def model(wall_name: str) -> str:
    """Retrieves the whole model of a wall"""
    model_ = wall_from_name(wall_name).model()
    return json.dumps(model_, default=lambda __o: to_external(__o.__dict__))


@app.route("/<wall_name>/file/<name>", methods=["GET"])
async def get_file(wall_name: str, name: str) -> Response:
    """Retrieves a file specified by @name"""
    return await send_file(app.config["UPLOAD_FOLDER"] / wall_name / name)


@app.route("/<wall_name>/preview/<name>", methods=["GET"])
async def get_file_preview(wall_name: str, name: str) -> Response:
    """GETs a thumbnail for file indicated by @name"""
    if Path(name).suffix.lower() in {".gif"}:
        preview_filename = app.config["UPLOAD_FOLDER"] / wall_name / name
    elif Path(name).suffix.lower() in {".jpeg", ".jpg", ".png"}:
        preview_filename = app.config["UPLOAD_FOLDER"] / wall_name / f"{name}.preview.jpeg"
        if not preview_filename.exists():
            create_preview(
                app.config["UPLOAD_FOLDER"] / wall_name / name,
                preview_filename,
            )
    else:
        return await send_file("static/unknown.png")
    return await send_file(preview_filename)


@app.route("/<wall_name>/add_elements", methods=["POST"])
async def add_elements(wall_name: str) -> str:
    """This function takes quite informal input from raw drop/paste data and
    turns it into something structured.
    """
    request_data: MutableGenMap = {
        name: parse_json_value(name, itemobj) for name, itemobj in (await request.form).items()
    }
    request_data["files"] = [
        # this is formally incorrect but works for now
        cast(GenMap, File.from_file_storage(wall_name, name, fileob))
        for name, fileob in (await request.files).items()
    ]
    if "text/plain" in request_data:
        request_data["text/html"] = markdown.markdown(
            str(request_data["text/plain"]),
            extensions=[
                "extra",
                "codehilite",
                "markdown_checklist.extension",
            ],
        )

    print(f"add on {wall_name}: {request_data}")

    return wall_from_name(wall_name).add_item(Item.from_tree(request_data))


@app.route("/<wall_name>/update_position", methods=["POST"])
async def update_position(wall_name: str) -> Literal["OK", "NOK"]:
    """Moves item indicated by `id` to another position"""
    form = await request.form
    item_id = form["id"]
    new_pos = json.loads(form["pos"])
    wall = wall_from_name(wall_name)
    print(item_id, new_pos)
    for item in wall.model().items:
        if item.id == item_id:
            item.pos = new_pos
            wall.save()
            return "OK"
    return "NOK"


@app.route("/<wall_name>/remove_item", methods=["POST"])
async def remove_item(wall_name: str) -> Literal["OK", "NOK"]:
    """Removes item indicated by `id`"""
    form = await request.form
    item_id = form["id"]
    wall = wall_from_name(wall_name)

    for item in (items := wall.model().items):
        if item.id == item_id:
            items.remove(item)
            wall.save()
            return "OK"
    return "NOK"


@app.route("/<wall_name>/download", methods=["GET"])
async def download_archive(wall_name: str) -> Response:
    """Creates a tar archive from wall indicated by @wall_name"""
    tar_file_name = app.config["UPLOAD_FOLDER"] / f"{wall_name}.tar.gz"
    with tarfile.open(tar_file_name, "w:gz") as tar:
        tar.add(app.config["UPLOAD_FOLDER"] / wall_name, arcname=wall_name)

    return await send_file(tar_file_name)


@app.before_serving
async def start_tasks() -> None:
    """Starts asynchronous background tasks after webserver has been started"""
    asyncio.ensure_future(watch_fs_changes())


def main() -> int:
    """Run Flask"""
    setup_logging(level="DEBUG")

    args = parse_args(sys.argv[1:])

    yaml.add_representer(File, mw_representer)
    yaml.add_representer(Item, mw_representer)
    yaml.add_representer(Model, mw_representer)

    app.config["BASE_FOLDER"] = Path(__file__).parent
    app.config["UPLOAD_FOLDER"] = Path(".").absolute() / "walls"
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    app.run(
        host="0.0.0.0",
        port=args.port,
        debug=args.debug,
        use_reloader=False,
        # loop=asyncio.get_event_loop(),
    )
    return 0


if __name__ == "__main__":
    main()
