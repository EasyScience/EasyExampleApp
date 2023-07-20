# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json, jsbeautifier
from datetime import datetime
from pycifstar.global_ import  Global as PycifstarGlobal
from pycifstar.data import Data as PycifstarData
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from PySide6.QtQml import QJSValue

from EasyApp.Logic.Logging import console
from Logic.Helpers import IO, CryspyParser, Parameter

try:
    import cryspy
    from cryspy.H_functions_global.function_1_cryspy_objects import str_to_globaln
except ImportError:
    console.debug('No CrysPy module has been found')


_DEFAULT_CIF = """data_DefaultProject
_description 'Default project description'
_location ''
_date_created ''
_date_last_modified ''
"""

_EMPTY_DATA = {
    'name': '',
    'params': {},
    'loops': {}
}

_DEFAULT_DATA = {
    'name': 'Project name',
    'params': {
        '_description': { 'value': 'Project description' },
        '_location': { 'value': '' },
        '_date_created': { 'value': '' },
        '_date_last_modified': { 'value': '' }

    },
    'loops': {}
}

_EXAMPLES = [
    {
        'name': 'Co2SiO4',
        'description': 'neutrons, powder, constant wavelength, D20@ILL',
        'path': '../../../../../../examples/Co2SiO4/project.cif'

     },
    {
        'name': 'Co2SiO4-Mult',
        'description': 'neutrons, powder, constant wavelength, D20@ILL, 2 phases, 2 datasets',
        'path': '../../../../../../examples/Co2SiO4-Mult/project.cif'
    }
]

