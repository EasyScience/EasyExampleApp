# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property


class Parameters(QObject):
    fittablesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._fittables = []

    @Property('QVariant', notify=fittablesChanged)
    def fittables(self):
        return self._fittables

    @Slot(str, str, str, str)
    def edit(self, group, name, item, value):
        needSetFittables = False
        if group == 'experiment':
            self._proxy.experiment.editParameter(name, item, value, needSetFittables)
        elif group == 'model':
            self._proxy.model.editParameter(name, item, value, needSetFittables)

    def setFittables(self):
        self._fittables = []
        for name, param in self._proxy.experiment.parameters.items():
            if param['fittable']:
                param['group'] = 'experiment'
                param['parent'] = self._proxy.experiment.description['name']
                param['name'] = name
                self._fittables.append(param)
        for name, param in self._proxy.model.parameters.items():
            if param['fittable']:
                param['group'] = 'model'
                param['parent'] = self._proxy.model.description['name']
                param['name'] = name
                self._fittables.append(param)
        #for i in range(1000):
        #    self._fittables.append(self._fittables[0])
        self.fittablesChanged.emit()
