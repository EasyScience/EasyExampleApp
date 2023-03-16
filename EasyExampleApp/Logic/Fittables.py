# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property


_EMPTY_DATA = [
    {
        "error": 0,
        "fit": True,
        "group": "",
        "max": 1,
        "min": -1,
        "name": "background",
        "parentIndex": 0,
        "parentName": "",
        "unit": "",
        "value": 0
    }
]

class Fittables(QObject):
    dataChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._data = _EMPTY_DATA

    @Property('QVariant', notify=dataChanged)
    def data(self):
        return self._data

    @Slot(str, int, str, str, str)
    def edit(self, group, parentIndex, name, item, value):
        needSetFittables = False
        if group == 'experiment':
            self._proxy.experiment.editParameter(parentIndex, name, item, value, needSetFittables)
        elif group == 'model':
            self._proxy.model.editParameter(parentIndex, name, item, value, needSetFittables)

    def set(self):
        _data = []
        for i in range(len(self._proxy.experiment.data)):
            block = self._proxy.experiment.data[i]
            for name, param in block['params'].items():
                if param['fittable']:
                    fittable = {}
                    fittable['group'] = 'experiment'
                    fittable['name'] = name
                    fittable['parentIndex'] = i
                    fittable['parentName'] = block['name']
                    fittable['value'] = param['value']
                    fittable['error'] = param['error']
                    fittable['min'] = param['min']
                    fittable['max'] = param['max']
                    fittable['unit'] = param['unit']
                    fittable['fit'] = param['fit']
                    _data.append(fittable)
        for i in range(len(self._proxy.model.data)):
            block = self._proxy.model.data[i]
            for name, param in block['params'].items():
                if param['fittable']:
                    fittable = {}
                    fittable['group'] = 'model'
                    fittable['name'] = name
                    fittable['parentIndex'] = i
                    fittable['parentName'] = block['name']
                    fittable['value'] = param['value']
                    fittable['error'] = param['error']
                    fittable['min'] = param['min']
                    fittable['max'] = param['max']
                    fittable['unit'] = param['unit']
                    fittable['fit'] = param['fit']
                    _data.append(fittable)
        if len(_data):
            self._data = _data
            self.dataChanged.emit()
