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
        #self._proxy.experiment.currentIndexChanged.connect(self.onExperimentCurrentIndexChanged)

        self._proxy.experiment.yMeasArraysChanged.connect(self.onExperimentYMeasArraysChanged)
        self._proxy.experiment.yBkgArraysChanged.connect(self.onExperimentYBkgArraysChanged)

        # Analysis
        self._proxy.analysis.definedChanged.connect(self.onAnalysisDefined)
        self._proxy.analysis.yCalcTotalChanged.connect(self.onAnalysisYCalcTotalChanged)

        # Fittables
        self._proxy.fittables.dataChanged.connect(self.onFittablesDataChanged)

        # Fitting
        self._proxy.fitting.fitFinished.connect(self.onFittingFitFinished)
        self._proxy.fitting.chiSqSignificantlyChanged.connect(self.onFittingChiSqSignificantlyChanged)




    # Project

    def onProjectDataChanged(self):
        self._proxy.status.project = self._proxy.project.data['name']
        self._proxy.project.setNeedSaveToTrue


    # Model

    def onModelDataBlocksChanged(self):
        self._proxy.model.defined = bool(len(self._proxy.model.dataBlocks))

        if self._proxy.model.defined:
            self._proxy.status.phaseCount = f'{len(self._proxy.model.dataBlocks)}'
        else:
            self._proxy.status.phaseCount = ''

        self._proxy.model.updateCurrentModelStructView()
        #self._proxy.model.setDataBlocksJson()
        #self._proxy.project.setNeedSaveToTrue()
        if self._proxy.analysis.defined:
            self._proxy.fittables.set()
            #self._proxy.analysis.calculateYCalcTotal()

        console.debug('')

    def onModelCurrentIndexChanged(self):
        self._proxy.model.updateCurrentModelStructView()
        #self._proxy.plotting.drawCalculatedOnModelChart()

    def onModelYCalcArraysChanged(self):
        self._proxy.analysis.calculateYCalcTotal()
        ############self._proxy.plotting.drawCalculatedOnModelChart()

    #def onModelParameterEdited(self, page, blockIndex, name):
    #    self._proxy.model.setDataBlocksJson()
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
        self._proxy.experiment.defined = bool(len(self._proxy.experiment.dataBlocks))

        self._proxy.experiment.updateCurrentExperimentYBkgArray()  # NEED FIX: Check if bkg param changed
        #self._proxy.plotting.drawBackgroundOnExperimentChart()
        #self._proxy.experiment.setDataBlocksJson()
        #self._proxy.project.setNeedSaveToTrue()
        if self._proxy.analysis.defined:
            self._proxy.fittables.set()
            #self._proxy.analysis.calculateYCalcTotal()

        console.debug('')

    #def onExperimentCurrentIndexChanged(self):
    #    self._proxy.plotting.drawMeasuredOnExperimentChart()
    #    self._proxy.plotting.drawBackgroundOnExperimentChart()

    def onExperimentYMeasArraysChanged(self):
        #####self._proxy.status.refresh()
        self._proxy.status.dataPoints = f'{self._proxy.experiment._xArrays[self._proxy.experiment.currentIndex].size}'
        self._proxy.plotting.drawMeasuredOnExperimentChart()

    def onExperimentYBkgArraysChanged(self):
        #self._proxy.analysis.calculateYCalcTotal()
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        #self._proxy.plotting.redrawBackgroundOnAnalysisChart()

    #def onExperimentParameterEdited(self, page, name):
    #    self._proxy.experiment.setDataBlocksJson()
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
        self._proxy.plotting.drawAllOnAnalysisChart()

    def onAnalysisYCalcTotalChanged(self):
        self._proxy.plotting.redrawCalculatedOnAnalysisChart()
        self._proxy.plotting.redrawBackgroundOnAnalysisChart()
        self._proxy.plotting.redrawResidualOnAnalysisChart()




    # Fittables

    def onFittablesDataChanged(self):
        self._proxy.fittables.setDataJson()





    # Fitting

    def onFittingFitFinished(self):
        self._proxy.experiment.setDataBlocksJson()
        self._proxy.model.setDataBlocksJson()
        self._proxy.model.updateYCalcArrayByIndex(0)  # NED FIX
        self._proxy.fittables.set()

    def onFittingChiSqSignificantlyChanged(self):
        self._proxy.model.updateYCalcArrayByIndex(0)
