# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property


class Fitting(QObject):
    isFitFinishedChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._pyProxy = parent
        self._isFitFinished = False
        self.isFitFinishedChanged.connect(self._pyProxy.project.setNeedSaveToTrue)

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
        self._pyProxy.model.slope = self._pyProxy.experiment._slope
        self._pyProxy.model.yIntercept = self._pyProxy.experiment._yIntercept
        self.isFitFinished = True