class Project(QObject):
    createdChanged = Signal()
    needSaveChanged = Signal()
    dataBlockChanged = Signal()
    dataBlockCifChanged = Signal()
    recentChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._dataBlock = self.createDataBlockFromCif(_DEFAULT_CIF)
        self._dataBlockCif = _DEFAULT_CIF
        self._examples = _EXAMPLES
        self._created = False
        self._needSave = False
        self._recent = []

    @Property('QVariant', notify=dataBlockChanged)
    def dataBlock(self):
        return self._dataBlock

    @Property(str, notify=dataBlockCifChanged)
    def dataBlockCif(self):
        return self._dataBlockCif

    @Property('QVariant', constant=True)
    def examples(self):
        return self._examples

    @Property(bool, notify=createdChanged)
    def created(self):
        return self._created

    @created.setter
    def created(self, newValue):
        if self._created == newValue:
            return
        self._created = newValue
        self.createdChanged.emit()

    @Property(bool, notify=needSaveChanged)
    def needSave(self):
        return self._needSave

    @needSave.setter
    def needSave(self, newValue):
        if self._needSave == newValue:
            return
        self._needSave = newValue
        self.needSaveChanged.emit()

    @Slot()
    def setNeedSaveToTrue(self):
        self.needSave = True


    #
    @Property('QVariant', notify=recentChanged)
    def recent(self):
        return self._recent

    @recent.setter
    def recent(self, newValue):
        newValue = newValue.toVariant()
        if self._recent == newValue:
            return
        self._recent = newValue
        self.recentChanged.emit()


    def createDataBlockFromCif(self, edCif):
        starObj = PycifstarData()
        starObj.take_from_string(edCif)
        dataBlock = CryspyParser.starObjToEdProject(starObj)
        return dataBlock


    @Slot('QVariant')
    def loadProjectFromFile(self, fpath):
        fpath = fpath.toLocalFile()
        fpath = IO.generalizePath(fpath)
        console.debug(f"Open an existing project from: {fpath}")
        with open(fpath, 'r') as file:
            edCif = file.read()

        starObj = PycifstarData()
        starObj.take_from_string(edCif)
        self._dataBlock = CryspyParser.starObjToEdProject(starObj)

        modelDirNames = [item['_dir_name']['value'] for item in self._dataBlock['loops']['_model']]
        modelFileNames = [item['_cif_file_name']['value'] for item in self._dataBlock['loops']['_model']]
        experimentDirNames = [item['_dir_name']['value'] for item in self._dataBlock['loops']['_experiment']]
        experimentFileNames = [item['_cif_file_name']['value'] for item in self._dataBlock['loops']['_experiment']]

        projectPath = os.path.dirname(fpath)
        modelFilePaths = [os.path.join(projectPath, dirName, fileName) for (dirName, fileName) in zip(modelDirNames, modelFileNames)]
        experimentFilePaths = [os.path.join(projectPath, dirName, fileName) for (dirName, fileName) in zip(experimentDirNames, experimentFileNames)]
        modelFilePaths = [QUrl.fromLocalFile(path) for path in modelFilePaths]
        experimentFilePaths = [QUrl.fromLocalFile(path) for path in experimentFilePaths]

        self._proxy.model.loadModelsFromFiles(modelFilePaths)
        self._proxy.experiment.loadExperimentsFromFiles(experimentFilePaths)

        if '_location' in self._dataBlock['params']:
            self.setMainParam('_location', 'value', projectPath)
        else:
            self._dataBlock['params']['_location'] = dict(Parameter(
                projectPath,
                name='_location',
                prettyName='Location',
                url='https://easydiffraction.org'
            ))
        if '_description' not in self._dataBlock['params']:
            self._dataBlock['params']['_description'] = dict(Parameter(
                '.',
                name='_description',
                prettyName='Description',
                url='https://easydiffraction.org'
            ))


        # NEED FIX: use _location insted of _project_dir_path
        #for model in self._dataBlock['loops']['_model']:
        #    model['_project_dir_path'] = os.path.dirname(fpath)
        #for experiment in self._dataBlock['loops']['_experiment']:
        #    experiment['_project_dir_path'] = os.path.dirname(fpath)
        #print(self._dataBlock['loops']['_model'][0]['_project_dir_path'])
        #print(self._dataBlock['loops']['_experiment'][0]['_project_dir_path'])


        if fpath in self._recent:
            self._recent.remove(fpath)
        self._recent.insert(0, fpath)
        self._recent = self._recent[:10]
        self.recentChanged.emit()

        self.dataBlockChanged.emit()
        self.created = True


    #
    @Slot(str)
    def setName(self, value):
        oldValue = self._dataBlock['name']
        if oldValue == value:
            return
        self._dataBlock['name'] = value
        console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value}', 'project.name'))
        self.dataBlockChanged.emit()

    def setModels(self):
        names = [f"{block['name']}" for block in self._proxy.model.dataBlocks]
        oldNames = []
        if '_model' in self._dataBlock['loops']:
            oldNames = [os.path.basename(item['_cif_file_name']['value']) for item in self._dataBlock['loops']['_model']]
        if oldNames == names:
            return
        print(oldNames)
        print(names)

        self._dataBlock['loops']['_model'] = []
        for name in names:
            edModel = {}
            edModel['_dir_name'] = dict(Parameter(
                'models',
                name='_dir_name',
                prettyName='Model directory',
                url='https://easydiffraction.org'
            ))
            edModel['_cif_file_name'] = dict(Parameter(
                f'{name}.cif',
                name='_cif_file_name',
                prettyName='Model file',
                url='https://easydiffraction.org'
            ))
            edModel['_jpg_file_name'] = dict(Parameter(
                f'{name}.jpg',
                name='_jpg_file_name',
                url='https://easydiffraction.org'
            ))
            self._dataBlock['loops']['_model'].append(edModel)

        console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldNames} → {names}'))
        self.dataBlockChanged.emit()

    #
    def setExperiments(self):
        names = [f"{block['name']}" for block in self._proxy.experiment.dataBlocksNoMeas]
        oldNames = []
        if '_experiment' in self._dataBlock['loops']:
            oldNames = [os.path.basename(item['_cif_file_name']['value']) for item in self._dataBlock['loops']['_experiment']]
        if oldNames == names:
            return

        self._dataBlock['loops']['_experiment'] = []
        for name in names:
            edExperiment = {}
            edExperiment['_dir_name'] = dict(Parameter(
                'experiments',
                name='_dir_name',
                prettyName='Experiment directory',
                url='https://easydiffraction.org'
            ))
            edExperiment['_cif_file_name'] = dict(Parameter(
                f'{name}.cif',
                name='_cif_file_name',
                prettyName='Experiment file',
                url='https://easydiffraction.org'
            ))
            edExperiment['_jpg_file_name'] = dict(Parameter(
                f'{name}.jpg',
                name='_jpg_file_name',
                url='https://easydiffraction.org'
            ))
            self._dataBlock['loops']['_experiment'].append(edExperiment)

        console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldNames} → {names}'))
        self.dataBlockChanged.emit()


    #
    @Slot(str, str, 'QVariant')
    def setMainParam(self, paramName, field, value):
        changedIntern = self.editDataBlockMainParam(paramName, field, value)
        if changedIntern:
            self.dataBlockChanged.emit()

    #
    def editDataBlockMainParam(self, paramName, field, value):
        blockType = 'model'
        oldValue = self._dataBlock['params'][paramName][field]
        if oldValue == value:
            return False
        self._dataBlock['params'][paramName][field] = value
        if type(value) == float:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value:.6f}', f'{blockType}.{paramName}.{field}'))
        else:
            console.debug(IO.formatMsg('sub', 'Intern dict', f'{oldValue} → {value}', f'{blockType}.{paramName}.{field}'))
        return True




    @Slot()
    def create(self):
        dateCreated = datetime.now().strftime("%d %b %Y %H:%M")
        self.setMainParam('_date_created', 'value', dateCreated)
        self.setMainParam('_date_last_modified', 'value', dateCreated)
        self.created = True


    @Slot()
    def save(self):
        console.debug(IO.formatMsg('main', 'Saving project...'))

        dateLastModified = datetime.now().strftime("%d %b %Y %H:%M")
        self.setMainParam('_date_last_modified', 'value', dateLastModified)

        projectDirPath = self._dataBlock['params']['_location']['value']
        projectFileName = 'project.cif'
        projectFilePath = os.path.join(projectDirPath, projectFileName)
        os.makedirs(projectDirPath, exist_ok=True)
        with open(projectFilePath, 'w') as file:
            file.write(self.dataBlockCif)
            console.debug(IO.formatMsg('sub', f'saved to: {projectFilePath}'))

        if self._proxy.model.defined:
            modelDirNames = [item['_dir_name']['value'] for item in self._dataBlock['loops']['_model']]
            modelFileNames = [item['_cif_file_name']['value'] for item in self._dataBlock['loops']['_model']]
            modelFilePaths = [os.path.join(projectDirPath, dirName, fileName) for (dirName, fileName) in zip(modelDirNames, modelFileNames)]
            for (modelFilePath, dataBlockCif) in zip(modelFilePaths, self._proxy.model.dataBlocksCif):
                dataBlockCif = dataBlockCif[0]
                os.makedirs(os.path.dirname(modelFilePath), exist_ok=True)
                with open(modelFilePath, 'w') as file:
                    file.write(dataBlockCif)
                    console.debug(IO.formatMsg('sub', f'saved to: {modelFilePath}'))

        if self._proxy.experiment.defined:
            experimentDirNames = [item['_dir_name']['value'] for item in self._dataBlock['loops']['_experiment']]
            experimentFileNames = [item['_cif_file_name']['value'] for item in self._dataBlock['loops']['_experiment']]
            experimentFilePaths = [os.path.join(projectDirPath, dirName, fileName) for (dirName, fileName) in zip(experimentDirNames, experimentFileNames)]
            for (experimentFilePath, dataBlockCifNoMeas, dataBlockCifMeasOnly) in zip(experimentFilePaths, self._proxy.experiment.dataBlocksCifNoMeas, self._proxy.experiment.dataBlocksCifMeasOnly):
                os.makedirs(os.path.dirname(experimentFilePath), exist_ok=True)
                dataBlockCif = dataBlockCifNoMeas + '\n\n' + dataBlockCifMeasOnly
                with open(experimentFilePath, 'w') as file:
                    file.write(dataBlockCif)
                    console.debug(IO.formatMsg('sub', f'saved to: {experimentFilePath}'))

        self.needSave = False


    #
    def setDataBlockCif(self):
        self._dataBlockCif = CryspyParser.dataBlockToCif(self._dataBlock)
        console.debug(IO.formatMsg('sub', 'Project', '', 'to CIF string', 'converted'))
        self.dataBlockCifChanged.emit()


