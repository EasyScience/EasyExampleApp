# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import math
import timeit

from PySide6.QtCore import QObject, Signal, Slot, Property

from Logic.Calculator import Calculator


class Model(QObject):
    asJsonChanged = Signal()
    isCreatedChanged = Signal()
    slopeChanged = Signal()
    yInterceptChanged = Signal()
    calculatedDataChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._pyProxy = parent

        self._as_json = [
            {
                'label': 'Line'
            }
        ]

        self._isCreated = False

        self._slope = 1.0
        self._yIntercept = 0.0

        self._xArray = []
        self._yArray = []
        self._calculatedData = {}

        self.slopeChanged.connect(self.generateCalculatedData)
        self.yInterceptChanged.connect(self.generateCalculatedData)

        self.asJsonChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.isCreatedChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.slopeChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.yInterceptChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.calculatedDataChanged.connect(self._pyProxy.project.setNeedSaveToTrue)


    @Property('QVariant', notify=asJsonChanged)
    def asJson(self):
        return self._as_json

    @Property(bool, notify=isCreatedChanged)
    def isCreated(self):
        return self._isCreated

    @isCreated.setter
    def isCreated(self, newValue):
        if self._isCreated == newValue:
            return
        self._isCreated = newValue
        self.isCreatedChanged.emit()

    @Property(float, notify=slopeChanged)
    def slope(self):
        return self._slope

    @slope.setter
    def slope(self, newValue):
        if self._slope == newValue:
            return
        self._slope = newValue
        self.slopeChanged.emit()

    @Property(float, notify=yInterceptChanged)
    def yIntercept(self):
        return self._yIntercept

    @yIntercept.setter
    def yIntercept(self, newValue):
        if self._yIntercept == newValue:
            return
        self._yIntercept = newValue
        self.yInterceptChanged.emit()

    @Property('QVariant', notify=calculatedDataChanged)
    def calculatedData(self):
        return self._calculatedData

    @calculatedData.setter
    def calculatedData(self, newObj):
        self._calculatedData = newObj
        self.calculatedDataChanged.emit()

    def setXArray(self):
        length = self._pyProxy.experiment.measuredDataLength
        self._xArray = [i / (length - 1) for i in range(length)]

    def setYArray(self):
        xArray = self._xArray
        slope = self._slope
        yIntercept = self._yIntercept
        self._yArray = Calculator.line(xArray, slope, yIntercept)

    @Slot()
    def generateCalculatedData(self):
        #starttime = timeit.default_timer()
        if len(self._xArray) != self._pyProxy.experiment.measuredDataLength:
            self.setXArray()
        self.setYArray()
        #endtime = timeit.default_timer()
        #print(f'py: The generate calculated data time is: {endtime - starttime}')

        self.calculatedData = {'x': self._xArray, 'y': self._yArray}
        self.isCreated = True

    @Slot()
    def emptyCalculatedData(self):
        self.calculatedData = {'x': [], 'y': []}
        self.isCreated = False
