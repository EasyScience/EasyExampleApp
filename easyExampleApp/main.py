# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import sys

from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import Qt, QIcon
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWebEngine import QtWebEngine

import easyApp


def main():
    # Paths
    current_path = os.path.dirname(sys.argv[0])
    main_qml_path = os.path.join(current_path, 'Gui', 'main.qml')
    easyApp_path = os.path.join(easyApp.__path__[0], '..')

    # QtWebEngine initialization for the QML GUI components
    QtWebEngine.initialize()

    # Create application
    app = QApplication(sys.argv)

    # Create QML application engine
    engine = QQmlApplicationEngine()

    # Add paths to be accessible from the QML components
    engine.addImportPath(easyApp_path) # EasyApp qml components
    engine.addImportPath(current_path) # Current app qml components

    # Load the root QML file
    engine.load(main_qml_path)

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
