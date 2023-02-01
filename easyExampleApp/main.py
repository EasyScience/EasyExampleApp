# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWebEngine import QtWebEngine


if __name__ == '__main__':

    # QtWebEngine initialization for the QML GUI components
    QtWebEngine.initialize()

    # Create application
    app = QApplication(sys.argv)

    # Create QML application engine
    engine = QQmlApplicationEngine()

    # Add paths to be accessible from the QML components
    engine.addImportPath('../easyApp')  # EasyApp qml components
    engine.addImportPath('EasyExampleApp')  # Current app qml components

    # Load the root QML file
    engine.load('EasyExampleApp/Gui/main.qml')

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
