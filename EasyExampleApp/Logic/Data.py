# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np

from PySide6.QtCore import QObject, Signal, Property

from EasyApp.Logic.Logging import console
from Logic.Fittables import Parameter

try:
    import cryspy
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')


class Data(QObject):
    edDictChanged = Signal()
    cryspyDictChanged = Signal()

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

    # Private methods

    def cryspyExperimentObjToDict(self):
        self._cryspyExperimentDict = self._cryspyExperimentObj.get_dictionary()

    def cryspyModelObjToDict(self):
        self._cryspyModelDict = self._cryspyModelObj.get_dictionary()

    def addDataBlock(self, dataBlock):
        console.debug(f"Adding data block (instrument parameters). Experiment no. {len(self._dataBlocks) + 1}")
        self._dataBlocks.append(dataBlock)
        self.dataBlocksChanged.emit()

    def cryspyExperimentToEdDict(self):
        edDict = self._edDict
        cryspyDict = self._cryspyExperimentDict
        cryspyObj = self._cryspyExperimentObj

        experimentNames = [name.replace('pd_', '') for name in cryspyDict.keys() if name.startswith('pd_')]

        for dataBlock in cryspyObj.items:
            dataBlockName = dataBlock.data_name

            # Experiment datablock
            if dataBlockName in experimentNames:
                edDict['experiments'] = []
                edExperimentBlock = {'name': dataBlockName,
                                     'params': {},
                                     'loops': {}}
                cryspyExperimentBlock = dataBlock.items
                xArray = []  #self.defaultXArray()  # NEED FIX
                yMeasArray = []  #self.defaultYMeasArray()  # NEED FIX
                yBkgArray = []  #self.defaultYBkgArray()  # NEED FIX

                for item in cryspyExperimentBlock:
                    # Ranges section
                    if type(item) == cryspy.C_item_loop_classes.cl_1Range.Range:
                        edExperimentBlock['params']['_pd_meas_2theta_range_min'] = dict(Parameter(item.tthetaMin))
                        edExperimentBlock['params']['_pd_meas_2theta_range_max'] = dict(Parameter(item.tthetaMax))
                        edExperimentBlock['params']['_pd_meas_2theta_range_inc'] = dict(Parameter(0.05))  # NEED FIX

                    # Setup section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_setup.Setup:
                        edExperimentBlock['params']['_diffrn_radiation_probe'] = dict(Parameter(item.radiation.replace('neutrons', 'neutron').replace('X-rays', 'x-ray')))
                        edExperimentBlock['params']['_diffrn_radiation_wavelength'] = dict(Parameter(item.wavelength, fittable=True, fit=item.wavelength_refinement))
                        edExperimentBlock['params']['_pd_meas_2theta_offset'] = dict(Parameter(item.offset_ttheta, fittable=True, fit=item.offset_ttheta_refinement))

                    # Instrument resolution section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_resolution.PdInstrResolution:
                        edExperimentBlock['params']['_pd_instr_resolution_u'] = dict(Parameter(item.u, fittable=True, fit=item.u_refinement))
                        edExperimentBlock['params']['_pd_instr_resolution_v'] = dict(Parameter(item.v, fittable=True, fit=item.v_refinement))
                        edExperimentBlock['params']['_pd_instr_resolution_w'] = dict(Parameter(item.w, fittable=True, fit=item.w_refinement))
                        edExperimentBlock['params']['_pd_instr_resolution_x'] = dict(Parameter(item.x, fittable=True, fit=item.x_refinement))
                        edExperimentBlock['params']['_pd_instr_resolution_y'] = dict(Parameter(item.y, fittable=True, fit=item.y_refinement))

                    # Peak assymetries section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_instr_reflex_asymmetry.PdInstrReflexAsymmetry:
                        edExperimentBlock['params']['_pd_instr_reflex_asymmetry_p1'] = dict(Parameter(item.p1, fittable=True, fit=item.p1_refinement))
                        edExperimentBlock['params']['_pd_instr_reflex_asymmetry_p2'] = dict(Parameter(item.p2, fittable=True, fit=item.p2_refinement))
                        edExperimentBlock['params']['_pd_instr_reflex_asymmetry_p3'] = dict(Parameter(item.p3, fittable=True, fit=item.p3_refinement))
                        edExperimentBlock['params']['_pd_instr_reflex_asymmetry_p4'] = dict(Parameter(item.p4, fittable=True, fit=item.p4_refinement))

                    # Phases section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1Phase.PhaseL:
                        edPhases = []
                        cryspyPhases = item.items
                        for cryspyPhase in cryspyPhases:
                            edPhase = {}
                            edPhase['_label'] = dict(Parameter(cryspyPhase.label))
                            edPhase['_scale'] = dict(Parameter(cryspyPhase.scale, fittable=True, fit=cryspyPhase.scale_refinement))
                            edPhases.append(edPhase)
                        edExperimentBlock['loops']['Phase'] = edPhases

                    # Background section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_background.PdBackgroundL:
                        edBkgPoints = []
                        cryspyBkgPoints = item.items
                        for cryspyBkgPoint in cryspyBkgPoints:
                            edBkgPoint = {}
                            edBkgPoint['_2theta'] = dict(Parameter(cryspyBkgPoint.ttheta))
                            edBkgPoint['_intensity'] = dict(Parameter(cryspyBkgPoint.intensity, fittable=True, fit=cryspyBkgPoint.intensity_refinement))
                            edBkgPoints.append(edBkgPoint)
                        edExperimentBlock['loops']['_pd_background'] = edBkgPoints

                    # Measured data section
                    elif type(item) == cryspy.C_item_loop_classes.cl_1_pd_meas.PdMeasL:
                        cryspyMeasPoints = item.items
                        xArray = [point.ttheta for point in cryspyMeasPoints]
                        yMeasArray = [point.intensity for point in cryspyMeasPoints]
                        xArray = np.array(xArray)
                        yMeasArray = np.array(yMeasArray)
                        # Background
                        yBkgArrayInterpolated = np.zeros_like(xArray)
                        if '_pd_background' in edExperimentBlock['loops'].keys():
                            bkg = edExperimentBlock['loops']['_pd_background']
                            xBkgArray = [point['_2theta']['value'] for point in bkg]
                            yBkgArray = [point['_intensity']['value'] for point in bkg]
                            yBkgArrayInterpolated = np.interp(xArray, xBkgArray, yBkgArray)
                        # Ranges (for charts)
                        xMin = dict(Parameter(float(xArray.min())))
                        xMax = dict(Parameter(float(xArray.max())))
                        yMin = float(yMeasArray.min())
                        yMax = float(yMeasArray.max())
                        yRange = yMax - yMin
                        yExtra = yRange * 0.1
                        yMin = dict(Parameter(yMin - yExtra))
                        yMax = dict(Parameter(yMax + yExtra))
                        self.chartRanges.append({'xMin': xMin,
                                                 'xMax': xMax,
                                                 'yMin': yMin,
                                                 'yMax': yMax})
                        self.chartRangesChanged.emit()

                edDict['experiments'].append(edExperimentBlock)

                self.addDataBlock(edExperimentBlock)
                self.addXArray(xArray)
                self.addYMeasArray(yMeasArray)
                self.addYBkgArray(yBkgArrayInterpolated)

    def editEdDictByCryspyDictPath(self):
        pass


    def editEdDictByPath(self):
        pass


    def editCryspyDictByEdDictPath(self):
        pass

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


