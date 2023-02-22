# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import argparse


class ResourcePaths:
    def __init__(self):
        self.main_qml = ''  # Current app main.qml file
        self.imports = []   # EasyApp qml components (EasyApp/...) & Current app qml components (Gui/...)
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
            self.imports = ['../../EasyApp', '.' ]
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
