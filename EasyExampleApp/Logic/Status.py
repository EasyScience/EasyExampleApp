# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Property


class Status(QObject):
    dataPointsChanged = Signal()
    calculatorChanged = Signal()
    minimizerChanged = Signal()
    variablesChanged = Signal()
    fitIterationChanged = Signal()
    goodnessOfFitChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._dataPoints = ''
        self._calculator = ''
        self._minimizer = ''
        self._variables = ''
        self._fitIteration = ''
        self._goodnessOfFit = ''

        self._as_json = [
            {'label': 'a', 'value': 'b'},
            {'label': 'a', 'value': 'b'},
            {'label': 'a', 'value': 'b'},
            {'label': 'a', 'value': 'b'},
            {'label': 'a', 'value': 'b'},
            {'label': 'a', 'value': 'b'}
        ]

    @Property(str, notify=dataPointsChanged)
    def dataPoints(self):
        return self._dataPoints

    @dataPoints.setter
    def dataPoints(self, newValue):
        if self._dataPoints == newValue:
            return
        self._dataPoints = newValue
        self.dataPointsChanged.emit()

    @Property(str, notify=calculatorChanged)
    def calculator(self):
        return self._calculator

    @calculator.setter
    def calculator(self, newValue):
        if self._calculator == newValue:
            return
        self._calculator = newValue
        self.calculatorChanged.emit()

    @Property(str, notify=minimizerChanged)
    def minimizer(self):
        return self._minimizer

    @minimizer.setter
    def minimizer(self, newValue):
        if self._minimizer == newValue:
            return
        self._minimizer = newValue
        self.minimizerChanged.emit()

    @Property(str, notify=variablesChanged)
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, newValue):
        if self._variables == newValue:
            return
        self._variables = newValue
        self.variablesChanged.emit()

    @Property(str, notify=fitIterationChanged)
    def fitIteration(self):
        return self._fitIteration

    @fitIteration.setter
    def fitIteration(self, newValue):
        if self._fitIteration == newValue:
            return
        self._fitIteration = newValue
        self.fitIterationChanged.emit()

    @Property(str, notify=goodnessOfFitChanged)
    def goodnessOfFit(self):
        return self._goodnessOfFit

    @goodnessOfFit.setter
    def goodnessOfFit(self, newValue):
        if self._goodnessOfFit == newValue:
            return
        self._goodnessOfFit = newValue
        self.goodnessOfFitChanged.emit()
