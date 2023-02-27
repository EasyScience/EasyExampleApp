# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import timeit

from PySide6.QtCore import QObject, Signal, Slot, Property

from Logic.Calculators import LineCalculator


class Experiment(QObject):
    descriptionChanged = Signal()
    parametersChanged = Signal()
    dataSizeChanged = Signal()
    xDataChanged = Signal()
    yDataChanged = Signal()
    isCreatedChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._description = {
            'label': 'PicoScope'
        }
        self._parameters = {
            'xMin': {
                'value': 0.0,
                'fittable': False,
            },
            'xMax': {
                'value': 1.0,
                'fittable': False,
            },
            'xStep': {
                'value': 0.01,
                'fittable': False,
            }
        }
        self._dataSize = 300
        self._xData = []
        self._yData = []
        self._isCreated = False

        self.dataSizeChanged.connect(self.onDataSizeChanged)

        self.descriptionChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self.parametersChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self.xDataChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self.yDataChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self.isCreatedChanged.connect(self._proxy.project.setNeedSaveToTrue)

    @Property('QVariant', notify=descriptionChanged)
    def description(self):
        return self._description

    @Property('QVariant', notify=parametersChanged)
    def parameters(self):
        return self._parameters

    @Property(int, notify=dataSizeChanged)
    def dataSize(self):
        return self._dataSize

    @dataSize.setter
    def dataSize(self, newValue):
        if self._dataSize == newValue:
            return
        self._dataSize = newValue
        self.dataSizeChanged.emit()

    @Property('QVariant', notify=xDataChanged)
    def xData(self):
        return self._xData

    @xData.setter
    def xData(self, newData):
        self._xData = newData
        self.xDataChanged.emit()

    @Property('QVariant', notify=yDataChanged)
    def yData(self):
        return self._yData

    @yData.setter
    def yData(self, newData):
        self._yData = newData
        self.yDataChanged.emit()

    @Property(bool, notify=isCreatedChanged)
    def isCreated(self):
        return self._isCreated

    @isCreated.setter
    def isCreated(self, newValue):
        if self._isCreated == newValue:
            return
        self._isCreated = newValue
        self.isCreatedChanged.emit()

    @Slot()
    def loadData(self):
        length = self._dataSize
        slope = -3.0
        yIntercept = 1.5
        self.xData = [i / (length - 1) for i in range(length)]
        self.yData = LineCalculator.pseudoMeasured(self.xData, slope, yIntercept)
        self.isCreated = True

    @Slot()
    def emptyData(self):
        self.xData = []
        self.yData = []
        self.isCreated = False

    def onDataSizeChanged(self):
        if self.isCreated:
            self.loadData()

    @Slot(str, str, str)
    def editParameter(self, label, item, value):
        if item == 'value':
            value = float(value)
        elif item == 'fit':
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
                self._parameters[label]['error'] = 0
        if self._parameters[label][item] == value:
            return
        self._parameters[label][item] = value
        self.parametersChanged.emit()
