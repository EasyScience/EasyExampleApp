# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, Property


class Application(QApplication):  # QGuiApplication crashes when using in combination with QtCharts
    def __init__(self, sys_argv):
        super(Application, self).__init__(sys_argv)
        self.setApplicationName('EasyExample')
        self.setOrganizationName('EasyScience')
        self.setOrganizationDomain('easyscience.software')
