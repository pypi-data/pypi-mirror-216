"use strict";

const wall = document.getElementById("wall");
wall.style.zIndex = 1;

const debug = document.getElementById("debugBox");
if (debug) {
    debug.style.zIndex = 2;
    debug.innerHTML = "<table><tr><th>Month</th><th>Savings</th></tr><tr><td>January</td><td>$100</td></tr></table>";
    //debug.style.visibility = "hidden";
}

const shredder = document.getElementById("shredder");
shredder.style.zIndex = 2;

const fullscreen_element = document.getElementById("fullscreen_image");
fullscreen_element.style.zIndex = 6;
fullscreen_element.addEventListener("click", (e) => {
    console.log(`fullscreen_element:click()`);
    fullscreen_element.style.visibility = "hidden";
});

var pointer_coupled_to_moved_element = true;
var setInterval_ID;
function clearTimer() {
    clearInterval(setInterval_ID);
    setInterval_ID = undefined;
}
document.documentElement.addEventListener('mouseleave', () => {
    console.log('leaving the window');
});

document.documentElement.addEventListener('mouseenter', () => {
    console.log('entering the window');
});

const model_data = {
    "items": [],
};
const elements_in_model = {};

/// create an empty image used for dragging without a ghost
const empty_img = document.createElement('img');
empty_img.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';

function nice_id(id) {
    return id.slice(0, 8);
}

function extract_int_list(datatransfer, key) {
  for(const it of datatransfer.items) {
    if (it.type.startsWith(`${key}|`))  {
        return it.type.split("|").slice(1).map(x => parseInt(x));
    }
  }
}

function extract_element_by_id(datatransfer, key) {
  for(const it of datatransfer.items) {
    if (it.type.startsWith(`${key}|`))  {
        return document.getElementById(it.type.split("|")[1]);
    }
  }
}

function store_element_by_id(datatransfer, key, element) {
    datatransfer.setData(
        `${key}|${element.id}`, '');
}

function int_list(number_list) {
    return number_list.map(x => ~~x);
}

function store_int_list(datatransfer, key, number_list) {
    datatransfer.setData(
        `${key}|${number_list.map(x => (~~x).toString()).join("|")}`, '');
}

function enable_pointer_coupling(element) {
    pointer_coupled_to_moved_element = true;
    // element.style.backgroundColor = "#00ff00";
    clearTimer();
    console.log("COUPLE");
}

function handleElementDragging(e) {
    const dragged_element = extract_element_by_id(e.dataTransfer, "dragged_element_id");
//            if (dragged_element != elem) return;
    if (!dragged_element) return;
    const relpos = extract_int_list(e.dataTransfer, "dragged_element_relpos");
    // console.log(`${[wall.scrollLeft, wall.scrollTop]}`);
    if (!relpos) return;

    enable_pointer_coupling(dragged_element);

    dragged_element.style.left = `${e.clientX - relpos[0] + wall.scrollLeft}px`;
    dragged_element.style.top = `${e.clientY - relpos[1] + wall.scrollTop}px`;
}

function sendPostRequest(command, data, cb) {
    console.log(`  sendPostRequest ${command}`);
    const request = new XMLHttpRequest();
    const fd = new FormData();

    for (const [k, v] of Object.entries(data)) {
        console.log(`    | '${k}'=${v}`);
        // console.log(`append ${it.type} ${dataTransfer.getData(it.type)}`);
        // console.log(`add file ${it.name} ${it.type} ${it.size}}`);
        fd.append(k, v);
    }

    request.open("POST", command, true);
    request.onreadystatechange = () => {
        if (request.readyState == 4 && request.status == 200) {
            if (cb) {
                cb();
            }
        } else {
            console.log(`  ${request.readyState} ${request.status}`);
        }
    };
    request.send(fd);
    return request;
}

