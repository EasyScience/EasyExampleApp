# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json

from PySide6.QtCore import QObject, Signal, Slot, Property

from Logic.Calculators import GaussianCalculator
from Logic.Helpers import Converter


_DEFAULT_DATA_BLOCK = {
    'name': 'GaussianB',
    'params': {
        'shift': {
            'value': 3.0,
            'error': 0,
            'min': -5,
            'max': 5,
            'unit': '',
            'fittable': True,
            'fit': True
        },
        'width': {
            'value': 2.0,
            'error': 0,
            'min': 0,
            'max': 5,
            'unit': '',
            'fittable': True,
            'fit': True
        },
        'scale': {
            'value': 1.5,
            'error': 0,
            'min': 0.1,
            'max': 5,
            'unit': '',
            'fittable': True,
            'fit': True
        }
    }
}

class Model(QObject):
    definedChanged = Signal()
    currentIndexChanged = Signal()
    dataBlocksChanged = Signal()
    dataBlocksJsonChanged = Signal()
    yCalcArraysChanged = Signal()
    parameterEdited = Signal(str, str)

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._defined = False
        self._currentIndex = 0
        self._dataBlocks = []
        self._dataBlocksJson = ''
        self._yCalcArrays = []

    # QML accessible properties

    @Property(bool, notify=definedChanged)
    def defined(self):
        return self._defined
    
    @defined.setter
    def defined(self, newValue):
        if self._defined == newValue:
            return
        self._defined = newValue
        print(f"Model defined: {newValue}")
        self.definedChanged.emit()

    @Property(int, notify=currentIndexChanged)
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, newValue):
        if self._currentIndex == newValue:
            return
        self._currentIndex = newValue
        print(f"Current model index: {newValue}")
        self.currentIndexChanged.emit()

    @Property('QVariant', notify=dataBlocksChanged)
    def dataBlocks(self):
        return self._dataBlocks

    @Property(str, notify=dataBlocksJsonChanged)
    def dataBlocksJson(self):
        return self._dataBlocksJson

    # QML accessible methods

    @Slot()
    def addDefaultModel(self):
        print("Adding default model")
        dataBlock = _DEFAULT_DATA_BLOCK
        self.addDataBlock(dataBlock)
        yCalcArray = self.defaultYCalcArray()
        self.addYCalcArray(yCalcArray)

    @Slot(str)
    def loadModelFromFile(self, fpath):
        fpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', fpath))
        print(f"Loading a model from '{fpath}'")
        with open(fpath, 'r') as f:
            dataBlock = json.load(f)
        index = len(self._dataBlocks) - 1
        self.addDataBlock(dataBlock)
        yCalcArray = self.calculateYCalcArray(index)
        self.addYCalcArray(yCalcArray)

    @Slot(int)
    def removeModel(self, index):
        print(f"Removing model no. {index + 1}")
        del self._dataBlocks[index]
        del self._yCalcArrays[index]
        self.dataBlocksChanged.emit()
        self.yCalcArraysChanged.emit()
        print(f"Model no. {index + 1} has been removed")

    @Slot()
    def removeAllModels(self):
        self._dataBlocks.clear()
        self._yCalcArrays.clear()
        self.dataBlocksChanged.emit()
        self.yCalcArraysChanged.emit()
        print("All models have been removed")

    @Slot(str, int, str, str, str)
    def editParameter(self, page, blockIndex, name, item, value):
        block = 'model'
        if blockIndex is None:
            blockIndex = self._currentIndex
        print(f"Editing parameter '{block}[{blockIndex}].{name}.{item}' to '{value}' requested from '{page}' page")
        # Convert input value
        if item == 'value':
            value = float(value)
        elif item == 'fit':
            if value == 'true':
                value = True
            elif value == 'false':
                value = False
            self._dataBlocks[blockIndex]['params'][name]['error'] = 0
        # Update value
        if self._dataBlocks[blockIndex]['params'][name][item] == value:
            return
        self._dataBlocks[blockIndex]['params'][name][item] = value
        print(f"Parameter '{block}[{blockIndex}].{name}.{item}' has been changed to '{value}'")
        # Signalling value has been changed
        self.parameterEdited.emit(page, name)
        print(f"Data blocks for '{block}' has been changed")
        self.dataBlocksChanged.emit()

    # Private methods

    def defaultYCalcArray(self):
        xArray = self._proxy.experiment._xArrays[0]  # NEED FIX
        params = _DEFAULT_DATA_BLOCK['params']
        yCalcArray = GaussianCalculator.calculated(xArray, params)
        return yCalcArray

    def calculateYCalcArray(self, index):
        xArray = self._proxy.experiment._xArrays[0]  # NEED FIX
        params = self._dataBlocks[index]['params']
        yCalcArray = GaussianCalculator.calculated(xArray, params)
        return yCalcArray

    def updateCurrentModelYCalcArray(self):
        index = self._currentIndex
        self._yCalcArrays[index] = self.calculateYCalcArray(index)
        print(f"Pattern for model no. {index + 1} has been calculated")
        self.yCalcArraysChanged.emit()

    def addDataBlock(self, dataBlock):
        print(f"Adding data block (model parameters). Model no. {len(self._dataBlocks) + 1}")
        self._dataBlocks.append(dataBlock)
        self.dataBlocksChanged.emit()

    def addYCalcArray(self, yCalcArray):
        print(f"Adding y-calculated data. Model no. {len(self._dataBlocks)}")
        self._yCalcArrays.append(yCalcArray)
        self.yCalcArraysChanged.emit()

    #def calculateAllYArrays(self):
    #    for i in range(len(self._dataBlocks)):
    #        self.calculateSingleYArray(i)

    #def scaleSingleDataBlock(self, index):
    #    scale = self._proxy.experiment.models[index]['scale']
    #    self._yCalcArrays[index]['yArray'] *= scale
    #    self.calculatedDataChanged.emit()

    def setDataBlocksJson(self):
        self._dataBlocksJson = Converter.dictToJson(self._dataBlocks)
        print(f"Model dataBlocks have been converted to JSON string")
        self.dataBlocksJsonChanged.emit()
