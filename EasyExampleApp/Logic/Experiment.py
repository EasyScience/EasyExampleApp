# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np
import timeit

from PySide6.QtCore import QObject, Signal, Slot, Property

from Logic.Calculator import Calculator


class Experiment(QObject):
    asJsonChanged = Signal()

    isCreatedChanged = Signal()

    amplitudeChanged = Signal()
    periodChanged = Signal()
    verticalShiftChanged = Signal()
    phaseShiftChanged = Signal()

    measuredDataLengthChanged = Signal()
    measuredDataChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._pyProxy = parent

        self._as_json = [
            {
                'label': 'PicoScope'
            }
        ]

        self._isCreated = False

        self._amplitude = np.random.uniform(0, 1)
        self._period = np.random.uniform(3, 4) * np.pi
        self._verticalShift = np.random.uniform(0, 1)
        self._phaseShift = np.random.uniform(0, 1) * np.pi

        self._measuredDataLength = 300
        self._measuredData = {}

        self.measuredDataLengthChanged.connect(self.onMeasuredDataLengthChanged)

        self.asJsonChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.isCreatedChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.measuredDataLengthChanged.connect(self._pyProxy.project.setNeedSaveToTrue)
        self.measuredDataChanged.connect(self._pyProxy.project.setNeedSaveToTrue)

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

    @Property(int, notify=measuredDataLengthChanged)
    def measuredDataLength(self):
        return self._measuredDataLength

    @measuredDataLength.setter
    def measuredDataLength(self, newValue):
        if self._measuredDataLength == newValue:
            return
        self._measuredDataLength = newValue
        self.measuredDataLengthChanged.emit()

    @Property('QVariant', notify=measuredDataChanged)
    def measuredData(self):
        return self._measuredData

    @measuredData.setter
    def measuredData(self, newObj):
        self._measuredData = newObj
        self.measuredDataChanged.emit()

    @Slot()
    def loadMeasuredData(self):
        starttime = timeit.default_timer()
        xArray = []
        yArray = []
        for i in range (self.measuredDataLength):
            xStep = 10 * np.pi / (self.measuredDataLength - 1)
            x = i * xStep
            randomVerticalShift = np.random.uniform(-0.05, 0.05)
            y = Calculator.sine(x,
                                self._amplitude,
                                self._period,
                                self._phaseShift,
                                self._verticalShift + randomVerticalShift
                                )
            xArray.append(x)
            yArray.append(y)
        endtime = timeit.default_timer()
        #print(f'py: The generate measured data time is: {endtime - starttime}')

        self.measuredData = { 'x': xArray, 'y': yArray }
        self.isCreated = True

    @Slot()
    def emptyMeasuredData(self):
        self.measuredData = { 'x': [], 'y': [] }
        self.isCreated = False

    def onMeasuredDataLengthChanged(self):
        if self._pyProxy.model.isCreated:
            self._pyProxy.model.generateCalculatedData()
        if self._pyProxy.experiment.isCreated:
            self._pyProxy.experiment.loadMeasuredData()
        if self._pyProxy.fitting.isFitFinished:
            self._pyProxy.fitting.fit()
