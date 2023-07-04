# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject

from EasyApp.Logic.Logging import console


class Connections(QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent

        # Project
        self._proxy.project.dataChanged.connect(self.onProjectDataChanged)
        self._proxy.project.createdChanged.connect(self._proxy.project.save)

        # Model
        self._proxy.model.dataBlocksChanged.connect(self.onModelDataBlocksChanged)
        self._proxy.model.currentIndexChanged.connect(self.onModelCurrentIndexChanged)

        self._proxy.model.yCalcArraysChanged.connect(self.onModelYCalcArraysChanged)

        # Experiment
        self._proxy.experiment.dataBlocksChanged.connect(self.onExperimentDataBlocksChanged)
        self._proxy.experiment.dataBlocksMeasOnlyChanged.connect(self.onExperimentDataBlocksMeasOnlyChanged)
        #self._proxy.experiment.currentIndexChanged.connect(self.onExperimentCurrentIndexChanged)

        self._proxy.experiment.yMeasArraysChanged.connect(self.onExperimentYMeasArraysChanged)
        self._proxy.experiment.yBkgArraysChanged.connect(self.onExperimentYBkgArraysChanged)

        # Analysis
        self._proxy.analysis.definedChanged.connect(self.onAnalysisDefined)
        self._proxy.analysis.yCalcTotalChanged.connect(self.onAnalysisYCalcTotalChanged)

        # Fittables
        #self._proxy.fittables.dataChanged.connect(self.onFittablesDataChanged)
        self._proxy.fittables.nameFilterCriteriaChanged.connect(self.onFittablesFilterCriteriaChanged)
        self._proxy.fittables.variabilityFilterCriteriaChanged.connect(self.onFittablesFilterCriteriaChanged)
        self._proxy.fittables.paramsCountChanged.connect(self.onFittablesParamsCountChanged)

        # Fitting
        self._proxy.fitting.fitFinished.connect(self.onFittingFitFinished)
        self._proxy.fitting.chiSqSignificantlyChanged.connect(self.onFittingChiSqSignificantlyChanged)

    # Project

    def onProjectDataChanged(self):
        self._proxy.status.project = self._proxy.project.data['name']
        self._proxy.project.setNeedSaveToTrue

    # Model

    def onModelDataBlocksChanged(self):        
        # Project page
        #self._proxy.project.setNeedSaveToTrue()

        # Model page
        self._proxy.model.defined = bool(len(self._proxy.model.dataBlocks))

        console.debug("Updating structure view for the current model...")
        self._proxy.model.updateCurrentModelStructView()

        console.debug("Converting model data blocks to CIF...")
        self._proxy.model.setDataBlocksCif()

        if self._proxy.experiment.defined:
            console.debug("Updating calculated data for the current model...")
            self._proxy.model.updateCurrentModelYCalcArray()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug("Setting fittables on the analysis page...")
            self._proxy.fittables.set()
            #self._proxy.analysis.calculateYCalcTotal()

        # Status bar
        if self._proxy.model.defined:
            self._proxy.status.phaseCount = f'{len(self._proxy.model.dataBlocks)}'
        else:
            self._proxy.status.phaseCount = ''

        console.debug('')

    def onModelCurrentIndexChanged(self):
        self._proxy.model.updateCurrentModelStructView()

    def onModelYCalcArraysChanged(self):
        self._proxy.analysis.calculateYCalcTotal()

    #def onModelParameterEdited(self, page, blockIndex, name):
    #    self._proxy.model.setDataBlocksCif()
    #    if page != 'analysis':
    #        self._proxy.fittables.set()
    #        self._proxy.model.updateCurrentModelYCalcArray()
    #    else:
    #        self._proxy.model.updateYCalcArrayByIndex(blockIndex)
    #    self._proxy.project.setNeedSaveToTrue()
    #def onModelParamChanged_OLD(self):
    #    self._proxy.model.defined = bool(len(self._proxy.model.dataBlocks))
    #    if self._proxy.analysis.defined:
    #        self._proxy.fittables.set()
    #        self._proxy.analysis.calculateYCalcTotal()

    # Experiment

    def onExperimentDataBlocksChanged(self):
        # Project page
        #self._proxy.project.setNeedSaveToTrue()

        # Experiment page
        self._proxy.experiment.defined = bool(len(self._proxy.experiment.dataBlocks))

        console.debug("Updating background for the current experiment...")
        self._proxy.experiment.updateCurrentExperimentYBkgArray()  # NEED FIX: Check if bkg param changed

        console.debug("Converting experiment data blocks to CIF...")
        self._proxy.experiment.setDataBlocksCif()

        # Model page
        console.debug("Updating calculated data for the current model...")
        self._proxy.model.updateCurrentModelYCalcArray()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug("Setting fittables on the analysis page...")
            self._proxy.fittables.set()
            #self._proxy.analysis.calculateYCalcTotal()

        #self._proxy.plotting.drawBackgroundOnExperimentChart()
        console.debug('')

    def onExperimentDataBlocksMeasOnlyChanged(self, idx):
        # Experiment page
        self._proxy.experiment.setDataBlocksCifMeasOnly()
        self._proxy.experiment.addXYArraysAndChartRanges(idx)

    def onExperimentYMeasArraysChanged(self):
        self._proxy.status.dataPoints = f'{self._proxy.experiment._xArrays[self._proxy.experiment.currentIndex].size}'
        self._proxy.plotting.drawMeasuredOnExperimentChart()

    def onExperimentYBkgArraysChanged(self):
        #self._proxy.analysis.calculateYCalcTotal()
        #self._proxy.plotting.redrawBackgroundOnAnalysisChart()
        self._proxy.plotting.drawBackgroundOnExperimentChart()

    #def onExperimentCurrentIndexChanged(self):
    #    self._proxy.plotting.drawMeasuredOnExperimentChart()
    #    self._proxy.plotting.drawBackgroundOnExperimentChart()

    #def onExperimentParameterEdited(self, page, name):
    #    self._proxy.experiment.setDataBlocksCif()
    #    if name.startswith('background'):
    #        self._proxy.experiment.updateCurrentExperimentYBkgArray()
    #    if page != 'analysis':
    #        self._proxy.fittables.set()
    #    self._proxy.project.setNeedSaveToTrue()
    #def onExperimentParamChanged(self):
    #    self._proxy.experiment.defined = bool(len(self._proxy.experiment.dataBlocks))
    #    if self._proxy.model.defined:
    #        self._proxy.model.updateCurrentModelYCalcArray()
    #    if self._proxy.analysis.defined:
    #        self._proxy.fittables.set()
    #        self._proxy.analysis.calculateYCalcTotal()

    # Analysis

    def onAnalysisDefined(self):
        self._proxy.status.calculator = 'CrysPy'
        self._proxy.status.minimizer = 'Lmfit (BFGS)'
        self._proxy.fittables.set()
        console.debug(f"Updating all curves on analysis page using {self._proxy.plotting.currentLib1d}")
        self._proxy.plotting.drawAllOnAnalysisChart()

    def onAnalysisYCalcTotalChanged(self):
        console.debug(f"Updating curves on analysis page using {self._proxy.plotting.currentLib1d}")
        self._proxy.plotting.redrawCalculatedOnAnalysisChart()
        self._proxy.plotting.redrawBackgroundOnAnalysisChart()
        self._proxy.plotting.redrawResidualOnAnalysisChart()

    # Fittables

    def onFittablesDataChanged(self):
        self._proxy.fittables.setDataJson()

    def onFittablesFilterCriteriaChanged(self):
        self._proxy.fittables.set()

    def onFittablesParamsCountChanged(self):
        free = self._proxy.fittables.freeParamsCount
        fixed = self._proxy.fittables.fixedParamsCount
        total = free + fixed
        self._proxy.status.variables = f'{total} ({free} free, {fixed} fixed)'

    # Fitting

    def onFittingFitFinished(self):
        self._proxy.experiment.setDataBlocksCif()
        self._proxy.model.setDataBlocksCif()
        self._proxy.model.updateYCalcArrayByIndex(0)  # NED FIX

        console.debug("Setting fittables on the analysis page...")
        self._proxy.fittables.set()

    def onFittingChiSqSignificantlyChanged(self):
        self._proxy.model.updateYCalcArrayByIndex(0)
