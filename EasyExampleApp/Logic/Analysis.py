# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import orjson

from PySide6.QtCore import QObject, Signal, Property


_EMPTY_DATA = {}

class Analysis(QObject):
    dataChanged = Signal()
    createdChanged = Signal()

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

    # Private methods

    def replaceExperimentXYArraysOnAnalysisChart(self):
        currentLib1d = self._proxy.plotting.currentLib1d
        if currentLib1d == 'QtCharts':
            experimentData = self._proxy.experiment.data[0]
            xArray = experimentData['xArray']
            yArray = experimentData['yArray']
            measSerie = self._proxy.plotting.appChartRefs['QtCharts']['analysisPage']['measSerie']
            measSerie.replaceNp(xArray, yArray)
        elif currentLib1d == 'Plotly':
            chart = self._proxy.plotting.appChartRefs['Plotly']['analysisPage']
            experimentData = self._proxy.experiment.data[0]
            # replace x-array
            array = experimentData['xArray']
            arrayStr = orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY).decode()
            scriptFunc = f'setXData({arrayStr})'
            chart.runJavaScript(scriptFunc, None)
            # replace measured y-array
            array = experimentData['yArray']
            arrayStr = orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY).decode()
            scriptFunc = f'setMeasuredYData({arrayStr})'
            chart.runJavaScript(scriptFunc, None)
        else:
            print(f'1D plotting library {currentLib1d} is not supported.')

    def replaceModelTotalYArrayOnAnalysisChartAndRedraw(self):
        currentLib1d = self._proxy.plotting.currentLib1d
        if currentLib1d == 'QtCharts': # QtCharts only allows to replace both x and y array.
            experimentData = self._proxy.experiment.data[0]
            xArray = experimentData['xArray']
            yArray = self._proxy.model.totalYArray
            calcSerie = self._proxy.plotting.appChartRefs['QtCharts']['analysisPage']['calcSerie']
            calcSerie.replaceNp(xArray, yArray)
        elif currentLib1d == 'Plotly':
            chart = self._proxy.plotting.appChartRefs['Plotly']['analysisPage']
            array = self._proxy.model.totalYArray
            arrayStr = orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY).decode()
            arrayJsonStr = '{y: [' + arrayStr + ']}'
            scriptFunc = f'redrawPlotWithNewCalculatedYJson({arrayJsonStr})'
            chart.runJavaScript(scriptFunc, None)
        else:
            print(f'1D plotting library {currentLib1d} is not supported.')
