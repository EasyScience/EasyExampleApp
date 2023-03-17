# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6 import QtCharts


_LIBS_1D = ['QtCharts', 'Plotly']

class Plotting(QObject):
    currentLib1dChanged = Signal()
    useWebGL1dChanged = Signal()
    appChartRefsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pyProxy = parent
        self._currentLib1d = 'QtCharts'
        self._useWebGL1d = True
        self._appChartRefs = {
            'Plotly': {
                'experimentPage': None,
                'modelPage': None,
                'analysisPage': None
            },
            'QtCharts': {
                'experimentPage': {
                    'measSerie': QtCharts.QXYSeries
                },
                'modelPage': {
                    'calcSerie': QtCharts.QXYSeries
                },
                'analysisPage': {
                    'measSerie': QtCharts.QXYSeries,
                    'calcSerie': QtCharts.QXYSeries
                }
            }
        }

    @Property(str, notify=currentLib1dChanged)
    def currentLib1d(self):
        return self._currentLib1d

    @currentLib1d.setter
    def currentLib1d(self, newValue):
        if self._currentLib1d == newValue:
            return
        self._currentLib1d = newValue
        self.currentLib1dChanged.emit()

    @Property(bool, notify=useWebGL1dChanged)
    def useWebGL1d(self):
        return self._useWebGL1d

    @useWebGL1d.setter
    def useWebGL1d(self, newValue):
        if self._useWebGL1d == newValue:
            return
        self._useWebGL1d = newValue
        self.useWebGL1dChanged.emit()

    @Property('QVariant', notify=appChartRefsChanged)
    def appChartRefs(self):
        return self._appChartRefs

    @Slot(str, str, 'QVariant')
    def setAppQtChartsSerieRef(self, page, serie, ref):
        if self._appChartRefs['QtCharts'][page][serie] == ref:
            return
        self._appChartRefs['QtCharts'][page][serie] = ref
        self.appChartRefsChanged.emit()

    @Slot(str, 'QVariant')
    def setAppPlotlyChartRef(self, page, ref):
        if self._appChartRefs['Plotly'][page] == ref:
            return
        self._appChartRefs['Plotly'][page] = ref
        self.appChartRefsChanged.emit()
