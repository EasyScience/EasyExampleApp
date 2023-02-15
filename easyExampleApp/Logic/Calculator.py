# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import math


class Calculator:

    @staticmethod
    def sine(x, amplitude, period, phaseShift, verticalShift):
        res = amplitude * math.sin( 2 * math.pi / period * (x + phaseShift) ) + verticalShift
        return res
