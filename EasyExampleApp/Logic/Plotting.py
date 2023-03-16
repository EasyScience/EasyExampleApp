# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property


class Plotting(QObject):
    useWebGL1dChanged = Signal()
    viewRefsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pyProxy = parent
        self._useWebGL1d = True
        self._viewRefs = {
            'experiment': None,
            'model': None,
            'analysis': None
        }

    @Property(bool, notify=useWebGL1dChanged)
    def useWebGL1d(self):
        return self._useWebGL1d

    @useWebGL1d.setter
    def useWebGL1d(self, newValue):
        if self._useWebGL1d == newValue:
            return
        self._useWebGL1d = newValue
        self.useWebGL1dChanged.emit()

    @Property('QVariant', notify=viewRefsChanged)
    def viewRefs(self):
        return self._viewRefs

    @Slot(str, 'QVariant')
    def setViewRef(self, key, value):
        if self._viewRefs[key] == value:
            return
        self._viewRefs[key] = value
        self.viewRefsChanged.emit()
