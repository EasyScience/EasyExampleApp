# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import sys, os

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from Logic.Helpers import ResourcePaths, CommandLineArguments
from Logic.PyProxy import PyProxy


def setEnvironmentVariables():
    os.environ['QSG_RHI_BACKEND'] = 'opengl'  # For QtCharts XYSeries useOpenGL

def initQtWebEngine():
    try:
        from PySide6.QtWebEngineQuick import QtWebEngineQuick
    except ModuleNotFoundError:
        print('No module named "PySide6.QtWebEngineQuick" is found.')
    else:
        QtWebEngineQuick.initialize()

if __name__ == '__main__':
    setEnvironmentVariables()

    # QtWebEngine initialization for the QML GUI components
    initQtWebEngine()

    # Create application
    app = QApplication(sys.argv)  # QGuiApplication crashes when using QtCharts

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
