# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import math

from PySide6.QtCore import QObject, Signal, Slot, Property


class Parameters(QObject):
    asJsonChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pyProxy = parent

        self._as_json = []
        self.generateAsJson()

        self.asJsonChanged.connect(self._pyProxy.project.setNeedSaveToTrue)

    @Property('QVariant', notify=asJsonChanged)
    def asJson(self):
        return self._as_json

    @Slot()
    def generateAsJson(self):
        self._as_json = [
            {
                'id': '4538458360',
                'number': 1,
                'label': 'Slope',
                'value': self._pyProxy.model.slope,
                'min': -5,
                'max': 5,
                'unit': '',
                'error': 0.1131,
                'fit': True
            },
            {
                'id': '4092346238',
                'number': 2,
                'label': 'y-Intercept',
                'value': self._pyProxy.model.yIntercept,
                'min': -5,
                'max': 5,
                'unit': 'rad',
                'error': 0.2573,
                'fit': True
            }
        ]
        self.asJsonChanged.emit()

    @Slot(str, str)
    def editParameterValue(self, pid, value):
        if (pid == '4538458360'):
            self._pyProxy.model.slope = float(value)
        elif (pid == '4092346238'):
            self._pyProxy.model.yIntercept = float(value)