function sendDropData(x, y, dataTransfer) {
    console.log(`  sendDropData(${x}, ${y})`);
    const relpos = JSON.parse(dataTransfer.getData("relpos") || "[0, 0]");
    const data = {
        "pos": JSON.stringify(int_list([x - relpos[0], y - relpos[1]])),
    };

    [...dataTransfer.items].forEach(it => {
        if (["pos"].includes(it.type)) return;
        data[`${it.type}`] = dataTransfer.getData(it.type);
    });

    [...dataTransfer.files].forEach(it => {
        data[it.name] = it;
    });

    sendPostRequest(
        "add_elements",
        data,
        syncWithServer,
    );
}

function updatePosition(elementId, pos) {
    console.log(`  sendUpdate(${elementId}, ${pos})`);
    sendPostRequest(
        "update_position",
        {
            "id": elementId,
            "pos": JSON.stringify(pos)
        },
    );
}

function removeItem(elementId) {
    console.log(`  removeItem(${elementId})`);
    sendPostRequest(
        "remove_item",
        {
            "id": elementId,
        },
        syncWithServer,
    );
}

function setDynamicElementProperties(element) {
    // element.style.backgroundColor = "rgb(200, 200, 250)";
    element.style.zIndex = 3;
}

function buildElements() {
    document.getElementById("message").innerHTML = (
        model_data.items.length == 0 ?
        "Nothing here yet<br>Try to drop something!" :
        "");

    wall.innerHTML = "";
    for (var member in elements_in_model) delete elements_in_model[member];

    model_data.items.forEach(it => {
        console.log(`  item: ${it} ${it.pos} ${Object.keys(it)}`);

        const new_element = document.createElement("div");
        new_element.id = it.id;
        new_element.draggable = true;
        new_element.style.left = `${it.pos[0]}px`;
        new_element.style.top = `${it.pos[1]}px`;
        new_element.style.zIndex = 3;

        if (it["text/html"]) {
            new_element.setAttribute("class", "textBox");
            new_element.innerHTML = it["text/html"];
            // new_element.style.textAlign = "center";
        } else if (it["text/plain"]) {
            new_element.setAttribute("class", "textBox");
            new_element.innerText = it["text/plain"];
        } else if (it["files"] && it["files"].length > 0) {
            const file = it["files"][0];
            const filename = file["safe_name"];
            const img_element = document.createElement("img");
            img_element.setAttribute('src', `preview/${filename}`);
            img_element.style.width = file["preview-width"] || "6cm";
            img_element.style.pointerEvents = "none";
            img_element.style.display = "block";
            new_element.setAttribute("class", "pictureBox");
            new_element.setAttribute('title', `${file["hovertext"] || filename}`);
            new_element.appendChild(img_element);
            new_element.addEventListener("click", (e) => {
                console.log(`element:click()`);
                document.getElementById("fullscreen_img").setAttribute('src', `file/${filename}`);
                fullscreen_element.style.visibility = "visible";
            });
        } else {
            new_element.setAttribute("class", "pictureBox");
            const dim = it.dim || ["3cm", "3cm"];
            new_element.style.width = "3cm";//`${it.pos[0]}px`;
            new_element.style.height = "3cm";//`${it.pos[1]}px`;
        }
        wall.appendChild(new_element);
        elements_in_model[new_element.id] = it;

        new_element.addEventListener("dragstart", (e) => {
            /// store information about dragged item in order to be able to move it
            const elem = e.currentTarget;
            const rect = elem.getBoundingClientRect();
            const model_item = elements_in_model[elem.id];
            const rel_pos = int_list([e.clientX - rect.x, e.clientY - rect.y]);
            const start_pos = int_list([elem.offsetLeft, elem.offsetTop]);
            console.log(`element:dragstart id='${nice_id(elem.id)}' pointer=${int_list([e.clientX, e.clientY])} pos=${int_list([rect.x, rect.y])} rel=${rel_pos}`);

            e.stopPropagation();
            // e.preventDefault();

            e.dataTransfer.setDragImage(empty_img, 0, 0);

            e.dataTransfer.effectAllowed = "all";
            e.dataTransfer.dropEffect = "copy";

            store_element_by_id(e.dataTransfer, "dragged_element_id", elem);
            store_int_list(e.dataTransfer, "dragged_element_startpos", start_pos);
            store_int_list(e.dataTransfer, "dragged_element_relpos", rel_pos);

            if ("text/plain" in model_item) {
                e.dataTransfer.setData("text/plain", it["text/plain"]);
            }
            if (model_item["files"] && model_item["files"].length > 0) {
                const filename = `${model_item["files"][0]["safe_name"]}`;
                e.dataTransfer.setData('text/plain', filename);
                e.dataTransfer.setData('text/html', `<h1>${filename}</h1>`);
                e.dataTransfer.setData('text/uri-list', new URL(`file/${filename}`, window.location).href);
            }
            elem.style.zIndex = 5;
            //elem.style.pointerEvents = "none";
        });

        new_element.addEventListener("dragend", (e) => {
            const elem = e.currentTarget;
            console.log(`element:dragend id=${nice_id(elem.id)}`);
            clearTimer();

            setDynamicElementProperties(elem);

            //elem.style.pointerEvents = "auto";

            if (pointer_coupled_to_moved_element) {
                const rect = elem.getBoundingClientRect();
                updatePosition(elem.id, int_list([rect.x + wall.scrollLeft, rect.y + wall.scrollTop]));
            } else {
                console.log("RESET");
                const startpos = extract_int_list(e.dataTransfer, "dragged_element_startpos");
                elem.style.left = `${startpos[0]}px`;
                elem.style.top = `${startpos[1]}px`;
            }
        });

        new_element.addEventListener("dragover", (e) => {
            const elem = e.currentTarget;
            console.log(`element:dragover ${nice_id(elem.id)} dragged_element=${nice_id(elem.id)}`);
            // without it `dragenter` and `dragleave` of other elements
            e.stopPropagation();

            //e.preventDefault(); // without it `dragover` won't reach wall
            handleElementDragging(e);
        });

        new_element.addEventListener("dragenter", (e) => {
            const elem = e.currentTarget;
            console.log(`element:dragenter id=${nice_id(elem.id)}`);
            if (extract_element_by_id(e.dataTransfer, "dragged_element_id") == elem) {
                enable_pointer_coupling(elem);
            }
        });

        new_element.addEventListener("dragleave", (e) => {
            const elem = e.currentTarget;
            console.log(`element:dragleave id=${nice_id(elem.id)}`);

            e.stopPropagation();  // needed
            //e.preventDefault();

            if (extract_element_by_id(e.dataTransfer, "dragged_element_id") == elem) {
                if (!setInterval_ID) {
                  setInterval_ID = setInterval(() => {
                    console.log(`DECOUPLE ${e}`);
                    clearTimer();
                    pointer_coupled_to_moved_element = false;
                    // elem.style.backgroundColor = "#ff0000";
                  }, 100);
                }
            }
        });
    });
}

