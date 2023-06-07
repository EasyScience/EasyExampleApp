# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property

from EasyApp.Logic.Logging import console
from Logic.Helpers import Converter

_EMPTY_DATA = [
    {
        "error": 0,
        "fit": True,
        "group": "",
        "max": 1,
        "min": -1,
        "name": "",
        "parentIndex": 0,
        "parentName": "",
        "unit": "",
        "value": 0
    }
]

class Parameter(dict):

    def __init__(self, value, fittable=False):
        self['value'] = value
        self['fittable'] = fittable
        self['fit'] = False
        self['error'] = 0
        self['group'] = ""
        self['max'] = 100
        self['min'] = -100
        self['name'] = ""
        self['parentIndex'] = 0
        self['parentName'] = ""
        self['unit'] = ""


class Fittables(QObject):
    dataChanged = Signal()
    dataJsonChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._data = _EMPTY_DATA
        self._dataJson = ''

    @Property('QVariant', notify=dataChanged)
    def data(self):
        return self._data

    @Property(str, notify=dataJsonChanged)
    def dataJson(self):
        return self._dataJson

    @Slot(str, int, str, str, str)
    def edit(self, block, blockIndex, name, item, value):
        console.debug(f"Editing fittable '{block}[{blockIndex}].{name}.{item}' to '{value}'")
        page = 'analysis'
        if block == 'experiment':
            self._proxy.experiment.editParameter(page, blockIndex, name, item, value)
        elif block == 'model':
            self._proxy.model.editParameter(page, blockIndex, name, item, value)

    def set(self):
        console.debug('Fittables have been changed')
        _data = []
        for i in range(len(self._proxy.experiment.dataBlocks)):
            block = self._proxy.experiment.dataBlocks[i]
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
        for i in range(len(self._proxy.model.dataBlocks)):
            block = self._proxy.model.dataBlocks[i]
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

    def setDataJson(self):
        self._dataJson = Converter.dictToJson(self._data)
        console.debug("Fittables data have been converted to JSON string")
        self.dataJsonChanged.emit()
