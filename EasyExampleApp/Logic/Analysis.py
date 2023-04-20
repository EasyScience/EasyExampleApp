# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np

from PySide6.QtCore import QObject, Signal, Property
from Logic.Logging import log


class Analysis(QObject):
    definedChanged = Signal()
    yCalcTotalChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._defined = False
        self._yCalcTotal = np.empty(0)  # MOVE TO ANALYSIS???

    # QML accessible properties

    @Property(bool, notify=definedChanged)
    def defined(self):
        return self._defined

    @defined.setter
    def defined(self, newValue):
        if self._defined == newValue:
            return
        self._defined = newValue
        log.debug(f"Analysis defined: {newValue}")
        self.definedChanged.emit()

    # Private methods

    def sumAllYCalcArays(self):
        log.debug("Summing all y-calculated data to single array")
        index = self._proxy.experiment.currentIndex
        sum = np.zeros(len(self._proxy.experiment._xArrays[index]))
        for i in range(len(self._proxy.model._yCalcArrays)):
            sum += self._proxy.model._yCalcArrays[i]
        self._yCalcTotal = sum

    def addBkgToYCalcTotal(self):
        log.debug("Adding background to total y-calculated array")
        index = self._proxy.experiment.currentIndex
        yBkgArray = self._proxy.experiment._yBkgArrays[index]
        self._yCalcTotal += yBkgArray

    def calculateYCalcTotal(self):
        self.sumAllYCalcArays()
        self.addBkgToYCalcTotal()
        self.yCalcTotalChanged.emit()
