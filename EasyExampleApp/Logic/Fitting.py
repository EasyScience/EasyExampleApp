# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import time

from PySide6.QtCore import QObject, Signal, Slot, Property, QThread, QThreadPool, QRunnable

from EasyApp.Logic.Logging import console

try:
    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_rietveld_refinement_by_dictionary
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')


ITER = 1


class WorkerSignals(QObject):
    finished = Signal()
    cancelled = Signal()


class Worker(QRunnable):

    def __init__(self, proxy):
        super().__init__()
        self._proxy = proxy
        self._needCancel = False
        self._signals = WorkerSignals()
        QThread.setTerminationEnabled()

    def run(self):
        def callbackFunc(xk):
            global ITER
            print(f'Iteration: {ITER}, Params: {xk.tolist()}')
            if self._needCancel:
                self._needCancel = False
                self._signals.cancelled.emit()
                console.error('Terminating the execution of the minimization thread')
                ITER = 1
                QThread.terminate()
            ITER += 1
        rhochi_rietveld_refinement_by_dictionary(global_dict=self._proxy.data._cryspyDict,
                                                 method='BFGS',
                                                 callback=callbackFunc)
        ITER = 1
        self._signals.finished.emit()
        console.info('Minimization process has been finished')


class Fitting(QObject):
    isFittingNowChanged = Signal()
    fitFinished = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._threadpool = QThreadPool.globalInstance()
        self._worker = Worker(self._proxy)
        self._isFittingNow = False

        self._worker._signals.finished.connect(self.setIsFittingNowToFalse)
        self._worker._signals.cancelled.connect(self.setIsFittingNowToFalse)
        self._worker._signals.finished.connect(self.fitFinished)

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


#https://stackoverflow.com/questions/30843876/using-qthreadpool-with-qrunnable-in-pyqt4
#https://stackoverflow.com/questions/70868493/what-is-the-best-way-to-stop-interrupt-qrunnable-in-qthreadpool
#https://stackoverflow.com/questions/24825441/stop-scipy-minimize-after-set-time
#https://stackoverflow.com/questions/22390479/qrunnable-trying-to-abort-a-task
