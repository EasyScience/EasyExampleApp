# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np
from PySide6.QtCore import QObject, Signal, Property

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO


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
        console.debug(IO.formatMsg('main', f'Analysis defined: {newValue}'))
        self.definedChanged.emit()

    # Private methods

    def sumAllYCalcArays(self):
        index = self._proxy.experiment.currentIndex  # NEED FIX
        sum = np.zeros(len(self._proxy.experiment._xArrays[index]))
        for i in range(len(self._proxy.model._yCalcArrays)):
            sum += self._proxy.model._yCalcArrays[i]
        self._yCalcTotal = sum
        console.debug(" - Y-calculated data of all phases has been summed up into single total y-calculated array")

    def addBkgToYCalcTotal(self):
        ##console.debug("Adding background to total y-calculated array")
        index = self._proxy.experiment.currentIndex
        yBkgArray = self._proxy.experiment._yBkgArrays[index]
        self._yCalcTotal += yBkgArray
        console.debug(" - Y-background has been added to total y-calculated array")

    def calculateYCalcTotal(self):
        self.sumAllYCalcArays()
        self.addBkgToYCalcTotal()
        self.yCalcTotalChanged.emit()
