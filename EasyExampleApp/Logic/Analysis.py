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
        chart = self._proxy.plotting.viewRefs['analysis']
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

    def replaceModelTotalYArrayOnAnalysisChartAndRedraw(self):
        chart = self._proxy.plotting._viewRefs['analysis']
        array = self._proxy.model.totalYArray
        arrayStr = orjson.dumps(array, option=orjson.OPT_SERIALIZE_NUMPY).decode()
        arrayJsonStr = '{y: [' + arrayStr + ']}'
        scriptFunc = f'redrawPlotWithNewCalculatedYJson({arrayJsonStr})'
        chart.runJavaScript(scriptFunc, None)