function syncWithServer() {
    fetch("model")
    .then( response => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    })
    .then( json => {
        console.log(`got ${json} keys=${Object.keys(json)}`);
        Object.assign(model_data, json);
        buildElements();
    })
    .catch( err => {
        console.error(`Fetch problem: ${err.message}`);
    });
}

function inspectDataTransfer(dataTransfer) {
    console.log(`dropEffect ${dataTransfer.dropEffect}`);
    console.log(`effectAllowed ${dataTransfer.effectAllowed}`);

    [...dataTransfer.types].forEach(it => {
        console.log(`  type ${it}`);
    });

    [...dataTransfer.items].forEach(it => {
        console.log(`  item ${it} ${it.type} ${dataTransfer.getData(it.type)}`);
    });

    [...dataTransfer.files].forEach(it => {
        console.log(`  file ${it} ${it.name} ${it.type} ${it.size}`);
    });
}

/// Main function - defines resize behavior and initially fetches
/// data from server
(function() {
    window.addEventListener("keydown", (e) => {
        console.log(`window:keydown key=${e.key}`);
        if (e.key == "Escape") {
            fullscreen_element.style.visibility = "hidden";
        }
    });
    wall.addEventListener("drop", (event) => {
        console.log(`wall:drop ${event} ${event.offsetX} ${event.offsetY}`);

        /// avoids leaving the page because the browser decides to
        /// display the dropped element instead
        event.preventDefault();

        /// happened somtimes during debugging..
        if (!event.dataTransfer) {
            console.error(`drop ${event} ${event.offsetX} ${event.offsetY}`);
            return;
        }

        /// don't handle elements which have just been moved
        if (extract_int_list(event.dataTransfer, "dragged_element_startpos")) {
            return;
        }

        inspectDataTransfer(event.dataTransfer);

        sendDropData(
            event.offsetX + wall.scrollLeft,
            event.offsetY + wall.scrollTop,
            event.dataTransfer);
        return;

        [...event.dataTransfer.files].forEach(file => {
            if (file.type.match(/image.*/)) {
                const reader = new FileReader();
                reader.onload = (progress) => {
                    const img = document.createElement('img');
                    img.src = progress.target.result;
                    document.body.appendChild(img);
                }
                reader.readAsDataURL(file); // start reading the file data.
            }
        });
    });

    wall.addEventListener("dragover", (e) => {
        console.log(`wall:dragover`);

        /// needed to accept the drag event
        e.preventDefault();
        // e.stopPropagation();  // needed?

        /// this prevents data to be removed on source side
        e.dataTransfer.dropEffect = "copy";
        handleElementDragging(e);
    });

    wall.addEventListener("dragenter", (e) => {
        console.log(`wall:dragenter ${e} ${Object.keys(e)}`);

        //e.preventDefault();
        //e.stopPropagation();
    });

    wall.addEventListener("dragleave", (e) => {
        console.log(`wall:dragleave ${e} ${Object.keys(e)}`);

        //e.preventDefault();
        //e.stopPropagation();
    });

    [...document.getElementsByClassName("filterBox")].forEach(elem => {
        elem.style.zIndex = 6;
        elem.addEventListener("dragstart", (e) => {
            console.log(`filter:dragstart`);
            e.dataTransfer.setData('relpos', JSON.stringify([e.offsetX, e.offsetY]));
            console.log(`dragstart ${e} ${e.offsetX} ${e.offsetY}`);
        });
        elem.addEventListener("dragstop", (e) => {
            console.log(`filter:dragstop`);
        });
        elem.addEventListener("drop", (e) => {
            console.log(`filter:drop`);
            // needed to prevent the browser to just display the dropped element
            event.preventDefault();
            elem.style.backgroundColor = "#d0d0ff";
            console.log(`magic ${elem.id}`);
        });
        elem.addEventListener("dragenter", (e) => {
            console.log(`filter:dragenter`);
            elem.style.backgroundColor = "#a0a0ff";
        });
        elem.addEventListener("dragleave", (e) => {
            console.log(`filter:dragleave`);
            elem.style.backgroundColor = "#d0d0ff";
        });
        elem.addEventListener("dragover", (e) => {
            console.log(`filter:dragover`);
            e.preventDefault(); // needed
            e.dataTransfer.dropEffect = "copy";
        });
    });

    //this prevents drag events but not strangely not parents dragenter/dragleave
    //shredder.style.pointerEvents = "none";

    shredder.addEventListener("drop", (e) => {
        console.log(`shredder:drop`);
        // needed to prevent the browser to just display the dropped element
        event.preventDefault();
        shredder.style.backgroundColor = "#ffd0d0";
        const dragged_element = extract_element_by_id(e.dataTransfer, "dragged_element_id");

        if (!dragged_element) return;
        console.log(`shredder ${dragged_element.id}`);
        removeItem(dragged_element.id);
    });
    shredder.addEventListener("dragenter", (e) => {
        console.log(`shredder:dragenter`);
        shredder.style.backgroundColor = "#ffa0a0";
    });
    shredder.addEventListener("dragleave", (e) => {
        console.log(`shredder:dragleave`);
        shredder.style.backgroundColor = "#ffd0d0";
    });
    shredder.addEventListener("dragover", (e) => {
        // console.log(`shredder:dragover`);
        //e.preventDefault(); // needed
    });

    syncWithServer();
})();

