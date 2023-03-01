# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property

from Logic.Calculators import LineCalculator


class Experiment(QObject):
    isCreatedChanged = Signal()
    descriptionChanged = Signal()
    parameterEdited = Signal(bool)
    parametersEdited = Signal(bool)
    parametersChanged = Signal()
    dataSizeChanged = Signal()
    xDataChanged = Signal()
    yDataChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._isCreated = False
        self._description = {
            'name': 'PicoScope'
        }
        self._parameters = {
            'xMin': {
                'value': 0.0,
                'fittable': False
            },
            'xMax': {
                'value': 1.0,
                'fittable': False
            },
            'xStep': {
                'value': 0.01,
                'fittable': False
            }
        }
        self._dataSize = 300
        self._xData = []
        self._yData = []

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

    @Slot(str, str, str, bool)
    def editParameter(self, name, item, value, needSetFittables):
        if item == 'value':
            value = float(value)
        elif item == 'fit':
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
                self._parameters[name]['error'] = 0
        if self._parameters[name][item] == value:
            return
        self._parameters[name][item] = value
        self.parameterEdited.emit(needSetFittables)
