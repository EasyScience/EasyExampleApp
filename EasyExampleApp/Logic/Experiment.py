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
        fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'examples', 'PbSO4.rcif')
        console.debug(f"Loading an experiment from {fpath}")
        # Load RCIF file by cryspy and extract experiments into easydiffraction data block
        cryspyObj = cryspy.load_file(fpath)
        cryspyDict = cryspyObj.get_dictionary()
        self.parseExperiments(cryspyObj, cryspyDict)

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

    # Extract experiments from cryspy_obj and cryspy_dict into internal ed_dict
    def parseExperiments(self, cryspy_obj, cryspy_dict):
        ed_dict = self._proxy.data.edDict
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
                        ed_experiment['params']['_pd_meas_2theta_range_min'] = Parameter(item.ttheta_min)
                        ed_experiment['params']['_pd_meas_2theta_range_max'] = Parameter(item.ttheta_min)
                        ed_experiment['params']['_pd_meas_2theta_range_inc'] = Parameter(0.05)  # NEED FIX
                    # Setup section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_setup.Setup:
                        ed_experiment['params']['_diffrn_radiation_probe'] = Parameter(item.radiation.replace('neutrons', 'neutron').replace('X-rays', 'x-ray'))
                        ed_experiment['params']['_diffrn_radiation_wavelength'] = Parameter(item.wavelength, fittable=True)
                        ed_experiment['params']['_pd_meas_2theta_offset'] = Parameter(item.offset_ttheta, fittable=True)
                    # Instrument resolution section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_resolution.PdInstrResolution:
                        ed_experiment['params']['_pd_instr_resolution_u'] = Parameter(item.u, fittable=True)
                        ed_experiment['params']['_pd_instr_resolution_v'] = Parameter(item.v, fittable=True)
                        ed_experiment['params']['_pd_instr_resolution_w'] = Parameter(item.w, fittable=True)
                        ed_experiment['params']['_pd_instr_resolution_x'] = Parameter(item.x, fittable=True)
                        ed_experiment['params']['_pd_instr_resolution_y'] = Parameter(item.y, fittable=True)
                    # Peak assymetries section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_reflex_asymmetry.PdInstrReflexAsymmetry:
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p1'] = Parameter(item.p1, fittable=True)
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p2'] = Parameter(item.p2, fittable=True)
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p3'] = Parameter(item.p3, fittable=True)
                        ed_experiment['params']['_pd_instr_reflex_asymmetry_p4'] = Parameter(item.p4, fittable=True)
                    # Phases section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_phase.PhaseL:
                        ed_phases = []
                        cryspy_phases = item.items
                        for cryspy_phase in cryspy_phases:
                            ed_phase = {}
                            ed_phase['_label'] = cryspy_phase.label
                            ed_phase['_scale'] = cryspy_phase.scale
                            ed_phases.append(ed_phase)
                        ed_experiment['loops']['_phase'] = ed_phases
                    # Background section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_background.PdBackgroundL:
                        ed_bkg_points = []
                        cryspy_bkg_points = item.items
                        for cryspy_bkg_point in cryspy_bkg_points:
                            ed_bkg_point = {}
                            ed_bkg_point['_2theta'] = cryspy_bkg_point.ttheta
                            ed_bkg_point['_intensity'] = cryspy_bkg_point.intensity
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
                        y_bkg_array = np.zeros_like(x_array)
                ed_dict['experiments'].append(ed_experiment)
                self.addDataBlock(ed_experiment)
                self.addXArray(x_array)
                self.addYMeasArray(y_meas_array)
                self.addYBkgArray(y_bkg_array)
