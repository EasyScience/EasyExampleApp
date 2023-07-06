# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import copy
import lmfit

from PySide6.QtCore import QObject, Signal, Slot, Property, QThreadPool

from EasyApp.Logic.Logging import console
from Logic.Data import Data

try:
    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_calc_chi_sq_by_dictionary
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')


SCALE = 1

class Worker(QObject):
    finished = Signal()
    cancelled = Signal()

    def __init__(self, proxy):
        super().__init__()
        self._proxy = proxy
        self._needCancel = False

        self._cryspyDict = self._proxy.data._cryspyDict
        self._cryspyDictInitial = copy.deepcopy(self._cryspyDict)
        self._cryspyDictInOut = {}
        self._cryspyUsePrecalculatedData = False
        self._cryspyCalcAnalyticalDerivatives = False

        #self._paramsInit = lmfit.Parameters()
        self._paramsFinal = lmfit.Parameters()

        self._gofPrevIter = None
        self._gofLastIter = None

        ###QThread.setTerminationEnabled()

    def run(self):
        def callbackFunc(params, iter, resid, *args, **kws):
            console.info(f"Iteration: {iter:5d},   Reduced chi2 per {self._proxy.fitting._pointsCount} points: {self._proxy.fitting._chiSq/self._proxy.fitting._pointsCount:16.6f}")
            self._proxy.fitting._fitIteration = iter
            # Check if fitting termination is requested
            if self._needCancel:
                self._needCancel = False
                self._cryspyDict = self._cryspyDictInitial
                self.cancelled.emit()
                self._proxy.status.fitStatus = 'Cancelled'
                console.error('Terminating the execution of the minimization thread')
                ###QThread.terminate()  # Not needed for Lmfit
                return True
            # ...
            self._proxy.status.fitIteration = f'{iter}'
            # Calc goodnes-of-fit (GOF) value shift between iterations
            if iter == 1:
                self._gofPrevIter = self._proxy.fitting._chiSqStart
            self._gofLastIter = self._proxy.fitting.chiSq
            gofShift = abs(self._gofLastIter - self._gofPrevIter) / self._proxy.fitting._pointsCount
            self._gofPrevIter = self._gofLastIter
            # Update goodnes-of-fit (GOF) value updated in the status bar
            if iter == 1 or gofShift > 0.01:
                ###reducedGofStart = self._proxy.fitting._chiSqStart / self._proxy.fitting._pointsCount
                ###reducedGofLastIter = self._gofLastIter / self._proxy.fitting._pointsCount
                ###self._proxy.status.goodnessOfFit = f'{reducedGofStart:0.2f} → {reducedGofLastIter:0.2f}'  # NEED move to connection
                self._proxy.fitting.chiSqSignificantlyChanged.emit()
            return False

        def chiSqFunc(params):
            for param in params:
                block, group, idx = Data.strToCryspyDictParamPath(param)
                self._cryspyDict[block][group][idx] = params[param].value
            self._proxy.fitting.chiSq, _, _, _, _ = rhochi_calc_chi_sq_by_dictionary(
                self._cryspyDict,
                dict_in_out=self._cryspyDictInOut,
                flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
                flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)
            return self._proxy.fitting.chiSq

        self._proxy.fitting._freezeChiSqStart = True

        # Save initial state of cryspyDict if cancel fit is requested
        self._cryspyDictInitial = copy.deepcopy(self._cryspyDict)

        # Preliminary calculations
        self._cryspyDictInOut = {}
        self._cryspyUsePrecalculatedData = False
        self._cryspyCalcAnalyticalDerivatives = False
        self._proxy.fitting.chiSq, self._proxy.fitting._pointsCount, _, _, parameter_names = rhochi_calc_chi_sq_by_dictionary(
            self._cryspyDict,
            dict_in_out=self._cryspyDictInOut,
            flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
            flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)

        # Create list of parameters to be varied
        parameter_names_free = [way for way in parameter_names]
        param_0 = [self._cryspyDict[way[0]][way[1]][way[2]] for way in parameter_names_free]
        paramsLmfit = lmfit.Parameters()
        for name, val in zip(parameter_names_free, param_0):
            nameStr = Data.cryspyDictParamPathToStr(name)
            #self._paramsInit.add(nameStr, value=val)
            paramsLmfit.add(nameStr, value=val)

        ###self._proxy.fitting._fittablesCount = len(param_0)
        ###self._proxy.status.variables = f'{self._proxy.fitting._fittablesCount}'  # NEED move to connection
        self._proxy.fitting._freeParamsCount = len(param_0)
        if self._proxy.fitting._freeParamsCount != self._proxy.fittables._freeParamsCount:
            console.error(f'Number of free parameters differs. Expected {self._proxy.fittables._freeParamsCount}, got {self._proxy.fitting._freeParamsCount}')

        # Minimization: lmfit.minimize
        self._proxy.fitting._chiSqStart = self._proxy.fitting.chiSq
        self._cryspyUsePrecalculatedData = True
        method = 'BFGS'
        tol = 1e+3
        result = lmfit.minimize(chiSqFunc,
                                paramsLmfit,
                                method=method,
                                iter_cb=callbackFunc,
                                tol=tol
                                )
        #lmfit.report_fit(result)

        if result.success:
            console.info('Minimization has been successfully finished')
            # Calculate optimal chi2
            self._cryspyDictInOut = {}
            self._cryspyUsePrecalculatedData = False
            self._cryspyCalcAnalyticalDerivatives = False
            self._proxy.fitting.chiSq, _, _, _, _ = rhochi_calc_chi_sq_by_dictionary(
                self._cryspyDict,
                dict_in_out=self._cryspyDictInOut,
                flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
                flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)
            console.info(f"Optimal reduced chi2 per {self._proxy.fitting._pointsCount} points: {self._proxy.fitting._chiSq/self._proxy.fitting._pointsCount:.2f}")

            ####self._proxy.fitting._chiSqStart = self._proxy.fitting.chiSq

            names = [Data.cryspyDictParamPathToStr(name) for name in parameter_names_free]
            self._proxy.experiment.editDataBlockByCryspyDictParams(names)
            self._proxy.model.editDataBlockByCryspyDictParams(names)

            self._proxy.fitting._freezeChiSqStart = False

            #self._paramsInit.pretty_print()
            #result.params.pretty_print()
            self._proxy.status.fitStatus = 'Success'
            #console.error('Success')
        else:
            self._proxy.status.fitStatus = 'Failure'
            #console.error('Failure')

        # Finishing
        self.finished.emit()
        console.info('Minimization process has been finished')


