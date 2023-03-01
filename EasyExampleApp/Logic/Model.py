# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property

from Logic.Calculators import LineCalculator


class Model(QObject):
    isCreatedChanged = Signal()
    descriptionChanged = Signal()
    parameterEdited = Signal(bool)
    parametersEdited = Signal(bool)
    parametersChanged = Signal()
    yDataChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._description = {
            'name': 'Line'
        }
        self._parameters = {
            'slope': {
                'value': 1.0,
                'error': 0,
                'min': -5,
                'max': 5,
                'unit': '',
                'fittable': True,
                'fit': True
            },
            'yIntercept': {
                'value': 0.0,
                'error': 0,
                'min': -5,
                'max': 5,
                'unit': '',
                'fittable': True,
                'fit': True
            }
        }
        self._yData = []
        self._isCreated = False

    @Property('QVariant', notify=descriptionChanged)
    def description(self):
        return self._description

    @Property('QVariant', notify=parametersChanged)
    def parameters(self):
        return self._parameters

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
    def calculateData(self):
        slope = self._parameters['slope']['value']
        yIntercept = self._parameters['yIntercept']['value']
        xData = self._proxy.experiment.xData
        self.yData = LineCalculator.calculated(xData, slope, yIntercept)
        self.isCreated = True

    @Slot()
    def emptyData(self):
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
