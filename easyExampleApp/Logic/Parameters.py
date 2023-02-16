# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np

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
                'label': 'Amplitude',
                'value': self._pyProxy.model.amplitude,
                'min': 0,
                'max': 1,
                'unit': '',
                'error': 0.1131,
                'fit': True
            },
            {
                'id': '4092346238',
                'number': 2,
                'label': 'Period',
                'value': self._pyProxy.model.period,
                'min': 3 * np.pi,
                'max': 4 * np.pi,
                'unit': 'rad',
                'error': 0.2573,
                'fit': True
            },
            {
                'id': '9834542745',
                'number': 3,
                'label': 'Vertical shift',
                'value': self._pyProxy.model.verticalShift,
                'min': 0,
                'max': 1,
                'unit': '',
                'error': 0.0212,
                'fit': True
            },
            {
                'id': '8655377643',
                'number': 4,
                'label': 'Phase shift',
                'value': self._pyProxy.model.phaseShift,
                'min': 0,
                'max': np.pi,
                'unit': 'rad',
                'error': 0.2238,
                'fit': True
            }
        ]
        self.asJsonChanged.emit()


    @Slot(str, str)
    def editParameterValue(self, pid, value):
        if (pid == '4538458360'):
            self._pyProxy.model.amplitude = float(value)
        elif (pid == '4092346238'):
            self._pyProxy.model.period = float(value)
        elif (pid == '9834542745'):
            self._pyProxy.model.verticalShift = float(value)
        elif (pid == '8655377643'):
            self._pyProxy.model.phaseShift = float(value)
