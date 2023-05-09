# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

# Import logger from EasyApp module
import sys
EASYAPP_LOCAL_PATH = '../../EasyApp'
sys.path.append(EASYAPP_LOCAL_PATH)
from EasyApp.Logic.Logging import console


if __name__ == '__main__':

    from PySide6.QtCore import qInstallMessageHandler
    qInstallMessageHandler(console.qmlMessageHandler)
    console.debug('Custom Qt message handler has been defined')

    from Logic.Helpers import EnvironmentVariables
    EnvironmentVariables.set()
    console.debug('Environment variables have been defined')

    from Logic.Helpers import WebEngine
    WebEngine.initialize()
    console.debug('QtWebEngine for the QML GUI components has been initialized')

    from Logic.Helpers import Application
    app = Application(sys.argv)
    console.debug('Qt Application has been created')

    from PySide6.QtQml import QQmlApplicationEngine
    engine = QQmlApplicationEngine()
    console.debug('QML application engine has been created')

    from Logic.Helpers import ResourcePaths
    resourcePaths = ResourcePaths()
    for p in resourcePaths.imports:
        engine.addImportPath(p)
    console.debug('Paths to be accessible from the QML components has been added')

    import pathlib
    appName = app.applicationName()
    homeDirPath = pathlib.Path.home()
    settingsIniFileName = 'settings.ini'
    settingsIniFilePath = str(homeDirPath.joinpath(f'.{appName}', settingsIniFileName))
    engine.rootContext().setContextProperty('pySettingsPath', settingsIniFilePath)
    console.debug('Persistent settings file path has been exposed to QML')

    from Logic.Helpers import CommandLineArguments
    cliArgs = CommandLineArguments()
    engine.rootContext().setContextProperty('pyIsTestMode', cliArgs.testmode)
    console.debug('pyIsTestMode object has been exposed to QML')

    from Logic.Helpers import ExitHelper
    exitHelper = ExitHelper()
    engine.rootContext().setContextProperty('pyExitHelper', exitHelper)
    console.debug('pyExitHelper object has been exposed to QML')

    from Logic.Helpers import PyProxyWorker
    from PySide6.QtCore import QThreadPool
    worker = PyProxyWorker(engine)
    worker.pyProxyExposedToQml.connect(lambda: engine.load(resourcePaths.mainQml))
    threadpool = QThreadPool.globalInstance()
    threadpool.start(worker.exposePyProxyToQml)
    console.debug('PyProxy object is creating in a separate thread and exposing to QML')

    engine.load(resourcePaths.splashScreenQml)
    console.debug('Splash screen QML component has been loaded')

    if not engine.rootObjects():
        sys.exit(-1)
    console.debug('QML engine has been checked for having root component')

    console.debug('Application event loop is about to start')
    exitCode = app.exec()

    console.debug(f'Application is about to exit with code {exitCode}')
    sys.exit(exitCode)
