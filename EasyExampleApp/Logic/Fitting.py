# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import time

from PySide6.QtCore import QObject, Signal, Slot, Property, QThreadPool

from EasyApp.Logic.Logging import console


class Worker(QObject):
    finished = Signal()
    cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._needCancel = False

    def run(self):
        for i in range (10):
            if self._needCancel:
                self._needCancel = False
                self.cancelled.emit()
                console.error('Minimization process has been cancelled')
                return
            time.sleep(3)
        self.finished.emit()
        console.info('Minimization process has been finished')


class Fitting(QObject):
    isFittingNowChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._threadpool = QThreadPool.globalInstance()
        self._worker = Worker()
        self._isFittingNow = False

        self._worker.finished.connect(self.setIsFittingNowToFalse)
        self._worker.cancelled.connect(self.setIsFittingNowToFalse)

    @Property(bool, notify=isFittingNowChanged)
    def isFittingNow(self):
        return self._isFittingNow

    @isFittingNow.setter
    def isFittingNow(self, newValue):
        if self._isFittingNow == newValue:
            return
        self._isFittingNow = newValue
        self.isFittingNowChanged.emit()

    @Slot()
    def startStop(self):
        if self._worker._needCancel:
            console.debug('Minimization process has been already requested to cancel')
            return
        if self.isFittingNow:
            self._worker._needCancel = True
            console.debug('Minimization process has been requested to cancel')
        else:
            self.isFittingNow = True
            self._threadpool.start(self._worker.run)
            console.debug('Minimization process has been started in a separate thread')

    def setIsFittingNowToFalse(self):
        self.isFittingNow = False
