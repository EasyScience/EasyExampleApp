# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property


class Fitting(QObject):
    fitFinishedChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._fitFinished = False

    @Property(bool, notify=fitFinishedChanged)
    def fitFinished(self):
        return self._fitFinished

    @fitFinished.setter
    def fitFinished(self, newValue):
        if self._fitFinished == newValue:
            return
        self._fitFinished = newValue
        self.fitFinishedChanged.emit()

    @Slot()
    def fit(self):
        self.fitFinished = False
        if self._proxy.model.parameters['slope']['fit']:
            self._proxy.model.parameters['slope']['value'] = -3.0015
            self._proxy.model.parameters['slope']['error'] = 0.0023
        if self._proxy.model.parameters['yIntercept']['fit']:
            self._proxy.model.parameters['yIntercept']['value'] = 1.4950
            self._proxy.model.parameters['yIntercept']['error'] = 0.0045
        self.fitFinished = True
