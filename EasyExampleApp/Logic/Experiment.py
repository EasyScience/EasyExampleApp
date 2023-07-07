# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot, Property

from EasyApp.Logic.Logging import console
from Logic.Calculators import GaussianCalculator
from Logic.Fittables import Parameter
from Logic.Helpers import Converter, IO
from Logic.Data import Data

try:
    import cryspy
    from cryspy.H_functions_global.function_1_cryspy_objects import \
        file_to_globaln, str_to_globaln
    console.debug('CrysPy modules have been imported')
except ImportError:
    console.debug('No CrysPy module have been found')

_DEFAULT_DATA_BLOCK = """data_default

_diffrn_radiation_probe neutron
_diffrn_radiation_wavelength 1.87

_pd_meas_2theta_offset 0
_pd_meas_2theta_range_min 36.5
_pd_meas_2theta_range_max 39
_pd_meas_2theta_range_inc 0.5

_pd_instr_resolution_u 0.2
_pd_instr_resolution_v -0.5
_pd_instr_resolution_w 0.4
_pd_instr_resolution_x 0
_pd_instr_resolution_y 0

_pd_instr_reflex_asymmetry_p1 0
_pd_instr_reflex_asymmetry_p2 0
_pd_instr_reflex_asymmetry_p3 0
_pd_instr_reflex_asymmetry_p4 0

loop_
_phase_label
_phase_scale
default 1

loop_
_pd_background_2theta
_pd_background_intensity
10  1
170 1

loop_
_pd_meas_2theta
_pd_meas_intensity
_pd_meas_intensity_sigma
36.5 1    1
37.0 10   3
37.5 700  25
38.0 1100 30
38.5 50   7
39.0 1    1
"""


