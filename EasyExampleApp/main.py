# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

# Import logger from EasyApp module
import sys
EASYAPP_LOCAL_PATH = '../../EasyApp'
sys.path.append(EASYAPP_LOCAL_PATH)
from EasyApp.Logic.Logging import console

console.debug('Starting default Python modules import')
import sys
import pathlib

console.debug('Starting PySide6 Python modules import')
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import qInstallMessageHandler

console.debug('Starting custom Python modules import')
from Logic.Helpers import ResourcePaths, CommandLineArguments, EnvironmentVariables, WebEngine, Application, ExitHelper
from Logic.PyProxy import PyProxy


console.debug('Starting __main__')
if __name__ == '__main__':
    console.debug('Set custom Qt message handler')
    qInstallMessageHandler(console.qmlMessageHandler)

    console.debug('Set environment variables')
    EnvironmentVariables.set()

    console.debug('QtWebEngine initialization for the QML GUI components')
    WebEngine.initialize()

    console.debug('Creating application')
    app = Application(sys.argv)

    console.debug('Creating QML application engine')
    engine = QQmlApplicationEngine()

    console.debug('Exposing the Python objects to QML')
    proxy = PyProxy()
    engine.rootContext().setContextProperty('pyProxy', proxy)

    cliArgs = CommandLineArguments()
    engine.rootContext().setContextProperty('pyIsTestMode', cliArgs.testmode)

    appName = app.applicationName()
    homeDirPath = pathlib.Path.home()
    settingsIniFileName = 'settings.ini'
    settingsIniFilePath = str(homeDirPath.joinpath(f'.{appName}', settingsIniFileName))
    engine.rootContext().setContextProperty('pySettingsPath', settingsIniFilePath)

    exitHelper = ExitHelper(app)
    engine.rootContext().setContextProperty('pyExitHelper', exitHelper)

    console.debug('Adding paths to be accessible from the QML components')
    resourcePaths = ResourcePaths()
    for p in resourcePaths.imports:
        engine.addImportPath(p)

    console.debug('Loading the root QML file')
    engine.load(resourcePaths.mainQml)

    console.debug('Starting event loop')
    if not engine.rootObjects():
        sys.exit(-1)
    exitCode = app.exec()

    console.debug(f"Exiting application with exit code {exitCode}")
    sys.exit(exitCode)
