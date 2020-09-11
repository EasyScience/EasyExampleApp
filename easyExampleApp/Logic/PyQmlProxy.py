import numpy as np
from typing import List

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCharts import QtCharts

from easyCore.Fitting.Fitting import Fitter

from easyExampleLib.interface import InterfaceFactory
from easyExampleLib.model import Sin, DummySin

from easyExampleApp.Logic.QtDataStore import QtDataStore
from easyExampleApp.Logic.DisplayModels.DataModels import MeasuredDataModel, CalculatedDataModel

class PyQmlProxy(QObject):

    appNameChanged = Signal()
    calculatorChanged = Signal()
    modelChanged = Signal()
    fitChanged = Signal()

    def __init__(self):
        self.appName = "easyTemplate"
        self.interface = InterfaceFactory()
        self.model = Sin(self.interface)
        self.fitter = Fitter(self.model, self.interface.fit_func)
        self.dummy_source = DummySin()
        self.data = QtDataStore(self.dummy_source.x_data, self.dummy_source.y_data, self.dummy_source.sy_data, None)
        self._measured_data_model = MeasuredDataModel(self.data)
        self._calculated_data_model = CalculatedDataModel(self.data)

    # App info
    @Property(str, notify=appNameChanged)
    def appName(self):
        return self._app_name

    @appName.setter
    def setAppName(self, value: str):
        self._app_name = value
        self.appNameChanged.emit()

    # Interfacing
    @Slot()
    def start_fitting(self):
        result = self.fitter.fit(self.data.x, self.data.y, weights=self.data.sy)
        self.data.y_opt = result.y_calc
        self._calculated_data_model.updateSeries()
        self.modelChanged.emit()

    # @Property(float, notify=fitChanged)
    # def fit_tollerence(self):
    #     pass

    # @Slot()
    # def get_calculators(self):
    #     pass
    #
    # @Property(int, notify=calculatorChanged)
    # def calculatorInt(self):
    #     return self.interface.calculatorList.index(self.interface.calculator)
    #
    # @calculatorInt.setter
    # def setCalculator(self, value: int):
    #     self.interface.calculator = self.interface.calculatorList[value]
    #     self.calculatorChanged.emit()

    @Slot()
    def calculate(self):
        y_opt = self.interface().fit_function(self.data.x)
        self.data.y_opt = y_opt
        self._calculated_data_model.updateSeries()
        self.modelChanged.emit()

    # Load/Generate Data
    @Slot()
    def generateReferenceData(self):
        self.dummy_source = DummySin()
        self.data = QtDataStore(self.dummy_source.x_data, self.dummy_source.y_data, self.dummy_source.sy_data, None)
        self._measured_data_model.updateSeries()

    # Model

    @Property(str, notify=modelChanged)
    def amplitude(self):
        return str(self.model.amplitude)

    @amplitude.setter
    def setAmplitude(self, value: str):
        value = float(value)
        self.model.amplitude = value
        self.calculate()

    @Property(str, notify=modelChanged)
    def period(self):
        return str(self.model.period)

    @period.setter
    def setPeriod(self, value: str):
        value = float(value)
        self.model.period = value
        self.calculate()

    @Property(str, notify=modelChanged)
    def xShift(self):
        return str(self.model.x_shift)

    @xShift.setter
    def setXShift(self, value: str):
        value = float(value)
        self.model.x_shift = value
        self.calculate()

    @Property(str, notify=modelChanged)
    def yShift(self):
        return str(self.model.y_shift)

    @yShift.setter
    def setYShift(self, value: str):
        value = float(value)
        self.model.y_shift = value
        self.calculate()

    # Charts
    @Slot(QtCharts.QXYSeries)
    def addMeasuredSeriesRef(self, series):
        self._measured_data_model.addSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def addLowerMeasuredSeriesRef(self, series):
        self._measured_data_model.addLowerSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def addUpperMeasuredSeriesRef(self, series):
        self._measured_data_model.addUpperSeriesRef(series)

    @Slot(QtCharts.QXYSeries)
    def setCalculatedSeriesRef(self, series):
        self._calculated_data_model.setSeriesRef(series)