class Experiment(QObject):
    definedChanged = Signal()
    currentIndexChanged = Signal()
    dataBlocksChanged = Signal(int)
    dataBlocksMeasOnlyChanged = Signal(int)
    dataBlocksCifChanged = Signal()
    dataBlocksCifNoMeasChanged = Signal()
    dataBlocksCifMeasOnlyChanged = Signal()
    yMeasArraysChanged = Signal()
    yBkgArraysChanged = Signal()
    chartRangesChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._defined = False
        self._currentIndex = 0
        self._dataBlocks = []
        self._dataBlocksMeasOnly = []
        self._dataBlocksCif = []
        self._dataBlocksCifNoMeas = []
        self._dataBlocksCifMeasOnly = []
        self._xArrays = []
        self._yMeasArrays = []
        self._yBkgArrays = []
        self._chartRanges = []

    # QML accessible properties

    @Property('QVariant', notify=chartRangesChanged)
    def chartRanges(self):
        return self._chartRanges

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

    @Property('QVariant', notify=dataBlocksMeasOnlyChanged)
    def dataBlocksMeasOnly(self):
        #console.error('dataBlocks (measured data only) getter')
        return self._dataBlocksMeasOnly

    @Property('QVariant', notify=dataBlocksChanged)
    def dataBlocks(self):
        #console.error('dataBlocks getter')
        return self._dataBlocks

    @Property('QVariant', notify=dataBlocksCifChanged)
    def dataBlocksCif(self):
        return self._dataBlocksCif

    @Property('QVariant', notify=dataBlocksCifNoMeasChanged)
    def dataBlocksCifNoMeas(self):
        return self._dataBlocksCifNoMeas

    @Property('QVariant', notify=dataBlocksCifMeasOnlyChanged)
    def dataBlocksCifMeasOnly(self):
        return self._dataBlocksCifMeasOnly

    # QML accessible methods

    @Slot()
    def addDefaultExperiment(self):
        console.debug('Adding default experiment')
        self.loadExperimentFromCif(_DEFAULT_DATA_BLOCK)

    @Slot(str)
    def loadExperimentFromFile(self, fpath):
        fpath = IO.generalizePath(fpath)
        console.debug(f"Loading experiment from: {fpath}")
        with open(fpath, 'r') as file:
            edCif = file.read()
        self.loadExperimentFromCif(edCif)

    @Slot(str)
    def loadExperimentFromCif(self, edCif):
        cryspyCif = Converter.edCifToCryspyCif(edCif)
        cryspyExperimentObj = str_to_globaln(cryspyCif)
        cryspyExperimentDict = cryspyExperimentObj.get_dictionary()
        self._proxy.data._cryspyDict.update(cryspyExperimentDict)
        self.parseExperiments(cryspyExperimentObj)

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

    @Slot(str, str, float)
    def setMainParam(self, paramName, field, value):
        if field == 'fit':
            value = bool(value)

        changedIntern = self.editDataBlockMainParam(paramName, field, value)
        changedCryspy = self.editCryspyDictByMainParam(paramName, field, value)

        if changedIntern and changedCryspy:
            self.dataBlocksChanged.emit(None)  # NED FIX

    @Slot(str, str, int, str, float)
    def setLoopParam(self, loopName, paramName, rowIndex, field, value):
        if field == 'fit':
            value = bool(value)

        changedIntern = self.editDataBlockLoopParam(loopName, paramName, rowIndex, field, value)
        changedCryspy = self.editCryspyDictByLoopParam(loopName, paramName, rowIndex, field, value)

        if changedIntern and changedCryspy:
            self.dataBlocksChanged.emit(None)  # NED FIX

    # Private methods

    def editDataBlockMainParam(self, paramName, field, value, blockIndex=None):
        block = 'experiment'
        if blockIndex is None:
            blockIndex = self._currentIndex

        if field == 'fit':
            value = bool(value)

        oldValue = self._dataBlocks[blockIndex]['params'][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocks[blockIndex]['params'][paramName][field] = value

        console.debug(f"Intern dict ▌ {oldValue} → {value} ▌ {block}[{blockIndex}].{paramName}.{field}")
        return True

    def editDataBlockLoopParam(self, loopName, paramName, rowIndex, field, value, blockIndex=None):
        block = 'experiment'
        if blockIndex is None:
            blockIndex = self._currentIndex

        if field == 'fit':
            value = bool(value)

        oldValue = self._dataBlocks[blockIndex]['loops'][loopName][rowIndex][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocks[blockIndex]['loops'][loopName][rowIndex][paramName][field] = value

        console.debug(f"Intern dict ▌ {oldValue} → {value} ▌ {block}[{blockIndex}].{loopName}[{rowIndex}].{paramName}.{field}")
        return True

    def editCryspyDictByMainParam(self, paramName, field, value):
        path, value = self.cryspyDictPathByMainParam(paramName, field, value)

        oldValue = self._proxy.data._cryspyDict[path[0]][path[1]][path[2]]
        if oldValue == value:
            return False
        self._proxy.data._cryspyDict[path[0]][path[1]][path[2]] = value

        console.debug(f"Cryspy dict ▌ {oldValue} → {value} ▌ {path}")
        return True

    def editCryspyDictByLoopParam(self, loopName, paramName, rowIndex, field, value):
        path, value = self.cryspyDictPathByLoopParam(loopName, paramName, rowIndex, field, value)

        oldValue = self._proxy.data._cryspyDict[path[0]][path[1]][path[2]]
        if oldValue == value:
            return False
        self._proxy.data._cryspyDict[path[0]][path[1]][path[2]] = value

        console.debug(f"Cryspy dict ▌ {oldValue} → {value} ▌ {path}")
        return True

    def cryspyDictPathByMainParam(self, paramName, field, value):
        blockIndex = self._currentIndex
        blockName = self._dataBlocks[blockIndex]['name']
        path = ['','','']
        path[0] = f"pd_{blockName}"

        # _diffrn_radiation
        if paramName == '_diffrn_radiation_wavelength':
            path[1] = 'wavelength'
            path[2] = 0

        # _pd_meas_2theta_offset
        elif paramName == '_pd_meas_2theta_offset':
            path[1] = 'offset_ttheta'
            path[2] = 0
            value = np.deg2rad(value)

        # _pd_instr_resolution
        elif paramName == '_pd_instr_resolution_u':
            path[1] = 'resolution_parameters'
            path[2] = 0
        elif paramName == '_pd_instr_resolution_v':
            path[1] = 'resolution_parameters'
            path[2] = 1
        elif paramName == '_pd_instr_resolution_w':
            path[1] = 'resolution_parameters'
            path[2] = 2
        elif paramName == '_pd_instr_resolution_x':
            path[1] = 'resolution_parameters'
            path[2] = 3
        elif paramName == '_pd_instr_resolution_y':
            path[1] = 'resolution_parameters'
            path[2] = 4
        elif paramName == '_pd_instr_resolution_z':
            path[1] = 'resolution_parameters'
            path[2] = 5

        # _pd_instr_reflex_asymmetry
        elif paramName == '_pd_instr_reflex_asymmetry_p1':
            path[1] = 'asymmetry_parameters'
            path[2] = 0
        elif paramName == '_pd_instr_reflex_asymmetry_p2':
            path[1] = 'asymmetry_parameters'
            path[2] = 1
        elif paramName == '_pd_instr_reflex_asymmetry_p3':
            path[1] = 'asymmetry_parameters'
            path[2] = 2
        elif paramName == '_pd_instr_reflex_asymmetry_p4':
            path[1] = 'asymmetry_parameters'
            path[2] = 3

        # undefined
        else:
            console.error(f"Undefined parameter name '{paramName}'")

        # if 'flags' objects are needed
        if field == 'fit':
            path[1] = f'flags_{path[1]}'

        return path, value

    def cryspyDictPathByLoopParam(self, loopName, paramName, rowIndex, field, value):
        blockIndex = self._currentIndex
        blockName = self._dataBlocks[blockIndex]['name']
        path = ['','','']
        path[0] = f"pd_{blockName}"

        # _pd_background
        if loopName == '_pd_background':
            if paramName == '_2theta':
                path[1] = 'background_ttheta'
                path[2] = rowIndex
                value = np.deg2rad(value)
            if paramName == '_intensity':
                path[1] = 'background_intensity'
                path[2] = rowIndex

        # _phase
        if loopName == '_phase':
            if paramName == '_scale':
                path[1] = 'phase_scale'
                path[2] = rowIndex

        # if 'flags' objects are needed
        if field == 'fit':
            path[1] = f'flags_{path[1]}'

        return path, value

    def editDataBlockByCryspyDictParams(self, params):
        for param in params:
            block, group, idx = Data.strToCryspyDictParamPath(param)

            # pd (powder diffraction) block
            if block.startswith('pd_'):
                blockName = block[3:]
                loopName = None
                paramName = None
                rowIndex = None
                value = self._proxy.data._cryspyDict[block][group][idx]

                # wavelength
                if group == 'wavelength':
                    paramName = '_diffrn_radiation_wavelength'

                # offset_ttheta
                elif group == 'offset_ttheta':
                    paramName = '_pd_meas_2theta_offset'
                    value = np.rad2deg(value)

                # resolution_parameters
                elif group == 'resolution_parameters':
                    if idx[0] == 0:
                        paramName = '_pd_instr_resolution_u'
                    elif idx[0] == 1:
                        paramName = '_pd_instr_resolution_v'
                    elif idx[0] == 2:
                        paramName = '_pd_instr_resolution_w'
                    elif idx[0] == 3:
                        paramName = '_pd_instr_resolution_x'
                    elif idx[0] == 4:
                        paramName = '_pd_instr_resolution_y'
                    elif idx[0] == 5:
                        paramName = '_pd_instr_resolution_z'

                # asymmetry_parameters
                elif group == 'asymmetry_parameters':
                    if idx[0] == 0:
                        paramName = '_pd_instr_reflex_asymmetry_p1'
                    elif idx[0] == 1:
                        paramName = '_pd_instr_reflex_asymmetry_p2'
                    elif idx[0] == 2:
                        paramName = '_pd_instr_reflex_asymmetry_p3'
                    elif idx[0] == 3:
                        paramName = '_pd_instr_reflex_asymmetry_p4'

                # background_ttheta
                elif group == 'background_ttheta':
                    loopName = '_pd_background'
                    paramName = '_2theta'
                    rowIndex = idx[0]
                    value = np.rad2deg(value)

                # background_intensity
                elif group == 'background_intensity':
                    loopName = '_pd_background'
                    paramName = '_intensity'
                    rowIndex = idx[0]

                # phase_scale
                elif group == 'phase_scale':
                    loopName = '_phase'
                    paramName = '_scale'
                    rowIndex = idx[0]

                value = float(value)  # convert float64 to float (needed for QML access)
                blockIndex = [block['name'] for block in self._dataBlocks].index(blockName)

                if loopName is None:
                    self.editDataBlockMainParam(paramName, 'value', value, blockIndex)
                else:
                    self.editDataBlockLoopParam(loopName, paramName, rowIndex, 'value', value, blockIndex)

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

    def calculatedYBkgArray(self, index):
        #console.error('Interpolation')
        dataBlock = self._dataBlocks[index]
        xArray = self._xArrays[index]
        yBkgArrayInterp = np.zeros_like(xArray)

        if '_pd_background' in dataBlock['loops'].keys():
            bkg = dataBlock['loops']['_pd_background']
            xBkgArray = [point['_2theta']['value'] for point in bkg]
            yBkgArray = [point['_intensity']['value'] for point in bkg]
            yBkgArrayInterp = np.interp(xArray, xBkgArray, yBkgArray)

        console.debug(f" - Interpolation of background for experiment data block no. {index + 1} has been done")
        return yBkgArrayInterp

    def updateCurrentExperimentYBkgArray(self):
        index = self._currentIndex
        self._yBkgArrays[index] = self.calculatedYBkgArray(index)
        console.debug(f" - Background for experiment data block no. {index + 1} has been calculated and saved to intern dataset")
        self.yBkgArraysChanged.emit()

    def addDataBlock(self, dataBlock):
        blockIdx = -1
        for i, block in enumerate(self._dataBlocks):
            if dataBlock['name'] == block['name']:
                blockIdx = i
                break
        if blockIdx == -1:
            self._dataBlocks.append(dataBlock)
            console.debug(f"Experiment data block no. {len(self._dataBlocks)} (without measured data) has been added to intern dataset")
        else:
            self._dataBlocks[blockIdx] = dataBlock
            console.debug(f"Experiment data block no. {blockIdx + 1} (without measured data) in intern dataset has been replaced")
        self.dataBlocksChanged.emit(blockIdx)

    def addDataBlockMeasOnly(self, dataBlock):
        blockIdx = -1
        for i, block in enumerate(self._dataBlocksMeasOnly):
            if dataBlock['name'] == block['name']:
                blockIdx = i
                break
        if blockIdx == -1:
            self._dataBlocksMeasOnly.append(dataBlock)
            console.debug(f"Experiment data block no. {len(self._dataBlocksMeasOnly)} (measured data only) has been added to intern dataset")
        else:
            self._dataBlocksMeasOnly[blockIdx] = dataBlock
            console.debug(f"Experiment data block no. {blockIdx + 1} (measured data only) in intern dataset has been replaced")
        self.dataBlocksMeasOnlyChanged.emit(blockIdx)

    def addXYArraysAndChartRanges(self, blockIdx):
        idx = blockIdx
        if idx == -1:
            idx = len(self._dataBlocksMeasOnly) - 1
        data = self._dataBlocksMeasOnly[idx]['loops']['_pd_meas']

        # X data
        x_array = [point['_2theta']['value'] for point in data]
        x_array = np.array(x_array)
        self.addXArray(x_array, blockIdx)

        # Measured Y data
        y_meas_array = [point['_intensity']['value'] for point in data]
        y_meas_array = np.array(y_meas_array)
        self.addYMeasArray(y_meas_array, blockIdx)

        # Standard deviation of the measured Y data
        #sy_meas_array = [point['_intensity_sigma']['value'] for point in data]
        #sy_meas_array = np.array(sy_meas_array)
        #self.addSYMeasArray(sy_meas_array)

        # Background Y data # NED FIX: use calculatedYBkgArray()
        y_bkg_array_interp = np.zeros_like(x_array)
        #if '_pd_background' in ed_experiment['loops'].keys():
        #    bkg = ed_experiment['loops']['_pd_background']
        #    x_bkg_array = [point['_2theta']['value'] for point in bkg]
        #    y_bkg_array = [point['_intensity']['value'] for point in bkg]
        #    y_bkg_array_interp = np.interp(x_array, x_bkg_array, y_bkg_array)
        self.addYBkgArray(y_bkg_array_interp, blockIdx)

        # Ranges (for charts)
        x_min = dict(Parameter(float(x_array.min())))
        x_max = dict(Parameter(float(x_array.max())))
        y_min = float(y_meas_array.min())
        y_max = float(y_meas_array.max())
        y_range = y_max - y_min
        y_extra = y_range * 0.1
        y_min = dict(Parameter(y_min - y_extra))
        y_max = dict(Parameter(y_max + y_extra))
        ranges = {'xMin':x_min, 'xMax':x_max, 'yMin':y_min, 'yMax':y_max}
        self.addChartRanges(ranges, blockIdx)

    def addXArray(self, xArray, blockIdx):
        if blockIdx == -1:
            self._xArrays.append(xArray)
            console.debug(f" - X data for experiment data block no. {len(self._dataBlocks) + 1} has been added to intern dataset")
        else:
            self._xArrays[blockIdx] = xArray
            console.debug(f" - X data for experiment data block no. {blockIdx + 1} in intern dataset has been replaced")

    def addYMeasArray(self, yMeasArray, blockIdx):
        if blockIdx == -1:
            self._yMeasArrays.append(yMeasArray)
            console.debug(f" - Y-measured data for experiment data block no. {len(self._dataBlocks) + 1} has been added to intern dataset")
        else:
            self._yMeasArrays[blockIdx] = yMeasArray
            console.debug(f" - Y-measured data for experiment data block no. {blockIdx + 1} in intern dataset has been replaced")
        self.yMeasArraysChanged.emit()

    def addYBkgArray(self, yBkgArray, blockIdx):
        if blockIdx == -1:
            self._yBkgArrays.append(yBkgArray)
            console.debug(f" - Y-background data for experiment data block no. {len(self._dataBlocks) + 1} has been added to intern dataset")
        else:
            self._yBkgArrays[blockIdx] = yBkgArray
            console.debug(f" - Y-background data for experiment data block no. {blockIdx + 1} in intern dataset has been replaced")
        self.yBkgArraysChanged.emit()

    def addChartRanges(self, ranges, blockIdx):
        if blockIdx == -1:
            self.chartRanges.append(ranges)
            console.debug(f" - Chart ranges for experiment data block no. {len(self._dataBlocks) + 1} has been added to intern dataset")
        else:
            self.chartRanges[blockIdx] = ranges
            console.debug(f" - Chart ranges for experiment data block no. {blockIdx + 1} in intern dataset has been replaced")
        self.chartRangesChanged.emit()

    def setDataBlocksCifNoMeas(self):
        self._dataBlocksCifNoMeas = Converter.dataBlocksToCif(self._dataBlocks)
        console.debug(" - Experiment data blocks (without measured data) have been converted to CIF string")
        self.dataBlocksCifNoMeasChanged.emit()

    def setDataBlocksCifMeasOnly(self):
        self._dataBlocksCifMeasOnly = Converter.dataBlockLoopsToCif(self._dataBlocksMeasOnly)
        console.debug(" - Experiment data blocks (measured data only) have been converted to CIF string")
        self.dataBlocksCifMeasOnlyChanged.emit()

    def setDataBlocksCif(self):
        self.setDataBlocksCifNoMeas()
        self.setDataBlocksCifMeasOnly()
        cifMeasOnlyReduced =  self._dataBlocksCifMeasOnly.split('\n')[:10] + ['...'] + self._dataBlocksCifMeasOnly.split('\n')[-6:]
        cifMeasOnlyReduced = '\n'.join(cifMeasOnlyReduced)
        cifMeasOnlyReduced = cifMeasOnlyReduced.rstrip()
        self._dataBlocksCif = [self._dataBlocksCifNoMeas] + [cifMeasOnlyReduced]
        console.debug(" - Experiment data blocks (including short measured data) have been converted to CIF string")
        self.dataBlocksCifChanged.emit()

    # Extract experiments from cryspy_obj and cryspy_dict into internal ed_dict
    def parseExperiments(self, cryspy_obj):
        ed_dict = self._proxy.data.edDict  # ???
        cryspy_dict = self._proxy.data._cryspyDict
        experiment_names = [name.replace('pd_', '') for name in cryspy_dict.keys() if name.startswith('pd_')]

        for data_block in cryspy_obj.items:
            data_block_name = data_block.data_name

            # Experiment datablock
            if data_block_name in experiment_names:
                ed_dict['experiments'] = []  # ???
                ed_experiment = {'name': data_block_name,
                                 'params': {},
                                 'loops': {}}
                ed_experiment_meas_only = {'name': data_block_name,
                                           'loops': {}}
                cryspy_experiment = data_block.items

                #x_array = self.defaultXArray()  # NEED FIX
                #y_meas_array = self.defaultYMeasArray()  # NEED FIX
                #y_bkg_array = self.defaultYBkgArray()  # NEED FIX

                for item in cryspy_experiment:
                    # Ranges section
                    if type(item) == cryspy.C_item_loop_classes.cl_1_range.Range:
                        ed_experiment['params']['_pd_meas_2theta_range_min'] = dict(Parameter(
                            item.ttheta_min,
                            name = '_pd_meas_2theta_range_min',
                            prettyName = 'range min',
                            url = 'https://easydiffraction.org',
                            cifDict = 'pd'
                        ))
                        ed_experiment['params']['_pd_meas_2theta_range_max'] = dict(Parameter(
                            item.ttheta_max,
                            name = '_pd_meas_2theta_range_max',
                            prettyName = 'range max',
                            url = 'https://easydiffraction.org',
                            cifDict = 'pd'
                        ))
                        ed_experiment['params']['_pd_meas_2theta_range_inc'] = dict(Parameter(
                            0.05, # NEED FIX
                            name = '_pd_meas_2theta_range_inc',
                            prettyName = 'range inc',
                            url = 'https://easydiffraction.org',
                            cifDict = 'pd'
                        ))

                    # Setup section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_setup.Setup:
                        ed_experiment['params']['_diffrn_radiation_probe'] = dict(Parameter(
                            item.radiation.replace('neutrons', 'neutron').replace('X-rays', 'x-ray'),
                            name = '_diffrn_radiation_probe',
                            prettyName = 'probe',
                            url = 'https://easydiffraction.org'
                        ))
                        ed_experiment['params']['_diffrn_radiation_wavelength'] = dict(Parameter(
                            item.wavelength,
                            name = '_diffrn_radiation_wavelength',
                            prettyName = 'wavelength',
                            url = 'https://easydiffraction.org',
                            min = 0.5,
                            max = 2.5,
                            units = 'Å',
                            fittable = True,
                            fit = item.wavelength_refinement
                        ))
                        ed_experiment['params']['_pd_meas_2theta_offset'] = dict(Parameter(
                            item.offset_ttheta,
                            name = '_pd_meas_2theta_offset',
                            prettyName = 'offset',
                            url = 'https://easydiffraction.org',
                            min = -0.5,
                            max = 0.5,
                            units = '°',
                            fittable = True,
                            fit = item.offset_ttheta_refinement
                        ))

                    # Instrument resolution section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_resolution.PdInstrResolution:
                        ed_experiment['params']['_pd_instr_resolution_u'] = dict(Parameter(
                            item.u,
                            name = '_pd_instr_resolution_u',
                            prettyName = 'u',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.u_refinement
                        ))
                        ed_experiment['params']['_pd_instr_resolution_v'] = dict(Parameter(
                            item.v,
                            name = '_pd_instr_resolution_v',
                            prettyName = 'v',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.v_refinement
                        ))
                        ed_experiment['params']['_pd_instr_resolution_w'] = dict(Parameter(
                            item.w,
                            name = '_pd_instr_resolution_w',
                            prettyName = 'w',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.w_refinement
                        ))
                        ed_experiment['params']['_pd_instr_resolution_x'] = dict(Parameter(
                            item.x,
                            name = '_pd_instr_resolution_x',
                            prettyName = 'x',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.x_refinement
                        ))
                        ed_experiment['params']['_pd_instr_resolution_y'] = dict(Parameter(
                            item.y,
                            name = '_pd_instr_resolution_y',
                            prettyName = 'y',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.y_refinement
                        ))

                    # Peak assymetries section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_reflex_asymmetry.PdInstrReflexAsymmetry:
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p1'] = dict(Parameter(
                            item.p1,
                            name = '_pd_instr_reflex_asymmetry_p1',
                            prettyName = 'p1',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.p1_refinement
                        ))
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p2'] = dict(Parameter(
                            item.p2,
                            name = '_pd_instr_reflex_asymmetry_p2',
                            prettyName = 'p2',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.p2_refinement
                        ))
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p3'] = dict(Parameter(
                            item.p3,
                            name = '_pd_instr_reflex_asymmetry_p3',
                            prettyName = 'p3',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.p3_refinement
                        ))
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p4'] = dict(Parameter(
                            item.p4,
                            name = '_pd_instr_reflex_asymmetry_p4',
                            prettyName = 'p4',
                            url = 'https://easydiffraction.org',
                            fittable = True,
                            fit = item.p4_refinement))

                    # Phases section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_phase.PhaseL:
                        ed_phases = []
                        cryspy_phases = item.items

                        for idx, cryspy_phase in enumerate(cryspy_phases):
                            ed_phase = {}
                            ed_phase['_label'] = dict(Parameter(
                                cryspy_phase.label,
                                idx = idx,
                                loopName = '_phase',
                                name = '_label',
                                prettyName = 'label',
                                url = 'https://easydiffraction.org',
                            ))
                            ed_phase['_scale'] = dict(Parameter(
                                cryspy_phase.scale,
                                idx = idx,
                                loopName = '_phase',
                                rowName = cryspy_phase.label,
                                name = '_scale',
                                prettyName = 'scale',
                                url = 'https://easydiffraction.org',
                                min = 0.1,
                                max = 10,
                                fittable = True,
                                fit = cryspy_phase.scale_refinement
                            ))
                            ed_phases.append(ed_phase)

                        ed_experiment['loops']['_phase'] = ed_phases

                    # Background section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_background.PdBackgroundL:
                        ed_bkg_points = []
                        cryspy_bkg_points = item.items

                        for idx, cryspy_bkg_point in enumerate(cryspy_bkg_points):
                            ed_bkg_point = {}
                            ed_bkg_point['_2theta'] = dict(Parameter(
                                cryspy_bkg_point.ttheta,
                                idx = idx,
                                loopName = '_pd_background',
                                name = '_2theta',
                                prettyName = '2θ',
                                url = 'https://easydiffraction.org'
                            ))
                            ed_bkg_point['_intensity'] = dict(Parameter(
                                cryspy_bkg_point.intensity,
                                idx = idx,
                                loopName = '_pd_background',
                                rowName = f'{cryspy_bkg_point.ttheta:g}_deg',  # formatting float to str without trailing zeros
                                name = '_intensity',
                                prettyName = 'intensity',
                                url = 'https://easydiffraction.org',
                                min = 0,
                                max = 3000,
                                fittable = True,
                                fit = cryspy_bkg_point.intensity_refinement
                            ))
                            ed_bkg_points.append(ed_bkg_point)

                        ed_experiment['loops']['_pd_background'] = ed_bkg_points

                    # Measured data section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_meas.PdMeasL:
                        ed_meas_points = []
                        cryspy_meas_points = item.items



                        for idx, cryspy_meas_point in enumerate(cryspy_meas_points):
                            ed_meas_point = {}
                            ed_meas_point['_2theta'] = dict(Parameter(
                                cryspy_meas_point.ttheta,
                                idx = idx,
                                loopName = '_pd_meas',
                                name = '_2theta',
                                prettyName = '2θ',
                                url = 'https://easydiffraction.org'
                            ))
                            ed_meas_point['_intensity'] = dict(Parameter(
                                cryspy_meas_point.intensity,
                                idx = idx,
                                loopName = '_pd_meas',
                                name = '_intensity',
                                prettyName = 'I',
                                url = 'https://easydiffraction.org'
                            ))
                            ed_meas_point['_intensity_sigma'] = dict(Parameter(
                                cryspy_meas_point.intensity_sigma,
                                idx = idx,
                                loopName = '_pd_meas',
                                name = '_intensity_sigma',
                                prettyName = 'sI',
                                url = 'https://easydiffraction.org'
                            ))
                            ed_meas_points.append(ed_meas_point)

                        ed_experiment_meas_only['loops']['_pd_meas'] = ed_meas_points



