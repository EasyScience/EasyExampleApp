# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json
import copy
import re
import random
import numpy as np
from PySide6.QtCore import QObject, Signal, Slot, Property

from EasyApp.Logic.Logging import console
from Logic.Calculators import GaussianCalculator
from Logic.Fittables import Parameter
from Logic.Helpers import Converter, IO, PERIODIC_TABLE
from Logic.Data import Data

try:
    import cryspy
    from cryspy.H_functions_global.function_1_cryspy_objects import \
        file_to_globaln, str_to_globaln
    from cryspy.A_functions_base.database import DATABASE
    from cryspy.A_functions_base.function_2_space_group import \
        get_it_coordinate_system_codes_by_it_number, \
        REFERENCE_TABLE_IT_COORDINATE_SYSTEM_CODE_NAME_HM_EXTENDED, \
        REFERENCE_TABLE_IT_NUMBER_NAME_HM_FULL, \
        ACCESIBLE_NAME_HM_SHORT

    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_calc_chi_sq_by_dictionary
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')

_DEFAULT_DATA_BLOCK = """data_default

_space_group_name_H-M_alt "P b n m"

_cell_length_a 10
_cell_length_b 6
_cell_length_c 5
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
_atom_site_adp_type
_atom_site_B_iso_or_equiv
C C 0 0 0 1 Biso 0
"""


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
        self._dataBlocksCif = []
        self._yCalcArrays = []
        self._yBkgArrays = []

        self._structViewAtomsModel = []
        self._structViewCellModel = []
        self._structViewAxesModel = []

        self._spaceGroupDict = {}
        self._spaceGroupNames = self.createSpaceGroupNames()
        self._isotopesNames = self.createIsotopesNames()

    def createSpaceGroupNames(self):
        names_short = ACCESIBLE_NAME_HM_SHORT
        names_full = tuple((_[1] for _ in REFERENCE_TABLE_IT_NUMBER_NAME_HM_FULL))
        names_extended = tuple((_[2] for _ in REFERENCE_TABLE_IT_COORDINATE_SYSTEM_CODE_NAME_HM_EXTENDED))
        return list(set(names_short + names_full + names_extended))

    def createIsotopesNames(self):
        return [_[1] for _ in list(DATABASE['Isotopes'].keys())]

    # QML accessible properties

    @Property('QVariant', constant=True)
    def spaceGroupNames(self):
        return self._spaceGroupNames

    @Property('QVariant', constant=True)
    def isotopesNames(self):
        return self._isotopesNames

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

    @Property('QVariant', notify=dataBlocksCifChanged)
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

    @Slot(str, str, result=str)
    def atomData(self, typeSymbol, key):
        if typeSymbol == '':
            return ''
        typeSymbol = re.sub(r'[0-9]', '', typeSymbol)  # '162Dy' -> 'Dy'
        return PERIODIC_TABLE[typeSymbol][key]

    @Slot()
    def addDefaultModel(self):
        console.debug("Adding default model")
        self.loadModelFromEdCif(_DEFAULT_DATA_BLOCK)

    @Slot(str)
    def loadModelFromFile(self, fpath):
        fpath = IO.generalizePath(fpath)
        console.debug(f"Loading model from: {fpath}")
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

    @Slot(str, str, 'QVariant')
    def setMainParamWithFullUpdate(self, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(paramName, field, value)
        if not changedIntern:
            return
        self.createCryspyDictFromDataBlocks()

    @Slot(str, str, 'QVariant')
    def setMainParam(self, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(paramName, field, value)
        changedCryspy = self.editCryspyDictByMainParam(paramName, field, value)

        if changedIntern and changedCryspy:
            self.dataBlocksChanged.emit()

    @Slot(str, str, int, str, 'QVariant')
    def setLoopParamWithFullUpdate(self, loopName, paramName, rowIndex, field, value):
        changedIntern = self.editDataBlockLoopParam(loopName, paramName, rowIndex, field, value)
        if not changedIntern:
            return
        self.createCryspyDictFromDataBlocks()

    @Slot(str, str, int, str, 'QVariant')
    def setLoopParam(self, loopName, paramName, rowIndex, field, value):
        changedIntern = self.editDataBlockLoopParam(loopName, paramName, rowIndex, field, value)
        changedCryspy = self.editCryspyDictByLoopParam(loopName, paramName, rowIndex, field, value)

        if changedIntern and changedCryspy:
            self.dataBlocksChanged.emit()

    @Slot(str, int)
    def removeLoopRow(self, loopName, rowIndex):
        self.removeDataBlockLoopRow(loopName, rowIndex)
        self.createCryspyDictFromDataBlocks()

    @Slot(str)
    def appendLoopRow(self, loopName):
        self.appendDataBlockLoopRow(loopName)
        self.createCryspyDictFromDataBlocks()

    @Slot(str, int)
    def duplicateLoopRow(self, loopName, idx):
        self.duplicateDataBlockLoopRow(loopName, idx)
        self.createCryspyDictFromDataBlocks()

    # Private methods

    def appendDataBlockLoopRow(self, loopName):
        block = 'model'
        blockIndex = self._currentIndex

        lastAtom = self._dataBlocks[blockIndex]['loops'][loopName][-1]

        newAtom = copy.deepcopy(lastAtom)
        newAtom['_label']['value'] = random.choice(self.isotopesNames)
        newAtom['_type_symbol']['value'] = newAtom['_label']['value']
        newAtom['_fract_x']['value'] = random.uniform(0, 1)
        newAtom['_fract_y']['value'] = random.uniform(0, 1)
        newAtom['_fract_z']['value'] = random.uniform(0, 1)
        newAtom['_occupancy']['value'] = 1
        newAtom['_B_iso_or_equiv']['value'] = 0

        self._dataBlocks[blockIndex]['loops'][loopName].append(newAtom)
        atomsCount = len(self._dataBlocks[blockIndex]['loops'][loopName])

        console.debug(f"Intern dict ▌ {block}[{blockIndex}].{loopName}[{atomsCount}] has been added")

    def duplicateDataBlockLoopRow(self, loopName, idx):
        block = 'model'
        blockIndex = self._currentIndex

        lastAtom = self._dataBlocks[blockIndex]['loops'][loopName][idx]

        self._dataBlocks[blockIndex]['loops'][loopName].append(lastAtom)
        atomsCount = len(self._dataBlocks[blockIndex]['loops'][loopName])

        console.debug(f"Intern dict ▌ {block}[{blockIndex}].{loopName}[{atomsCount}] has been added")

    def removeDataBlockLoopRow(self, loopName, rowIndex):
        block = 'model'
        blockIndex = self._currentIndex
        del self._dataBlocks[blockIndex]['loops'][loopName][rowIndex]

        console.debug(f"Intern dict ▌ {block}[{blockIndex}].{loopName}[{rowIndex}] has been removed")

    def editDataBlockMainParam(self, paramName, field, value, blockIndex=None):
        block = 'model'
        if blockIndex is None:
            blockIndex = self._currentIndex

        oldValue = self._dataBlocks[blockIndex]['params'][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocks[blockIndex]['params'][paramName][field] = value

        console.debug(f"Intern dict ▌ {oldValue} → {value} ▌ {block}[{blockIndex}].{paramName}.{field}")
        return True

    def editDataBlockLoopParam(self, loopName, paramName, rowIndex, field, value, blockIndex=None):
        block = 'model'
        if blockIndex is None:
            blockIndex = self._currentIndex

        oldValue = self._dataBlocks[blockIndex]['loops'][loopName][rowIndex][paramName][field]
        if oldValue == value:
            return False
        self._dataBlocks[blockIndex]['loops'][loopName][rowIndex][paramName][field] = value

        console.debug(f"Intern dict ▌ {oldValue} → {value} ▌ {block}[{blockIndex}].{loopName}[{rowIndex}].{paramName}.{field}")
        return True

    def createCryspyDictFromDataBlocks(self):
        console.debug("Cryspy dict need to be recreated")

        # remove model from self._proxy.data._cryspyDict
        currentModelName = self.dataBlocks[self.currentIndex]['name']
        del self._proxy.data._cryspyDict[f'crystal_{currentModelName}']

        # add model to self._proxy.data._cryspyDict
        edCif = Converter.dataBlocksToCif(self._dataBlocks)
        self.loadModelFromEdCif(edCif)

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

        # if 'flags' objects are needed
        if field == 'fit':
            path[1] = f'flags_{path[1]}'

        return path, value

    def cryspyDictPathByLoopParam(self, loopName, paramName, rowIndex, field, value):
        blockIndex = self._currentIndex
        blockName = self._dataBlocks[blockIndex]['name']
        path = ['','','']
        path[0] = f"crystal_{blockName}"

        # _atom_site
        if loopName == '_atom_site':
            if paramName == '_fract_x':
                path[1] = 'atom_fract_xyz'
                path[2] = (0, rowIndex)
            elif paramName == '_fract_y':
                path[1] = 'atom_fract_xyz'
                path[2] = (1, rowIndex)
            elif paramName == '_fract_z':
                path[1] = 'atom_fract_xyz'
                path[2] = (2, rowIndex)
            elif paramName == '_occupancy':
                path[1] = 'atom_occupancy'
                path[2] = rowIndex
            elif paramName == '_B_iso_or_equiv':
                path[1] = 'atom_b_iso'
                path[2] = rowIndex

        # if 'flags' objects are needed
        if field == 'fit':
            path[1] = f'flags_{path[1]}'

        return path, value

    def editDataBlockByCryspyDictParams(self, params):
        for param in params:
            block, group, idx = Data.strToCryspyDictParamPath(param)

            # crystal block
            if block.startswith('crystal_'):
                blockName = block[8:]
                loopName = None
                paramName = None
                rowIndex = None
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
                    rowIndex = idx[1]
                    if idx[0] == 0:
                        paramName = '_fract_x'
                    elif idx[0] == 1:
                        paramName = '_fract_y'
                    elif idx[0] == 2:
                        paramName = '_fract_z'

                # atom_occupancy
                elif group == 'atom_occupancy':
                    loopName = '_atom_site'
                    rowIndex = idx[0]
                    paramName = '_occupancy'

                # b_iso_or_equiv
                elif group == 'atom_b_iso':
                    loopName = '_atom_site'
                    rowIndex = idx[0]
                    paramName = '_B_iso_or_equiv'

                value = float(value)  # convert float64 to float (needed for QML access)
                blockIndex = [block['name'] for block in self._dataBlocks].index(blockName)

                if loopName is None:
                    self.editDataBlockMainParam(paramName, 'value', value, blockIndex)
                else:
                    self.editDataBlockLoopParam(loopName, paramName, rowIndex, 'value', value, blockIndex)

    def defaultYCalcArray(self):
        xArray = self._proxy.experiment._xArrays[0]  # NEED FIX
        params = _DEFAULT_DATA_BLOCK['params']
        yCalcArray = GaussianCalculator.calculated(xArray, params)
        return yCalcArray

    def calculateYCalcArray(self, index):
        # Re-calculate diffraction pattern
        yCalcArray = self.calculateDiffractionPattern()
        return yCalcArray

    def updateYCalcArrayByIndex(self, index):
        if index < len(self._yCalcArrays):
            self._yCalcArrays[index] = self.calculateYCalcArray(index)
        else:
            self._yCalcArrays.append(self.calculateYCalcArray(index))
        console.debug(f" - Pattern for model no. {index + 1} has been calculated")
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
        console.debug(f" - Y-calculated data for model data block no. {len(self._dataBlocks)} has been added to intern dataset")
        self.yCalcArraysChanged.emit()

    #def calculateAllYArrays(self):
    #    for i in range(len(self._dataBlocks)):
    #        self.calculateSingleYArray(i)

    #def scaleSingleDataBlock(self, index):
    #    scale = self._proxy.experiment.models[index]['scale']
    #    self._yCalcArrays[index]['yArray'] *= scale
    #    self.calculatedDataChanged.emit()

    def setDataBlocksCif(self):
        self._dataBlocksCif = [Converter.dataBlocksToCif([block]) for block in self._dataBlocks]
        console.debug(" - Model dataBlocks have been converted to CIF string")
        self.dataBlocksCifChanged.emit()

    # Extract phases from cryspy_obj and cryspy_dict into internal ed_dict
    def parseModels(self, cryspy_obj):
        cryspy_dict = self._proxy.data._cryspyDict
        phase_names = [name.replace('crystal_', '') for name in cryspy_dict.keys() if name.startswith('crystal_')]

        for data_block in cryspy_obj.items:
            data_block_name = data_block.data_name

            # Phase datablock
            if data_block_name in phase_names:

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
                            prettyName = 'name',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core'
                        ))
                        ed_phase['params']['_space_group_IT_coordinate_system_code'] = dict(Parameter(
                            item.it_coordinate_system_code,
                            permittedValues = list(get_it_coordinate_system_codes_by_it_number(item.it_number)),
                            name = '_space_group_IT_coordinate_system_code',
                            prettyName = 'code',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core'
                        ))
                        ed_phase['params']['_space_group_crystal_system'] = dict(Parameter(
                            item.crystal_system,
                            name = '_space_group_crystal_system',
                            prettyName = 'crystal system',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core',
                            optional = True
                        ))
                        ed_phase['params']['_space_group_IT_number'] = dict(Parameter(
                            item.it_number,
                            name = '_space_group_IT_number',
                            prettyName = 'number',
                            url = 'https://easydiffraction.org',
                            cifDict = 'core',
                            optional = True
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
                                rowName = cryspy_atom.label,
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
                                rowName = cryspy_atom.label,
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
                                rowName = cryspy_atom.label,
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
                                rowName = cryspy_atom.label,
                                name = '_occupancy',
                                prettyName = 'occ',
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
                                rowName = cryspy_atom.label,
                                name = '_B_iso_or_equiv',
                                prettyName = 'iso',
                                url = 'https://easydiffraction.org',
                                cifDict = 'core',
                                enabled = not cryspy_atom.b_iso_or_equiv_constraint,
                                min = 0,
                                max = 1,
                                units = 'Å²',
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

                self.addDataBlock(ed_phase)

    def calculateDiffractionPattern(self):
        self._proxy.fitting.chiSq, self._proxy.fitting._pointsCount, _, _, paramNames = rhochi_calc_chi_sq_by_dictionary(self._proxy.data._cryspyDict,
            dict_in_out=self._proxy.data._cryspyInOutDict,
            flag_use_precalculated_data=False,
            flag_calc_analytical_derivatives=False)
        first_experiment_name = self._proxy.data.edDict['experiments'][0]['name']  # NEED FIX
        y_calc_array = self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['signal_minus'] + self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['signal_plus']

        #################self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['dict_in_out_co2sio4']['ttheta_hkl']
        self._proxy.experiment._yBkgArrays[0] = self._proxy.data._cryspyInOutDict[f'pd_{first_experiment_name}']['signal_background']  # NEED FIX

        reducedGofLastIter = self._proxy.fitting.chiSq / self._proxy.fitting._pointsCount            # NEED FIX
        if self._proxy.fitting._chiSqStart is None:
            self._proxy.status.goodnessOfFit = f'{reducedGofLastIter:0.2f}'                           # NEED move to connection
        else:
            reducedGofStart = self._proxy.fitting._chiSqStart / self._proxy.fitting._pointsCount      # NEED FIX
            self._proxy.status.goodnessOfFit = f'{reducedGofStart:0.2f} → {reducedGofLastIter:0.2f}'  # NEED move to connection
            if not self._proxy.fitting._freezeChiSqStart:
                self._proxy.fitting._chiSqStart = self._proxy.fitting.chiSq

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
        console.debug(f" - Structure view atoms for model no. {self._currentIndex + 1} has been set. Atoms count: {len(atoms)}")
        self.structViewAtomsModelChanged.emit()
