# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>


from pycifstar.global_ import Global

from EasyApp.Logic.Logging import console

try:
    import cryspy
    from cryspy.A_functions_base.function_2_space_group import \
        get_it_coordinate_system_codes_by_it_number
    console.debug('CrysPy module imported')
except ImportError:
    console.error('No CrysPy module found')


class Parameter(dict):

    def __init__(self,
                value,
                permittedValues = None,
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
                optional = False,
                enabled = True,
                fittable = False,
                fit = False):
        self['value'] = value
        self['permittedValues'] = permittedValues
        self['idx'] = idx
        self['optional'] = optional
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


class CryspyParser:

    @staticmethod
    def cifToDict(cif):
        obj = Global()
        obj.take_from_string(cif)
        data = obj.datas[0]
        out = {'name': data.name, 'items': {}, 'loops': {}}
        for item in data.items.items:
            out['items'][item.name] = item.value
        for loop in data.loops:
            loopName = loop.prefix
            out['loops'][loopName] = {}
            for paramIdx, fullParamName in enumerate(loop.names):
                paramName = fullParamName.replace(loopName, '')
                paramValues = [values[paramIdx] for values in loop.values]
                out['loops'][loopName][paramName] = paramValues
        return out

    @staticmethod
    def dataBlocksToCif(blocks):
        cif = ''
        for block in blocks:
            cif += CryspyParser.dataBlockToCif(block) + '\n\n'
        return cif

    @staticmethod
    def dataBlockToCif(block, includeBlockName=True):
        cif = ''
        if includeBlockName:
            cif += f'data_{block["name"]}'
            cif += '\n\n'
        if 'params' in block:
            for name, param in block['params'].items():
                if param["optional"]:
                    continue
                value = param["value"]
                if value is None:
                    continue
                # convert
                if isinstance(value, float):
                    value = f'{round(value, 4):.8g}'  # 3.0 -> "3", 3.012345 -> "3.0123"
                elif isinstance(value, str) and ' ' in value:  # P n m a -> "P n m a"
                    value = f'"{value}"'
                # add brackets for free params
                if param["fit"]:
                    cif += f'{name} {value}()'
                else:
                    cif += f'{name} {value}'
                cif += '\n'
        if 'loops' in block:
            for loopName, loop in block['loops'].items():
                cif += '\n'
                cif += 'loop_'
                cif += '\n'
                # loop header
                for paramName in loop[0].keys():
                    cif += f'{loopName}{paramName}\n'
                # loop data
                for loopItem in loop:
                    line = ''
                    for param in loopItem.values():
                        value = param["value"]
                        # convert
                        if isinstance(value, float):
                            value = f'{round(value, 4):.8g}'  # 3.0 -> "3", 3.012345 -> "3.0123"
                        elif isinstance(value, str) and ' ' in value:  # P n m a -> "P n m a"
                            value = f'"{value}"'
                        # add brackets for free params
                        if param["fit"]:
                            line += f'{value}()'
                        else:
                            line += f'{value}'
                        line += ' '
                    cif += line
                    cif += '\n'
                #cif += '\n'
        cif = cif.strip()
        return cif

    @staticmethod
    def edCifToCryspyCif(edCif):
        cryspyCif = edCif
        edToCryspyNamesMap = {
            '_diffrn_radiation_probe': '_setup_radiation',
            '_diffrn_radiation_wavelength': '_setup_wavelength',
            '_pd_meas_2theta_offset': '_setup_offset_2theta',
            '_pd_meas_2theta_range_min': '_range_2theta_min',
            '_pd_meas_2theta_range_max': '_range_2theta_max'
        }
        edToCryspyValuesMap = {
            'neutron': 'neutrons',
            'x-ray': 'X-rays'
        }
        for edName, cryspyName in edToCryspyNamesMap.items():
            cryspyCif = cryspyCif.replace(edName, cryspyName)
        for edValue, cryspyValue in edToCryspyValuesMap.items():
            cryspyCif = cryspyCif.replace(edValue, cryspyValue)
        return cryspyCif

    @staticmethod
    def starObjToEdProject(starObj):
        edProject = {'name': starObj.name,
                     'params': {},
                     'loops': {}}

        for param in starObj.items.items:
            if param.name == '_description':
                edProject['params'][param.name] = dict(Parameter(
                    param.value,
                    name = param.name,
                    prettyName = 'Description',
                    url = 'https://easydiffraction.org',
                ))
            elif param.name == '_location':
                edProject['params'][param.name] = dict(Parameter(
                    param.value,
                    name = param.name,
                    prettyName = 'Location',
                    url = 'https://easydiffraction.org',
                ))
            elif param.name == '_date_created':
                edProject['params'][param.name] = dict(Parameter(
                    param.value,
                    name = param.name,
                    prettyName = 'Created',
                    url = 'https://easydiffraction.org',
                ))
            elif param.name == '_date_last_modified':
                edProject['params'][param.name] = dict(Parameter(
                    param.value,
                    name = param.name,
                    prettyName = 'Last modified',
                    url = 'https://easydiffraction.org',
                ))

        for loop in starObj.loops:
            loopName = loop.prefix

            if loopName == '_model':
                edModels = []
                for rowIdx, rowItems in enumerate(loop.values):
                    edModel = {}
                    for columnIdx, columnName in enumerate(loop.names):
                        paramName = columnName.replace(loopName, '')
                        if paramName == '_dir_name':
                            edModel[paramName] = dict(Parameter(
                                rowItems[columnIdx],
                                name=paramName,
                                prettyName='Model directory',
                                url='https://easydiffraction.org'
                            ))
                        elif paramName == '_cif_file_name':
                            edModel[paramName] = dict(Parameter(
                                rowItems[columnIdx],
                                name=paramName,
                                prettyName='Model file',
                                url='https://easydiffraction.org'
                            ))
                        elif paramName == '_jpg_file_name':
                            edModel[paramName] = dict(Parameter(
                                rowItems[columnIdx],
                                name=paramName,
                                url='https://easydiffraction.org'
                            ))
                    edModels.append(edModel)
                edProject['loops'][loopName] = edModels

            elif loopName == '_experiment':
                edExperiments = []
                for rowIdx, rowItems in enumerate(loop.values):
                    edExperiment = {}
                    for columnIdx, columnName in enumerate(loop.names):
                        paramName = columnName.replace(loopName, '')
                        if paramName == '_dir_name':
                            edExperiment[paramName] = dict(Parameter(
                                rowItems[columnIdx],
                                name=paramName,
                                prettyName='Experiment directory',
                                url='https://easydiffraction.org'
                            ))
                        elif paramName == '_cif_file_name':
                            edExperiment[paramName] = dict(Parameter(
                                rowItems[columnIdx],
                                name=paramName,
                                prettyName='Experiment file',
                                url='https://easydiffraction.org'
                            ))
                        elif paramName == '_jpg_file_name':
                            edExperiment[paramName] = dict(Parameter(
                                rowItems[columnIdx],
                                name=paramName,
                                url='https://easydiffraction.org'
                            ))
                    edExperiments.append(edExperiment)
                edProject['loops'][loopName] = edExperiments

        return edProject

    @staticmethod
    def cryspyObjAndDictToEdModels(cryspy_obj, cryspy_dict):
        phase_names = [name.replace('crystal_', '') for name in cryspy_dict.keys() if name.startswith('crystal_')]
        ed_phases = []

        for data_block in cryspy_obj.items:
            data_block_name = data_block.data_name

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

            ed_phases.append(ed_phase)

        return ed_phases

    @staticmethod
    def cryspyObjAndDictToEdExperiments(cryspy_obj, cryspy_dict):
        experiment_names = [name.replace('pd_', '') for name in cryspy_dict.keys() if name.startswith('pd_')]
        ed_experiments_meas_only = []
        ed_experiments = []

        for data_block in cryspy_obj.items:
            data_block_name = data_block.data_name

            if data_block_name in experiment_names:
                ed_experiment = {'name': data_block_name,
                                 'params': {},
                                 'loops': {}}
                ed_experiment_meas_only = {'name': data_block_name,
                                           'loops': {}}
                cryspy_experiment = data_block.items

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
                            permittedValues = ['neutron', 'x-ray'],
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

            ed_experiments_meas_only.append(ed_experiment_meas_only)
            ed_experiments.append(ed_experiment)

        return ed_experiments_meas_only, ed_experiments
