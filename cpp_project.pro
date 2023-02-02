TEMPLATE = app

# Application name
TARGET = cpp_project #EasyExampleApp doesn't work for WASM

CONFIG += c++14

# Makes compiler emit warnings if deprecated feature is used
DEFINES += QT_DEPRECATED_WARNINGS

QT += widgets svg qml charts gui quick webengine

SOURCES += \
    EasyExampleApp/main.cpp

RESOURCES += resources.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH += \
    EasyExampleApp \
    ../easyApp

# Additional import path used to resolve QML modules just for Qt Quick Designer
QML_DESIGNER_IMPORT_PATH += \
    EasyExampleApp \
    ../easyApp
