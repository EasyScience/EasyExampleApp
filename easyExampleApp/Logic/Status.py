# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Property, Signal


class Status(QObject):
    asJsonChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._pyProxy = parent

        self._as_json = [
            {
                'label': 'Calculations',
                'value': 'CrysPy'
            },
            {
                'label': 'Minimization',
                'value': 'lmfit'
            }
        ]

    @Property('QVariant', notify=asJsonChanged)
    def asJson(self):
        return self._as_json
