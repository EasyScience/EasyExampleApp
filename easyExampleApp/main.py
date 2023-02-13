# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import sys, os

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWebEngineQuick import QtWebEngineQuick

import numpy as np

from PySide6.QtCore import QObject, Signal, Slot, Property


class ResourcePaths:
    def __init__(self):
        self.main_qml_path = ''  # Current app main.qml file
        self.import_paths = []   # EasyApp qml components (EasyApp/...) & Current app qml components (Gui/...)
        self.setPaths()

    def setPaths(self):

        # EasyApp from resources.py file
        try:
            import resources
            print(f'Resources: {resources}')
            self.main_qml = 'qrc:/Gui/main.qml'
            self.import_paths = ['qrc:/EasyApp', 'qrc:/']
            return()
        except ImportError:
            print('No rc resources file is found.')

        # EasyApp from the module installed via pip
        try:
            import EasyApp
            print(f'EasyApp: {EasyApp.__path__[0]}')
            self.main_qml = 'Gui/main.qml'
            self.import_paths = [os.path.join(EasyApp.__path__[0], '..'), '.']
            return()
        except ImportError:
            print('No EasyApp module is installed.')

        # EasyApp from the local copy
        if os.path.exists('../../EasyApp'):
            self.main_qml = 'Gui/main.qml'
            self.import_paths = ['../../EasyApp', '.' ]
            return()
        else:
            print('No EasyApp directory is found.')


class BackendProxy(QObject):
    measuredDataLengthChanged = Signal()
    measuredDataChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._measured_data_length = 10
        self._measured_data_obj = {}
        self._setMeasuredDataObj()

    def _setMeasuredDataObj(self):
        length = self._measured_data_length
        self._measured_data_obj = {
            'x': np.arange(0, length + 1, 1).tolist(),
            'y': np.random.randint(100, size=(length + 1)).tolist()
        }
        self.measuredDataChanged.emit()

    @Property(int, notify=measuredDataLengthChanged)
    def measuredDataLength(self):
        return self._measured_data_length

    @measuredDataLength.setter
    def measuredDataLength(self, new_length):
        if self._measured_data_length != new_length:
            self._measured_data_length = new_length
            self.measuredDataLengthChanged.emit()

    @Property('QVariant', notify=measuredDataChanged)
    def measuredDataObj(self):
        return self._measured_data_obj

    @Slot()
    def generateMeasuredDataObj(self):
        self._setMeasuredDataObj()


if __name__ == '__main__':
    # QtWebEngine initialization for the QML GUI components
    QtWebEngineQuick.initialize()

    # Create application
    app = QGuiApplication(sys.argv)

    # Create QML application engine
    engine = QQmlApplicationEngine()

    # Expose the Python objects to QML
    #backendProxy = BackendProxy()
    #engine.rootContext().setContextProperty('pyProxy', backendProxy)

    # Add paths to be accessible from the QML components
    resourcePaths = ResourcePaths()
    for p in resourcePaths.import_paths:
        engine.addImportPath(p)

    # Load the root QML file
    engine.load(resourcePaths.main_qml)

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
