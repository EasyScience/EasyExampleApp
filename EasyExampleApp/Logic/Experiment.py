# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json
import numpy as np

from PySide6.QtCore import QObject, Signal, Slot, Property

from Logic.Calculators import GaussianCalculator
from Logic.Helpers import Converter
from Logic.Logging import console


_DEFAULT_DATA_BLOCK = {
    'name': 'PicoScopeB',
    'params': {
        'xMin': {
            'value': -10.0,
            'fittable': False
        },
        'xMax': {
            'value': 10.0,
            'fittable': False
        },
        'xStep': {
            'value': 0.05,
            'fittable': False
        },
        'background_min': {
            'value': 0.5,
            'error': 0,
            'min': -5,
            'max': 5,
            'unit': '',
            'fittable': True,
            'fit': True
        },
        'background_max': {
            'value': 0.75,
            'error': 0,
            'min': -5,
            'max': 5,
            'unit': '',
            'fittable': True,
            'fit': True
        }
    }
}

class Experiment(QObject):
    definedChanged = Signal()
    currentIndexChanged = Signal()
    dataBlocksChanged = Signal()
    dataBlocksJsonChanged = Signal()
    yMeasArraysChanged = Signal()
    yBkgArraysChanged = Signal()
    parameterEdited = Signal(str, str)

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._defined = False
        self._currentIndex = 0
        self._dataBlocks = []
        self._dataBlocksJson = ''
        self._xArrays = []
        self._yMeasArrays = []
        self._yBkgArrays = []

    # QML accessible properties

    @Property(bool, notify=definedChanged)
    def defined(self):
        return self._defined

    @defined.setter
    def defined(self, newValue):
        if self._defined == newValue:
            return
        self._defined = newValue
        console.debug(f"Experiment defined: {newValue}")
        self.definedChanged.emit()

    @Property(int, notify=currentIndexChanged)
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, newValue):
        if self._currentIndex == newValue:
            return
        self._currentIndex = newValue
        console.debug(f"Current experiment index: {newValue}")
        self.currentIndexChanged.emit()

    @Property('QVariant', notify=dataBlocksChanged)
    def dataBlocks(self):
        return self._dataBlocks

    @Property(str, notify=dataBlocksJsonChanged)
    def dataBlocksJson(self):
        return self._dataBlocksJson

    # QML accessible methods

    @Slot()
    def addDefaultExperiment(self):
        console.debug('Adding default experiment')
        dataBlock = _DEFAULT_DATA_BLOCK
        xArray = self.defaultXArray()
        yMeasArray = self.defaultYMeasArray()
        yBkgArray = self.defaultYBkgArray()
        self.addDataBlock(dataBlock)
        self.addXArray(xArray)
        self.addYMeasArray(yMeasArray)
        self.addYBkgArray(yBkgArray)

    @Slot(str)
    def loadExperimentFromFile(self, fpath):
        fpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', fpath))
        console.debug(f"Loading an experiment from '{fpath}'")
        # add to dataBlocks, xArrays, yMeasArrays
        with open(fpath, 'r') as f:
            dataBlock = json.load(f)
        xArray = self.defaultXArray()  # NEED FIX
        yMeasArray = self.defaultYMeasArray()  # NEED FIX
        if 'xArray' and 'yMeasArray' in dataBlock.keys():
            xArray = np.array(dataBlock['xArray'])
            yMeasArray = np.array(dataBlock['yMeasArray'])
            del dataBlock['xArray']
            del dataBlock['yMeasArray']
        self.addDataBlock(dataBlock)
        self.addXArray(xArray)
        self.addYMeasArray(yMeasArray)
        # add to yBkgArray
        yBkgArray = self.defaultYBkgArray()  # NEED FIX
        if 'background_min' and 'background_max' in dataBlock['params'].keys():
            index = len(self._dataBlocks) - 1
            yBkgArray = self.calculateYBkgArray(index)
        self.addYBkgArray(yBkgArray)

    @Slot(int)
    def removeExperiment(self, index):
        console.debug(f"Removing experiment no. {index + 1}")
        self.currentIndex = index - 1
        del self._dataBlocks[index]
        del self._xArrays[index]
        del self._yMeasArrays[index]
        del self._yBkgArrays[index]
        self.dataBlocksChanged.emit()
        self.yMeasArraysChanged.emit()
        self.yBkgArraysChanged.emit()
        console.debug(f"Experiment no. {index + 1} has been removed")

    @Slot()
    def removeAllExperiments(self):
        self._dataBlocks.clear()
        self._xArrays.clear()
        self._yMeasArrays.clear()
        self.dataBlocksChanged.emit()
        self.yMeasArraysChanged.emit()
        self.yBkgArraysChanged.emit()
        console.debug("All experiments have been removed")

    @Slot(str, int, str, str, str)
    def editParameter(self, page, blockIndex, name, item, value):
        block = 'experiment'
        if blockIndex is None:
            blockIndex = self._currentIndex
        console.debug(f"Editing parameter '{block}[{blockIndex}].{name}.{item}' to '{value}' requested from '{page}' page")
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
        console.debug(f"Parameter '{block}[{blockIndex}].{name}.{item}' has been changed to '{value}'")
        # Signalling value has been changed
        self.parameterEdited.emit(page, name)
        console.debug(f"Data blocks for '{block}' has been changed")
        self.dataBlocksChanged.emit()

    # Private methods

    def defaultXArray(self):
        xMin = _DEFAULT_DATA_BLOCK['params']['xMin']['value']
        xMax = _DEFAULT_DATA_BLOCK['params']['xMax']['value']
        xStep = _DEFAULT_DATA_BLOCK['params']['xStep']['value']
        xArray = np.arange(xMin, xMax + xStep, xStep)
        return xArray

    def defaultYMeasArray(self):
        xArray = self.defaultXArray()
        params1 = {'shift': {'value': -1.0}, 'width': {'value': 1.5}, 'scale': {'value': 2.5}}
        yArray1 = GaussianCalculator.pseudoMeasured(xArray, params1)
        params2 = {'shift': {'value': 0.0}, 'width': {'value': 0.5}, 'scale': {'value': 0.5}}
        yArray2 = GaussianCalculator.pseudoMeasured(xArray, params2)
        background = self.defaultYBkgArray()
        yMeasArray = yArray1 + yArray2 + background
        return yMeasArray

    def defaultYBkgArray(self):
        xArray = self.defaultXArray()
        xMin = _DEFAULT_DATA_BLOCK['params']['xMin']['value']
        xMax = _DEFAULT_DATA_BLOCK['params']['xMax']['value']
        yBkgMin = _DEFAULT_DATA_BLOCK['params']['background_min']['value']
        yBkgMax = _DEFAULT_DATA_BLOCK['params']['background_max']['value']
        xBkgPoints = np.array([xMin, xMax])
        yBkgPoints = np.array([yBkgMin, yBkgMax])
        yBkgArray = np.interp(xArray, xBkgPoints, yBkgPoints)
        return yBkgArray

    def calculateYBkgArray(self, index):
        xArray = self._xArrays[index]
        xMin = self._dataBlocks[index]['params']['xMin']['value']
        xMax = self._dataBlocks[index]['params']['xMax']['value']
        yBkgMin = self._dataBlocks[index]['params']['background_min']['value']
        yBkgMax = self._dataBlocks[index]['params']['background_max']['value']
        xBkgPoints = np.array([xMin, xMax])
        yBkgPoints = np.array([yBkgMin, yBkgMax])
        yBkgArray = np.interp(xArray, xBkgPoints, yBkgPoints)
        return yBkgArray

    def updateCurrentExperimentYBkgArray(self):
        index = self._currentIndex
        self._yBkgArrays[index] = self.calculateYBkgArray(index)
        console.debug(f"Background for experiment no. {index + 1} has been calculated")
        self.yBkgArraysChanged.emit()

    def addDataBlock(self, dataBlock):
        console.debug(f"Adding data block (instrument parameters). Experiment no. {len(self._dataBlocks) + 1}")
        self._dataBlocks.append(dataBlock)
        self.dataBlocksChanged.emit()

    def addXArray(self, xArray):
        console.debug(f"Adding x data. Experiment no. {len(self._dataBlocks)}")
        self._xArrays.append(xArray)

    def addYMeasArray(self, yMeasArray):
        console.debug(f"Adding y-measured data. Experiment no. {len(self._dataBlocks)}")
        self._yMeasArrays.append(yMeasArray)
        self.yMeasArraysChanged.emit()

    def addYBkgArray(self, yBkgArray):
        console.debug(f"Adding y-background data. Experiment no. {len(self._dataBlocks)}")
        self._yBkgArrays.append(yBkgArray)
        self.yBkgArraysChanged.emit()

    def setDataBlocksJson(self):
        console.debug("Converting experiment dataBlocks to JSON string")
        self._dataBlocksJson = Converter.dictToJson(self._dataBlocks)
        console.debug("Experiment dataBlocks have been converted to JSON string")
        self.dataBlocksJsonChanged.emit()
