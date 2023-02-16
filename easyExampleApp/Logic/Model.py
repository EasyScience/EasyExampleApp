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

    amplitudeChanged = Signal()
    periodChanged = Signal()
    verticalShiftChanged = Signal()
    phaseShiftChanged = Signal()

    calculatedDataChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._pyProxy = parent

        self._as_json = [
            {
                'label': 'Sine wave'
            }
        ]

        self._isCreated = False

        self._amplitude = 1
        self._period = 3.5 * math.pi
        self._verticalShift = 0
        self._phaseShift = 0

        self._xArray = []
        self._yArray = []
        self._calculatedData = {}

        self.amplitudeChanged.connect(self.generateCalculatedData)
        self.periodChanged.connect(self.generateCalculatedData)
        self.verticalShiftChanged.connect(self.generateCalculatedData)
        self.phaseShiftChanged.connect(self.generateCalculatedData)

        self.asJsonChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.isCreatedChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.amplitudeChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.periodChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.verticalShiftChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.phaseShiftChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
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

    @Property(float, notify=amplitudeChanged)
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, newValue):
        if self._amplitude == newValue:
            return
        self._amplitude = newValue
        self.amplitudeChanged.emit()

    @Property(float, notify=periodChanged)
    def period(self):
        return self._period

    @period.setter
    def period(self, newValue):
        if self._period == newValue:
            return
        self._period = newValue
        self.periodChanged.emit()

    @Property(float, notify=verticalShiftChanged)
    def verticalShift(self):
        return self._verticalShift

    @verticalShift.setter
    def verticalShift(self, newValue):
        if self._verticalShift == newValue:
            return
        self._verticalShift = newValue
        self.verticalShiftChanged.emit()

    @Property(float, notify=phaseShiftChanged)
    def phaseShift(self):
        return self._phaseShift

    @phaseShift.setter
    def phaseShift(self, newValue):
        if self._phaseShift == newValue:
            return
        self._phaseShift = newValue
        self.phaseShiftChanged.emit()

    @Property('QVariant', notify=calculatedDataChanged)
    def calculatedData(self):
        return self._calculatedData

    @calculatedData.setter
    def calculatedData(self, newObj):
        self._calculatedData = newObj
        self.calculatedDataChanged.emit()

    @Slot()
    def generateCalculatedDataSlow(self):
        starttime = timeit.default_timer()
        xArray = []
        yArray = []
        for i in range(self._pyProxy.experiment.measuredDataLength):
            xStep = 10 * math.pi / (self._pyProxy.experiment.measuredDataLength - 1)
            x = i * xStep
            y = Calculator.sine(x,
                                self._amplitude,
                                self._period,
                                self._phaseShift,
                                self._verticalShift
                                )
            xArray.append(x)
            yArray.append(y)
        endtime = timeit.default_timer()
        #print(f'py: The generate calculated data time is: {endtime - starttime}')

        self.calculatedData = { 'x': xArray, 'y': yArray }
        self.isCreated = True

    def setXArray(self):
        measuredDataLength = self._pyProxy.experiment.measuredDataLength
        pi = math.pi
        self._xArray = [i * 10 * pi / (measuredDataLength - 1) for i in range(measuredDataLength)]

    def setYArray(self):
        amplitude = self._amplitude
        period = self._period
        phaseShift = self._phaseShift
        verticalShift = self._verticalShift
        pi = math.pi
        self._yArray = [amplitude * math.sin( 2 * pi / period * (x + phaseShift) ) + verticalShift for x in self._xArray]

    @Slot()
    def generateCalculatedData(self):
        starttime = timeit.default_timer()
        if len(self._xArray) != self._pyProxy.experiment.measuredDataLength:
            self.setXArray()
        self.setYArray()
        endtime = timeit.default_timer()
        #print(f'py: The generate calculated data time is: {endtime - starttime}')

        self.calculatedData = { 'x': self._xArray, 'y': self._yArray }
        self.isCreated = True

    @Slot()
    def emptyCalculatedData(self):
        self.calculatedData = { 'x': [], 'y': [] }
        self.isCreated = False
