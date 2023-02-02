# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWebEngineQuick import QtWebEngineQuick


if __name__ == '__main__':

    # QtWebEngine initialization for the QML GUI components
    QtWebEngineQuick.initialize()

    # Create application
    app = QGuiApplication(sys.argv)

    # Create QML application engine
    engine = QQmlApplicationEngine()

    # Add paths to be accessible from the QML components
    #engine.addImportPath('../easyApp')  # EasyApp qml components
    #engine.addImportPath('EasyExampleApp')  # Current app qml components
    engine.addImportPath('../../easyApp')  # EasyApp qml components
    engine.addImportPath('.')  # Current app qml components

    # Load the root QML file
    #engine.load('EasyExampleApp/Gui/main.qml')
    engine.load('Gui/main.qml')

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
