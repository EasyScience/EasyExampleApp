# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np

from PySide6.QtCore import QObject, Property, Signal

from EasyApp.Logic.Logging import console


class Status(QObject):
    asJsonChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._as_json = [
            {
                'label': 'Calculations',
                'value': 'CrysPy'
            },
            {
                'label': 'Minimization',
                'value': 'Lmfit-BFGS'
            },
            {
                'label': 'Data points',
                'value': None
            },
            {
                'label': 'Variables',
                'value': None
            },
            {
                'label': 'Fit iteration',
                'value': None
            },
            {
                'label': 'Goodness-of-fit (χ2)',
                'value': None
            }
        ]

    @Property('QVariant', notify=asJsonChanged)
    def asJson(self):
        return self._as_json

    def refresh(self):
        self._as_json[2]['value'] = f'{self._proxy.experiment._xArrays[self._proxy.experiment.currentIndex].size}'  # NEED FIX
        self._as_json[3]['value'] = f'{self._proxy.fitting._fittablesCount}'  # NEED FIX
        self._as_json[4]['value'] = f'{self._proxy.fitting._fitIteration}'  # NEED FIX
        self._as_json[5]['value'] = f'{self._proxy.fitting._chiSqStr}'  # NEED FIX
        self.asJsonChanged.emit()
