# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np

class LineCalculator:

    @staticmethod
    def calculated(xArray, slope, yIntercept):
        return slope * xArray + yIntercept

    @staticmethod
    def pseudoMeasured(xArray, slope, yIntercept):
        np.random.seed(1)
        return slope * xArray + yIntercept + np.random.uniform(-0.1, 0.1, size=xArray.size)
