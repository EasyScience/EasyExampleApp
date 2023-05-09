# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from EasyApp.Logic.Logging import console

try:
    import cryspy
    console.debug('CrysPy module has been imported')
except ImportError:
    console.debug('No CrysPy module has been found')

import numpy as np
console.debug('Numpy module has been imported')


class LineCalculator:

    @staticmethod
    def calculated(xArray, params):
        slope = params['slope']['value']
        yIntercept = params['yIntercept']['value']
        return slope * xArray + yIntercept

    @staticmethod
    def pseudoMeasured(xArray, params):
        np.random.seed(1)
        noise = np.random.uniform(-0.1, 0.1, size=xArray.size)
        return LineCalculator.calculated(xArray, params) + noise


class GaussianCalculator:

    @staticmethod
    def calculated(xArray, params):
        scale = params['scale']['value']
        shift = params['shift']['value']
        width = params['width']['value']
        return scale * np.exp(-np.square((xArray - shift) / (2 * width)))

    @staticmethod
    def pseudoMeasured(xArray, params):
        np.random.seed(1)
        noise = np.random.uniform(-0.05, 0.05, size=xArray.size)
        return GaussianCalculator.calculated(xArray, params) + noise
