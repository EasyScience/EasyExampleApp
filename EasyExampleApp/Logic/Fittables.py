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
        "units": "",
        "value": 0,
        "enabeld": True
    }
]

class Parameter(dict):

    def __init__(self,
                value,
                idx = 0,
                error = 0.0,
                min = -1.0,
                max = 1.0,
                units = '',
                loopName = '',
                rowName = '',
                name = '',
                prettyName = '',
                url = '',
                cifDict = '',
                enabled = True,
                fittable = False,
                fit = False):
        self['value'] = value
        self['idx'] = idx
        self['enabled'] = enabled
        self['fittable'] = fittable
        self['fit'] = fit
        self['error'] = error
        self['group'] = ""
        self['min'] = min
        self['max'] = max
        self['loopName'] = loopName
        self['rowName'] = rowName
        self['name'] = name
        self['prettyName'] = prettyName
        self['url'] = url
        self['cifDict'] = cifDict
        self['parentIndex'] = 0
        self['parentName'] = ''
        self['units'] = units


class Fittables(QObject):
    dataChanged = Signal()
    dataJsonChanged = Signal()
    nameFilterCriteriaChanged = Signal()
    variabilityFilterCriteriaChanged = Signal()
    paramsCountChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._data = _EMPTY_DATA
        self._dataJson = ''
        self._nameFilterCriteria = ''
        self._variabilityFilterCriteria = ''
        self._freeParamsCount = 0
        self._fixedParamsCount = 0
        self._modelParamsCount = 0
        self._experimentParamsCount = 0

    @Property('QVariant', notify=dataChanged)
    def data(self):
        return self._data

    @Property(str, notify=dataJsonChanged)
    def dataJson(self):
        return self._dataJson

    @Property(str, notify=nameFilterCriteriaChanged)
    def nameFilterCriteria(self):
        return self._nameFilterCriteria

    @nameFilterCriteria.setter
    def nameFilterCriteria(self, newValue):
        if self._nameFilterCriteria == newValue:
            return
        self._nameFilterCriteria = newValue
        console.debug(f"Fittables table filter criteria changed to {newValue}")
        self.nameFilterCriteriaChanged.emit()

    @Property(str, notify=variabilityFilterCriteriaChanged)
    def variabilityFilterCriteria(self):
        return self._variabilityFilterCriteria

    @variabilityFilterCriteria.setter
    def variabilityFilterCriteria(self, newValue):
        if self._variabilityFilterCriteria == newValue:
            return
        self._variabilityFilterCriteria = newValue
        console.debug(f"Fittables table variability filter criteria changed to {newValue}")
        self.variabilityFilterCriteriaChanged.emit()

    @Property(float, notify=paramsCountChanged)
    def freeParamsCount(self):
        return self._freeParamsCount

    @Property(float, notify=paramsCountChanged)
    def fixedParamsCount(self):
        return self._fixedParamsCount

    @Property(float, notify=paramsCountChanged)
    def modelParamsCount(self):
        return self._modelParamsCount

    @Property(float, notify=paramsCountChanged)
    def experimentParamsCount(self):
        return self._experimentParamsCount

    @Slot(str, int, str, int, str, str, float)
    def edit(self, blockType, blockIndex, loopName, rowIndex, paramName, field, value):
        if loopName == '':
            console.debug(f"Changing fittable {blockType}[{blockIndex}].{paramName}.{field} to {value}")
            if blockType == 'experiment':
                self._proxy.experiment.setMainParam(paramName, field, value)
            elif blockType == 'model':
                self._proxy.model.setMainParam(paramName, field, value)
        else:
            console.debug(f"Changing fittable {blockType}[{blockIndex}].{loopName}[{rowIndex}].{paramName}.{field} to {value}")
            if blockType == 'experiment':
                self._proxy.experiment.setLoopParam(loopName, paramName, rowIndex, field, value)
            elif blockType == 'model':
                self._proxy.model.setLoopParam(loopName, paramName, rowIndex, field, value)

    def set(self):
        _data = []
        _freeParamsCount = 0
        _fixedParamsCount = 0
        _modelParamsCount = 0
        _experimentParamsCount = 0

        # Model params
        for i in range(len(self._proxy.model.dataBlocks)):
            block = self._proxy.model.dataBlocks[i]

            # Model main params
            for paramName, paramContent in block['params'].items():
                if paramContent['fittable']:
                    fittable = {}
                    fittable['blockType'] = 'model'
                    fittable['blockIndex'] = i
                    fittable['blockName'] = block['name']
                    fittable['paramName'] = paramName
                    fittable['fullName'] = f"{fittable['blockType']}.{fittable['blockName']}.{fittable['paramName'][1:]}"
                    fittable['iconifiedName'] = fittable['fullName']
                    fittable['enabled'] = paramContent['enabled']
                    fittable['value'] = paramContent['value']
                    fittable['error'] = paramContent['error']
                    fittable['min'] = paramContent['min']
                    fittable['max'] = paramContent['max']
                    fittable['units'] = paramContent['units']
                    fittable['fit'] = paramContent['fit']
                    if fittable['enabled']:
                        _modelParamsCount += 1
                        if fittable['fit']:
                            _freeParamsCount += 1
                        else:
                            _fixedParamsCount += 1
                        if self.nameFilterCriteria in fittable['fullName']:
                            if self.variabilityFilterCriteria == 'free' and fittable['fit']:
                                _data.append(fittable)
                            elif self.variabilityFilterCriteria == 'fixed' and not fittable['fit']:
                                _data.append(fittable)
                            elif self.variabilityFilterCriteria == 'all':
                                _data.append(fittable)
                            elif self.variabilityFilterCriteria == '':
                                _data.append(fittable)

            # Model loop params
            for loopName, loopContent in block['loops'].items():
                for rowIndex, param in enumerate(loopContent):
                    for paramName, paramContent in param.items():
                        if paramContent['fittable']:
                            fittable = {}
                            fittable['blockType'] = 'model'
                            fittable['blockIndex'] = i
                            fittable['blockName'] = block['name']
                            fittable['loopName'] = loopName
                            fittable['rowName'] = paramContent['rowName']
                            fittable['rowIndex'] = rowIndex
                            fittable['paramName'] = paramName
                            fittable['fullName'] = f"{fittable['blockType']}.{fittable['blockName']}.{fittable['loopName'][1:]}.{fittable['rowName']}.{fittable['paramName'][1:]}"
                            fittable['iconifiedName'] = fittable['fullName']
                            fittable['enabled'] = paramContent['enabled']
                            fittable['value'] = paramContent['value']
                            fittable['error'] = paramContent['error']
                            fittable['min'] = paramContent['min']
                            fittable['max'] = paramContent['max']
                            fittable['units'] = paramContent['units']
                            fittable['fit'] = paramContent['fit']
                            if fittable['enabled']:
                                _modelParamsCount += 1
                                if fittable['fit']:
                                    _freeParamsCount += 1
                                else:
                                    _fixedParamsCount += 1
                                if self.nameFilterCriteria in fittable['fullName']:
                                    if self.variabilityFilterCriteria == 'free' and fittable['fit']:
                                        _data.append(fittable)
                                    elif self.variabilityFilterCriteria == 'fixed' and not fittable['fit']:
                                        _data.append(fittable)
                                    elif self.variabilityFilterCriteria == 'all':
                                        _data.append(fittable)
                                    elif self.variabilityFilterCriteria == '':
                                        _data.append(fittable)

        # Experiment params
        for i in range(len(self._proxy.experiment.dataBlocks)):
            block = self._proxy.experiment.dataBlocks[i]

            # Experiment main params
            for paramName, paramContent in block['params'].items():
                if paramContent['fittable']:
                    fittable = {}
                    fittable['blockType'] = 'experiment'
                    fittable['blockIndex'] = i
                    fittable['blockName'] = block['name']
                    fittable['paramName'] = paramName
                    fittable['fullName'] = f"{fittable['blockType']}.{fittable['blockName']}.{fittable['paramName'][1:]}"
                    fittable['iconifiedName'] = fittable['fullName']
                    fittable['enabled'] = paramContent['enabled']
                    fittable['value'] = paramContent['value']
                    fittable['error'] = paramContent['error']
                    fittable['min'] = paramContent['min']
                    fittable['max'] = paramContent['max']
                    fittable['units'] = paramContent['units']
                    fittable['fit'] = paramContent['fit']
                    if fittable['enabled']:
                        _experimentParamsCount += 1
                        if fittable['fit']:
                            _freeParamsCount += 1
                        else:
                            _fixedParamsCount += 1
                        if self.nameFilterCriteria in fittable['fullName']:
                            if self.variabilityFilterCriteria == 'free' and fittable['fit']:
                                _data.append(fittable)
                            elif self.variabilityFilterCriteria == 'fixed' and not fittable['fit']:
                                _data.append(fittable)
                            elif self.variabilityFilterCriteria == 'all':
                                _data.append(fittable)
                            elif self.variabilityFilterCriteria == '':
                                _data.append(fittable)

            # Experiment loop params
            for loopName, loopContent in block['loops'].items():
                for rowIndex, param in enumerate(loopContent):
                    for paramName, paramContent in param.items():
                        if paramContent['fittable']:
                            fittable = {}
                            fittable['blockType'] = 'experiment'
                            fittable['blockIndex'] = i
                            fittable['blockName'] = block['name']
                            fittable['loopName'] = loopName
                            fittable['rowName'] = paramContent['rowName']
                            fittable['rowIndex'] = rowIndex
                            fittable['paramName'] = paramName
                            fittable['fullName'] = f"{fittable['blockType']}.{fittable['blockName']}.{fittable['loopName'][1:]}.{fittable['rowName']}.{fittable['paramName'][1:]}"
                            fittable['iconifiedName'] = fittable['fullName']
                            fittable['enabled'] = paramContent['enabled']
                            fittable['value'] = paramContent['value']
                            fittable['error'] = paramContent['error']
                            fittable['min'] = paramContent['min']
                            fittable['max'] = paramContent['max']
                            fittable['units'] = paramContent['units']
                            fittable['fit'] = paramContent['fit']
                            if fittable['enabled']:
                                _experimentParamsCount += 1
                                if fittable['fit']:
                                    _freeParamsCount += 1
                                else:
                                    _fixedParamsCount += 1
                                if self.nameFilterCriteria in fittable['fullName']:
                                    if self.variabilityFilterCriteria == 'free' and fittable['fit']:
                                        _data.append(fittable)
                                    elif self.variabilityFilterCriteria == 'fixed' and not fittable['fit']:
                                        _data.append(fittable)
                                    elif self.variabilityFilterCriteria == 'all':
                                        _data.append(fittable)
                                    elif self.variabilityFilterCriteria == '':
                                        _data.append(fittable)

        if True:  # len(_data):
            self._data = _data
            console.debug(' - Fittables have been changed')
            self.dataChanged.emit()
            self._freeParamsCount = _freeParamsCount
            self._fixedParamsCount = _fixedParamsCount
            self._modelParamsCount = _modelParamsCount
            self._experimentParamsCount = _experimentParamsCount
            self.paramsCountChanged.emit()

    def setDataJson(self):
        self._dataJson = Converter.dictToJson(self._data)
        console.debug(" - Fittables data have been converted to JSON string")
        self.dataJsonChanged.emit()
