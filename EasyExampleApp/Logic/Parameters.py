# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import math

from PySide6.QtCore import QObject, Signal, Slot, Property


class Parameters(QObject):
    fittablesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._fittables = []

        self._proxy.experiment.isCreatedChanged.connect(self.setFittables)
        self._proxy.model.isCreatedChanged.connect(self.setFittables)
        self._proxy.experiment.parametersChanged.connect(self.setFittables)
        self._proxy.model.parametersChanged.connect(self.setFittables)

    @Property('QVariant', notify=fittablesChanged)
    def fittables(self):
        return self._fittables

    @Slot(str, str, str, str)
    def edit(self, group, label, item, value):
        if group == 'experiment':
            self._proxy.experiment.editParameter(label, item, value)
        if group == 'model':
            self._proxy.model.editParameter(label, item, value)

    def setFittables(self):
        self._fittables = []
        for label, param in self._proxy.experiment.parameters.items():
            if param['fittable']:
                param['group'] = 'experiment'
                param['parent'] = self._proxy.experiment.description['label']
                param['label'] = label
                self._fittables.append(param)
        for label, param in self._proxy.model.parameters.items():
            if param['fittable']:
                param['group'] = 'model'
                param['parent'] = self._proxy.model.description['label']
                param['label'] = label
                self._fittables.append(param)
        self.fittablesChanged.emit()
