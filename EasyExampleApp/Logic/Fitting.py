# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property


class Fitting(QObject):
    isFitFinishedChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._isFitFinished = False

        self.isFitFinishedChanged.connect(self._proxy.model.parametersChanged)

    @Property(bool, notify=isFitFinishedChanged)
    def isFitFinished(self):
        return self._isFitFinished

    @isFitFinished.setter
    def isFitFinished(self, newValue):
        if self._isFitFinished == newValue:
            return
        self._isFitFinished = newValue
        self.isFitFinishedChanged.emit()

    @Slot()
    def fit(self):
        self.isFitFinished = False
        if self._proxy.model.parameters['slope']['fit']:
            self._proxy.model.parameters['slope']['value'] = -3.0015
            self._proxy.model.parameters['slope']['error'] = 0.0023
        if self._proxy.model.parameters['yIntercept']['fit']:
            self._proxy.model.parameters['yIntercept']['value'] = 1.4950
            self._proxy.model.parameters['yIntercept']['error'] = 0.0045
        self.isFitFinished = True
