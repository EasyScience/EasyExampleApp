# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np
import orjson

from PySide6.QtCore import QObject, Signal, Slot, Property

from Logic.Calculators import LineCalculator


_EMPTY_DATA = [
    {
        'name': '',
        'params': {},
        'yArray': []
    }
]

_DEFAULT_DATA = [
    {
        'name': 'LineA',
        'params': {
            'slope': {
                'value': 3.0,
                'error': 0,
                'min': -5,
                'max': 5,
                'unit': '',
                'fittable': True,
                'fit': True
            },
            'yIntercept': {
                'value': -2.0,
                'error': 0,
                'min': -5,
                'max': 5,
                'unit': '',
                'fittable': True,
                'fit': True
            }
        },
        'yArray': []
    },
    {
        'name': 'LineB',
        'params': {
            'slope': {
                'value': -1.5,
                'error': 0,
                'min': -5,
                'max': 5,
                'unit': '',
                'fittable': True,
                'fit': True
            },
            'yIntercept': {
                'value': 0.7,
                'error': 0,
                'min': -5,
                'max': 5,
                'unit': '',
                'fittable': True,
                'fit': True
            }
        },
        'yArray': []
    }
]


class Model(QObject):
    dataChanged = Signal()
    dataLoaded = Signal()
    dataReseted = Signal()
    createdChanged = Signal()
    currentIndexChanged = Signal()
    yArraysChanged = Signal()
    parameterEdited = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._data = _EMPTY_DATA
        self._created = False
        self._totalYArray = np.empty(0)
        self._currentIndex = 0

    # QML accessable properties

    @Property('QVariant', notify=dataChanged)
    def data(self):
        return self._data

    @Property(bool, notify=createdChanged)
    def created(self):
        return self._created

    @created.setter
    def created(self, newValue):
        if self._created == newValue:
            return
        self._created = newValue
        self.createdChanged.emit()

    @Property(int, notify=currentIndexChanged)
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, newValue):
        if self._currentIndex == newValue:
            return
        self._currentIndex = newValue
        self.currentIndexChanged.emit()

    @Property('QVariant', notify=yArraysChanged)
    def totalYArray(self):
        return self._totalYArray

    # QML accessable methods

    @Slot()
    def load(self):
        self._data = _DEFAULT_DATA
        self.dataLoaded.emit()

    @Slot()
    def reset(self):
        self._data = _EMPTY_DATA
        self.dataReseted.emit()

    @Slot()
    def calculate(self):
        self.calculateYArrays()
        self.calculateTotalYArray()
        self.yArraysChanged.emit()

    @Slot(int, str, str, str, bool)
    def editParameter(self, currentModelIndex, name, item, value, needSetFittables):
        if item == 'value':
            value = float(value)
        elif item == 'fit':
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            self._data[currentModelIndex]['params'][name]['error'] = 0
        if self._data[currentModelIndex]['params'][name][item] == value:
            return
        self._data[currentModelIndex]['params'][name][item] = value
        self.parameterEdited.emit(needSetFittables)

    # Private methods

    def calculateYArrays(self):
        for i in range(len(self._data)):
            experimentData = self._proxy.experiment.data[0]
            slope = self._data[i]['params']['slope']['value']
            yIntercept = self._data[i]['params']['yIntercept']['value']
            background = experimentData['params']['background']['value']
            xArray = experimentData['xArray']
            yArray = LineCalculator.calculated(xArray, slope, yIntercept) + background
            self._data[i]['yArray'] = yArray

    def calculateTotalYArray(self):
        out = np.zeros(len(self._data[0]['yArray']))
        for i in range(len(self._data)):
            out += self._data[i]['yArray']
        self._totalYArray = out

    def replaceXArrayOnModelChart(self):
        chart = self._proxy.plotting.viewRefs['model']
        experimentData = self._proxy.experiment.data[0]
        array = experimentData['xArray']
        arrayStr = orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY).decode()
        scriptFunc = f'setXData({arrayStr})'
        chart.runJavaScript(scriptFunc, None)

    def replaceYArrayOnModelChartAndRedraw(self):
        chart = self._proxy.plotting.viewRefs['model']
        array = self._data[self._currentIndex]['yArray']
        arrayStr = orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY).decode()
        arrayJsonStr = '{y: [' + arrayStr + ']}'
        scriptFunc = f'redrawPlotWithNewCalculatedYJson({arrayJsonStr})'
        chart.runJavaScript(scriptFunc, None)
