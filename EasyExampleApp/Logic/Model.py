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
        fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'examples', 'PbSO4_model.cif')
        console.debug(f"Loading a model from {fpath}")
        # Load RCIF file by cryspy and extract phases into easydiffraction data block
        cryspyModelObj = cryspy.load_file(fpath)
        cryspyModelDict = cryspyModelObj.get_dictionary()
        self._proxy.data._cryspyDict.update(cryspyModelDict)
        self.parseModels(cryspyModelObj)

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

    @Slot(str, result=str)
    def parameter(self, name):
        return name
        console.error(f'self.defined {self.defined}')
        if not self.defined:
            return ''
        value = self.dataBlocks[self.currentIndex].params[name]['value']
        formattedValue = "{:.4f}".format(value)
        console.error(f'formattedValue {formattedValue}')
        return formattedValue

    @Slot(str, str, str)
    def editParameter(self, name, item, value):
        block = 'model'
        blockIndex = self._currentIndex
        console.debug(f"Editing '{block}' block parameter '{block}[{blockIndex}].{name}.{item}' to '{value}'")
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

        # Updating cryspy_dict: NEED FIX
        blockName = self._dataBlocks[blockIndex]['name']
        cryspyBlockName = f'crystal_{blockName}'
        cryspyBlock = self._proxy.data._cryspyDict[cryspyBlockName]
        if name == '_cell_length_a': cryspyBlock['unit_cell_parameters'][0] = value
        if name == '_cell_length_b': cryspyBlock['unit_cell_parameters'][1] = value
        if name == '_cell_length_c': cryspyBlock['unit_cell_parameters'][2] = value
        if name == '_cell_angle_alpha': cryspyBlock['unit_cell_parameters'][3] = np.deg2rad(value)
        if name == '_cell_angle_beta': cryspyBlock['unit_cell_parameters'][4] = np.deg2rad(value)
        if name == '_cell_angle_gamma': cryspyBlock['unit_cell_parameters'][5] = np.deg2rad(value)

        # Signalling value has been changed
        page = 'model'  # ???????
        self.parameterEdited.emit(page, blockIndex, name)
        console.debug(f"Data blocks for '{block}' has been changed")
        self.dataBlocksChanged.emit()

    #
    @Slot(str, str, int, float)
    def editLoopParameterValue(self, loopName, parameterName, parameterIndex, value):
        block = 'model'
        blockIndex = self._currentIndex

        oldValue = self._dataBlocks[blockIndex]['loops'][loopName][parameterIndex][parameterName]['value']
        if oldValue == value:
            return
        self._dataBlocks[blockIndex]['loops'][loopName][parameterIndex][parameterName]['value'] = value
        console.debug(f"Parameter {block}[{blockIndex}].loops['{loopName}'][{parameterIndex}]['{parameterName}']['value'] changed: '{oldValue}' -> '{value}'")

        # Updating cryspy_dict: NEED FIX
        blockName = self._dataBlocks[blockIndex]['name']
        cryspyBlockName = f'crystal_{blockName}'
        cryspyBlock = self._proxy.data._cryspyDict[cryspyBlockName]
        if loopName == '_atom_site':
            if parameterName == '_fract_x': cryspyBlock['atom_fract_xyz'][0][parameterIndex] = value
            if parameterName == '_fract_y': cryspyBlock['atom_fract_xyz'][1][parameterIndex] = value
            if parameterName == '_fract_z': cryspyBlock['atom_fract_xyz'][2][parameterIndex] = value
            if parameterName == '_occupancy': cryspyBlock['atom_occupancy'][parameterIndex] = value

        # Signalling value has been changed
        page = 'model'  # ???????
        self.parameterEdited.emit(page, blockIndex, parameterName)  # parameterName not needed???
        console.debug(f"Data blocks for '{block}' has been changed")
        self.dataBlocksChanged.emit()

    # Private methods

    def defaultYCalcArray(self):
        xArray = self._proxy.experiment._xArrays[0]  # NEED FIX
        params = _DEFAULT_DATA_BLOCK['params']
        yCalcArray = GaussianCalculator.calculated(xArray, params)
        return yCalcArray

    def calculateYCalcArray_OLD(self, index):
        xArray = self._proxy.experiment._xArrays[0]  # NEED FIX
        params = self._dataBlocks[index]['params']
        yCalcArray = GaussianCalculator.calculated(xArray, params)
        return yCalcArray

    def calculateYCalcArray(self, index):
        # Re-calculate diffraction pattern
        yCalcArray = self.calculateDiffractionPattern()
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

    # Extract phases from cryspy_obj and cryspy_dict into internal ed_dict
    def parseModels(self, cryspy_obj):
        ed_dict = self._proxy.data.edDict
        cryspy_dict = self._proxy.data._cryspyDict
        phase_names = [name.replace('crystal_', '') for name in cryspy_dict.keys() if name.startswith('crystal_')]
        for data_block in cryspy_obj.items:
            data_block_name = data_block.data_name
            # Phase datablock
            if data_block_name in phase_names:
                ed_dict['phases'] = []
                ed_phase = {'name': data_block_name,
                                 'params': {},
                                 'loops': {}}
                cryspy_phase = data_block.items
                for item in cryspy_phase:
                    # Space group section
                    if type(item) == cryspy.C_item_loop_classes.cl_2_space_group.SpaceGroup:
                        ed_phase['params']['_space_group_name_H-M_alt'] = dict(Parameter(item.name_hm_alt))
                        ed_phase['params']['_space_group_IT_coordinate_system_code'] = dict(Parameter(item.it_coordinate_system_code))
                    # Cell section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_cell.Cell:
                        ed_phase['params']['_cell_length_a'] = dict(Parameter(item.length_a, min=1, max=10, fittable=True))
                        ed_phase['params']['_cell_length_b'] = dict(Parameter(item.length_b, min=1, max=10, fittable=True))
                        ed_phase['params']['_cell_length_c'] = dict(Parameter(item.length_c, min=1, max=10, fittable=True))
                        ed_phase['params']['_cell_angle_alpha'] = dict(Parameter(item.angle_alpha, min=0, max=180, fittable=True))
                        ed_phase['params']['_cell_angle_beta'] = dict(Parameter(item.angle_beta, min=0, max=180, fittable=True))
                        ed_phase['params']['_cell_angle_gamma'] = dict(Parameter(item.angle_gamma, min=0, max=180, fittable=True))
                    # Atoms section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_atom_site.AtomSiteL:
                        ed_atoms = []
                        cryspy_atoms = item.items
                        for cryspy_atom in cryspy_atoms:
                            ed_atom = {}
                            ed_atom['_label'] = dict(Parameter(cryspy_atom.label))
                            ed_atom['_type_symbol'] = dict(Parameter(cryspy_atom.type_symbol))
                            ed_atom['_fract_x'] = dict(Parameter(cryspy_atom.fract_x, min=-1, max=1, fittable=True))
                            ed_atom['_fract_y'] = dict(Parameter(cryspy_atom.fract_y, min=-1, max=1, fittable=True))
                            ed_atom['_fract_z'] = dict(Parameter(cryspy_atom.fract_z, min=-1, max=1, fittable=True))
                            ed_atom['_occupancy'] = dict(Parameter(cryspy_atom.occupancy, min=0, max=1, fittable=True))
                            ed_atom['_adp_type'] = dict(Parameter(cryspy_atom.adp_type))
                            ed_atom['_B_iso_or_equiv'] = dict(Parameter(cryspy_atom.b_iso_or_equiv, min=0, max=1, fittable=True))
                            ed_atom['_multiplicity'] = dict(Parameter(cryspy_atom.multiplicity))
                            ed_atom['_Wyckoff_symbol'] = dict(Parameter(cryspy_atom.wyckoff_symbol))
                            ed_atoms.append(ed_atom)
                        ed_phase['loops']['_atom_site'] = ed_atoms
                ed_dict['phases'].append(ed_phase)
                self.addDataBlock(ed_phase)

                # Calculate data based on...
                y_calc_array = self.calculateDiffractionPattern()
                self.addYCalcArray(y_calc_array)

    def calculateDiffractionPattern(self):        
        rhochi_calc_chi_sq_by_dictionary(self._proxy.data._cryspyDict,
                                         dict_in_out=self._proxy.data._cryspyInOutDict,
                                         flag_use_precalculated_data=False,
                                         flag_calc_analytical_derivatives=False)
        first_experiment_name = self._proxy.data.edDict['experiments'][0]['name']  # NEED FIX
        y_calc_array = self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['signal_plus']
        return y_calc_array