#                        x_array = [point.ttheta for point in cryspy_meas_points]
#                        y_meas_array = [point.intensity for point in cryspy_meas_points]
#                        #sy_meas_array = [point.intensity_sigma for point in cryspy_meas_points]
#                        x_array = np.array(x_array)
#                        y_meas_array = np.array(y_meas_array)
#
#                        # Background  # NED FIX: use calculatedYBkgArray()
#                        y_bkg_array_interp = np.zeros_like(x_array)
#                        if '_pd_background' in ed_experiment['loops'].keys():
#                            bkg = ed_experiment['loops']['_pd_background']
#                            x_bkg_array = [point['_2theta']['value'] for point in bkg]
#                            y_bkg_array = [point['_intensity']['value'] for point in bkg]
#                            y_bkg_array_interp = np.interp(x_array, x_bkg_array, y_bkg_array)

#                        # Ranges (for charts)
#                        x_min = dict(Parameter(float(x_array.min())))
#                        x_max = dict(Parameter(float(x_array.max())))
#                        y_min = float(y_meas_array.min())
#                        y_max = float(y_meas_array.max())
#                        y_range = y_max - y_min
#                        y_extra = y_range * 0.1
#                        y_min = dict(Parameter(y_min - y_extra))
#                        y_max = dict(Parameter(y_max + y_extra))
#                        self.chartRanges.append({'xMin': x_min,
#                                                 'xMax': x_max,
#                                                 'yMin': y_min,
#                                                 'yMax': y_max})
#                        self.chartRangesChanged.emit()

                ed_dict['experiments'].append(ed_experiment)  # ???


#                self.addXArray(x_array)
#                self.addYMeasArray(y_meas_array)
#                self.addYBkgArray(y_bkg_array_interp)

                self.addDataBlockMeasOnly(ed_experiment_meas_only)  # NEED FIX: need to be called before self.addDataBlock(ed_experiment)
                self.addDataBlock(ed_experiment) # NEED FIX: need to be called after self.addDataBlockMeasOnly(ed_experiment_meas_only)

#
#                # Calculate data based on...
#                y_calc_array = self._proxy.model.calculateDiffractionPattern()
#                self._proxy.model.addYCalcArray(y_calc_array)
