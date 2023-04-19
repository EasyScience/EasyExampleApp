# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

# https://docs.python.org/3/library/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
# https://stackoverflow.com/questions/42936810/python-logging-module-set-formatter-dynamically

from PySide6.QtCore import QObject, Signal, Slot, Property
import logging


pyFormat = logging.Formatter(' py: %(asctime)s.%(msecs)04d %(lineno)5d: %(filename)-17s %(funcName)-33s %(levelname)8s: %(message)s',
                             datefmt='%H:%M:%S')

qmlFormat = logging.Formatter('qml: %(asctime)s.%(msecs)04d %(levelname)67s: %(message)s',
                              datefmt='%H:%M:%S')


log = logging.getLogger('main')
log.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(pyFormat)

log.addHandler(consoleHandler)


LEVELS = {
    'Critical': logging.CRITICAL,
    'Error': logging.ERROR,
    'Warning': logging.WARNING,
    'Info': logging.INFO,
    'Debug': logging.DEBUG,
    'Notset': logging.NOTSET
}


class Logger(QObject):
    levelChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._level = logging.DEBUG
        self.levelChanged.connect(self.onLevelChanged)

    # QML accessible properties

    @Property(str, notify=levelChanged)
    def level(self):
        return self._level

    @level.setter
    def level(self, newValue):
        if self._level == newValue:
            return
        self._level = newValue
        self.levelChanged.emit()

    @Slot(str)
    def info(self, message):
        consoleHandler.setFormatter(qmlFormat)
        log.info(message)
        consoleHandler.setFormatter(pyFormat)

    @Slot(str)
    def debug(self, message):
        consoleHandler.setFormatter(qmlFormat)
        log.debug(message)
        consoleHandler.setFormatter(pyFormat)


    # Private methods

    def onLevelChanged(self):
        log.setLevel(LEVELS[self.level])
        #qmlLog.setLevel(LEVELS[self.level])
