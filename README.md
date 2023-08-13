# Development 

## Project structure

### EasyExampleApp project structure

```
EasyExampleApp        		- Project directory.
├── EasyExampleApp     		- Directory with GUI and Logic components.
│   ├── Gui   			- Directory with Qt QML components of the graphical interface / front-end.
│   │   ├── main.qml		- Main QML file.
│   │   └── ...
│   ├── Logic			- Directory with Python components of the back-end.
│   ├── main.py   		- Main Python file.
│   └── ...
├── qml_project.qmlproject	- QML project description file for QtCreator (to be loaded by qml/qmlscene).
├── py_project.qmlproject	- Python project description file for QtCreator (to be loaded by Python).
├── pyproject.toml		- Python build system requirements.
└── ...
```

### EasyScience project structure

For EasyApp developers, the following shows where EasyApp can be located relative to EasyExampleApp to simplify the development process.

```
EasyScience 	       		- Parent directory.
├── EasyApp     		- Directory with EasyApp project.
├── EasyExampleApp     		- Directory with EasyExampleApp project.
└── ...
```

## GUI prototyping / front-end development (QML)

This is the easiest way of prototyping EasyApp-based GUI. Here, no Python back-end is needed and only QML components are to be displayed via the Qt `qml` tool.

### Developers of both EasyExampleApp & EasyApp

In this case, `EasyApp` need to be cloned manually and located on the same lavel as `EasyExampleApp`.

* Install Qt 6.4.2 including the following modules:
	* Qt 5 Compatibility Module
	* Qt WebEngine
* Go to the project directory (`EasyScience/EasyExampleApp`)
* Run `main.qml` by the `qml` tool from QtCreator (`qml_project.qmlproject`) or terminal, e.g.:
	* `~/Qt/6.4.2/macos/bin/qml -I EasyExampleApp -I ../EasyApp EasyExampleApp/Gui/main.qml`

## Front-end and back-end development (QML + Python)

This is the second step of the development, when the GUI prototype is approved. Now, we can develop Python back-end and run application directly from Python instead of the Qt `qml` tool.

### Developers of EasyExampleApp only

In this case, `EasyApp` is installed via PIP from GitHub.

* Go to the project directory (`EasyScience/EasyExampleApp`)
* Create Python environment and activate it:
	* `python3.9 -m venv .venv`
	* `source .venv/bin/activate`
* Upgrade PIP and install `numpy` and `jsbeautifier`
	* `pip install --upgrade pip`
	* `pip install numpy jsbeautifier`
* Install `EasyApp` from GitHub (`new-easy-app` branch).
	* `pip install git+https://github.com/easyscience/EasyApp.git@new-easy-app`
* Run `main.py` by Python from QtCreator (`py_project.qmlproject`) or terminal, e.g.:
	* `cd EasyExampleApp` (`EasyScience/EasyExampleApp/EasyExampleApp`)
	* `python main.py`

### Developers of both EasyExampleApp & EasyApp

In this case, `EasyApp` need to be cloned manually and located on the same lavel as `EasyExampleApp`.

* Go to the project directory (`EasyScience/EasyExampleApp`)
* `python3.9 -m venv .venv`
* `source .venv/bin/activate`
* `pip install --upgrade pip`
* `pip install PySide6 numpy jsbeautifier`
* `cd EasyExampleApp`
* `python EasyExampleApp/main.py`

### Build app

In this case, `EasyApp` need to be cloned manually and located on the same lavel as `EasyExampleApp`.

* Go to the project directory (`EasyScience/EasyExampleApp`)
* Convert `resources.qrc` to `resources.py`
	* `pyside6-rcc EasyExampleApp/resources.qrc -o EasyExampleApp/resources.py`
* Install PyInstaller
	* `pip install pyinstaller`
* Freeze app
	* `pyinstaller EasyExampleApp/main.py --name=EasyDiffraction --log-level WARN --noconfirm --clean --noconsole --onedir --distpath .build/pyinstaller/dist --workpath .build/pyinstaller/temp --specpath .build/pyinstaller`
