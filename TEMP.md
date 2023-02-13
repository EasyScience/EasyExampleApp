# Development

## Project structure

### EasyExampleApp project structure

```
EasyExampleApp        			- Project directory.
├── EasyExampleApp     			- Directory with GUI and Logic components.
│   ├── Gui   					- Directory with Qt QML components of the graphical interface / front-end.
│   │   ├── main.qml			- Main QML file.
│   │   └── ...
│   ├── Logic					- Directory with Python components of the back-end.
│   ├── main.py   				- Main Python file.
│   └── ...
├── qml_project.qmlproject		- QML project description file for QtCreator (to be loaded by qml/qmlscene).
├── py_project.qmlproject		- Python project description file for QtCreator (to be loaded by Python).
├── pyproject.toml				- Python build system requirements.
└── ...
```

### EasyScience project structure

For EasyApp developers, the following shows where EasyApp can be located relative to EasyExampleApp to simplify the development process.

```
EasyScience 	       			- Parent directory.
├── EasyApp     				- Directory with EasyApp project.
├── EasyExampleApp     			- Directory with EasyExampleApp project.
└── ...
```

## GUI prototyping / front-end development (QML)

This is the easiest way of prototyping EasyApp-based GUI. Here, no Python back-end is needed and only QML components are to be displayed via the Qt `qml` tool. 

### Developers of both EasyExampleApp & EasyApp

* Install Qt 6.4.2 including the following modules:
	* Qt 5 Compatibility Module
	* Qt WebEngine
* Go to the project directory (`EasyScience/EasyExampleApp`)
* Run `main.qml` by the `qml` tool from QtCreator or terminal, e.g.:
	* ~/Qt/6.4.2/macos/bin/qml -I EasyExampleApp -I ../EasyApp EasyExampleApp/Gui/main.qml

## Front-end and back-end development (QML + Python)

### Developers of EasyExampleApp only

* cd EasyExampleApp
* python3.9 -m venv .venv
* source .venv/bin/activate
* pip install --upgrade pip
* pip install numpy
* pip install git+https://github.com/easyscience/EasyApp.git@new-easy-app
* cd EasyExampleApp
* python main.py

### Developers of both EasyExampleApp & EasyApp

* cd EasyExampleApp
* python3.9 -m venv .venv
* source .venv/bin/activate
* pip install --upgrade pip
* pip install PySide2
* python EasyExampleApp/main.py
```
engine.addImportPath('../easyApp')  # EasyApp qml components
```


### Pre-build with resources.qrc  
* https://www.pythonguis.com/tutorials/pyside-qresource-system/
* https://www.pythonguis.com/tutorials/packaging-data-files-pyside6-with-qresource-system/
* https://doc.qt.io/qtforpython/tutorials/basictutorial/qrcfiles.html
* python3.9 -m venv .venv
* source .venv/bin/activate
* pip install --upgrade pip
* pip install PySide2
* pyside6-rcc EasyExampleApp/resources.qrc -o EasyExampleApp/resources.py
* python EasyExampleApp/main.py
```
import resources  # resources.py created from resources.qrc by pyside2-rcc
engine.addImportPath('qrc:/easyApp')  # EasyApp qml components
engine.addImportPath('qrc:/EasyExampleApp')  # Current app qml components
engine.load('qrc:/EasyExampleApp/Gui/main.qml')
```

## C++

## WebAssembly

* https://doc.qt.io/qtcreator/creator-setup-webassembly.html
* https://doc.qt.io/qt-6/wasm.html
* https://forum.qt.io/topic/109672/qt-for-webassembly-binaries-for-mac-os/4
* https://www.qtcentre.org/threads/71184-Webassembly-Project-ERROR-Unknown-module(s)-in-QT-webengine

### Run
emrun --browser chrome .build_wasm/Debug/cpp_project.html
