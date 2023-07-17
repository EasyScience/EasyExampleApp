# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import sys
import orjson
import argparse
from urllib.parse import urlparse
from pycifstar.global_ import Global
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, QCoreApplication

from EasyApp.Logic.Logging import console

try:
    import cryspy
    from cryspy.A_functions_base.function_2_space_group import \
        get_it_coordinate_system_codes_by_it_number
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')


class ResourcePaths:
    def __init__(self):
        self.mainQml = ''  # Current app main.qml file
        self.splashScreenQml = ''  # Splash screen .qml file
        self.imports = []  # EasyApp qml components (EasyApp/...) & Current app qml components (Gui/...)
        self.settings_ini = ''  # Persistent settings ini file location
        self.setPaths()

    def setPaths(self):

        console.debug('Trying to import python resources.py file with EasyApp')
        try:
            import resources
            console.info(f'Resources: {resources}')
            self.mainQml = 'qrc:/Gui/main.qml'
            self.splashScreenQml = 'qrc:/Gui/Components/SplashScreen.qml'
            self.imports = ['qrc:/EasyApp', 'qrc:/']
            return
        except ImportError:
            console.debug('No rc resources file has been found')

        console.debug('Trying to import the locally installed EasyApp module')
        try:
            import EasyApp
            easyAppPath = os.path.abspath(EasyApp.__path__[0])
            console.info(f'EasyApp: {easyAppPath}')
            self.mainQml = 'Gui/main.qml'
            self.splashScreenQml = 'Gui/Components/SplashScreen.qml'
            self.imports = [os.path.join(easyAppPath, '..'), '.']
            return
        except ImportError:
            console.debug('No EasyApp module is installed')

        console.error('No EasyApp module has been found')


class CommandLineArguments:

    def __new__(cls):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '-t',
            '--testmode',
            action='store_true',
            help='run the application in test mode: run tests, take screenshots and exit the application'
        )

        return parser.parse_args()


class EnvironmentVariables:

    @staticmethod
    def set():
        os.environ['QSG_RHI_BACKEND'] = 'opengl'  # For QtCharts XYSeries useOpenGL
        #os.environ['QT_MESSAGE_PATTERN'] = "\033[32m%{time h:mm:ss.zzz}%{if-category}\033[32m %{category}:%{endif} %{if-debug}\033[34m%{function}%{endif}%{if-warning}\033[31m%{backtrace depth=3}%{endif}%{if-critical}\033[31m%{backtrace depth=3}%{endif}%{if-fatal}\033[31m%{backtrace depth=3}%{endif}\033[0m %{message}"


class WebEngine:

    @staticmethod
    def initialize():
        try:
            from PySide6.QtWebEngineQuick import QtWebEngineQuick
        except ModuleNotFoundError:
            #console.debug('No module named "PySide6.QtWebEngineQuick" is found.')
            pass
        else:
            QtWebEngineQuick.initialize()

    @staticmethod
    def runJavaScriptWithoutCallback(webEngine, script):
        callback = None
        webEngine.runJavaScript(script, callback)


class IO:

    @staticmethod
    def generalizePath(fpath: str) -> str:
        """
        Generalize the filepath to be platform-specific, so all file operations
        can be performed.
        :param URI rcfPath: URI to the file
        :return URI filename: platform specific URI
        """
        filename = urlparse(fpath).path
        if not sys.platform.startswith("win"):
            return filename
        if filename[0] == '/':
            filename = filename[1:].replace('/', os.path.sep)
        return filename

    @staticmethod
    def formatMsg(type, *args):
        types = {'main': '•', 'sub': ' ◦'}
        mark = types[type]
        widths = [22,21,20,10]
        widths[0] -= len(mark)
        msgs = []
        for idx, arg in enumerate(args):
            msgs.append(f'{arg:<{widths[idx]}}')
        msg = ' ▌ '.join(msgs)
        msg = f'{mark} {msg}'
        return msg


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


class Converter:

    @staticmethod
    def jsStrToPyBool(value):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            #console.debug(f'Input value "{value}" is not supported. It should either be "true" or "false".')
            pass

    @staticmethod
    def dictToJson(obj):
        # Dump to json
        dumpOption = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2
        jsonBytes = orjson.dumps(obj, option=dumpOption)
        json = jsonBytes.decode()
        return json
        #if not formatted:
        #    return jsonStr
        ## Format to have arrays shown in one line. Can orjson do this?
        #formatOptions = jsbeautifier.default_options()
        #formatOptions.indent_size = 2
        #formattedJsonStr = jsbeautifier.beautify(jsonStr, formatOptions)
        #return formattedJsonStr


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



class Application(QApplication):  # QGuiApplication crashes when using in combination with QtCharts

    def __init__(self, sysArgv):
        super(Application, self).__init__(sysArgv)
        self.setApplicationName('EasyExample')
        self.setOrganizationName('EasyScience')
        self.setOrganizationDomain('easyscience.software')


class ExitHelper(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def exitApp(self, exitCode):
        console.debug(f'Force exiting application with code {exitCode}')
        os._exit(exitCode)


class PyProxyWorker(QObject):
    pyProxyExposedToQml = Signal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self._engine = engine

    def exposePyProxyToQml(self):
        import time
        time.sleep(0.5)
        console.debug('Slept for 0.5s to allow splash screen to start')
        from Logic.PyProxy import PyProxy
        mainThread = QCoreApplication.instance().thread()
        proxy = PyProxy()
        console.debug('PyProxy object has been created')
        proxy.moveToThread(mainThread)
        self._engine.rootContext().setContextProperty('pyProxy', proxy)
        self.pyProxyExposedToQml.emit()
        console.debug('PyProxy object has been exposed to QML')


PERIODIC_TABLE = {
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
