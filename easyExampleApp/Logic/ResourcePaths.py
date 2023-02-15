# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os


class ResourcePaths:
    def __init__(self):
        self.main_qml_path = ''  # Current app main.qml file
        self.import_paths = []   # EasyApp qml components (EasyApp/...) & Current app qml components (Gui/...)
        self.setPaths()

    def setPaths(self):

        # EasyApp from resources.py file
        try:
            import resources
            print(f'Resources: {resources}')
            self.main_qml = 'qrc:/Gui/main.qml'
            self.import_paths = ['qrc:/EasyApp', 'qrc:/']
            return
        except ImportError:
            print('No rc resources file is found.')

        # EasyApp from the module installed via pip
        try:
            import EasyApp
            print(f'EasyApp: {EasyApp.__path__[0]}')
            self.main_qml = 'Gui/main.qml'
            self.import_paths = [os.path.join(EasyApp.__path__[0], '..'), '.']
            return
        except ImportError:
            print('No EasyApp module is installed.')

        # EasyApp from the local copy
        if os.path.exists('../../EasyApp'):
            self.main_qml = 'Gui/main.qml'
            self.import_paths = ['../../EasyApp', '.' ]
            return
        else:
            print('No EasyApp directory is found.')
