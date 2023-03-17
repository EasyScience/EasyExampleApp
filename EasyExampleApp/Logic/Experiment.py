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
        'xArray': [],
        'yArray': []
    }
]

_DEFAULT_DATA = [
    {
        'name': 'PicoScope',
        'params': {
            'xMin': {
                'value': 0.0,
                'fittable': False
            },
            'xMax': {
                'value': 1.0,
                'fittable': False
            },
            'xStep': {
                'value': 0.001,
                'fittable': False
            },
            'background': {
                'value': 0.5,
                'error': 0,
                'min': -5,
                'max': 5,
                'unit': '',
                'fittable': True,
                'fit': True
            }
        },
        'xArray': [],
        'yArray': []
    }
]


class Experiment(QObject):
    dataChanged = Signal()
    dataLoaded = Signal()
    dataReseted = Signal()
    createdChanged = Signal()
    parameterEdited = Signal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._data = _EMPTY_DATA
        self._created = False

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

    # QML accessable methods

    @Slot()
    def load(self):
        self._data = _DEFAULT_DATA
        xMin = self._data[0]['params']['xMin']['value']
        xMax = self._data[0]['params']['xMax']['value']
        xStep = self._data[0]['params']['xStep']['value']
        xArray = np.arange(xMin, xMax + xStep, xStep)
        slope1 = -1.0
        yIntercept1 = 1.5
        yArray1 = LineCalculator.pseudoMeasured(xArray, slope1, yIntercept1)
        slope2 = 0.0
        yIntercept2 = -1.0
        yArray2 = LineCalculator.pseudoMeasured(xArray, slope2, yIntercept2)
        background = 0.5
        yArray = yArray1 + yArray2 + background
        self._data[0]['xArray'] = xArray
        self._data[0]['yArray'] = yArray
        self.dataLoaded.emit()

    @Slot()
    def reset(self):
        self._data = _EMPTY_DATA
        self.dataReseted.emit()

    @Slot(int, str, str, str, bool)
    def editParameter(self, currentExperimentIndex, name, item, value, needSetFittables):
        if item == 'value':
            value = float(value)
        elif item == 'fit':
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            self._data[currentExperimentIndex]['params'][name]['error'] = 0
        if self._data[currentExperimentIndex]['params'][name][item] == value:
            return
        self._data[currentExperimentIndex]['params'][name][item] = value
        self.parameterEdited.emit(needSetFittables)

    # Private methods

    def replaceXYArraysOnExperimentChartAndRedraw(self):
        currentLib1d = self._proxy.plotting.currentLib1d
        if currentLib1d == 'QtCharts':
            xArray = self._data[0]['xArray']
            yArray = self._data[0]['yArray']
            measSerie = self._proxy.plotting.appChartRefs['QtCharts']['experimentPage']['measSerie']
            try:
                measSerie.replaceNp(xArray, yArray)
            except AttributeError:
                print('No Numpy support in QtCharts. Compile PySide6 with "--pyside-numpy-support" to enable it.')
        elif currentLib1d == 'Plotly':
            chart = self._proxy.plotting.appChartRefs['Plotly']['experimentPage']
            # replace x-array
            array = self._data[0]['xArray']
            arrayStr = orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY).decode()
            scriptFunc = f'setXData({arrayStr})'
            chart.runJavaScript(scriptFunc, None)
            # replace y-array
            array = self._data[0]['yArray']
            arrayStr = orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY).decode()
            scriptFunc = f'setMeasuredYData({arrayStr})'
            chart.runJavaScript(scriptFunc, None)
            # redraw plot
            scriptFunc = 'redrawPlot()'
            chart.runJavaScript(scriptFunc, None)
        else:
            print(f'1D plotting library {currentLib1d} is not supported.')
