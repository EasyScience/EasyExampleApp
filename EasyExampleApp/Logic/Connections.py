# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject


class Connections(QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent

        # Project
        self._proxy.project.dataChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self._proxy.project.createdChanged.connect(self._proxy.project.save)

        # Experiment
        self._proxy.experiment.dataLoaded.connect(self.onExperimentDataLoaded)
        self._proxy.experiment.parameterEdited.connect(self.onParameterEdited)

        # Model
        self._proxy.model.dataLoaded.connect(self.onModelDataLoaded)
        self._proxy.model.currentIndexChanged.connect(self._proxy.model.replaceYArrayOnModelChartAndRedraw)
        self._proxy.model.parameterEdited.connect(self.onParameterEdited)
        self._proxy.model.yArraysChanged.connect(self.onModelYArraysChanged)

        # Analysis
        self._proxy.analysis.createdChanged.connect(self.onAnalysisCreated)

        # Fitting
        self._proxy.fitting.fitFinishedChanged.connect(self.onFittingFitFinishedChanged)

    # Experiment

    def onExperimentDataLoaded(self):
        self._proxy.experiment.created = True
        self._proxy.experiment.replaceXYArraysOnExperimentChartAndRedraw()

    # Model

    def onModelDataLoaded(self):
        self._proxy.model.created = True
        self._proxy.model.calculate()
        self._proxy.model.replaceXArrayOnModelChart()
        self._proxy.model.replaceYArrayOnModelChartAndRedraw()
        self._proxy.project.setNeedSaveToTrue()

    def onModelYArraysChanged(self):
        if self._proxy.analysis.created:
            self._proxy.analysis.replaceModelTotalYArrayOnAnalysisChartAndRedraw()

    # Analysis

    def onAnalysisCreated(self):
        self._proxy.fittables.set()
        self._proxy.analysis.replaceExperimentXYArraysOnAnalysisChart()
        self._proxy.analysis.replaceModelTotalYArrayOnAnalysisChartAndRedraw()

    # Parameters

    def onParameterEdited(self, needSetFittables):
        if self._proxy.model.created:
            self._proxy.model.calculate()
            self._proxy.model.replaceYArrayOnModelChartAndRedraw()
        if needSetFittables:
            self._proxy.fittables.set()
        self._proxy.project.setNeedSaveToTrue()

    # Fitting

    def onFittingFitFinishedChanged(self):
        print(f'Fit finished: {self._proxy.fitting.fitFinished}')
        #needSetFittables = True
        #self._proxy.model.parametersEdited.emit(needSetFittables)
