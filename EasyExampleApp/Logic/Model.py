# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json
from PySide6.QtCore import QObject, Signal, Slot, Property

from EasyApp.Logic.Logging import console
from Logic.Calculators import GaussianCalculator
from Logic.Helpers import Converter

try:
    import cryspy
    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_calc_chi_sq_by_dictionary
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')


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
    parameterEdited = Signal(str, int, str)

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
        console.debug(f"Model defined: {newValue}")
        self.definedChanged.emit()

    @Property(int, notify=currentIndexChanged)
    def currentIndex(self):
        return self._currentIndex

    @currentIndex.setter
    def currentIndex(self, newValue):
        if self._currentIndex == newValue:
            return
        self._currentIndex = newValue
        console.debug(f"Current model index: {newValue}")
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
        console.debug("Adding default model")
        dataBlock = _DEFAULT_DATA_BLOCK
        self.addDataBlock(dataBlock)
        yCalcArray = self.defaultYCalcArray()
        self.addYCalcArray(yCalcArray)

    @Slot(str)
    def loadModelFromFile_OLD(self, fpath):
        fpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', fpath))
        console.debug(f"Loading a model from {fpath}")
        with open(fpath, 'r') as f:
            dataBlock = json.load(f)
        index = len(self._dataBlocks) - 1
        self.addDataBlock(dataBlock)
        yCalcArray = self.calculateYCalcArray(index)
        self.addYCalcArray(yCalcArray)

    @Slot(str)
    def loadModelFromFile(self, fpath):
        fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'examples', 'PbSO4.rcif')
        console.debug(f"Loading a model from {fpath}")

        # Load RCIF file by cryspy and convert it into easydiffraction data block
        cryspyObj = cryspy.load_file(fpath)
        cryspyDict = cryspyObj.get_dictionary()
        edDict = self.createEdDict(cryspyObj, cryspyDict)

        # Calculate data based on...
        cryspyInOutDict = {}
        rhochi_calc_chi_sq_by_dictionary(cryspyDict,
                                         dict_in_out=cryspyInOutDict,
                                         flag_use_precalculated_data=False,
                                         flag_calc_analytical_derivatives=False)

        first_experiment_name = list(edDict['experiments'][0].keys())[0]
        yCalcArray = cryspyInOutDict[f'pd_{first_experiment_name}']['signal_plus']
        self.addYCalcArray(yCalcArray)

    @Slot(int)
    def removeModel(self, index):
        console.debug(f"Removing model no. {index + 1}")
        del self._dataBlocks[index]
        del self._yCalcArrays[index]
        self.dataBlocksChanged.emit()
        self.yCalcArraysChanged.emit()
        console.debug(f"Model no. {index + 1} has been removed")

    @Slot()
    def removeAllModels(self):
        self._dataBlocks.clear()
        self._yCalcArrays.clear()
        self.dataBlocksChanged.emit()
        self.yCalcArraysChanged.emit()
        console.debug("All models have been removed")

    @Slot(str, int, str, str, str)
    def editParameter(self, page, blockIndex, name, item, value):
        block = 'model'
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
            #####self._dataBlocks[blockIndex]['params'][name]['error'] = 0
        # Update value
        if self._dataBlocks[blockIndex]['params'][name][item] == value:
            return
        self._dataBlocks[blockIndex]['params'][name][item] = value
        console.debug(f"Parameter '{block}[{blockIndex}].{name}.{item}' has been changed to '{value}'")
        # Signalling value has been changed
        self.parameterEdited.emit(page, blockIndex, name)
        console.debug(f"Data blocks for '{block}' has been changed")
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

    def updateYCalcArrayByIndex(self, index):
        self._yCalcArrays[index] = self.calculateYCalcArray(index)
        console.debug(f"Pattern for model no. {index + 1} has been calculated")
        self.yCalcArraysChanged.emit()

    def updateCurrentModelYCalcArray(self):
        index = self._currentIndex
        self.updateYCalcArrayByIndex(index)

    def addDataBlock(self, dataBlock):
        console.debug(f"Adding data block (model parameters). Model no. {len(self._dataBlocks) + 1}")
        self._dataBlocks.append(dataBlock)
        self.dataBlocksChanged.emit()

    def addYCalcArray(self, yCalcArray):
        console.debug(f"Adding y-calculated data. Model no. {len(self._dataBlocks)}")
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
        console.debug("Converting model dataBlocks to JSON string")
        self._dataBlocksJson = Converter.dictToJson(self._dataBlocks)
        console.debug("Model dataBlocks have been converted to JSON string")
        self.dataBlocksJsonChanged.emit()

    # Convert cryspy_obj and cryspy_dict into easydiffraction_dict for further use as datablock
    def createEdDict(self, cryspy_obj, cryspy_dict):
        phase_names = [name.replace('crystal_', '') for name in cryspy_dict.keys() if name.startswith('crystal_')]
        experiment_names = [name.replace('pd_', '') for name in cryspy_dict.keys() if name.startswith('pd_')]
        ed_dict = {}
        for data_block in cryspy_obj.items:
            data_block_name = data_block.data_name
            # Phase datablock
            if data_block_name in phase_names:
                ed_dict['phases'] = []
                ed_phase = {data_block_name: {}}
                cryspy_phase = data_block.items
                for item in cryspy_phase:
                    # Space group section
                    if type(item) == cryspy.C_item_loop_classes.cl_2_space_group.SpaceGroup:
                        ed_phase[data_block_name]['_space_group_name_H-M_alt'] = item.name_hm_alt
                    # Cell section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_cell.Cell:
                        ed_phase[data_block_name]['_cell_length_a'] = item.length_a
                        ed_phase[data_block_name]['_cell_length_b'] = item.length_b
                        ed_phase[data_block_name]['_cell_length_c'] = item.length_c
                        ed_phase[data_block_name]['_cell_angle_alpha'] = item.angle_alpha
                        ed_phase[data_block_name]['_cell_angle_beta'] = item.angle_beta
                        ed_phase[data_block_name]['_cell_angle_gamma'] = item.angle_gamma
                    # Atoms section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_atom_site.AtomSiteL:
                        ed_atoms = []
                        cryspy_atoms = item.items
                        for cryspy_atom in cryspy_atoms:
                            ed_atom = {}
                            ed_atom['_label'] = cryspy_atom.label
                            ed_atom['_type_symbol'] = cryspy_atom.type_symbol
                            ed_atom['_fract_x'] = cryspy_atom.fract_x
                            ed_atom['_fract_y'] = cryspy_atom.fract_y
                            ed_atom['_fract_z'] = cryspy_atom.fract_z
                            ed_atom['_occupancy'] = cryspy_atom.occupancy
                            ed_atom['_adp_type'] = cryspy_atom.adp_type
                            ed_atom['_B_iso_or_equiv'] = cryspy_atom.b_iso_or_equiv
                            ed_atom['_multiplicity'] = cryspy_atom.multiplicity
                            ed_atom['_Wyckoff_symbol'] = cryspy_atom.wyckoff_symbol
                            ed_atoms.append(ed_atom)
                        ed_phase[data_block_name]['_atom_site'] = ed_atoms
                ed_dict['phases'].append(ed_phase)
                # Experiment datablock
            if data_block_name in experiment_names:
                ed_dict['experiments'] = []
                ed_experiment = {data_block_name: {}}
                cryspy_experiment = data_block.items
                for item in cryspy_experiment:
                    # Ranges section
                    if type(item) == cryspy.C_item_loop_classes.cl_1_range.Range:
                        ed_experiment[data_block_name]['_pd_meas_2theta_range_min'] = item.ttheta_min
                        ed_experiment[data_block_name]['_pd_meas_2theta_range_max'] = item.ttheta_max
                        ed_experiment[data_block_name]['_pd_meas_2theta_range_inc'] = 0.05  # NEED FIX
                    # Setup section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_setup.Setup:
                        ed_experiment[data_block_name]['_diffrn_radiation_probe'] = item.radiation.replace('neutrons', 'neutron').replace('X-rays', 'x-ray')
                        ed_experiment[data_block_name]['_diffrn_radiation_wavelength'] = item.wavelength
                        ed_experiment[data_block_name]['_pd_meas_2theta_offset'] = item.offset_ttheta
                    # Instrument resolution section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_resolution.PdInstrResolution:
                        ed_experiment[data_block_name]['_pd_instr_resolution_u'] = item.u
                        ed_experiment[data_block_name]['_pd_instr_resolution_v'] = item.v
                        ed_experiment[data_block_name]['_pd_instr_resolution_w'] = item.w
                        ed_experiment[data_block_name]['_pd_instr_resolution_x'] = item.x
                        ed_experiment[data_block_name]['_pd_instr_resolution_y'] = item.y
                    # Peak assymetries section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_reflex_asymmetry.PdInstrReflexAsymmetry:
                        ed_experiment[data_block_name]['_pd_instr_reflex_asymmetry_p1'] = item.p1
                        ed_experiment[data_block_name]['_pd_instr_reflex_asymmetry_p2'] = item.p2
                        ed_experiment[data_block_name]['_pd_instr_reflex_asymmetry_p3'] = item.p3
                        ed_experiment[data_block_name]['_pd_instr_reflex_asymmetry_p4'] = item.p4
                    # Phases section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_phase.PhaseL:
                        ed_phases = []
                        cryspy_phases = item.items
                        for cryspy_phase in cryspy_phases:
                            ed_phase = {}
                            ed_phase['_label'] = cryspy_phase.label
                            ed_phase['_scale'] = cryspy_phase.scale
                            ed_phases.append(ed_phase)
                        ed_experiment[data_block_name]['_phase'] = ed_phases
                    # Background section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_background.PdBackgroundL:
                        ed_bkg_points = []
                        cryspy_bkg_points = item.items
                        for cryspy_bkg_point in cryspy_bkg_points:
                            ed_bkg_point = {}
                            ed_bkg_point['_2theta'] = cryspy_bkg_point.ttheta
                            ed_bkg_point['_intensity'] = cryspy_bkg_point.intensity
                            ed_bkg_points.append(ed_bkg_point)
                        ed_experiment[data_block_name]['_pd_background'] = ed_bkg_points
                    # Measured data section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_meas.PdMeasL:
                        ed_meas_points = []
                        cryspy_meas_points = item.items
                        for cryspy_meas_point in cryspy_meas_points:
                            ed_meas_point = {}
                            ed_meas_point['_2theta'] = cryspy_meas_point.ttheta
                            ed_meas_point['_intensity'] = cryspy_meas_point.intensity
                            ed_meas_point['_intensity_sigma'] = cryspy_meas_point.intensity_sigma
                            ed_meas_points.append(ed_meas_point)
                        ed_experiment[data_block_name]['_pd_meas'] = ed_meas_points
                ed_dict['experiments'].append(ed_experiment)
        return ed_dict

