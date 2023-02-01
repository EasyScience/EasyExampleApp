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
* python3.9 -m venv .venv
* source .venv/bin/activate
* pip install --upgrade pip
* pip install PySide2
* pyside2-rcc resources.qrc -o EasyExampleApp/resources.py
* python EasyExampleApp/main.py
```
import resources  # resources.py created from resources.qrc by pyside2-rcc
engine.addImportPath('qrc:/easyApp')  # EasyApp qml components
engine.addImportPath('qrc:/EasyExampleApp')  # Current app qml components
engine.load('qrc:/EasyExampleApp/Gui/main.qml')
```
