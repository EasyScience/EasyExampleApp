# Notes

## GUI prototyping / front-end development (QML)

Qt 5 includes qmlscene, a utility that loads and displays QML documents even before the application is complete. More at https://doc.qt.io/qt-5/qtquick-qmlscene.html

Important: qmlscene is deprecated and will be removed in a future version of Qt. Please use qml instead.

Qt 6 includes the qml executable, a utility that loads and displays QML documents. More at https://doc.qt.io/qt-6/qtquick-qml-runtime.html

Note `qml` tool is installed when installing Qt via it's own installer. Unfortunatelly, it's not a part of PySide6 installation. However, at least on macOS, it is enough to `pip install PySide6` and then add `qml` executable from the insatlled Qt to the installed PySide6. E.g. 
```
cp ~/Qt/6.4.2/macos/bin/qml .venv/lib/python3.9/site-packages/PySide6/Qt/bin
```
So this way, we can have a GitHub CI with GUI tests via `qml` first, and then via `python`, etc.


## C++

## WebAssembly

* https://doc.qt.io/qtcreator/creator-setup-webassembly.html
* https://doc.qt.io/qt-6/wasm.html
* https://forum.qt.io/topic/109672/qt-for-webassembly-binaries-for-mac-os/4
* https://www.qtcentre.org/threads/71184-Webassembly-Project-ERROR-Unknown-module(s)-in-QT-webengine

### Run
emrun --browser chrome .build_wasm/Debug/cpp_project.html


