# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Property

from Logic.Connections import Connections
from Logic.Project import Project
from Logic.Model import Model
from Logic.Experiment import Experiment
from Logic.Fitting import Fitting
from Logic.Parameters import Parameters
from Logic.Summary import Summary
from Logic.Status import Status
from Logic.Plotting import Plotting


class PyProxy(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project = Project(self)
        self._experiment = Experiment(self)
        self._model = Model(self)
        self._parameters = Parameters(self)
        self._fitting = Fitting(self)
        self._summary = Summary(self)
        self._status = Status(self)
        self._plotting = Plotting(self)
        self._connections = Connections(self)

    @Property('QVariant', constant=True)
    def connections(self):
        return self._connections

    @Property('QVariant', constant=True)
    def project(self):
        return self._project

    @Property('QVariant', constant=True)
    def experiment(self):
        return self._experiment

    @Property('QVariant', constant=True)
    def model(self):
        return self._model

    @Property('QVariant', constant=True)
    def fitting(self):
        return self._fitting

    @Property('QVariant', constant=True)
    def parameters(self):
        return self._parameters

    @Property('QVariant', constant=True)
    def summary(self):
        return self._summary

    @Property('QVariant', constant=True)
    def status(self):
        return self._status

    @Property('QVariant', constant=True)
    def plotting(self):
        return self._plotting
