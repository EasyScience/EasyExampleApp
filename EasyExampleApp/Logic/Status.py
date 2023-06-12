# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np

from PySide6.QtCore import QObject, Property, Signal


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
                'value': 'lmfit'
            },
            {
                'label': 'Points count',
                'value': 'Undefined'
            },
            {
                'label': 'Reduced χ2',
                'value': 'Undefined'
            }
        ]

    @Property('QVariant', notify=asJsonChanged)
    def asJson(self):
        return self._as_json

    def refresh(self):
        index = self._proxy.experiment.currentIndex
        pointsCount = f'{self._proxy.experiment._xArrays[index].size}'  # NEED FIX
        self._as_json[2]['value'] = pointsCount

        chiSq = self._proxy.fitting.chiSq
        pointsCount = self._proxy.fitting._pointsCount
        reducedChiSq = 'Undefined'
        if self._proxy.fitting._chiSq != np.inf and self._proxy.fitting._pointsCount != 0:
            reducedChiSq = f'{chiSq/pointsCount:0.2f}'  # NEED FIX
        self._as_json[3]['value'] = reducedChiSq

        self.asJsonChanged.emit()
