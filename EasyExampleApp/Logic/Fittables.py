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

    def __init__(self,
                value,
                error=0.0,
                min=-1.0,
                max=1.0,
                unit='',
                enabled=True,
                fittable=False,
                fit=False):
        self['value'] = value
        self['enabled'] = enabled
        self['fittable'] = fittable
        self['fit'] = fit
        self['error'] = error
        self['group'] = ""
        self['min'] = min
        self['max'] = max
        self['name'] = ''
        self['parentIndex'] = 0
        self['parentName'] = ''
        self['unit'] = unit


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

    @Slot(str, int, str, int, str, float)
    def edit(self, blockType, blockIndex, loopName, paramIndex, paramName, value):
        if loopName == '':
            console.debug(f"Editing fittable {blockType}[{blockIndex}].{paramName}.value to '{value}'")
            if blockType == 'experiment':
                self._proxy.experiment.setMainParameterValue(paramName, value)
            elif blockType == 'model':
                self._proxy.model.setMainParameterValue(paramName, value)
        else:
            console.debug(f"Editing fittable {blockType}[{blockIndex}].{loopName}[{paramIndex}].{paramName}.value to '{value}'")
            if blockType == 'experiment':
                self._proxy.experiment.setLoopParamValue(loopName, paramName, paramIndex, value)
            elif blockType == 'model':
                self._proxy.model.setLoopParamValue(loopName, paramName, paramIndex, value)

    def set(self):
        console.debug('Fittables have been changed')
        _data = []

        for i in range(len(self._proxy.experiment.dataBlocks)):
            block = self._proxy.experiment.dataBlocks[i]

            for paramName, paramContent in block['params'].items():
                if paramContent['fittable']:
                    fittable = {}
                    fittable['blockType'] = 'experiment'
                    fittable['blockIndex'] = i
                    fittable['blockName'] = block['name']
                    fittable['paramName'] = paramName
                    fittable['enabled'] = paramContent['enabled']
                    fittable['value'] = paramContent['value']
                    fittable['error'] = paramContent['error']
                    fittable['min'] = paramContent['min']
                    fittable['max'] = paramContent['max']
                    fittable['unit'] = paramContent['unit']
                    fittable['fit'] = paramContent['fit']
                    _data.append(fittable)

            for loopName, loopContent in block['loops'].items():
                for paramIndex, param in enumerate(loopContent):
                    for paramName, paramContent in param.items():
                        if paramContent['fittable']:
                            fittable = {}
                            fittable['blockType'] = 'experiment'
                            fittable['blockIndex'] = i
                            fittable['blockName'] = block['name']
                            fittable['loopName'] = loopName
                            fittable['paramIndex'] = paramIndex
                            fittable['paramName'] = paramName
                            fittable['enabled'] = paramContent['enabled']
                            fittable['value'] = paramContent['value']
                            fittable['error'] = paramContent['error']
                            fittable['min'] = paramContent['min']
                            fittable['max'] = paramContent['max']
                            fittable['unit'] = paramContent['unit']
                            fittable['fit'] = paramContent['fit']
                            _data.append(fittable)

        for i in range(len(self._proxy.model.dataBlocks)):
            block = self._proxy.model.dataBlocks[i]

            for paramName, paramContent in block['params'].items():
                if paramContent['fittable']:
                    fittable = {}
                    fittable['blockType'] = 'model'
                    fittable['blockIndex'] = i
                    fittable['blockName'] = block['name']
                    fittable['paramName'] = paramName
                    fittable['enabled'] = paramContent['enabled']
                    fittable['value'] = paramContent['value']
                    fittable['error'] = paramContent['error']
                    fittable['min'] = paramContent['min']
                    fittable['max'] = paramContent['max']
                    fittable['unit'] = paramContent['unit']
                    fittable['fit'] = paramContent['fit']
                    _data.append(fittable)

            for loopName, loopContent in block['loops'].items():
                for paramIndex, param in enumerate(loopContent):
                    for paramName, paramContent in param.items():
                        if paramContent['fittable']:
                            fittable = {}
                            fittable['blockType'] = 'model'
                            fittable['blockIndex'] = i
                            fittable['blockName'] = block['name']
                            fittable['loopName'] = loopName
                            fittable['paramIndex'] = paramIndex
                            fittable['paramName'] = paramName
                            fittable['enabled'] = paramContent['enabled']
                            fittable['value'] = paramContent['value']
                            fittable['error'] = paramContent['error']
                            fittable['min'] = paramContent['min']
                            fittable['max'] = paramContent['max']
                            fittable['unit'] = paramContent['unit']
                            fittable['fit'] = paramContent['fit']
                            _data.append(fittable)

        if len(_data):
            self._data = _data
            self.dataChanged.emit()

    def setDataJson(self):
        self._dataJson = Converter.dictToJson(self._data)
        console.debug("Fittables data have been converted to JSON string")
        self.dataJsonChanged.emit()
