# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json, jsbeautifier
from datetime import datetime

from PySide6.QtCore import QObject, Signal, Slot, Property


class Project(QObject):
    examplesAsJsonChanged = Signal()

    isCreatedChanged = Signal()
    needSaveChanged = Signal()

    currentProjectNameChanged = Signal()
    currentProjectDescriptionChanged = Signal()
    currentProjectLocationChanged = Signal()
    currentProjectCreatedDateChanged = Signal()
    currentProjectImageChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pyProxy = parent

        self._isCreated = False
        self._needSave = False

        self._currentProjectName = 'Default project'
        self._currentProjectDescription = 'Default project description'
        self._currentProjectLocation = ''
        self._currentProjectCreatedDate = ''
        self._currentProjectImage = '../Resources/Project/Sine.svg'

        self._examples_as_json = [
            {
                'name': 'Horizontal line',
                'description': 'Straight line, horizontal, PicoScope 2204A',
                'path': '../Resources/Examples/HorizontalLine/project.json'
            },
            {
                'name': 'Slanting line 1',
                'description': 'Straight line, positive slope, Tektronix 2430A',
                'path': '../Resources/Examples/SlantingLine1/project.json'
            },
            {
                'name': 'Slanting line 2',
                'description': 'Straight line, negative slope, Siglent SDS1202X-E',
                'path': '../Resources/Examples/SlantingLine2/project.json'
            }
        ]

        self.examplesAsJsonChanged.connect(self.setNeedSaveToTrue)
        self.isCreatedChanged.connect(self.setNeedSaveToTrue)
        self.currentProjectNameChanged.connect(self.setNeedSaveToTrue)
        self.currentProjectDescriptionChanged.connect(self.setNeedSaveToTrue)
        self.currentProjectLocationChanged.connect(self.setNeedSaveToTrue)
        self.currentProjectCreatedDateChanged.connect(self.setNeedSaveToTrue)
        self.currentProjectImageChanged.connect(self.setNeedSaveToTrue)

    @Property(bool, notify=isCreatedChanged)
    def isCreated(self):
        return self._isCreated

    @isCreated.setter
    def isCreated(self, newValue):
        if self._isCreated == newValue:
            return
        self._isCreated = newValue
        self.isCreatedChanged.emit()

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

    @Property(str, notify=currentProjectNameChanged)
    def currentProjectName(self):
        return self._currentProjectName

    @currentProjectName.setter
    def currentProjectName(self, newValue):
        if self._currentProjectName == newValue:
            return
        self._currentProjectName = newValue
        self.currentProjectNameChanged.emit()

    @Property(str, notify=currentProjectDescriptionChanged)
    def currentProjectDescription(self):
        return self._currentProjectDescription

    @currentProjectDescription.setter
    def currentProjectDescription(self, newValue):
        if self._currentProjectDescription == newValue:
            return
        self._currentProjectDescription = newValue
        self.currentProjectDescriptionChanged.emit()

    @Property(str, notify=currentProjectLocationChanged)
    def currentProjectLocation(self):
        return self._currentProjectLocation

    @currentProjectLocation.setter
    def currentProjectLocation(self, newValue):
        if self._currentProjectLocation == newValue:
            return
        self._currentProjectLocation = newValue
        self.currentProjectLocationChanged.emit()

    @Property(str, notify=currentProjectCreatedDateChanged)
    def currentProjectCreatedDate(self):
        return self._currentProjectCreatedDate

    @currentProjectCreatedDate.setter
    def currentProjectCreatedDate(self, newValue):
        if self._currentProjectCreatedDate == newValue:
            return
        self._currentProjectCreatedDate = newValue
        self.currentProjectCreatedDateChanged.emit()

    @Property(str, notify=currentProjectImageChanged)
    def currentProjectImage(self):
        return self._currentProjectImage

    @currentProjectImage.setter
    def currentProjectImage(self, newValue):
        if self._currentProjectImage == newValue:
            return
        self._currentProjectImage = newValue
        self.currentProjectImageChanged.emit()

    @Property('QVariant', notify=examplesAsJsonChanged)
    def examplesAsJson(self):
        return self._examples_as_json

    @Slot()
    def create(self):
        self.currentProjectCreatedDate = datetime.now().strftime("%d.%b.%Y %H:%M")
        self.isCreated = True

    @Slot()
    def save(self):
        project = {}
        if self._pyProxy.project.isCreated:
            project['project'] = {
                'name': self._pyProxy.project.currentProjectName,
                'description': self._pyProxy.project.currentProjectDescription,
                'location': self._pyProxy.project.currentProjectLocation,
                'creationDate': self._pyProxy.project.currentProjectCreatedDate
            }
        if self._pyProxy.model.isCreated:
            project['model'] = {
                'label': self._pyProxy.model.asJson[0]['label'],
                'isCreated': self._pyProxy.model.isCreated,
                'slope': self._pyProxy.model.slope,
                'yIntercept': self._pyProxy.model.yIntercept,
                'calculatedData': self._pyProxy.model.calculatedData
            }
        if self._pyProxy.experiment.isCreated:
            project['experiment'] = {
                'label': self._pyProxy.experiment.asJson[0]['label'],
                'isCreated': self._pyProxy.experiment.isCreated,
                'measuredDataLength': self._pyProxy.experiment.measuredDataLength,
                'measuredData': self._pyProxy.experiment.measuredData
            }
        if True:
            project['fitting'] = {
                'isFitFinished': self._pyProxy.fitting.isFitFinished
            }
        if self._pyProxy.summary.isCreated:
            project['summary'] = {
                'isCreated': self._pyProxy.summary.isCreated
            }

        options = jsbeautifier.default_options()
        options.indent_size = 2
        formatted_project = jsbeautifier.beautify(json.dumps(project), options)

        file_path = os.path.join(self.currentProjectLocation, 'project.json')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(formatted_project)

        self.needSave = False