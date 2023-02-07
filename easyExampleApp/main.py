# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import sys, os

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWebEngineQuick import QtWebEngineQuick


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


if __name__ == '__main__':
    # Resource paths
    resource_paths = ResourcePaths()

    # QtWebEngine initialization for the QML GUI components
    QtWebEngineQuick.initialize()

    # Create application
    app = QGuiApplication(sys.argv)

    # Create QML application engine
    engine = QQmlApplicationEngine()

    # Add paths to be accessible from the QML components
    for p in resource_paths.import_paths:
        engine.addImportPath(p)

    # Load the root QML file
    engine.load(resource_paths.main_qml)

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
