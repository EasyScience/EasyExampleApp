# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import argparse
import orjson


class ResourcePaths:
    def __init__(self):
        self.main_qml = ''  # Current app main.qml file
        self.imports = []  # EasyApp qml components (EasyApp/...) & Current app qml components (Gui/...)
        self.settings_ini = ''  # Persistent settings ini file location
        self.setPaths()

    def setPaths(self):

        # EasyApp from resources.py file
        try:
            import resources
            print(f'Resources: {resources}')
            self.main_qml = 'qrc:/Gui/main.qml'
            self.imports = ['qrc:/EasyApp', 'qrc:/']
            return
        except ImportError:
            print('No rc resources file is found.')

        # EasyApp from the module installed via pip
        try:
            import EasyApp
            print(f'EasyApp: {EasyApp.__path__[0]}')
            self.main_qml = 'Gui/main.qml'
            self.imports = [os.path.join(EasyApp.__path__[0], '..'), '.']
            return
        except ImportError:
            print('No EasyApp module is installed.')

        # EasyApp from the local copy
        if os.path.exists('../../EasyApp'):
            self.main_qml = 'Gui/main.qml'
            self.imports = ['../../EasyApp', '.']
            return
        else:
            print('No EasyApp directory is found.')


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


class WebEngine:

    @staticmethod
    def initialize():
        try:
            from PySide6.QtWebEngineQuick import QtWebEngineQuick
        except ModuleNotFoundError:
            print('No module named "PySide6.QtWebEngineQuick" is found.')
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
            print(f'Input value "{value}" is not supported. It should either be "true" or "false".')

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
