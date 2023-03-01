# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject


class Connections(QObject):

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent

        # Project
        self._proxy.project.nameChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self._proxy.project.descriptionChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self._proxy.project.isCreatedChanged.connect(self._proxy.project.save)

        # Experiment
        self._proxy.experiment.descriptionChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self._proxy.experiment.isCreatedChanged.connect(self.onExperimentIsCreatedChanged)
        self._proxy.experiment.parameterEdited.connect(self.onExperimentParameterEdited)
        self._proxy.experiment.parametersEdited.connect(self.onExperimentParametersEdited)
        self._proxy.experiment.dataSizeChanged.connect(self.onExperimentDataSizeChanged)

        # Model
        self._proxy.model.descriptionChanged.connect(self._proxy.project.setNeedSaveToTrue)
        self._proxy.model.isCreatedChanged.connect(self.onModelIsCreatedChanged)
        self._proxy.model.parameterEdited.connect(self.onModelParameterEdited)
        self._proxy.model.parametersEdited.connect(self.onModelParametersEdited)

        # Fitting
        self._proxy.fitting.fitFinishedChanged.connect(self.onFittingFitFinishedChanged)

    # Experiment

    def onExperimentIsCreatedChanged(self):
        print(f'Experiment created: {self._proxy.experiment.isCreated}')
        self._proxy.parameters.setFittables()
        self._proxy.project.setNeedSaveToTrue()

    def onExperimentParameterEdited(self, needSetFittables):
        self._proxy.experiment.parametersEdited.emit(needSetFittables)

    def onExperimentParametersEdited(self, needSetFittables):
        print(f'Experiment parameters changed. Need set fittables: {needSetFittables}')
        self._proxy.experiment.parametersChanged.emit()
        self._proxy.experiment.loadData()
        if needSetFittables:
            self._proxy.parameters.setFittables()
        self._proxy.project.setNeedSaveToTrue()

    def onExperimentDataSizeChanged(self):
        print(f'Experiment data size: {self._proxy.experiment.dataSize}')
        self._proxy.experiment.loadData()
        if self._proxy.model.isCreated:
            self._proxy.model.calculateData()

    # Model

    def onModelIsCreatedChanged(self):
        print(f'Model created: {self._proxy.model.isCreated}')
        self._proxy.parameters.setFittables()
        self._proxy.project.setNeedSaveToTrue()

    def onModelParameterEdited(self, needSetFittables):
        self._proxy.model.parametersEdited.emit(needSetFittables)

    def onModelParametersEdited(self, needSetFittables):
        self._proxy.model.parametersChanged.emit()
        self._proxy.model.calculateData()
        if needSetFittables:
            self._proxy.parameters.setFittables()
        self._proxy.project.setNeedSaveToTrue()

    # Fitting

    def onFittingFitFinishedChanged(self):
        print(f'Fit finished: {self._proxy.fitting.fitFinished}')
        needSetFittables = True
        self._proxy.model.parametersEdited.emit(needSetFittables)
