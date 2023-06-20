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
from Logic.Helpers import Converter
from Logic.Data import Data

try:
    import cryspy
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')

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
    chartRangesChanged = Signal()
    parameterEdited = Signal(str, str)

    paramChanged = Signal()

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
    def loadExperimentFromFile_OLD(self, fpath):
        fpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', fpath))
        console.debug(f"Loading an experiment from {fpath}")
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

    @Slot(str)
    def loadExperimentFromFile(self, fpath):
        fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'examples', 'Co2SiO4_experiment.cif')
        console.debug(f"Loading an experiment from {fpath}")
        # Load RCIF file by cryspy and extract experiments into easydiffraction data block
        cryspyExperimentObj = cryspy.load_file(fpath)
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





    @Slot(str, float)
    def setMainParameterValue(self, paramName, value):
        self.editDataBlockMainParam(paramName, value)
        self.editCryspyDictByMainParam(paramName, value)

        self.paramChanged.emit()

    @Slot(str, str, int, float)
    def setLoopParameterValue(self, loopName, paramName, parameterIndex, value):
        self.editDataBlockLoopParameter(loopName, paramName, parameterIndex, value)
        self.editCryspyDictByLoopParam(loopName, paramName, parameterIndex, value)

        self.paramChanged.emit()

    def editDataBlockMainParam(self, paramName, value, blockIndex=None):
        block = 'experiment'
        if blockIndex is None:
            blockIndex = self._currentIndex

        oldValue = self._dataBlocks[blockIndex]['params'][paramName]['value']
        if oldValue == value:
            return
        self._dataBlocks[blockIndex]['params'][paramName]['value'] = value

        console.debug(f"Parameter '{block}[{blockIndex}].{paramName}.value' has been changed: '{oldValue}' -> '{value}'")

    def editDataBlockLoopParameter(self, loopName, paramName, parameterIndex, value, blockIndex=None):
        block = 'experiment'
        if blockIndex is None:
            blockIndex = self._currentIndex

        oldValue = self._dataBlocks[blockIndex]['loops'][loopName][parameterIndex][paramName]['value']
        if oldValue == value:
            return
        self._dataBlocks[blockIndex]['loops'][loopName][parameterIndex][paramName]['value'] = value

        console.debug(f"Parameter {block}[{blockIndex}].loops['{loopName}'][{parameterIndex}]['{paramName}']['value'] changed: '{oldValue}' -> '{value}'")

    def editCryspyDictByMainParam(self, paramName, value):
        path, value = self.cryspyDictPathByMainParam(paramName, value)

        oldValue = self._proxy.data._cryspyDict[path[0]][path[1]][path[2]]
        if oldValue == value:
            return
        self._proxy.data._cryspyDict[path[0]][path[1]][path[2]] = value

        console.debug(f"Cryspy dict parameter {path} changed: '{oldValue}' -> '{value}'")

    def editCryspyDictByLoopParam(self, loopName, paramName, parameterIndex, value):
        path, value = self.cryspyDictPathByLoopParam(loopName, paramName, parameterIndex, value)

        oldValue = self._proxy.data._cryspyDict[path[0]][path[1]][path[2]]
        if oldValue == value:
            return
        self._proxy.data._cryspyDict[path[0]][path[1]][path[2]] = value

        console.debug(f"Cryspy dict parameter {path} changed: '{oldValue}' -> '{value}'")

    def cryspyDictPathByMainParam(self, paramName, value):
        blockIndex = self._currentIndex
        blockName = self._dataBlocks[blockIndex]['name']
        path = ['','','']
        path[0] = f"pd_{blockName}"

        # _diffrn_radiation
        if paramName == '_diffrn_radiation_wavelength':
            path[1] = 'wavelength'
            path[2] = 0

        # _pd_meas_2theta_offset
        if paramName == '_pd_meas_2theta_offset':
            path[1] = 'offset_ttheta'
            path[2] = 0

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
        elif paramName == '_pd_instr_reflex_asymmetry_p1':
            path[1] = 'asymmetry_parameters'
            path[2] = 1
        elif paramName == '_pd_instr_reflex_asymmetry_p1':
            path[1] = 'asymmetry_parameters'
            path[2] = 2
        elif paramName == '_pd_instr_reflex_asymmetry_p1':
            path[1] = 'asymmetry_parameters'
            path[2] = 3

        # undefined
        else:
            console.error(f"Undefined parameter name '{paramName}'")

        return path, value

    def cryspyDictPathByLoopParam(self, loopName, paramName, parameterIndex, value):
        blockIndex = self._currentIndex
        blockName = self._dataBlocks[blockIndex]['name']
        path = ['','','']
        path[0] = f"pd_{blockName}"

        # _pd_background
        if loopName == '_pd_background':
            if paramName == '_2theta':
                path[1] = 'background_ttheta'
                path[2] = parameterIndex
                value = np.deg2rad(value)
            if paramName == '_intensity':
                path[1] = 'background_intensity'
                path[2] = parameterIndex

        # _phase
        if loopName == '_phase':
            if paramName == '_scale':
                path[1] = 'phase_scale'
                path[2] = parameterIndex

        return path, value

    def editDataBlockByCryspyDictParams(self, params):
        for param in params:
            block, group, idx = Data.strToCryspyDictParamPath(param)

            # pd (powder diffraction) block
            if block.startswith('pd_'):
                blockType = 'experiment'
                blockName = block[3:]

                blockName = None
                loopName = None
                paramName = None
                parameterIndex = None
                value = self._proxy.data._cryspyDict[block][group][idx]

                # wavelength
                if group == 'wavelength':
                    paramName = '_diffrn_radiation_wavelength'

                # offset_ttheta
                elif group == 'offset_ttheta':
                    paramName = '_pd_meas_2theta_offset'

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
                    parameterIndex = idx[0]
                    value = np.rad2deg(value)

                # background_intensity
                elif group == 'background_intensity':
                    loopName = '_pd_background'
                    paramName = '_intensity'
                    parameterIndex = idx[0]

                # phase_scale
                elif group == 'phase_scale':
                    loopName = '_phase'
                    paramName = '_scale'
                    parameterIndex = idx[0]

                value = float(value)  # convert float64 to float (needed for QML access)
                blockIndex = [block['name'] for block in self._dataBlocks].index(blockName)

                ##
                if loopName is None:
                    self.editDataBlockMainParam(paramName, value, blockIndex)
                else:
                    self.editDataBlockLoopParameter(loopName, paramName, parameterIndex, value, blockIndex)







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

    # Extract experiments from cryspy_obj and cryspy_dict into internal ed_dict
    def parseExperiments(self, cryspy_obj):
        ed_dict = self._proxy.data.edDict
        cryspy_dict = self._proxy.data._cryspyDict
        experiment_names = [name.replace('pd_', '') for name in cryspy_dict.keys() if name.startswith('pd_')]
        for data_block in cryspy_obj.items:
            data_block_name = data_block.data_name
            # Experiment datablock
            if data_block_name in experiment_names:
                ed_dict['experiments'] = []
                ed_experiment = {'name': data_block_name,
                                 'params': {},
                                 'loops': {}}
                cryspy_experiment = data_block.items
                x_array = self.defaultXArray()  # NEED FIX
                y_meas_array = self.defaultYMeasArray()  # NEED FIX
                y_bkg_array = self.defaultYBkgArray()  # NEED FIX
                for item in cryspy_experiment:
                    # Ranges section
                    if type(item) == cryspy.C_item_loop_classes.cl_1_range.Range:
                        ed_experiment['params']['_pd_meas_2theta_range_min'] = dict(Parameter(item.ttheta_min))
                        ed_experiment['params']['_pd_meas_2theta_range_max'] = dict(Parameter(item.ttheta_max))
                        ed_experiment['params']['_pd_meas_2theta_range_inc'] = dict(Parameter(0.05))  # NEED FIX
                    # Setup section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_setup.Setup:
                        ed_experiment['params']['_diffrn_radiation_probe'] = dict(Parameter(item.radiation.replace('neutrons', 'neutron').replace('X-rays', 'x-ray')))
                        ed_experiment['params']['_diffrn_radiation_wavelength'] = dict(Parameter(item.wavelength, fittable=True, fit=item.wavelength_refinement))
                        ed_experiment['params']['_pd_meas_2theta_offset'] = dict(Parameter(item.offset_ttheta, fittable=True, fit=item.offset_ttheta_refinement))
                    # Instrument resolution section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_resolution.PdInstrResolution:
                        ed_experiment['params']['_pd_instr_resolution_u'] = dict(Parameter(item.u, fittable=True, fit=item.u_refinement))
                        ed_experiment['params']['_pd_instr_resolution_v'] = dict(Parameter(item.v, fittable=True, fit=item.v_refinement))
                        ed_experiment['params']['_pd_instr_resolution_w'] = dict(Parameter(item.w, fittable=True, fit=item.w_refinement))
                        ed_experiment['params']['_pd_instr_resolution_x'] = dict(Parameter(item.x, fittable=True, fit=item.x_refinement))
                        ed_experiment['params']['_pd_instr_resolution_y'] = dict(Parameter(item.y, fittable=True, fit=item.y_refinement))
                    # Peak assymetries section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_reflex_asymmetry.PdInstrReflexAsymmetry:
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p1'] = dict(Parameter(item.p1, fittable=True, fit=item.p1_refinement))
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p2'] = dict(Parameter(item.p2, fittable=True, fit=item.p2_refinement))
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p3'] = dict(Parameter(item.p3, fittable=True, fit=item.p3_refinement))
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p4'] = dict(Parameter(item.p4, fittable=True, fit=item.p4_refinement))
                    # Phases section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_phase.PhaseL:
                        ed_phases = []
                        cryspy_phases = item.items
                        for cryspy_phase in cryspy_phases:
                            ed_phase = {}
                            ed_phase['_label'] = dict(Parameter(cryspy_phase.label))
                            ed_phase['_scale'] = dict(Parameter(cryspy_phase.scale, fittable=True, fit=cryspy_phase.scale_refinement))
                            ed_phases.append(ed_phase)
                        ed_experiment['loops']['_phase'] = ed_phases
                    # Background section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_background.PdBackgroundL:
                        ed_bkg_points = []
                        cryspy_bkg_points = item.items
                        for cryspy_bkg_point in cryspy_bkg_points:
                            ed_bkg_point = {}
                            ed_bkg_point['_2theta'] = dict(Parameter(cryspy_bkg_point.ttheta))
                            ed_bkg_point['_intensity'] = dict(Parameter(cryspy_bkg_point.intensity, fittable=True, fit=cryspy_bkg_point.intensity_refinement))
                            ed_bkg_points.append(ed_bkg_point)
                        ed_experiment['loops']['_pd_background'] = ed_bkg_points
                    # Measured data section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_meas.PdMeasL:
                        cryspy_meas_points = item.items
                        x_array = [point.ttheta for point in cryspy_meas_points]
                        y_meas_array = [point.intensity for point in cryspy_meas_points]
                        #sy_meas_array = [point.intensity_sigma for point in cryspy_meas_points]
                        x_array = np.array(x_array)
                        y_meas_array = np.array(y_meas_array)
                        # Background
                        y_bkg_array_interp = np.zeros_like(x_array)
                        if '_pd_background' in ed_experiment['loops'].keys():
                            bkg = ed_experiment['loops']['_pd_background']
                            x_bkg_array = [point['_2theta']['value'] for point in bkg]
                            y_bkg_array = [point['_intensity']['value'] for point in bkg]
                            y_bkg_array_interp = np.interp(x_array, x_bkg_array, y_bkg_array)
                        # Ranges (for charts)
                        x_min = dict(Parameter(float(x_array.min())))
                        x_max = dict(Parameter(float(x_array.max())))
                        y_min = float(y_meas_array.min())
                        y_max = float(y_meas_array.max())
                        y_range = y_max - y_min
                        y_extra = y_range * 0.1
                        y_min = dict(Parameter(y_min - y_extra))
                        y_max = dict(Parameter(y_max + y_extra))
                        self.chartRanges.append({'xMin': x_min,
                                                 'xMax': x_max,
                                                 'yMin': y_min,
                                                 'yMax': y_max})
                        self.chartRangesChanged.emit()
                ed_dict['experiments'].append(ed_experiment)
                self.addDataBlock(ed_experiment)
                self.addXArray(x_array)
                self.addYMeasArray(y_meas_array)
                self.addYBkgArray(y_bkg_array_interp)
