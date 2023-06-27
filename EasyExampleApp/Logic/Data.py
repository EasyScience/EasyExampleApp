# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np
from PySide6.QtCore import QObject, Signal, Property


class Data(QObject):
    edDictChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._edDict = {}

        self._cryspyExperimentObj = None
        self._cryspyModelObj = None

        self._cryspyExperimentDict = {}
        self._cryspyModelDict = {}

        self._cryspyDict = {}
        self._cryspyInOutDict = {}

    # QML accessible properties

    @Property('QVariant', notify=edDictChanged)
    def edDict(self):
        return self._edDict

    # Static methods

    @staticmethod
    def cryspyDictParamPathToStr(p):
        block = p[0]
        group = p[1]
        idx = '__'.join([str(v) for v in p[2]])  # (1,0) -> '1__0', (1,) -> '1'
        s = f'{block}___{group}___{idx}'  # name should match the regular expression [a-zA-Z_][a-zA-Z0-9_]
        return s

    @staticmethod
    def strToCryspyDictParamPath(s):
        l = s.split('___')
        block = l[0]
        group = l[1]
        idx = tuple(np.fromstring(l[2], dtype=int, sep='__'))
        return block, group, idx
