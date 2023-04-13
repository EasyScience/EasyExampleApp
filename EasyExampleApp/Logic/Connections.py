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
        self._proxy.experiment.dataBlocksChanged.connect(self.onExperimentDataBlocksChanged)
        self._proxy.experiment.yMeasArraysChanged.connect(self.onExperimentYMeasArraysChanged)
        self._proxy.experiment.yBkgArraysChanged.connect(self.onExperimentYBkgArraysChanged)
        self._proxy.experiment.parameterEdited.connect(self.onExperimentParameterEdited)
        self._proxy.experiment.currentIndexChanged.connect(self.onExperimentCurrentIndexChanged)

        # Model
        self._proxy.model.dataBlocksChanged.connect(self.onModelDataBlocksChanged)
        self._proxy.model.yCalcArraysChanged.connect(self.onModelYCalcArraysChanged)
        self._proxy.model.parameterEdited.connect(self.onModelParameterEdited)
        self._proxy.model.currentIndexChanged.connect(self.onModelCurrentIndexChanged)

        # Analysis
        self._proxy.analysis.definedChanged.connect(self.onAnalysisDefined)
        self._proxy.analysis.yCalcTotalChanged.connect(self.onAnalysisYCalcTotalChanged)

        self._proxy.fittables.dataChanged.connect(self.onFittablesDataChanged)

        # Fitting
        self._proxy.fitting.fitFinishedChanged.connect(self.onFittingFitFinishedChanged)

    # Experiment

    def onExperimentDataBlocksChanged(self):
        self._proxy.experiment.defined = bool(len(self._proxy.experiment.dataBlocks))
        self._proxy.experiment.setDataBlocksJson()

    def onExperimentYMeasArraysChanged(self):
        self._proxy.plotting.drawMeasuredOnExperimentChart()

    def onExperimentYBkgArraysChanged(self):
        self._proxy.analysis.calculateYCalcTotal()
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        self._proxy.plotting.redrawBackgroundOnAnalysisChart()

    def onExperimentParameterEdited(self, page, name):
        self._proxy.experiment.setDataBlocksJson()
        if name.startswith('background'):
            self._proxy.experiment.updateCurrentExperimentYBkgArray()
        if page != 'analysis':
            self._proxy.fittables.set()

    def onExperimentCurrentIndexChanged(self):
        self._proxy.plotting.drawMeasuredOnExperimentChart()
        self._proxy.plotting.drawBackgroundOnExperimentChart()

    # Model

    def onModelDataBlocksChanged(self):
        self._proxy.model.defined = bool(len(self._proxy.model.dataBlocks))
        self._proxy.model.setDataBlocksJson()

    def onModelYCalcArraysChanged(self):
        self._proxy.analysis.calculateYCalcTotal()
        self._proxy.plotting.drawCalculatedOnModelChart()

    def onModelParameterEdited(self, page, name):
        self._proxy.model.setDataBlocksJson()
        self._proxy.model.updateCurrentModelYCalcArray()  # !!!!!! if called from 'analysis' page, one need to update YCalcArray associated with the changed value !!!!!
        if page != 'analysis':
            self._proxy.fittables.set()

    def onModelCurrentIndexChanged(self):
        self._proxy.plotting.drawCalculatedOnModelChart()

    # Analysis

    def onAnalysisDefined(self):
        self._proxy.fittables.set()
        self._proxy.plotting.drawAllOnAnalysisChart()

    def onAnalysisYCalcTotalChanged(self):
        self._proxy.plotting.redrawCalculatedOnAnalysisChart()

    # Fittables

    def onFittablesDataChanged(self):
        self._proxy.fittables.setDataJson()

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
