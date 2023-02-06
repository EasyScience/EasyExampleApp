# Development

## QML

### Developers of both EasyExampleApp & EasyApp

* ~/Qt/5.15.2/clang_64/bin/qmlscene -I EasyExampleApp -I ../easyApp EasyExampleApp/Gui/main.qml

## Python

### Developers of both EasyExampleApp & EasyApp

* python3.9 -m venv .venv
* source .venv/bin/activate
* pip install --upgrade pip
* pip install PySide2
* python EasyExampleApp/main.py
```
engine.addImportPath('../easyApp')  # EasyApp qml components
```

### Developers of EasyExampleApp only

* python3.9 -m venv .venv
* source .venv/bin/activate
* pip install --upgrade pip
* pip install PySide2
* pip install git+https://github.com/easyScience/easyApp.git@plotly2
* python EasyExampleApp/main.py
```
import os
import easyApp
engine.addImportPath(os.path.join(easyApp.__path__[0], '..'))  # EasyApp qml components
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
