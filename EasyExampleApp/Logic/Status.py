# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

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
                'value': ''
            }
        ]

    @Property('QVariant', notify=asJsonChanged)
    def asJson(self):
        return self._as_json

    def refresh(self):
        index = self._proxy.experiment.currentIndex
        pointsCount = self._proxy.experiment._xArrays[index].size  # NEED FIX
        self._as_json[2]['value'] = str(pointsCount)
        self.asJsonChanged.emit()
