# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from Logic.Helpers import ResourcePaths, CommandLineArguments, EnvironmentVariables, WebEngine
from Logic.PyProxy import PyProxy


if __name__ == '__main__':
    # Set environment variables
    EnvironmentVariables.set()

    # QtWebEngine initialization for the QML GUI components
    WebEngine.initialize()

    # Create application
    app = QApplication(sys.argv)  # QGuiApplication crashes when using QtCharts
    app.setApplicationName('EasyExample')
    app.setOrganizationName('EasyScience')
    app.setOrganizationDomain('easyscience.software')

    # Create QML application engine
    engine = QQmlApplicationEngine()

    # Expose the Python objects to QML
    proxy = PyProxy()
    engine.rootContext().setContextProperty('pyProxy', proxy)

    cliArgs = CommandLineArguments()
    engine.rootContext().setContextProperty('pyIsTestMode', cliArgs.testmode)

    # Add paths to be accessible from the QML components
    resourcePaths = ResourcePaths()
    for p in resourcePaths.imports:
        engine.addImportPath(p)

    # Load the root QML file
    engine.load(resourcePaths.main_qml)

    # Event loop
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
