from PySide2.QtCore import QObject, Slot, Signal, Property
from PySide2.QtCharts import QtCharts
from dicttoxml import dicttoxml

from easyCore import borg
from easyCore.Fitting.Fitting import Fitter

from easyExampleLib.interface import InterfaceFactory
from easyExampleLib.model import Sin, DummySin

from easyExampleApp.Logic.QtDataStore import QtDataStore
from easyExampleApp.Logic.DisplayModels.DataModels import MeasuredDataModel, CalculatedDataModel


class PyQmlProxy(QObject):
    _borg = borg
    modelChanged = Signal()
    calculatorChanged = Signal()
    minimizerChanged = Signal()
    statusChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interface = InterfaceFactory()
        self.model = Sin(self.interface)
        self.fitter = Fitter(self.model, self.interface.fit_func)
        self.dummy_source = DummySin()
        self.data = QtDataStore(self.dummy_source.x_data, self.dummy_source.y_data, self.dummy_source.sy_data, None)
        self._measured_data_model = MeasuredDataModel(self.data)
        self._calculated_data_model = CalculatedDataModel(self.data)
        self.updateCalculatedData()
        # when to emit status bar items cnahged
        self.calculatorChanged.connect(self.statusChanged)
        self.minimizerChanged.connect(self.statusChanged)

    # Data

    @Slot()
    def generateMeasuredData(self):
        self.dummy_source = DummySin()
        self.data = QtDataStore(self.dummy_source.x_data, self.dummy_source.y_data, self.dummy_source.sy_data, None)
        self._measured_data_model.updateData(self.data)

    @Slot()
    def updateCalculatedData(self):
        self.data.y_opt = self.interface.fit_func(self.data.x)
        self._calculated_data_model.updateData(self.data)
        self.modelChanged.emit()

    # Calculator

    @Property('QVariant', notify=calculatorChanged)
    def calculatorList(self):
        return self.interface.available_interfaces

    @Property(int, notify=calculatorChanged)
    def calculatorIndex(self):
        return self.calculatorList.index(self.interface.current_interface_name)

    @calculatorIndex.setter
    def setCalculator(self, index: int):
        self.model.switch_interface(self.calculatorList[index])
        self.updateCalculatedData()
        self.calculatorChanged.emit()

    # Minimizer

    @Property('QVariant', notify=minimizerChanged)
    def minimizerList(self):
        return self.fitter.available_engines

    @Property(int, notify=minimizerChanged)
    def minimizerIndex(self):
        return self.minimizerList.index(self.fitter.current_engine.name)

    @minimizerIndex.setter
    def setMinimizer(self, index: int):
        self.fitter.switch_engine(self.minimizerList[index])
        self.minimizerChanged.emit()

    # Model

    @Property(str, notify=modelChanged)
    def amplitude(self):
        return str(self.model.amplitude.raw_value)

    @amplitude.setter
    def setAmplitude(self, value: str):
        value = float(value)
        self.model.amplitude = value
        self.updateCalculatedData()

    @Property(str, notify=modelChanged)
    def period(self):
        return str(self.model.period.raw_value)

    @period.setter
    def setPeriod(self, value: str):
        value = float(value)
        self.model.period = value
        self.updateCalculatedData()

    @Property(str, notify=modelChanged)
    def xShift(self):
        return str(self.model.x_shift.raw_value)

    @xShift.setter
    def setXShift(self, value: str):
        value = float(value)
        self.model.x_shift = value
        self.updateCalculatedData()

    @Property(str, notify=modelChanged)
    def yShift(self):
        return str(self.model.y_shift.raw_value)

    @yShift.setter
    def setYShift(self, value: str):
        value = float(value)
        self.model.y_shift = value
        self.updateCalculatedData()

    # Calculator

    @Property('QVariant', notify=calculatorChanged)
    def calculatorList(self):
        return self.interface.available_interfaces

    @Property(int, notify=calculatorChanged)
    def calculatorIndex(self):
        return self.calculatorList.index(self.interface.current_interface_name)

    @calculatorIndex.setter
    def setCalculator(self, index: int):
        self.model.switch_interface(self.calculatorList[index])
        self.updateCalculatedData()
        self.calculatorChanged.emit()

    # Minimizer

    @Property('QVariant', notify=minimizerChanged)
    def minimizerList(self):
        return self.fitter.available_engines

    @Property(int, notify=minimizerChanged)
    def minimizerIndex(self):
        return self.minimizerList.index(self.fitter.current_engine.name)

    @minimizerIndex.setter
    def setMinimizer(self, index: int):
        print("setMinimizer", index)
        self.fitter.switch_engine(self.minimizerList[index])
        self.minimizerChanged.emit()

    @Slot()
    def startFitting(self):
        result = self.fitter.fit(self.data.x, self.data.y, weights=self.data.sy)
        self.data.y_opt = result.y_calc
        self._calculated_data_model.updateData(self.data)
        self.modelChanged.emit()

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

    # Undo/redo

    @Slot()
    def undo(self):
        self._borg.stack.undo()
        self.modelChanged.emit()

    @Slot(result=bool)
    def canUndo(self):
        return self._borg.stack.canUndo()

    @Slot()
    def redo(self):
        self._borg.stack.redo()
        self.modelChanged.emit()

    @Slot(result=bool)
    def canRedo(self):
        return self._borg.stack.canRedo()

    # Status

    @Property(str, notify=statusChanged)
    def statusModelAsXml(self):
        items = [ { "label": "Calculator", "value": self.interface.current_interface_name },
                  { "label": "Minimizer", "value": self.fitter.current_engine.name } ]
        xml = dicttoxml(items, attr_type=False)
        xml = xml.decode()
        return xml

    # Display Models
    @Property(str, notify=modelChanged)
    def fitablesModelAsXml(self):
        pars = self.model.get_parameters()
        fitables = []
        for index, par in enumerate(pars):
            unit = str(par.unit)
            if unit == "dimensionless":
                unit = ""
            fitables.append(
                { "number": index + 1,
                  "label": par.name,
                  "value": par.raw_value,
                  "unit": unit,
                  "error": par.error,
                  "fit": int(not par.fixed) }
            )

        xml = dicttoxml(fitables, attr_type=False)
        xml = xml.decode()
        return xml

    @Slot(int, str, str)
    def editFitablesModel(self, index, key, value):
        print(index, key, value)
