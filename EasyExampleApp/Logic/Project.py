# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json, jsbeautifier
from datetime import datetime

from PySide6.QtCore import QObject, Signal, Slot, Property


class Project(QObject):
    isCreatedChanged = Signal()
    needSaveChanged = Signal()
    nameChanged = Signal()
    descriptionChanged = Signal()
    locationChanged = Signal()
    createdDateChanged = Signal()
    imageChanged = Signal()
    examplesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._isCreated = False
        self._needSave = False
        self._name = 'Default project'
        self._description = 'Default project description'
        self._location = ''
        self._createdDate = ''
        self._image = '../Resources/Project/Sine.svg'
        self._examples = [
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

        self.examplesChanged.connect(self.setNeedSaveToTrue)
        self.nameChanged.connect(self.setNeedSaveToTrue)
        self.descriptionChanged.connect(self.setNeedSaveToTrue)
        self.imageChanged.connect(self.setNeedSaveToTrue)

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

    @Property(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, newValue):
        if self._name == newValue:
            return
        self._name = newValue
        self.nameChanged.emit()

    @Property(str, notify=descriptionChanged)
    def description(self):
        return self._description

    @description.setter
    def description(self, newValue):
        if self._description == newValue:
            return
        self._description = newValue
        self.descriptionChanged.emit()

    @Property(str, notify=locationChanged)
    def location(self):
        return self._location

    @location.setter
    def location(self, newValue):
        if self._location == newValue:
            return
        self._location = newValue
        self.locationChanged.emit()

    @Property(str, notify=createdDateChanged)
    def createdDate(self):
        return self._createdDate

    @createdDate.setter
    def createdDate(self, newValue):
        if self._createdDate == newValue:
            return
        self._createdDate = newValue
        self.createdDateChanged.emit()

    @Property(str, notify=imageChanged)
    def image(self):
        return self._image

    @image.setter
    def image(self, newValue):
        if self._image == newValue:
            return
        self._image = newValue
        self.imageChanged.emit()

    @Property('QVariant', notify=examplesChanged)
    def examples(self):
        return self._examples

    @Slot()
    def create(self):
        self.createdDate = datetime.now().strftime("%d.%b.%Y %H:%M")
        self.isCreated = True

    @Slot()
    def save(self):
        # Create project json

        project = {}

        if self.isCreated:
            project['project'] = {
                'name': self._proxy.project.name,
                'description': self._proxy.project.description,
                'location': self._proxy.project.location,
                'creationDate': self._proxy.project.createdDate
            }

        if self._proxy.experiment.isCreated:
            project['experiment'] = {
                'name': self._proxy.experiment.description['name'],
                'isCreated': self._proxy.experiment.isCreated,
                'parameters': self._proxy.model.parameters,
                'dataSize': self._proxy.experiment.dataSize,
                'xData': self._proxy.experiment.xData,
                'yData': self._proxy.experiment.yData,
            }

        if self._proxy.model.isCreated:
            project['model'] = {
                'name': self._proxy.model.description['name'],
                'isCreated': self._proxy.model.isCreated,
                'parameters': self._proxy.model.parameters,
                'yData': self._proxy.model.yData
            }

        if self._proxy.fitting.fitFinished:
            project['fitting'] = {
                'fitFinished': self._proxy.fitting.fitFinished
            }

        if self._proxy.summary.isCreated:
            project['summary'] = {
                'isCreated': self._proxy.summary.isCreated
            }

        # Style project json

        options = jsbeautifier.default_options()
        options.indent_size = 2
        formattedProject = jsbeautifier.beautify(json.dumps(project), options)

        # Save formatted project json

        filePath = os.path.join(self.location, 'project.json')
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, 'w') as file:
            file.write(formattedProject)

        # Toggle need save

        self.needSave = False
