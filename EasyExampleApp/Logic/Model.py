# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json
import copy
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
    dataBlocksCifChanged = Signal()
    yCalcArraysChanged = Signal()

    structViewAtomsModelChanged = Signal()
    structViewCellModelChanged = Signal()
    structViewAxesModelChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._defined = False
        self._currentIndex = 0
        self._dataBlocks = []
        self._dataBlocksCif = ''
        self._yCalcArrays = []
        self._yBkgArrays = []

        self._structViewAtomsModel = []
        self._structViewCellModel = []
        self._structViewAxesModel = []

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

    @Property(str, notify=dataBlocksCifChanged)
    def dataBlocksCif(self):
        return self._dataBlocksCif

    @Property('QVariant', notify=structViewAtomsModelChanged)
    def structViewAtomsModel(self):
        return self._structViewAtomsModel

    @Property('QVariant', notify=structViewCellModelChanged)
    def structViewCellModel(self):
        return self._structViewCellModel

    @Property('QVariant', notify=structViewAxesModelChanged)
    def structViewAxesModel(self):
        return self._structViewAxesModel

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
        #fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'examples', 'Co2SiO4_model.cif')
        fpath = IO.generalizePath(fpath)
        console.debug(f"File: {fpath}")
        # Load ED CIF file, convert it to CrysPy RCIF and create CrysPy obj from string
        edCif = ''
        with open(fpath, 'r') as file:
            edCif = file.read()
        self.loadModelFromEdCif(edCif)

    @Slot(str)
    def loadModelFromEdCif(self, edCif):
        cryspyCif = Converter.edCifToCryspyCif(edCif)
        cryspyModelObj = str_to_globaln(cryspyCif)
        self._proxy.data._cryspyModelObj = cryspyModelObj  # NEED FIX!!!
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

    @Slot(str, str, float)
    def setMainParam(self, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(paramName, field, value)
        changedCryspy = True
        if field == 'value':
            changedCryspy = self.editCryspyDictByMainParam(paramName, value)

        if changedIntern and changedCryspy:
            self.dataBlocksChanged.emit()

    @Slot(str, str, int, str, float)
    def setLoopParam(self, loopName, paramName, paramIndex, field, value):
        changedIntern = self.editDataBlockLoopParam(loopName, paramName, paramIndex, field, value)
        changedCryspy = True
        if field == 'value':
            changedCryspy = self.editCryspyDictByLoopParam(loopName, paramName, paramIndex, value)

        if changedIntern and changedCryspy:
            self.dataBlocksChanged.emit()

    # Private methods

    def editDataBlockMainParam(self, paramName, field, value, blockIndex=None):
        block = 'model'
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

    def editDataBlockLoopParam(self, loopName, paramName, paramIndex, field, value, blockIndex=None):
        block = 'model'
        if blockIndex is None:
            blockIndex = self._currentIndex

        if field == 'fit':
            value = bool(value)

        oldValue = self._dataBlocks[blockIndex]['loops'][loopName][paramIndex][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocks[blockIndex]['loops'][loopName][paramIndex][paramName][field] = value

        console.debug(f"Intern dict ▌ {oldValue} → {value} ▌ {block}[{blockIndex}].{loopName}[{paramIndex}].{paramName}.{field}")
        return True

    def editCryspyDictByMainParam(self, paramName, value):
        path, value = self.cryspyDictPathByMainParam(paramName, value)

        oldValue = self._proxy.data._cryspyDict[path[0]][path[1]][path[2]]
        if oldValue == value:
            return False
        self._proxy.data._cryspyDict[path[0]][path[1]][path[2]] = value

        console.debug(f"Cryspy dict ▌ {oldValue} → {value} ▌ {path}")
        return True

    def editCryspyDictByLoopParam(self, loopName, paramName, paramIndex, value):
        path, value = self.cryspyDictPathByLoopParam(loopName, paramName, paramIndex, value)

        oldValue = self._proxy.data._cryspyDict[path[0]][path[1]][path[2]]
        if oldValue == value:
            return False
        self._proxy.data._cryspyDict[path[0]][path[1]][path[2]] = value

        console.debug(f"Cryspy dict ▌ {oldValue} → {value} ▌ {path}")
        return True

    def cryspyDictPathByMainParam(self, paramName, value):
        blockIndex = self._currentIndex
        blockName = self._dataBlocks[blockIndex]['name']
        path = ['','','']
        path[0] = f"crystal_{blockName}"

        # _cell
        if paramName == '_cell_length_a':
            path[1] = 'unit_cell_parameters'
            path[2] = 0
        elif paramName == '_cell_length_b':
            path[1] = 'unit_cell_parameters'
            path[2] = 1
        elif paramName == '_cell_length_c':
            path[1] = 'unit_cell_parameters'
            path[2] = 2
        elif paramName == '_cell_angle_alpha':
            path[1] = 'unit_cell_parameters'
            path[2] = 3
            value = np.deg2rad(value)
        elif paramName == '_cell_angle_beta':
            path[1] = 'unit_cell_parameters'
            path[2] = 4
            value = np.deg2rad(value)
        elif paramName == '_cell_angle_gamma':
            path[1] = 'unit_cell_parameters'
            path[2] = 5
            value = np.deg2rad(value)

        # undefined
        else:
            console.error(f"Undefined parameter name '{paramName}'")

        return path, value

    def cryspyDictPathByLoopParam(self, loopName, paramName, paramIndex, value):
        blockIndex = self._currentIndex
        blockName = self._dataBlocks[blockIndex]['name']
        path = ['','','']
        path[0] = f"crystal_{blockName}"

        # _atom_site
        if loopName == '_atom_site':
            if paramName == '_fract_x':
                path[1] = 'atom_fract_xyz'
                path[2] = (0, paramIndex)
            if paramName == '_fract_y':
                path[1] = 'atom_fract_xyz'
                path[2] = (1, paramIndex)
            if paramName == '_fract_z':
                path[1] = 'atom_fract_xyz'
                path[2] = (2, paramIndex)
            if paramName == '_occupancy':
                path[1] = 'atom_occupancy'
                path[2] = paramIndex

        return path, value

    def editDataBlockByCryspyDictParams(self, params):
        for param in params:
            block, group, idx = Data.strToCryspyDictParamPath(param)

            # crystal block
            if block.startswith('crystal_'):
                blockName = block[8:]
                loopName = None
                paramName = None
                paramIndex = None
                value = self._proxy.data._cryspyDict[block][group][idx]

                # unit_cell_parameters
                if group == 'unit_cell_parameters':
                    if idx[0] == 0:
                        paramName = '_cell_length_a'
                    elif idx[0] == 1:
                        paramName = '_cell_length_b'
                    elif idx[0] == 2:
                        paramName = '_cell_length_c'
                    elif idx[0] == 3:
                        paramName = '_cell_angle_alpha'
                        value = np.rad2deg(value)
                    elif idx[0] == 4:
                        paramName = '_cell_angle_beta'
                        value = np.rad2deg(value)
                    elif idx[0] == 5:
                        paramName = '_cell_angle_gamma'
                        value = np.rad2deg(value)

                # atom_fract_xyz
                elif group == 'atom_fract_xyz':
                    loopName = '_atom_site'
                    paramIndex = idx[1]
                    if idx[0] == 0:
                        paramName = '_fract_x'
                    elif idx[0] == 1:
                        paramName = '_fract_y'
                    elif idx[0] == 2:
                        paramName = '_fract_z'

                # atom_occupancy
                elif group == 'atom_occupancy':
                    loopName = '_atom_site'
                    paramIndex = idx[0]
                    paramName = '_occupancy'

                # b_iso_or_equiv
                elif group == 'atom_b_iso':
                    loopName = '_atom_site'
                    paramIndex = idx[0]
                    paramName = '_B_iso_or_equiv'

                value = float(value)  # convert float64 to float (needed for QML access)
                blockIndex = [block['name'] for block in self._dataBlocks].index(blockName)

                if loopName is None:
                    self.editDataBlockMainParam(paramName, value, blockIndex)
                else:
                    self.editDataBlockLoopParam(loopName, paramName, paramIndex, value, blockIndex)




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
        idx = -1
        for i, block in enumerate(self._dataBlocks):
            if dataBlock['name'] == block['name']:
                idx = i
                continue
        if idx == -1:
            self._dataBlocks.append(dataBlock)
        else:
            self._dataBlocks[idx] = dataBlock
        console.debug(f"Model data block no. {len(self._dataBlocks)} has been added to intern dataset")
        self.dataBlocksChanged.emit()

    def addYCalcArray(self, yCalcArray):
        self._yCalcArrays.append(yCalcArray)
        console.debug(f"Y-calculated data for model data block no. {len(self._dataBlocks)} has been added to intern dataset")
        self.yCalcArraysChanged.emit()

    #def calculateAllYArrays(self):
    #    for i in range(len(self._dataBlocks)):
    #        self.calculateSingleYArray(i)

    #def scaleSingleDataBlock(self, index):
    #    scale = self._proxy.experiment.models[index]['scale']
    #    self._yCalcArrays[index]['yArray'] *= scale
    #    self.calculatedDataChanged.emit()

    def setDataBlocksCif(self):
        #console.debug("Converting model dataBlocks to CIF string")
        #self._dataBlocksCif = Converter.dictToJson(self._dataBlocks)
        self._dataBlocksCif = Converter.dataBlocksToCif(self._dataBlocks)
        console.debug("Model dataBlocks have been converted to CIF string")
        self.dataBlocksCifChanged.emit()

    # Extract phases from cryspy_obj and cryspy_dict into internal ed_dict
    def parseModels(self, cryspy_obj):
        ###ed_dict = self._proxy.data.edDict
        cryspy_dict = self._proxy.data._cryspyDict
        phase_names = [name.replace('crystal_', '') for name in cryspy_dict.keys() if name.startswith('crystal_')]

        for data_block in cryspy_obj.items:
            data_block_name = data_block.data_name

            # Phase datablock
            if data_block_name in phase_names:

                ###ed_dict['phases'] = []
                ed_phase = {'name': data_block_name,
                            'params': {},
                            'loops': {}}
                cryspy_phase = data_block.items

                for item in cryspy_phase:

                    # Space group section
                    if type(item) == cryspy.C_item_loop_classes.cl_2_space_group.SpaceGroup:
                        ed_phase['params']['_space_group_name_H-M_alt'] = dict(Parameter(
                            item.name_hm_alt,
                            name = '_space_group_name_H-M_alt',
                            prettyName = 'name H-M alt',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core'
                        ))
                        ed_phase['params']['_space_group_IT_coordinate_system_code'] = dict(Parameter(
                            item.it_coordinate_system_code,
                            name = '_space_group_IT_coordinate_system_code',
                            prettyName = 'IT coordinate system code',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core'
                        ))
                    # Cell section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_cell.Cell:
                        ed_phase['params']['_cell_length_a'] = dict(Parameter(
                            item.length_a,
                            name = '_cell_length_a',
                            prettyName = 'length a',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core',
                            enabled = not item.length_a_constraint,
                            min = 1,
                            max = 30,
                            units = 'Å',
                            fittable = True,
                            fit = item.length_a_refinement
                        ))
                        ed_phase['params']['_cell_length_b'] = dict(Parameter(
                            item.length_b,
                            name = '_cell_length_b',
                            prettyName = 'length b',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core',
                            enabled = not item.length_b_constraint,
                            min = 1,
                            max = 30,
                            units = 'Å',
                            fittable = True,
                            fit = item.length_b_refinement
                        ))
                        ed_phase['params']['_cell_length_c'] = dict(Parameter(
                            item.length_c,
                            name = '_cell_length_c',
                            prettyName = 'length c',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core',
                            enabled = not item.length_c_constraint,
                            min = 1,
                            max = 30,
                            units = 'Å',
                            fittable = True,
                            fit = item.length_c_refinement
                        ))
                        ed_phase['params']['_cell_angle_alpha'] = dict(Parameter(
                            item.angle_alpha,
                            name = '_cell_angle_alpha',
                            prettyName = 'angle α',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core',
                            enabled = not item.angle_alpha_constraint,
                            min = 0,
                            max = 180,
                            units = '°',
                            fittable = True,
                            fit = item.angle_alpha_refinement
                        ))
                        ed_phase['params']['_cell_angle_beta'] = dict(Parameter(
                            item.angle_beta,
                            name = '_cell_angle_beta',
                            prettyName = 'angle β',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core',
                            enabled = not item.angle_alpha_constraint,
                            min = 0,
                            max = 180,
                            units = '°',
                            fittable = True,
                            fit = item.angle_beta_refinement
                        ))
                        ed_phase['params']['_cell_angle_gamma'] = dict(Parameter(
                            item.angle_gamma,
                            name = '_cell_angle_gamma',
                            prettyName = 'angle γ',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core',
                            enabled = not item.angle_alpha_constraint,
                            min = 0,
                            max = 180,
                            units = '°',
                            fittable = True,
                            fit = item.angle_gamma_refinement
                        ))

                    # Atoms section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_atom_site.AtomSiteL:
                        ed_atoms = []
                        cryspy_atoms = item.items
                        for idx, cryspy_atom in enumerate(cryspy_atoms):
                            ed_atom = {}
                            ed_atom['_label'] = dict(Parameter(
                                cryspy_atom.label,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_label',
                                prettyName = 'label',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core'
                            ))
                            ed_atom['_type_symbol'] = dict(Parameter(
                                cryspy_atom.type_symbol,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_type_symbol',
                                prettyName = 'type',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core'
                            ))
                            ed_atom['_fract_x'] = dict(Parameter(
                                cryspy_atom.fract_x,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_fract_x',
                                prettyName = 'fract x',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core',
                                enabled = not cryspy_atom.fract_x_constraint,
                                min = -1,
                                max = 1,
                                fittable = True,
                                fit = cryspy_atom.fract_x_refinement
                            ))
                            ed_atom['_fract_y'] = dict(Parameter(
                                cryspy_atom.fract_y,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_fract_y',
                                prettyName = 'fract y',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core',
                                enabled = not cryspy_atom.fract_y_constraint,
                                min = -1,
                                max = 1,
                                fittable = True,
                                fit = cryspy_atom.fract_y_refinement
                            ))
                            ed_atom['_fract_z'] = dict(Parameter(
                                cryspy_atom.fract_z,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_fract_z',
                                prettyName = 'fract z',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core',
                                enabled = not cryspy_atom.fract_z_constraint,
                                min = -1,
                                max = 1,
                                fittable = True,
                                fit = cryspy_atom.fract_z_refinement
                            ))
                            ed_atom['_occupancy'] = dict(Parameter(
                                cryspy_atom.occupancy,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_occupancy',
                                prettyName = 'occ.',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core',
                                enabled = not cryspy_atom.occupancy_constraint,
                                min = 0,
                                max = 1,
                                fittable = True,
                                fit = cryspy_atom.occupancy_refinement
                            ))
                            ed_atom['_adp_type'] = dict(Parameter(
                                cryspy_atom.adp_type,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_adp_type',
                                prettyName = 'type',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core'
                            ))
                            ed_atom['_B_iso_or_equiv'] = dict(Parameter(
                                cryspy_atom.b_iso_or_equiv,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_B_iso_or_equiv',
                                prettyName = 'iso',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core',
                                enabled = not cryspy_atom.b_iso_or_equiv_constraint,
                                min = 0,
                                max = 1,
                                fittable = True,
                                fit = cryspy_atom.b_iso_or_equiv_refinement
                            ))
                            ed_atom['_multiplicity'] = dict(Parameter(
                                cryspy_atom.multiplicity,
                                idx = idx,
                                loopName = '_atom_site',
                                name = '_multiplicity',
                                prettyName = '',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core'
                            ))
                            ed_atom['_Wyckoff_symbol'] = dict(Parameter(
                                cryspy_atom.wyckoff_symbol,
                                name = '_atom_site_Wyckoff_symbol',
                                prettyName = '',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core'
                            ))
                            ed_atoms.append(ed_atom)
                        ed_phase['loops']['_atom_site'] = ed_atoms

                ###ed_dict['phases'].append(ed_phase)
                self.addDataBlock(ed_phase)

#                # Calculate data based on...
#                y_calc_array = self.calculateDiffractionPattern()
#                self.addYCalcArray(y_calc_array)
#
#                pass
#
#                self.setCurrentModelStructViewCellModel()
#                self.setCurrentModelStructViewAxesModel()
#                self.setCurrentModelStructViewAtomsModel()

    def calculateDiffractionPattern(self):        
        chiSq, pointsCount, _, _, paramNames = rhochi_calc_chi_sq_by_dictionary(self._proxy.data._cryspyDict,
                                         dict_in_out=self._proxy.data._cryspyInOutDict,
                                         flag_use_precalculated_data=False,
                                         flag_calc_analytical_derivatives=False)
        first_experiment_name = self._proxy.data.edDict['experiments'][0]['name']  # NEED FIX
        y_calc_array = self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['signal_minus'] + self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['signal_plus']

        #################self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['dict_in_out_co2sio4']['ttheta_hkl']
        self._proxy.experiment._yBkgArrays[0] = self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['signal_background']  # NEED FIX

        return y_calc_array

    def updateCurrentModelStructView(self):
        self.setCurrentModelStructViewAtomsModel()
        #self.setCurrentModelStructViewCellModel()
        #self.setCurrentModelStructViewAxesModel()

    def setCurrentModelStructViewCellModel(self):
        params = self._dataBlocks[self._currentIndex]['params']
        a = params['_cell_length_a']['value']
        b = params['_cell_length_b']['value']
        c = params['_cell_length_c']['value']
        self._structViewCellModel = [
            # x
            { "x": 0,     "y":-0.5*b, "z":-0.5*c, "rotx": 0, "roty": 0,  "rotz":-90, "len": a },
            { "x": 0,     "y": 0.5*b, "z":-0.5*c, "rotx": 0, "roty": 0,  "rotz":-90, "len": a },
            { "x": 0,     "y":-0.5*b, "z": 0.5*c, "rotx": 0, "roty": 0,  "rotz":-90, "len": a },
            { "x": 0,     "y": 0.5*b, "z": 0.5*c, "rotx": 0, "roty": 0,  "rotz":-90, "len": a },
            # y
            { "x":-0.5*a, "y": 0,     "z":-0.5*c, "rotx": 0, "roty": 0,  "rotz": 0,  "len": b },
            { "x": 0.5*a, "y": 0,     "z":-0.5*c, "rotx": 0, "roty": 0,  "rotz": 0,  "len": b },
            { "x":-0.5*a, "y": 0,     "z": 0.5*c, "rotx": 0, "roty": 0,  "rotz": 0,  "len": b },
            { "x": 0.5*a, "y": 0,     "z": 0.5*c, "rotx": 0, "roty": 0,  "rotz": 0,  "len": b },
            # z
            { "x":-0.5*a, "y":-0.5*b, "z": 0,     "rotx": 0, "roty": 90, "rotz": 90, "len": c },
            { "x": 0.5*a, "y":-0.5*b, "z": 0,     "rotx": 0, "roty": 90, "rotz": 90, "len": c },
            { "x":-0.5*a, "y": 0.5*b, "z": 0,     "rotx": 0, "roty": 90, "rotz": 90, "len": c },
            { "x": 0.5*a, "y": 0.5*b, "z": 0,     "rotx": 0, "roty": 90, "rotz": 90, "len": c },
        ]
        console.debug(f"Structure view cell  for model no. {self._currentIndex + 1} has been set. Cell lengths: ({a}, {b}, {c})")
        self.structViewCellModelChanged.emit()

    def setCurrentModelStructViewAxesModel(self):
        params = self._dataBlocks[self._currentIndex]['params']
        a = params['_cell_length_a']['value']
        b = params['_cell_length_b']['value']
        c = params['_cell_length_c']['value']
        self._structViewAxesModel = [
            {"x": 0.5, "y": 0,   "z": 0,   "rotx": 0, "roty":  0, "rotz": -90, "len": a},
            {"x": 0,   "y": 0.5, "z": 0,   "rotx": 0, "roty":  0, "rotz":   0, "len": b},
            {"x": 0,   "y": 0,   "z": 0.5, "rotx": 0, "roty": 90, "rotz":  90, "len": c}
        ]
        console.debug(f"Structure view axes  for model no. {self._currentIndex + 1} has been set. Cell lengths: ({a}, {b}, {c})")
        self.structViewAxesModelChanged.emit()

    def setCurrentModelStructViewAtomsModel(self):
        structViewModel = set()
        #self._structViewAtomsModel = []
        spaceGroup = self._proxy.data._cryspyModelObj.items[0].items[1]  # NEED FIX. model index!!! [0], 'Space group' [1] cryspy.C_item_loop_classes.cl_2_space_group.SpaceGroup
        atoms = self._dataBlocks[self._currentIndex]['loops']['_atom_site']
        #params = self._dataBlocks[self._currentIndex]['params']
        #a = params['_cell_length_a']['value']
        #b = params['_cell_length_b']['value']
        #c = params['_cell_length_c']['value']
        # Add all atoms in the cell, including those in equivalent positions
        for atom in atoms:
            symbol = atom['_type_symbol']['value']
            xUnique = atom['_fract_x']['value']
            yUnique = atom['_fract_y']['value']
            zUnique = atom['_fract_z']['value']
            xArray, yArray, zArray, _ = spaceGroup.calc_xyz_mult(xUnique, yUnique, zUnique)
            for x, y, z in zip(xArray, yArray, zArray):
                structViewModel.add((
                    float(x),
                    float(y),
                    float(z),
                    0.333333 * self.atomData(symbol, 'covalentRadius'),
                    self.atomData(symbol, 'color')
                ))
        # Add those atoms, which have 0 in xyz to be translated into 1
        structViewModelCopy = copy.copy(structViewModel)
        for item in structViewModelCopy:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                structViewModel.add((1, 0, 0, item[3], item[4]))
                structViewModel.add((0, 1, 0, item[3], item[4]))
                structViewModel.add((0, 0, 1, item[3], item[4]))
                structViewModel.add((1, 1, 0, item[3], item[4]))
                structViewModel.add((1, 0, 1, item[3], item[4]))
                structViewModel.add((0, 1, 1, item[3], item[4]))
                structViewModel.add((1, 1, 1, item[3], item[4]))
            elif item[0] == 0 and item[1] == 0:
                structViewModel.add((1, 0, item[2], item[3], item[4]))
                structViewModel.add((0, 1, item[2], item[3], item[4]))
                structViewModel.add((1, 1, item[2], item[3], item[4]))
            elif item[0] == 0 and item[2] == 0:
                structViewModel.add((1, item[1], 0, item[3], item[4]))
                structViewModel.add((0, item[1], 1, item[3], item[4]))
                structViewModel.add((1, item[1], 1, item[3], item[4]))
            elif item[1] == 0 and item[2] == 0:
                structViewModel.add((item[0], 1, 0, item[3], item[4]))
                structViewModel.add((item[0], 0, 1, item[3], item[4]))
                structViewModel.add((item[0], 1, 1, item[3], item[4]))
            elif item[0] == 0:
                structViewModel.add((1, item[1], item[2], item[3], item[4]))
            elif item[1] == 0:
                structViewModel.add((item[0], 1, item[2], item[3], item[4]))
            elif item[2] == 0:
                structViewModel.add((item[0], item[1], 1, item[3], item[4]))
        # Create dict from set for GUI
        self._structViewAtomsModel = [{'x':x, 'y':y, 'z':z, 'diameter':diameter, 'color':color}
                                      for x, y, z, diameter, color in structViewModel]
        console.debug(f"Structure view atoms for model no. {self._currentIndex + 1} has been set. Atoms count: {len(atoms)}")
        self.structViewAtomsModelChanged.emit()


    def atomData(self, typeSymbol, key):
        data = {
            "H": {
              "symbol": "H",
              "name": "Hydrogen",
              "atomicNumber": 1,
              "addH": False,
              "color": "#FFFFFF",
              "covalentRadius": 0.31,
              "vdWRadius": 1.1,
              "valency": 1,
              "mass": 1
            },
            "He": {
              "symbol": "He",
              "name": "Helium",
              "atomicNumber": 2,
              "addH": False,
              "color": "#D9FFFF",
              "covalentRadius": 0.28,
              "vdWRadius": 1.4,
              "valency": 0,
              "mass": 4
            },
            "Li": {
              "symbol": "Li",
              "name": "Lithium",
              "atomicNumber": 3,
              "addH": False,
              "color": "#CC80FF",
              "covalentRadius": 1.28,
              "vdWRadius": 1.82,
              "valency": 1,
              "mass": 7
            },
            "Be": {
              "symbol": "Be",
              "name": "Beryllium",
              "atomicNumber": 4,
              "addH": False,
              "color": "#C2FF00",
              "covalentRadius": 0.96,
              "vdWRadius": 1.53,
              "valency": 2,
              "mass": 9
            },
            "B": {
              "symbol": "B",
              "name": "Boron",
              "atomicNumber": 5,
              "addH": False,
              "color": "#FFB5B5",
              "covalentRadius": 0.84,
              "vdWRadius": 1.92,
              "valency": 3,
              "mass": 11
            },
            "C": {
              "symbol": "C",
              "name": "Carbon",
              "atomicNumber": 6,
              "addH": False,
              "color": "#909090",
              "covalentRadius": 0.76,
              "vdWRadius": 1.7,
              "valency": 4,
              "mass": 12
            },
            "N": {
              "symbol": "N",
              "name": "Nitrogen",
              "atomicNumber": 7,
              "addH": False,
              "color": "#3050F8",
              "covalentRadius": 0.71,
              "vdWRadius": 1.55,
              "valency": 3,
              "mass": 14
            },
            "O": {
              "symbol": "O",
              "name": "Oxygen",
              "atomicNumber": 8,
              "addH": False,
              "color": "#FF0D0D",
              "covalentRadius": 0.66,
              "vdWRadius": 1.52,
              "valency": 2,
              "mass": 16
            },
            "F": {
              "symbol": "F",
              "name": "Fluorine",
              "atomicNumber": 9,
              "addH": False,
              "color": "#90E050",
              "covalentRadius": 0.57,
              "vdWRadius": 1.47,
              "valency": 1,
              "mass": 19
            },
            "Ne": {
              "symbol": "Ne",
              "name": "Neon",
              "atomicNumber": 10,
              "addH": False,
              "color": "#B3E3F5",
              "covalentRadius": 0.58,
              "vdWRadius": 1.54,
              "valency": 0,
              "mass": 20
            },
            "Na": {
              "symbol": "Na",
              "name": "Sodium",
              "atomicNumber": 11,
              "addH": True,
              "color": "#AB5CF2",
              "covalentRadius": 1.66,
              "vdWRadius": 2.27,
              "valency": 1,
              "mass": 23
            },
            "Mg": {
              "symbol": "Mg",
              "name": "Magnesium",
              "atomicNumber": 12,
              "addH": True,
              "color": "#8AFF00",
              "covalentRadius": 1.41,
              "vdWRadius": 1.73,
              "valency": 2,
              "mass": 24
            },
            "Al": {
              "symbol": "Al",
              "name": "Aluminum",
              "atomicNumber": 13,
              "addH": True,
              "color": "#BFA6A6",
              "covalentRadius": 1.21,
              "vdWRadius": 2.11,
              "valency": 3,
              "mass": 27
            },
            "Si": {
              "symbol": "Si",
              "name": "Silicon",
              "atomicNumber": 14,
              "addH": True,
              "color": "#F0C8A0",
              "covalentRadius": 1.11,
              "vdWRadius": 2.03,
              "valency": 4,
              "mass": 28
            },
            "P": {
              "symbol": "P",
              "name": "Phosphorus",
              "atomicNumber": 15,
              "addH": True,
              "color": "#FF8000",
              "covalentRadius": 1.07,
              "vdWRadius": 1.8,
              "valency": 3,
              "mass": 31
            },
            "S": {
              "symbol": "S",
              "name": "Sulfur",
              "atomicNumber": 16,
              "addH": True,
              "color": "#FFFF30",
              "covalentRadius": 1.05,
              "vdWRadius": 1.8,
              "valency": 2,
              "mass": 32
            },
            "Cl": {
              "symbol": "Cl",
              "name": "Chlorine",
              "atomicNumber": 17,
              "addH": False,
              "color": "#1FF01F",
              "covalentRadius": 1.02,
              "vdWRadius": 1.75,
              "valency": 1,
              "mass": 35
            },
            "Ar": {
              "symbol": "Ar",
              "name": "Argon",
              "atomicNumber": 18,
              "addH": False,
              "color": "#80D1E3",
              "covalentRadius": 1.06,
              "vdWRadius": 1.88,
              "valency": 0,
              "mass": 40
            },
            "K": {
              "symbol": "K",
              "name": "Potassium",
              "atomicNumber": 19,
              "addH": True,
              "color": "#8F40D4",
              "covalentRadius": 2.03,
              "vdWRadius": 2.75,
              "valency": 1,
              "mass": 39
            },
            "Ca": {
              "symbol": "Ca",
              "name": "Calcium",
              "atomicNumber": 20,
              "addH": True,
              "color": "#3DFF00",
              "covalentRadius": 1.76,
              "vdWRadius": 2.31,
              "valency": 2,
              "mass": 40
            },
            "Sc": {
              "symbol": "Sc",
              "name": "Scandium",
              "atomicNumber": 21,
              "addH": True,
              "color": "#E6E6E6",
              "covalentRadius": 1.7,
              "vdWRadius": 2.11,
              "valency": 3,
              "mass": 45
            },
            "Ti": {
              "symbol": "Ti",
              "name": "Titanium",
              "atomicNumber": 22,
              "addH": True,
              "color": "#BFC2C7",
              "covalentRadius": 1.6,
              "vdWRadius": 2.0,
              "valency": 4,
              "mass": 48
            },
            "V": {
              "symbol": "V",
              "name": "Vanadium",
              "atomicNumber": 23,
              "addH": True,
              "color": "#A6A6AB",
              "covalentRadius": 1.53,
              "vdWRadius": 1.92,
              "valency": 5,
              "mass": 51
            },
            "Cr": {
              "symbol": "Cr",
              "name": "Chromium",
              "atomicNumber": 24,
              "addH": True,
              "color": "#8A99C7",
              "covalentRadius": 1.39,
              "vdWRadius": 1.85,
              "valency": 3,
              "mass": 52
            },
            "Mn": {
              "symbol": "Mn",
              "name": "Manganese",
              "atomicNumber": 25,
              "addH": True,
              "color": "#9C7AC7",
              "covalentRadius": 1.39,
              "vdWRadius": 1.79,
              "valency": 2,
              "mass": 55
            },
            "Fe": {
              "symbol": "Fe",
              "name": "Iron",
              "atomicNumber": 26,
              "addH": True,
              "color": "#E06633",
              "covalentRadius": 1.32,
              "vdWRadius": 1.72,
              "valency": 2,
              "mass": 56
            },
            "Co": {
              "symbol": "Co",
              "name": "Cobalt",
              "atomicNumber": 27,
              "addH": True,
              "color": "#F090A0",
              "covalentRadius": 1.26,
              "vdWRadius": 1.67,
              "valency": 2,
              "mass": 59
            },
            "Ni": {
              "symbol": "Ni",
              "name": "Nickel",
              "atomicNumber": 28,
              "addH": True,
              "color": "#50D050",
              "covalentRadius": 1.24,
              "vdWRadius": 1.62,
              "valency": 2,
              "mass": 59
            },
            "Cu": {
              "symbol": "Cu",
              "name": "Copper",
              "atomicNumber": 29,
              "addH": True,
              "color": "#C88033",
              "covalentRadius": 1.32,
              "vdWRadius": 1.57,
              "valency": 2,
              "mass": 64
            },
            "Zn": {
              "symbol": "Zn",
              "name": "Zinc",
              "atomicNumber": 30,
              "addH": True,
              "color": "#7D80B0",
              "covalentRadius": 1.22,
              "vdWRadius": 1.53,
              "valency": 2,
              "mass": 65
            },
            "Ga": {
              "symbol": "Ga",
              "name": "Gallium",
              "atomicNumber": 31,
              "addH": True,
              "color": "#C28F8F",
              "covalentRadius": 1.22,
              "vdWRadius": 1.87,
              "valency": 3,
              "mass": 70
            },
            "Ge": {
              "symbol": "Ge",
              "name": "Germanium",
              "atomicNumber": 32,
              "addH": True,
              "color": "#668F8F",
              "covalentRadius": 1.2,
              "vdWRadius": 2.11,
              "valency": 4,
              "mass": 73
            },
            "As": {
              "symbol": "As",
              "name": "Arsenic",
              "atomicNumber": 33,
              "addH": True,
              "color": "#BD80E3",
              "covalentRadius": 1.19,
              "vdWRadius": 1.85,
              "valency": 3,
              "mass": 75
            },
            "Se": {
              "symbol": "Se",
              "name": "Selenium",
              "atomicNumber": 34,
              "addH": True,
              "color": "#FFA100",
              "covalentRadius": 1.2,
              "vdWRadius": 1.9,
              "valency": 2,
              "mass": 79
            },
            "Br": {
              "symbol": "Br",
              "name": "Bromine",
              "atomicNumber": 35,
              "addH": True,
              "color": "#A62929",
              "covalentRadius": 1.2,
              "vdWRadius": 1.85,
              "valency": 1,
              "mass": 80
            },
            "Kr": {
              "symbol": "Kr",
              "name": "Krypton",
              "atomicNumber": 36,
              "addH": False,
              "color": "#5CB8D1",
              "covalentRadius": 1.16,
              "vdWRadius": 2.02,
              "valency": 0,
              "mass": 84
            },
            "Rb": {
              "symbol": "Rb",
              "name": "Rubidium",
              "atomicNumber": 37,
              "addH": True,
              "color": "#702EB0",
              "covalentRadius": 2.2,
              "vdWRadius": 3.03,
              "valency": 1,
              "mass": 85
            },
            "Sr": {
              "symbol": "Sr",
              "name": "Strontium",
              "atomicNumber": 38,
              "addH": True,
              "color": "#00FF00",
              "covalentRadius": 1.95,
              "vdWRadius": 2.49,
              "valency": 2,
              "mass": 88
            },
            "Y": {
              "symbol": "Y",
              "name": "Yttrium",
              "atomicNumber": 39,
              "addH": True,
              "color": "#94FFFF",
              "covalentRadius": 1.9,
              "vdWRadius": 2.27,
              "valency": 3,
              "mass": 89
            },
            "Zr": {
              "symbol": "Zr",
              "name": "Zirconium",
              "atomicNumber": 40,
              "addH": True,
              "color": "#94E0E0",
              "covalentRadius": 1.75,
              "vdWRadius": 2.16,
              "valency": 4,
              "mass": 91
            },
            "Nb": {
              "symbol": "Nb",
              "name": "Niobium",
              "atomicNumber": 41,
              "addH": True,
              "color": "#73C2C9",
              "covalentRadius": 1.64,
              "vdWRadius": 2.08,
              "valency": 5,
              "mass": 93
            },
            "Mo": {
              "symbol": "Mo",
              "name": "Molybdenum",
              "atomicNumber": 42,
              "addH": True,
              "color": "#54B5B5",
              "covalentRadius": 1.54,
              "vdWRadius": 2.01,
              "valency": 6,
              "mass": 96
            },
            "Tc": {
              "symbol": "Tc",
              "name": "Technetium",
              "atomicNumber": 43,
              "addH": True,
              "color": "#3B9E9E",
              "covalentRadius": 1.47,
              "vdWRadius": 1.95,
              "valency": 7,
              "mass": 98
            },
            "Ru": {
              "symbol": "Ru",
              "name": "Ruthenium",
              "atomicNumber": 44,
              "addH": True,
              "color": "#248F8F",
              "covalentRadius": 1.46,
              "vdWRadius": 1.89,
              "valency": 8,
              "mass": 101
            },
            "Rh": {
              "symbol": "Rh",
              "name": "Rhodium",
              "atomicNumber": 45,
              "addH": True,
              "color": "#0A7D8C",
              "covalentRadius": 1.42,
              "vdWRadius": 1.83,
              "valency": 9,
              "mass": 103
            },
            "Pd": {
              "symbol": "Pd",
              "name": "Palladium",
              "atomicNumber": 46,
              "addH": True,
              "color": "#006985",
              "covalentRadius": 1.39,
              "vdWRadius": 1.79,
              "valency": 10,
              "mass": 106
            },
            "Ag": {
              "symbol": "Ag",
              "name": "Silver",
              "atomicNumber": 47,
              "addH": True,
              "color": "#C0C0C0",
              "covalentRadius": 1.45,
              "vdWRadius": 1.75,
              "valency": 11,
              "mass": 108
            },
            "Cd": {
              "symbol": "Cd",
              "name": "Cadmium",
              "atomicNumber": 48,
              "addH": True,
              "color": "#FFD98F",
              "covalentRadius": 1.44,
              "vdWRadius": 1.71,
              "valency": 12,
              "mass": 112
            },
            "In": {
              "symbol": "In",
              "name": "Indium",
              "atomicNumber": 49,
              "addH": True,
              "color": "#A67573",
              "covalentRadius": 1.42,
              "vdWRadius": 1.66,
              "valency": 13,
              "mass": 115
            },
            "Sn": {
              "symbol": "Sn",
              "name": "Tin",
              "atomicNumber": 50,
              "addH": True,
              "color": "#668080",
              "covalentRadius": 1.39,
              "vdWRadius": 1.62,
              "valency": 14,
              "mass": 119
            },
            "Sb": {
              "symbol": "Sb",
              "name": "Antimony",
              "atomicNumber": 51,
              "addH": True,
              "color": "#9E63B5",
              "covalentRadius": 1.39,
              "vdWRadius": 1.59,
              "valency": 15,
              "mass": 122
            },
            "Te": {
              "symbol": "Te",
              "name": "Tellurium",
              "atomicNumber": 52,
              "addH": True,
              "color": "#D47A00",
              "covalentRadius": 1.38,
              "vdWRadius": 1.57,
              "valency": 16,
              "mass": 128
            },
            "I": {
              "symbol": "I",
              "name": "Iodine",
              "atomicNumber": 53,
              "addH": True,
              "color": "#940094",
              "covalentRadius": 1.39,
              "vdWRadius": 1.56,
              "valency": 17,
              "mass": 127
            },
            "Xe": {
              "symbol": "Xe",
              "name": "Xenon",
              "atomicNumber": 54,
              "addH": False,
              "color": "#429EB0",
              "covalentRadius": 1.4,
              "vdWRadius": 2.16,
              "valency": 18,
              "mass": 131
            },
            "Cs": {
              "symbol": "Cs",
              "name": "Cesium",
              "atomicNumber": 55,
              "addH": True,
              "color": "#57178F",
              "covalentRadius": 2.44,
              "vdWRadius": 3.43,
              "valency": 1,
              "mass": 133
            },
            "Ba": {
              "symbol": "Ba",
              "name": "Barium",
              "atomicNumber": 56,
              "addH": True,
              "color": "#00C900",
              "covalentRadius": 2.15,
              "vdWRadius": 2.68,
              "valency": 2,
              "mass": 137
            },
            "La": {
              "symbol": "La",
              "name": "Lanthanum",
              "atomicNumber": 57,
              "addH": True,
              "color": "#70D4FF",
              "covalentRadius": 2.07,
              "vdWRadius": 2.57,
              "valency": 3,
              "mass": 139
            },
            "Ce": {
              "symbol": "Ce",
              "name": "Cerium",
              "atomicNumber": 58,
              "addH": True,
              "color": "#FFFFC7",
              "covalentRadius": 2.04,
              "vdWRadius": 2.58,
              "valency": 4,
              "mass": 140
            },
            "Pr": {
              "symbol": "Pr",
              "name": "Praseodymium",
              "atomicNumber": 59,
              "addH": True,
              "color": "#D9FFC7",
              "covalentRadius": 2.03,
              "vdWRadius": 2.47,
              "valency": 3,
              "mass": 141
            },
            "Nd": {
              "symbol": "Nd",
              "name": "Neodymium",
              "atomicNumber": 60,
              "addH": True,
              "color": "#C7FFC7",
              "covalentRadius": 2.01,
              "vdWRadius": 2.49,
              "valency": 3,
              "mass": 144
            },
            "Pm": {
              "symbol": "Pm",
              "name": "Promethium",
              "atomicNumber": 61,
              "addH": True,
              "color": "#A3FFC7",
              "covalentRadius": 1.99,
              "vdWRadius": 2.43,
              "valency": 3,
              "mass": 145
            },
            "Sm": {
              "symbol": "Sm",
              "name": "Samarium",
              "atomicNumber": 62,
              "addH": True,
              "color": "#8FFFC7",
              "covalentRadius": 1.98,
              "vdWRadius": 2.46,
              "valency": 3,
              "mass": 150
            },
            "Eu": {
              "symbol": "Eu",
              "name": "Europium",
              "atomicNumber": 63,
              "addH": True,
              "color": "#61FFC7",
              "covalentRadius": 1.98,
              "vdWRadius": 2.4,
              "valency": 3,
              "mass": 152
            },
            "Gd": {
              "symbol": "Gd",
              "name": "Gadolinium",
              "atomicNumber": 64,
              "addH": True,
              "color": "#45FFC7",
              "covalentRadius": 1.96,
              "vdWRadius": 2.38,
              "valency": 3,
              "mass": 157
            },
            "Tb": {
              "symbol": "Tb",
              "name": "Terbium",
              "atomicNumber": 65,
              "addH": True,
              "color": "#30FFC7",
              "covalentRadius": 1.94,
              "vdWRadius": 2.33,
              "valency": 3,
              "mass": 159
            },
            "Dy": {
              "symbol": "Dy",
              "name": "Dysprosium",
              "atomicNumber": 66,
              "addH": True,
              "color": "#1FFFC7",
              "covalentRadius": 1.92,
              "vdWRadius": 2.31,
              "valency": 3,
              "mass": 163
            },
            "Ho": {
              "symbol": "Ho",
              "name": "Holmium",
              "atomicNumber": 67,
              "addH": True,
              "color": "#00FF9C",
              "covalentRadius": 1.92,
              "vdWRadius": 2.33,
              "valency": 3,
              "mass": 165
            },
            "Er": {
              "symbol": "Er",
              "name": "Erbium",
              "atomicNumber": 68,
              "addH": True,
              "color": "#00E675",
              "covalentRadius": 1.89,
              "vdWRadius": 2.31,
              "valency": 3,
              "mass": 167
            },
            "Tm": {
              "symbol": "Tm",
              "name": "Thulium",
              "atomicNumber": 69,
              "addH": True,
              "color": "#00D452",
              "covalentRadius": 1.9,
              "vdWRadius": 2.33,
              "valency": 3,
              "mass": 169
            },
            "Yb": {
              "symbol": "Yb",
              "name": "Ytterbium",
              "atomicNumber": 70,
              "addH": True,
              "color": "#00BF38",
              "covalentRadius": 1.87,
              "vdWRadius": 2.32,
              "valency": 3,
              "mass": 173
            },
            "Lu": {
              "symbol": "Lu",
              "name": "Lutetium",
              "atomicNumber": 71,
              "addH": True,
              "color": "#00AB24",
              "covalentRadius": 1.87,
              "vdWRadius": 2.25,
              "valency": 3,
              "mass": 175
            },
            "Hf": {
              "symbol": "Hf",
              "name": "Hafnium",
              "atomicNumber": 72,
              "addH": True,
              "color": "#4DC2FF",
              "covalentRadius": 1.75,
              "vdWRadius": 2.16,
              "valency": 4,
              "mass": 178
            },
            "Ta": {
              "symbol": "Ta",
              "name": "Tantalum",
              "atomicNumber": 73,
              "addH": True,
              "color": "#4DA6FF",
              "covalentRadius": 1.7,
              "vdWRadius": 2.09,
              "valency": 5,
              "mass": 181
            },
            "W": {
              "symbol": "W",
              "name": "Tungsten",
              "atomicNumber": 74,
              "addH": True,
              "color": "#2194D6",
              "covalentRadius": 1.62,
              "vdWRadius": 2.02,
              "valency": 6,
              "mass": 184
            },
            "Re": {
              "symbol": "Re",
              "name": "Rhenium",
              "atomicNumber": 75,
              "addH": True,
              "color": "#267DAB",
              "covalentRadius": 1.51,
              "vdWRadius": 1.96,
              "valency": 7,
              "mass": 186
            },
            "Os": {
              "symbol": "Os",
              "name": "Osmium",
              "atomicNumber": 76,
              "addH": True,
              "color": "#266696",
              "covalentRadius": 1.44,
              "vdWRadius": 1.9,
              "valency": 8,
              "mass": 190
            },
            "Ir": {
              "symbol": "Ir",
              "name": "Iridium",
              "atomicNumber": 77,
              "addH": True,
              "color": "#175487",
              "covalentRadius": 1.41,
              "vdWRadius": 1.83,
              "valency": 9,
              "mass": 192
            },
            "Pt": {
              "symbol": "Pt",
              "name": "Platinum",
              "atomicNumber": 78,
              "addH": True,
              "color": "#D0D0E0",
              "covalentRadius": 1.36,
              "vdWRadius": 1.79,
              "valency": 10,
              "mass": 195
            },
            "Au": {
              "symbol": "Au",
              "name": "Gold",
              "atomicNumber": 79,
              "addH": True,
              "color": "#FFD123",
              "covalentRadius": 1.36,
              "vdWRadius": 1.75,
              "valency": 11,
              "mass": 197
            },
            "Hg": {
              "symbol": "Hg",
              "name": "Mercury",
              "atomicNumber": 80,
              "addH": True,
              "color": "#B8B8D0",
              "covalentRadius": 1.32,
              "vdWRadius": 1.71,
              "valency": 12,
              "mass": 201
            },
            "Tl": {
              "symbol": "Tl",
              "name": "Thallium",
              "atomicNumber": 81,
              "addH": True,
              "color": "#A6544D",
              "covalentRadius": 1.45,
              "vdWRadius": 1.56,
              "valency": 13,
              "mass": 204
            },
            "Pb": {
              "symbol": "Pb",
              "name": "Lead",
              "atomicNumber": 82,
              "addH": True,
              "color": "#575961",
              "covalentRadius": 1.46,
              "vdWRadius": 1.54,
              "valency": 14,
              "mass": 207
            },
            "Bi": {
              "symbol": "Bi",
              "name": "Bismuth",
              "atomicNumber": 83,
              "addH": True,
              "color": "#9E4FB5",
              "covalentRadius": 1.48,
              "vdWRadius": 1.51,
              "valency": 15,
              "mass": 208
            },
            "Po": {
              "symbol": "Po",
              "name": "Polonium",
              "atomicNumber": 84,
              "addH": True,
              "color": "#AB5C00",
              "covalentRadius": 1.4,
              "vdWRadius": 1.5,
              "valency": 16,
              "mass": 209
            },
            "At": {
              "symbol": "At",
              "name": "Astatine",
              "atomicNumber": 85,
              "addH": True,
              "color": "#754F45",
              "covalentRadius": 1.5,
              "vdWRadius": 1.62,
              "valency": 17,
              "mass": 210
            },
            "Rn": {
              "symbol": "Rn",
              "name": "Radon",
              "atomicNumber": 86,
              "addH": False,
              "color": "#428296",
              "covalentRadius": 1.5,
              "vdWRadius": 2.2,
              "valency": 18,
              "mass": 222
            },
            "Fr": {
              "symbol": "Fr",
              "name": "Francium",
              "atomicNumber": 87,
              "addH": True,
              "color": "#420066",
              "covalentRadius": 2.6,
              "vdWRadius": 3.48,
              "valency": 1,
              "mass": 223
            },
            "Ra": {
              "symbol": "Ra",
              "name": "Radium",
              "atomicNumber": 88,
              "addH": True,
              "color": "#007D00",
              "covalentRadius": 2.21,
              "vdWRadius": 2.83,
              "valency": 2,
              "mass": 226
            },
            "Ac": {
              "symbol": "Ac",
              "name": "Actinium",
              "atomicNumber": 89,
              "addH": True,
              "color": "#70ABFA",
              "covalentRadius": 2.15,
              "vdWRadius": 2.835,
              "valency": 3,
              "mass": 227
            },
            "Th": {
              "symbol": "Th",
              "name": "Thorium",
              "atomicNumber": 90,
              "addH": True,
              "color": "#00BAFF",
              "covalentRadius": 2.06,
              "vdWRadius": 2.81,
              "valency": 4,
              "mass": 232
            },
            "Pa": {
              "symbol": "Pa",
              "name": "Protactinium",
              "atomicNumber": 91,
              "addH": True,
              "color": "#00A1FF",
              "covalentRadius": 2,
              "vdWRadius": 2.82,
              "valency": 5,
              "mass": 231
            },
            "U": {
              "symbol": "U",
              "name": "Uranium",
              "atomicNumber": 92,
              "addH": True,
              "color": "#008FFF",
              "covalentRadius": 1.96,
              "vdWRadius": 2.82,
              "valency": 6,
              "mass": 238
            },
            "Np": {
              "symbol": "Np",
              "name": "Neptunium",
              "atomicNumber": 93,
              "addH": True,
              "color": "#0080FF",
              "covalentRadius": 1.9,
              "vdWRadius": 2.81,
              "valency": 7,
              "mass": 237
            },
            "Pu": {
              "symbol": "Pu",
              "name": "Plutonium",
              "atomicNumber": 94,
              "addH": True,
              "color": "#006BFF",
              "covalentRadius": 1.87,
              "vdWRadius": 2.84,
              "valency": 8,
              "mass": 244
            },
            "Am": {
              "symbol": "Am",
              "name": "Americium",
              "atomicNumber": 95,
              "addH": True,
              "color": "#545CF2",
              "covalentRadius": 1.8,
              "vdWRadius": 2.83,
              "valency": 3,
              "mass": 243
            },
            "Cm": {
              "symbol": "Cm",
              "name": "Curium",
              "atomicNumber": 96,
              "addH": True,
              "color": "#785CE3",
              "covalentRadius": 1.69,
              "vdWRadius": 2.8,
              "valency": 3,
              "mass": 247
            },
            "Bk": {
              "symbol": "Bk",
              "name": "Berkelium",
              "atomicNumber": 97,
              "addH": True,
              "color": "#8A4FE3",
              "covalentRadius": 1.69,
              "vdWRadius": 2.8,
              "valency": 3,
              "mass": 247
            },
            "Cf": {
              "symbol": "Cf",
              "name": "Californium",
              "atomicNumber": 98,
              "addH": True,
              "color": "#A136D4",
              "covalentRadius": 1.68,
              "vdWRadius": 2.8,
              "valency": 3,
              "mass": 251
            },
            "Es": {
              "symbol": "Es",
              "name": "Einsteinium",
              "atomicNumber": 99,
              "addH": True,
              "color": "#B31FD4",
              "covalentRadius": 1.65,
              "vdWRadius": 2.8,
              "valency": 3,
              "mass": 252
            },
            "Fm": {
              "symbol": "Fm",
              "name": "Fermium",
              "atomicNumber": 100,
              "addH": True,
              "color": "#B31FBA",
              "covalentRadius": 1.67,
              "vdWRadius": 2.8,
              "valency": 3,
              "mass": 257
            },
            "Md": {
              "symbol": "Md",
              "name": "Mendelevium",
              "atomicNumber": 101,
              "addH": True,
              "color": "#B30DA6",
              "covalentRadius": 1.73,
              "vdWRadius": 2.8,
              "valency": 3,
              "mass": 258
            },
            "No": {
              "symbol": "No",
              "name": "Nobelium",
              "atomicNumber": 102,
              "addH": True,
              "color": "#BD0D87",
              "covalentRadius": 1.76,
              "vdWRadius": 2.8,
              "valency": 3,
              "mass": 259
            },
            "Lr": {
              "symbol": "Lr",
              "name": "Lawrencium",
              "atomicNumber": 103,
              "addH": True,
              "color": "#C70066",
              "covalentRadius": 1.61,
              "vdWRadius": 2.7,
              "valency": 3,
              "mass": 262
            },
            "Rf": {
              "symbol": "Rf",
              "name": "Rutherfordium",
              "atomicNumber": 104,
              "addH": True,
              "color": "#CC0059",
              "covalentRadius": 1.57,
              "vdWRadius": 2.5,
              "valency": 4,
              "mass": 267
            },
            "Db": {
              "symbol": "Db",
              "name": "Dubnium",
              "atomicNumber": 105,
              "addH": True,
              "color": "#D1004F",
              "covalentRadius": 1.49,
              "vdWRadius": 2.4,
              "valency": 5,
              "mass": 270
            },
            "Sg": {
              "symbol": "Sg",
              "name": "Seaborgium",
              "atomicNumber": 106,
              "addH": True,
              "color": "#D90045",
              "covalentRadius": 1.43,
              "vdWRadius": 2.3,
              "valency": 6,
              "mass": 271
            },
            "Bh": {
              "symbol": "Bh",
              "name": "Bohrium",
              "atomicNumber": 107,
              "addH": True,
              "color": "#E00038",
              "covalentRadius": 1.41,
              "vdWRadius": 2.25,
              "valency": 7,
              "mass": 270
            },
            "Hs": {
              "symbol": "Hs",
              "name": "Hassium",
              "atomicNumber": 108,
              "addH": True,
              "color": "#E6002E",
              "covalentRadius": 1.34,
              "vdWRadius": 2.2,
              "valency": 8,
              "mass": 277
            },
            "Mt": {
              "symbol": "Mt",
              "name": "Meitnerium",
              "atomicNumber": 109,
              "addH": True,
              "color": "#EB0026",
              "covalentRadius": 1.29,
              "vdWRadius": 2.1,
              "valency": 9,
              "mass": 278
            },
            "Ds": {
              "symbol": "Ds",
              "name": "Darmstadtium",
              "atomicNumber": 110,
              "addH": True,
              "color": "#EE0026",
              "covalentRadius": 1.28,
              "vdWRadius": 2.1,
              "valency": 10,
              "mass": 281
            },
            "Rg": {
              "symbol": "Rg",
              "name": "Roentgenium",
              "atomicNumber": 111,
              "addH": True,
              "color": "#F10014",
              "covalentRadius": 1.21,
              "vdWRadius": 2.05,
              "valency": 11,
              "mass": 282
            },
            "Cn": {
              "symbol": "Cn",
              "name": "Copernicium",
              "atomicNumber": 112,
              "addH": True,
              "color": "#F60002",
              "covalentRadius": 1.22,
              "vdWRadius": 2,
              "valency": 12,
              "mass": 285
            },
            "Nh": {
              "symbol": "Nh",
              "name": "Nihonium",
              "atomicNumber": 113,
              "addH": True,
              "color": "#FF4F00",
              "covalentRadius": 1.36,
              "vdWRadius": 2,
              "valency": 13,
              "mass": 286
            },
            "Fl": {
              "symbol": "Fl",
              "name": "Flerovium",
              "atomicNumber": 114,
              "addH": True,
              "color": "#FF7000",
              "covalentRadius": 1.42,
              "vdWRadius": 2,
              "valency": 14,
              "mass": 289
            },
            "Mc": {
              "symbol": "Mc",
              "name": "Moscovium",
              "atomicNumber": 115,
              "addH": True,
              "color": "#FF8C00",
              "covalentRadius": 1.47,
              "vdWRadius": 2,
              "valency": 15,
              "mass": 290
            },
            "Lv": {
              "symbol": "Lv",
              "name": "Livermorium",
              "atomicNumber": 116,
              "addH": True,
              "color": "#FFA100",
              "covalentRadius": 1.6,
              "vdWRadius": 2,
              "valency": 16,
              "mass": 293
            },
            "Ts": {
              "symbol": "Ts",
              "name": "Tennessine",
              "atomicNumber": 117,
              "addH": True,
              "color": "#FFBA00",
              "covalentRadius": 1.6,
              "vdWRadius": 2,
              "valency": 17,
              "mass": 294
            },
            "Og": {
              "symbol": "Og",
              "name": "Oganesson",
              "atomicNumber": 118,
              "addH": True,
              "color": "#FFD100",
              "covalentRadius": 1.6,
              "vdWRadius": 2,
              "valency": 18,
              "mass": 294
            }
        }
        return data[typeSymbol][key]
