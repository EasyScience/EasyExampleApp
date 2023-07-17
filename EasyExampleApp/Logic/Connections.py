# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO


class Connections(QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._silent = False

        # Project
        self._proxy.project.dataChanged.connect(self.onProjectDataChanged)
        self._proxy.project.createdChanged.connect(self._proxy.project.save)

        # Model
        self._proxy.model.currentIndexChanged.connect(self.onModelCurrentIndexChanged)
        self._proxy.model.dataBlocksChanged.connect(self.onModelDataBlocksChanged)
        #self._proxy.model.yCalcArraysChanged.connect(self.onModelYCalcArraysChanged)

        # Experiment
        self._proxy.experiment.currentIndexChanged.connect(self.onExperimentCurrentIndexChanged)
        self._proxy.experiment.dataBlocksNoMeasChanged.connect(self.onExperimentDataBlocksNoMeasChanged)
        self._proxy.experiment.dataBlocksChanged.connect(self.onExperimentDataBlocksChanged)
        #self._proxy.experiment.yMeasArraysChanged.connect(self.onExperimentYMeasArraysChanged)
        #self._proxy.experiment.yBkgArraysChanged.connect(self.onExperimentYBkgArraysChanged)
        #self._proxy.experiment.yCalcTotalArraysChanged.connect(self.onExperimentYCalcTotalArraysChanged)
        #self._proxy.experiment.yResidArraysChanged.connect(self.onExperimentYResidArraysChanged)

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

    def onModelCurrentIndexChanged(self):
        # Model page
        console.debug("* Updating current model structure view...")
        self._proxy.model.updateCurrentModelStructView()

    def onModelDataBlocksChanged(self):        
        # Project page
        #self._proxy.project.setNeedSaveToTrue()

        # Model page
        console.debug(IO.formatMsg('main', 'Updating structure view for the current model...'))
        self._proxy.model.updateCurrentModelStructView()
        console.debug(IO.formatMsg('main', 'Converting model data blocks to CIF...'))
        self._proxy.model.setDataBlocksCif()

        # Experiment page
        if self._proxy.experiment.defined:
            console.debug(IO.formatMsg('main', 'Recalculating data...'))
            self._proxy.experiment.runCryspyCalculations()
            self._proxy.experiment.replaceArrays()
            console.debug(IO.formatMsg('main', f'Updating curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawBackgroundOnExperimentChart()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug(IO.formatMsg('main', f'Updating curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawCalculatedOnAnalysisChart()
            self._proxy.plotting.drawResidualOnAnalysisChart()
            console.debug(IO.formatMsg('main', 'Updating fittables on the analysis page...'))
            self._proxy.fittables.set()

        # Status bar
        if self._proxy.model.defined:
            self._proxy.status.phaseCount = f'{len(self._proxy.model.dataBlocks)}'
        else:
            self._proxy.status.phaseCount = ''

        console.debug('')

    #def onModelYCalcArraysChanged(self):
    #    self._proxy.analysis.calculateYCalcTotal()

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

    def onExperimentCurrentIndexChanged(self):
        # Experiment page
        console.debug(IO.formatMsg('main', f'Updating curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawMeasuredOnExperimentChart()
        self._proxy.plotting.drawBackgroundOnExperimentChart()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug(IO.formatMsg('main', f'Updating curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawMeasuredOnAnalysisChart()
            self._proxy.plotting.drawBackgroundOnAnalysisChart()
            self._proxy.plotting.drawCalculatedOnAnalysisChart()
            self._proxy.plotting.drawResidualOnAnalysisChart()

    def onExperimentDataBlocksChanged(self):
        # Project page
        #self._proxy.project.setNeedSaveToTrue()

        # Experiment page
        console.debug(IO.formatMsg('main', 'Calculating data...'))
        self._proxy.experiment.runCryspyCalculations()
        console.debug(IO.formatMsg('main', 'Adding arrays and ranges...'))
        self._proxy.experiment.addArraysAndChartRanges()
        console.debug(IO.formatMsg('main', f'Drawing curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawMeasuredOnExperimentChart()
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        console.debug(IO.formatMsg('main', 'Converting experiment data blocks to CIF...'))
        self._proxy.experiment.setDataBlocksCif()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug(IO.formatMsg('main', 'Setting fittables on the analysis page...'))
            self._proxy.fittables.set()
            console.debug(IO.formatMsg('main', f'Drawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawMeasuredOnAnalysisChart()
            self._proxy.plotting.drawBackgroundOnExperimentChart()
            self._proxy.plotting.drawCalculatedOnAnalysisChart()
            self._proxy.plotting.drawResidualOnAnalysisChart()

        # Status bar
        if self._proxy.experiment.defined:
            self._proxy.status.experimentsCount = f'{len(self._proxy.experiment.dataBlocksNoMeas)}'
        else:
            self._proxy.status.experimentsCount = ''

        # GUI upadte silently (without calling self.onExperimentDataBlocksNoMeasChanged)
        self._silent = True
        self._proxy.experiment.dataBlocksNoMeasChanged.emit()
        self._silent = False

        console.debug('')

    def onExperimentDataBlocksNoMeasChanged(self):
        if self._silent:
            return

        # Project page
        #self._proxy.project.setNeedSaveToTrue()

        # Experiment page
        console.debug(IO.formatMsg('main', 'Recalculating data...'))
        self._proxy.experiment.runCryspyCalculations()
        console.debug(IO.formatMsg('main', 'Replacing arrays...'))
        self._proxy.experiment.replaceArrays()
        console.debug(IO.formatMsg('main', 'Redrawing curves on experiment page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawBackgroundOnExperimentChart()
        console.debug(IO.formatMsg('main', 'Reconverting experiment data blocks to CIF...'))
        self._proxy.experiment.setDataBlocksCif()

        # Analysis page
        if self._proxy.analysis.defined:
            console.debug(IO.formatMsg('main', 'Updating fittables on the analysis page...'))
            self._proxy.fittables.set()
            console.debug(IO.formatMsg('main', 'Redrawing curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
            self._proxy.plotting.drawBackgroundOnExperimentChart()
            self._proxy.plotting.drawCalculatedOnAnalysisChart()
            self._proxy.plotting.drawResidualOnAnalysisChart()

        # Status bar
        if self._proxy.experiment.defined:
            self._proxy.status.experimentsCount = f'{len(self._proxy.experiment.dataBlocksNoMeas)}'
        else:
            self._proxy.status.experimentsCount = ''

        console.debug('')



        #####self._proxy.experiment.replaceChartRanges()
    #    #self._proxy.experiment.setDataBlocksCif()  # setDataBlocksCifMeasOnly()
    #    self._proxy.experiment.runCryspyCalculations()
    #    self._proxy.experiment.addArrays()

    #def onExperimentYMeasArraysChanged(self):
    #######    self._proxy.status.dataPoints = f'{self._proxy.experiment._xArrays[self._proxy.experiment.currentIndex].size}'
    #    self._proxy.plotting.drawMeasuredOnExperimentChart()

    #def onExperimentYBkgArraysChanged(self):
    #    #self._proxy.analysis.calculateYCalcTotal()
    #    #self._proxy.plotting.drawBackgroundOnAnalysisChart()
    #    self._proxy.plotting.drawBackgroundOnExperimentChart()

    #def onExperimentYCalcTotalArraysChanged(self):
    #    self._proxy.plotting.drawCalculatedOnAnalysisChart()

    #def onExperimentYResidArraysChanged(self):
    #    self._proxy.plotting.drawResidualOnAnalysisChart()

    # Analysis

    def onAnalysisDefined(self):
        self._proxy.status.calculator = 'CrysPy'
        self._proxy.status.minimizer = 'Lmfit (BFGS)'
        self._proxy.fittables.set()
        console.debug(IO.formatMsg('main', f'Updating curves on analysis page using {self._proxy.plotting.currentLib1d}...'))
        self._proxy.plotting.drawMeasuredOnAnalysisChart()
        self._proxy.plotting.drawBackgroundOnAnalysisChart()
        self._proxy.plotting.drawCalculatedOnAnalysisChart()
        self._proxy.plotting.drawResidualOnAnalysisChart()

    def onAnalysisYCalcTotalChanged(self):
        console.debug(f"Updating curves on analysis page using {self._proxy.plotting.currentLib1d}")
        self._proxy.plotting.drawCalculatedOnAnalysisChart()
        self._proxy.plotting.drawBackgroundOnAnalysisChart()
        self._proxy.plotting.drawResidualOnAnalysisChart()

    # Fittables

    #def onFittablesDataChanged(self):
    #    self._proxy.fittables.setDataJson()

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
        self._proxy.experiment.replaceArrays()
