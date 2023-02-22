# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import os
import json, jsbeautifier
from datetime import datetime

from PySide6.QtCore import QObject, Signal, Slot, Property


class Plotting(QObject):
    useWebGL1dChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pyProxy = parent
        self._useWebGL1d = True

    @Property(bool, notify=useWebGL1dChanged)
    def useWebGL1d(self):
        return self._useWebGL1d

    @useWebGL1d.setter
    def useWebGL1d(self, newValue):
        if self._useWebGL1d == newValue:
            return
        self._useWebGL1d = newValue
        self.useWebGL1dChanged.emit()
