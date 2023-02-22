# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import random


class Calculator:

    @staticmethod
    def line(xArray, slope, yIntercept):
        return [slope * x + yIntercept for x in xArray]

    @staticmethod
    def lineMeas(xArray, slope, yIntercept):
        random.seed(1)
        return [slope * x + yIntercept + random.uniform(-0.1, 0.1) for x in xArray]