class Fitting(QObject):
    isFittingNowChanged = Signal()
    fitFinished = Signal()
    chiSqChanged = Signal()
    chiSqSignificantlyChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._threadpool = QThreadPool.globalInstance()
        self._worker = Worker(self._proxy)
        self._isFittingNow = False

        self._chiSqStart = None
        self._chiSq = None
        self._pointsCount = None # self._proxy.experiment._xArrays[self._proxy.experiment.currentIndex].size  # ???
        self._fitIteration = None

        self._freezeChiSqStart = False

        self._freeParamsCount = 0

        self._worker.finished.connect(self.setIsFittingNowToFalse)
        self._worker.cancelled.connect(self.setIsFittingNowToFalse)
        self._worker.finished.connect(self.fitFinished)

    @Property(bool, notify=isFittingNowChanged)
    def isFittingNow(self):
        return self._isFittingNow

    @isFittingNow.setter
    def isFittingNow(self, newValue):
        if self._isFittingNow == newValue:
            return
        self._isFittingNow = newValue
        self.isFittingNowChanged.emit()

    @Property(float, notify=chiSqChanged)
    def chiSq(self):
        return self._chiSq

    @chiSq.setter
    def chiSq(self, newValue):
        if self._chiSq == newValue:
            return
        self._chiSq = newValue
        self.chiSqChanged.emit()

    @Slot()
    def startStop(self):
        self._proxy.status.fitStatus = ''

        if self._worker._needCancel:
            console.debug('Minimization process has been already requested to cancel')
            return

        if self.isFittingNow:
            self._worker._needCancel = True
            console.debug('Minimization process has been requested to cancel')
        else:
            if self._proxy.fittables._freeParamsCount > 0:
                self.isFittingNow = True
                #self._worker.run()
                self._threadpool.start(self._worker.run)
                console.debug('Minimization process has been started in a separate thread')
            else:
                self._proxy.status.fitStatus = 'No free params'
                console.debug('Minimization process has not been started. No free parameters found.')

    def setIsFittingNowToFalse(self):
        self.isFittingNow = False


#https://stackoverflow.com/questions/30843876/using-qthreadpool-with-qrunnable-in-pyqt4
#https://stackoverflow.com/questions/70868493/what-is-the-best-way-to-stop-interrupt-qrunnable-in-qthreadpool
#https://stackoverflow.com/questions/24825441/stop-scipy-minimize-after-set-time
#https://stackoverflow.com/questions/22390479/qrunnable-trying-to-abort-a-task
