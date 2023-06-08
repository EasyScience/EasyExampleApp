# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Property


class Data(QObject):
    edDictChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._edDict = {}
        self._cryspyDict = {}
        self._cryspyInOutDict = {}

    # QML accessible properties

    @Property('QVariant', notify=edDictChanged)
    def edDict(self):
        return self._edDict
