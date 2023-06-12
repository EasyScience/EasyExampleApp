# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import time
import copy
import numpy as np
import lmfit

from PySide6.QtCore import QObject, Signal, Slot, Property, QThread, QThreadPool, QRunnable

from EasyApp.Logic.Logging import console

try:
    from cryspy.procedure_rhochi.rhochi_by_dictionary import \
        rhochi_calc_chi_sq_by_dictionary
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

        self._cryspyDict = self._proxy.data._cryspyDict
        self._cryspyDictInitial = copy.deepcopy(self._cryspyDict)
        self._cryspyDictInOut = {}
        self._cryspyUsePrecalculatedData = False
        self._cryspyCalcAnalyticalDerivatives = False

        self._chiSq = np.inf
        self._pointsCount = np.inf

        self._signals = WorkerSignals()
        ###QThread.setTerminationEnabled()

    def run(self):

        def callbackFunc(params, iter, resid, *args, **kws):
            console.debug(f"Iteration: {iter:5d},   Reduced chi2 per {self._pointsCount} points: {self._chiSq/self._pointsCount:10.2f}")
            if self._needCancel:
                self._needCancel = False
                self._cryspyDict = self._cryspyDictInitial
                self._signals.cancelled.emit()
                console.error('Terminating the execution of the minimization thread')
                ###QThread.terminate()
                return True
            return False

        def chiSqFunc(params):
            for param in params:
                name = param.split('__')
                way = (name[0], name[1], tuple([np.int_(name[2])]))
                self._cryspyDict[way[0]][way[1]][way[2]] = params[param].value
            self._chiSq, _, _, _, _ = rhochi_calc_chi_sq_by_dictionary(
                self._cryspyDict,
                dict_in_out=self._cryspyDictInOut,
                flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
                flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)
            return self._chiSq

        # Save initial state of cryspyDict if cancel fit is requested
        self._cryspyDictInitial = copy.deepcopy(self._cryspyDict)

        # Preliminary calculations
        self._cryspyDictInOut = {}
        self._cryspyUsePrecalculatedData = False
        self._cryspyCalcAnalyticalDerivatives = False
        self._chiSq, self._pointsCount, _, _, parameter_names = rhochi_calc_chi_sq_by_dictionary(
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

        # Minimization: lmfit.minimize
        # 'lbfgsb'
        #Warning: uncertainties could not be estimated:
        #    this fitting method does not natively calculate uncertainties
        #    and numdifftools is not installed for lmfit to do this. Use
        #    `pip install numdifftools` for lmfit to estimate uncertainties
        #    with this fitting method.
        self._cryspyUsePrecalculatedData = True
        #method='least_squares'  # fails
        #method='leastsq'  # fails
        #method = 'bfgs'  # 47s
        method = 'lbfgsb'  # 18s
        result = lmfit.minimize(chiSqFunc, paramsLmfit, method=method, iter_cb=callbackFunc)
        lmfit.report_fit(result)

        # Calculate optimal chi2
        self._cryspyDictInOut = {}
        self._cryspyUsePrecalculatedData = False
        self._cryspyCalcAnalyticalDerivatives = False
        self._chiSq, _, _, _, _ = rhochi_calc_chi_sq_by_dictionary(
            self._cryspyDict,
            dict_in_out=self._cryspyDictInOut,
            flag_use_precalculated_data=self._cryspyUsePrecalculatedData,
            flag_calc_analytical_derivatives=self._cryspyCalcAnalyticalDerivatives)
        console.info(f"Optimal reduced chi2 per {self._pointsCount} points: {self._chiSq/self._pointsCount:.2f}")

        # Finishing
        self._signals.finished.emit()
        console.info('Minimization process has been finished')

    def run_OLD(self):
        def callbackFuncScipy(xk):
            global ITER
            print(f'Iteration: {ITER}, Params: {xk.tolist()}')
            if self._needCancel:
                self._needCancel = False
                self._signals.cancelled.emit()
                console.error('Terminating the execution of the minimization thread')
                ITER = 1
                QThread.terminate()
            ITER += 1



        #
        def callbackFuncLmfit(params, iter, resid, *args, **kws):
            print(f'Iteration: {iter}, Resid: {resid}')
            if self._needCancel:
                self._needCancel = False
                self._signals.cancelled.emit()
                console.error('Terminating the execution of the minimization thread')
                #QThread.terminate()
                return True
            return False


        global_dict = self._proxy.data._cryspyDict

        print("*********************************************")
        print("Rietveld refinement by CrysPy (module RhoChi)")
        print("*********************************************\n")
        print("Derivatives are calculated numerically.")
        dict_in_out = {}
        flag_use_precalculated_data = False
        flag_calc_analytical_derivatives = False
        print("Preliminary calculations...", end="\r")
        chi_sq, n_point, der_chi_sq, dder_chi_sq, parameter_names = rhochi_calc_chi_sq_by_dictionary(
            global_dict,
            dict_in_out=dict_in_out,
            flag_use_precalculated_data=flag_use_precalculated_data, flag_calc_analytical_derivatives=flag_calc_analytical_derivatives)


        parameter_names_free = [way for way in parameter_names]



        paramsScipy = [global_dict[way[0]][way[1]][way[2]] for way in parameter_names_free]
        print(f"Started chi_sq per number of points is {chi_sq/n_point:.2f}.         ")
        if len(paramsScipy) == 0:
            res = {}
            print("For refinement procedure some parameters have to be set as refined.")
            return chi_sq, parameter_names, dict_in_out, res
        print(f"Number of fitting parameters {len(paramsScipy):}")
        for name, val in zip(parameter_names_free, paramsScipy):
            print(f" - {name:}  {val:.5f}")


        paramsLmfit = lmfit.Parameters()
        for name, val in zip(parameter_names_free, paramsScipy):
            nameStr = f'{name[0]}__{name[1]}__{name[2][0]}'
            paramsLmfit.add(nameStr, value=val)

        flag_use_precalculated_data = True


        def chiSqFuncScipy(l_param):
            for way, param in zip(parameter_names_free, l_param):
                global_dict[way[0]][way[1]][way[2]] = param

            chi_sq = rhochi_calc_chi_sq_by_dictionary(
                global_dict,
                dict_in_out=dict_in_out,
                flag_use_precalculated_data=flag_use_precalculated_data,
                flag_calc_analytical_derivatives=flag_calc_analytical_derivatives)[0]
            return chi_sq

        #
        def chiSqFuncLmfit(l_param):
            for param in l_param:
                name = param.split('__')
                way = (name[0], name[1], tuple([np.int_(name[2])]))
                global_dict[way[0]][way[1]][way[2]] = l_param[param].value

            chi_sq = rhochi_calc_chi_sq_by_dictionary(
                global_dict,
                dict_in_out=dict_in_out,
                flag_use_precalculated_data=flag_use_precalculated_data,
                flag_calc_analytical_derivatives=flag_calc_analytical_derivatives)[0]
            return chi_sq


        print("\nMinimization procedure of chi_sq is running... ", end="\r")


        # scipy.optimize.minimize
        #method = 'lbfgsb'  # fails
        #method = 'bfgs'  # 45s
        #result = scipy.optimize.minimize(chiSqFuncScipy, paramsScipy, method=method, callback=callbackFuncScipy)
        #print(result)

        # lmfit.minimize
        method = 'lbfgsb'  # 18s
        #method = 'bfgs'  # 47s
        #method='least_squares'  # fails
        #method='leastsq'  # fails
        result = lmfit.minimize(chiSqFuncLmfit, paramsLmfit, method=method, iter_cb=callbackFuncLmfit)
        lmfit.report_fit(result)





        print("Optimization is done.                          ", end="\n")

        print("Calculations for optimal parameters... ", end="\r")
        dict_in_out = {}
        flag_use_precalculated_data = False
        chi_sq, n_point = rhochi_calc_chi_sq_by_dictionary(
            global_dict,
            dict_in_out=dict_in_out,
            flag_use_precalculated_data=flag_use_precalculated_data, flag_calc_analytical_derivatives=flag_calc_analytical_derivatives)[:2]
        print(f"Optimal chi_sq per n is {chi_sq/n_point:.2f}", end="\n")




        ###rhochi_rietveld_refinement_by_dictionary(global_dict=self._proxy.data._cryspyDict,
        ###                                         method='BFGS',
        ###                                         callback=callbackFunc)
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
            #self._worker.run()




    def setIsFittingNowToFalse(self):
        self.isFittingNow = False


#https://stackoverflow.com/questions/30843876/using-qthreadpool-with-qrunnable-in-pyqt4
#https://stackoverflow.com/questions/70868493/what-is-the-best-way-to-stop-interrupt-qrunnable-in-qthreadpool
#https://stackoverflow.com/questions/24825441/stop-scipy-minimize-after-set-time
#https://stackoverflow.com/questions/22390479/qrunnable-trying-to-abort-a-task
