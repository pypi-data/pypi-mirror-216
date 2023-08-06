# magicwall.io

View, share, compose, edit visual, textual and acustical content and apply
arbitraty effects on it.

Consider magicwall a combination of file sharing, content presentation, blogging
and programmable playground. Create your own wall by just navigating to it, add
content by dropping or pasting files and arbitrary data from outside, arrange it
spacially and write code which can be applied to any of that content.

Other people you shared the link to your wall with can copy its content using
the drag&drop or copy&paste mechanism or by using Git to clone the whole wall
content.

Use it: [magicwall.io](https://magicwall.io)

Have your own:
```
git clone https://projects.om-office.de/frans/magicwall.io
```

Have Python3.7+ and `flask` installed and run
```
magicwall.io/magicwall.py
```

Or use a Docker container:
```
magicwall.io/run-server
```

Visit the [locally created site](http://localhost:8006)


##  Milestone 1

Requirements for basic usage as simple blogging system and for concept
demonstration.

* [x] <magicwall.io> registered and used with https
* [x] Previews of files get turned into HTML elements
* [x] Visualization works (geometry)
* [x] Create element from dropping a filter element, text or images
* [x] Drag/drop of element inside wall area moves it
* [x] Drag/drop of element outside wall area copies as file
* [x] Drag/drop of element on remove field removes it
* [x] Pictures get displayed
* [x] Basic Markdown text formatting works
* [x] Basic file info on mouse hover
* [ ] Drag/drop works on mobile
* [ ] Basic text editing
* [ ] Basic "filter" work (e.g. b/w for images and running python)
* [ ] Auto-update (-> collab mode)
* [ ] Pasting of text, image data or image files works as dropping
* [ ] Multiple elements can be dropped/pasted at once


##  Milestone 2

* [ ] User / access permission control
* [ ] Arbitrary files can be added for sharing
* [ ] CTRL+drag&drop copies
* [ ] Resize elments
* [ ] Caching mechanism
* [ ] Square-select multiple items


## Future

* Notification on change
* Fullscreen / slideshow mode
* Undo-stack
* Config-YAML
* Filter-Hub
* Search
* Offline use
* Git support
* Editor
* Links
* Copy / Paste between sites
* Video
* Live-Update (Weather)
* Support for folders -> Tree
* Tree-Structure (allows entering)
* Filter chaining/stacking


## Use cases

* Picture gallery
* Blogging
* Mind mapping
* Algorithm demonstration / education (-> Jupyter)
* File exchange
* Note taking


## Magic ideas

* Document optimizer
* Simple auto optimize images (contrast, etc)
* Simple BW images
* Polaroid images
* Configurable Image with roation, cropping, color improvement, vignetting
* Files to animation
* SVG background
* Auto align by date
* fetch URL -> return generated HTML


## License

For all code contained in this repository the rules of GPLv3 apply unless
otherwise noted. That means that you can do what you want with the source
code as long as you make the files with their original copyright notice
and all modifications available.

See [GNU / GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.


## Contributing

Before contributing consider installing a pre-commit which runs some static
checks, code cleaners and unit tests:

```
ln -s ../../.git-pre-commit .git/hooks/pre-commit
```
This `pre-commit` just runs `./qualitygate`, which you can also run manually.


## Paradigms

* each site can be seen as a filesystem folder managed and visualized by
  magicwall.io. I.e. applying an arbitrary folder should give nice results
  magically.


## Random ideas

* Visual Filter (looks like polaroid filter and can be moved over arbitrary elements)
* Transformer filter


## Technical challenges

Feel free to help me with each of those questions

* how to recursively stack drop areas
* how to keep instances across browsers in sync, see
    - https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API
    - https://stackoverflow.com/questions/55700655/store-data-offline-and-sync-once-online-using-react-native-and-redux-store


## Read this

* my [to-go scribble](https://notes.om-office.de/tGG_sJgTThut6-v8F72xYQ#)

* https://stackoverflow.com/questions/57014217/putting-an-image-from-flask-to-an-html5-canvas
* https://stackoverflow.com/questions/10929941/make-drag-and-drop-uploader-in-flask
* https://codepen.io/anatomic/pen/DJgrvq
* https://stackoverflow.com/questions/4288253/html5-canvas-100-width-height-of-viewport

* [Dropzone](https://www.dropzone.dev/js/)

* https://www.reddit.com/r/Python/comments/60gl8w/drag_and_drop_files_with_html5_and_flask/
* http://hundredminutehack.blogspot.com/2017/03/drag-and-drop-files-with-html5-and-flask.html

* https://www.javascripttutorial.net/web-apis/javascript-drag-and-drop/
* https://stackoverflow.com/questions/10261989/html5-javascript-drag-and-drop-file-from-external-window-windows-explorer
* https://stackoverflow.com/questions/21339924/drop-event-not-firing-in-chrome
* https://stackoverflow.com/questions/2438320/html5-dragover-drop-how-get-current-x-y-coordinates
* https://stackoverflow.com/questions/2075337/uncaught-referenceerror-is-not-defined
* https://github.com/gokercebeci/droparea


