import numpy as np
from typing import List

from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCharts import QtCharts

from easyTemplateLib.Objects.fitting import Parameter, Model

from easyExampleApp.Logic.DisplayModels.DataModels import MeasuredDataModel, CalculatedDataModel
from easyExampleApp.Logic.QtInterface import QtInterface


def model():
    p1 = Parameter("amplitude", 3.5)
    p2 = Parameter("period", np.pi)
    p3 = Parameter("x_shift", 0.0)
    p4 = Parameter("y_shift", 0.0)
    f = lambda x, amplitude, period, x_shift, y_shift: amplitude * np.sin((2 * np.pi / period) * (x + x_shift)) + y_shift
    m = Model(f, [p1, p2, p3, p4])
    return m

def scatterGenerator(x: np.ndarray) -> np.ndarray:
    amplitude = np.random.uniform(3.0, 4.0)
    period = np.random.uniform(np.pi*0.9, np.pi*1.1)
    x_shift = np.random.uniform(-np.pi*0.25, np.pi*0.25)
    y_shift = np.random.uniform(-0.5, 0.5)
    y = amplitude * np.sin((2 * np.pi / period) * (x + x_shift)) + y_shift
    y_noise = np.random.normal(0, 0.5, x.shape)
    return y + y_noise

class PyQmlProxy(QObject):

    appNameChanged = Signal()
    calculatorChanged = Signal()
    modelChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.appName = "easyTemplate"
        self.interface = QtInterface(model=model(), generator=scatterGenerator)
        self._measured_data_model = MeasuredDataModel(self.interface)
        self._calculated_data_model = CalculatedDataModel(self.interface)

    # App info

    @Property(str, notify=appNameChanged)
    def appName(self):
        return self._app_name

    @appName.setter
    def setAppName(self, value: str):
        self._app_name = value
        self.appNameChanged.emit()

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

    # Data

    @Slot()
    def generateMeasuredData(self):
        self.interface.new_model()
        self._measured_data_model.updateSeries()

    # Calculator

    @Property('QVariant', notify=calculatorChanged)
    def calculatorList(self):
        return self.interface.calculatorList

    @Property(int, notify=calculatorChanged)
    def calculatorInt(self):
        return self.interface.calculatorList.index(self.interface.calculator)

    @calculatorInt.setter
    def setCalculator(self, value: int):
        self.interface.calculator = self.interface.calculatorList[value]
        self.calculatorChanged.emit()

    @Slot()
    def updateCalculatedData(self):
        self.interface.update_model()
        self._calculated_data_model.updateSeries()
        self.modelChanged.emit()

    # Fitting

    @Slot()
    def startFitting(self):
        self.interface.fit()
        self._calculated_data_model.updateSeries()
        self.modelChanged.emit()

    @Slot(float)
    def fittingFTol(self, ftol: float):
        self.interface.ftol = ftol

    @Property(str, notify=modelChanged)
    def amplitude(self):
        return str(self.interface.model.amplitude)

    @amplitude.setter
    def setAmplitude(self, value: str):
        value = float(value)
        self.interface.set_parameter('amplitude', value)
        self._calculated_data_model.updateSeries()
        self.modelChanged.emit()

    @Property(str, notify=modelChanged)
    def period(self):
        return str(self.interface.model.period)

    @period.setter
    def setPeriod(self, value: str):
        value = float(value)
        self.interface.set_parameter('period', value)
        self._calculated_data_model.updateSeries()
        self.modelChanged.emit()

    @Property(str, notify=modelChanged)
    def xShift(self):
        return str(self.interface.model.x_shift)

    @xShift.setter
    def setXShift(self, value: str):
        value = float(value)
        self.interface.set_parameter('x_shift', value)
        self._calculated_data_model.updateSeries()
        self.modelChanged.emit()

    @Property(str, notify=modelChanged)
    def yShift(self):
        return str(self.interface.model.y_shift)

    @yShift.setter
    def setYShift(self, value: str):
        value = float(value)
        self.interface.set_parameter('y_shift', value)
        self._calculated_data_model.updateSeries()
        self.modelChanged.emit()
