TEMPLATE = app

# Application name
TARGET = EasyExampleApp

CONFIG += c++14

# Makes compiler emit warnings if deprecated feature is used
DEFINES += QT_DEPRECATED_WARNINGS

QT += widgets svg qml charts gui quick webengine

SOURCES += \
    EasyExampleApp/main.cpp

RESOURCES += resources.qrc
