# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import copy
import numpy as np
import lmfit

from PySide6.QtCore import QObject, Signal, Slot, Property, QThreadPool

from EasyApp.Logic.Logging import console

try:
    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_calc_chi_sq_by_dictionary
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')


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

        ###QThread.setTerminationEnabled()

    def run(self):

        def callbackFunc(params, iter, resid, *args, **kws):
            console.debug(f"Iteration: {iter:5d},   Reduced chi2 per {self._proxy.fitting._pointsCount} points: {self._proxy.fitting._chiSq/self._proxy.fitting._pointsCount:16.6f}")
            if self._needCancel:
                self._needCancel = False
                self._cryspyDict = self._cryspyDictInitial
                self.cancelled.emit()
                console.error('Terminating the execution of the minimization thread')
                ###QThread.terminate()
                return True
            return False

        def chiSqFunc(params):
            for param in params:
                name = param.split('__')
                way = (name[0], name[1], tuple([np.int_(name[2])]))
                self._cryspyDict[way[0]][way[1]][way[2]] = params[param].value
            self._proxy.fitting.chiSq, _, _, _, _ = rhochi_calc_chi_sq_by_dictionary(
                self._cryspyDict,
                dict_in_out=self._cryspyDictInOut,
                flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
                flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)
            return self._proxy.fitting._chiSq

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
            nameStr = f'{name[0]}__{name[1]}__{name[2][0]}'
            paramsLmfit.add(nameStr, value=val)
        ###for name, val in zip(parameter_names_free, param_0):
        ###    print(f" - {name:}  {val:.5f}")


        # Minimization: lmfit.minimize
        # 'lbfgsb'
        #Warning: uncertainties could not be estimated:
        #    this fitting method does not natively calculate uncertainties
        #    and numdifftools is not installed for lmfit to do this. Use
        #    `pip install numdifftools` for lmfit to estimate uncertainties
        #    with this fitting method.
        self._cryspyUsePrecalculatedData = True
        #method='least_squares'  # fails
        #method='leastsq'  # freezes
        method = 'bfgs'  # 47s
        #method = 'nelder'
        #method = 'lbfgsb'  # 18s
        #tol = 1000.0
        ###fitter = lmfit.Minimizer(lm_min, params, fcn_args=(x, ydata), fit_kws={'xatol':0.01})
        #leastsq_kws = dict(tol=0.000000000000001)
        #leastsq_kws = dict(ftol=1e-09, xtol=1e-09, gtol=1e-09, max_nfev=200)
        #leastsq_nelder = dict(tol=tol, options=dict(fatol=tol, xatol=tol, maxfev=100))
        #leastsq_bfgs = dict(tol=tol, options=dict(eps=0.1, xrtol=tol))
        #print('----',type(param_0))
        #leastsq_bfgs = dict(options=dict(eps=0.01 * np.array(param_0)))
        #leastsq_bfgs = dict(options=dict(eps=0.001))
        leastsq_bfgs = dict(options=dict(xrtol=1e-5))
        result = lmfit.minimize(chiSqFunc,
                                paramsLmfit,
                                method=method,
                                iter_cb=callbackFunc,
                                **leastsq_bfgs)
        lmfit.report_fit(result)

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

        # Finishing
        self.finished.emit()
        console.info('Minimization process has been finished')


class Fitting(QObject):
    isFittingNowChanged = Signal()
    fitFinished = Signal()
    chiSqChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self._proxy = parent
        self._threadpool = QThreadPool.globalInstance()
        self._worker = Worker(self._proxy)
        self._isFittingNow = False

        self._chiSq = np.inf
        self._pointsCount = 0 # self._proxy.experiment._xArrays[self._proxy.experiment.currentIndex].size  # ???

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
        if self._worker._needCancel:
            console.debug('Minimization process has been already requested to cancel')
            return
        if self.isFittingNow:
            self._worker._needCancel = True
            console.debug('Minimization process has been requested to cancel')
        else:
            self.isFittingNow = True
            self._worker.run()
            #self._threadpool.start(self._worker.run)
            #console.debug('Minimization process has been started in a separate thread')

    def setIsFittingNowToFalse(self):
        self.isFittingNow = False


#https://stackoverflow.com/questions/30843876/using-qthreadpool-with-qrunnable-in-pyqt4
#https://stackoverflow.com/questions/70868493/what-is-the-best-way-to-stop-interrupt-qrunnable-in-qthreadpool
#https://stackoverflow.com/questions/24825441/stop-scipy-minimize-after-set-time
#https://stackoverflow.com/questions/22390479/qrunnable-trying-to-abort-a-task
