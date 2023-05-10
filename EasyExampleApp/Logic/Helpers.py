# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import argparse
import orjson
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, QCoreApplication

from EasyApp.Logic.Logging import console


class ResourcePaths:
    def __init__(self):
        self.mainQml = ''  # Current app main.qml file
        self.splashScreenQml = ''  # Splash screen .qml file
        self.imports = []  # EasyApp qml components (EasyApp/...) & Current app qml components (Gui/...)
        self.settings_ini = ''  # Persistent settings ini file location
        self.setPaths()

    def setPaths(self):

        console.debug('Trying to import python resources.py file with EasyApp')
        try:
            import resources
            console.info(f'Resources: {resources}')
            self.mainQml = 'qrc:/Gui/main.qml'
            self.splashScreenQml = 'qrc:/Gui/Components/SplashScreen.qml'
            self.imports = ['qrc:/EasyApp', 'qrc:/']
            return
        except ImportError:
            console.debug('No rc resources file has been found')

        console.debug('Trying to import the locally installed EasyApp module')
        try:
            import EasyApp
            easyAppPath = os.path.abspath(EasyApp.__path__[0])
            console.info(f'EasyApp: {easyAppPath}')
            self.mainQml = 'Gui/main.qml'
            self.splashScreenQml = 'Gui/Components/SplashScreen.qml'
            self.imports = [os.path.join(easyAppPath, '..'), '.']
            return
        except ImportError:
            console.debug('No EasyApp module is installed')

        console.error('No EasyApp module has been found')


class CommandLineArguments:

    def __new__(cls):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '-t',
            '--testmode',
            action='store_true',
            help='run the application in test mode: run tests, take screenshots and exit the application'
        )

        return parser.parse_args()


class EnvironmentVariables:

    @staticmethod
    def set():
        os.environ['QSG_RHI_BACKEND'] = 'opengl'  # For QtCharts XYSeries useOpenGL
        #os.environ['QT_MESSAGE_PATTERN'] = "\033[32m%{time h:mm:ss.zzz}%{if-category}\033[32m %{category}:%{endif} %{if-debug}\033[34m%{function}%{endif}%{if-warning}\033[31m%{backtrace depth=3}%{endif}%{if-critical}\033[31m%{backtrace depth=3}%{endif}%{if-fatal}\033[31m%{backtrace depth=3}%{endif}\033[0m %{message}"


class WebEngine:

    @staticmethod
    def initialize():
        try:
            from PySide6.QtWebEngineQuick import QtWebEngineQuick
        except ModuleNotFoundError:
            #console.debug('No module named "PySide6.QtWebEngineQuick" is found.')
            pass
        else:
            QtWebEngineQuick.initialize()

    @staticmethod
    def runJavaScriptWithoutCallback(webEngine, script):
        callback = None
        webEngine.runJavaScript(script, callback)

class Converter:

    @staticmethod
    def jsStrToPyBool(value):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            #console.debug(f'Input value "{value}" is not supported. It should either be "true" or "false".')
            pass

    @staticmethod
    def dictToJson(obj):
        # Dump to json
        dumpOption = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2
        jsonBytes = orjson.dumps(obj, option=dumpOption)
        json = jsonBytes.decode()
        return json
        #if not formatted:
        #    return jsonStr
        ## Format to have arrays shown in one line. Can orjson do this?
        #formatOptions = jsbeautifier.default_options()
        #formatOptions.indent_size = 2
        #formattedJsonStr = jsbeautifier.beautify(jsonStr, formatOptions)
        #return formattedJsonStr


class Application(QApplication):  # QGuiApplication crashes when using in combination with QtCharts

    def __init__(self, sysArgv):
        super(Application, self).__init__(sysArgv)
        self.setApplicationName('EasyExample')
        self.setOrganizationName('EasyScience')
        self.setOrganizationDomain('easyscience.software')


class ExitHelper(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def exitApp(self, exitCode):
        console.debug(f'Force exiting application with code {exitCode}')
        os._exit(exitCode)


class PyProxyWorker(QObject):
    pyProxyExposedToQml = Signal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self._engine = engine

    def exposePyProxyToQml(self):
        import time
        time.sleep(0.5)
        console.debug('Slept for 0.5s to allow splash screen to start')
        from Logic.PyProxy import PyProxy
        mainThread = QCoreApplication.instance().thread()
        proxy = PyProxy()
        console.debug('PyProxy object has been created')
        proxy.moveToThread(mainThread)
        self._engine.rootContext().setContextProperty('pyProxy', proxy)
        self.pyProxyExposedToQml.emit()
        console.debug('PyProxy object has been exposed to QML')
