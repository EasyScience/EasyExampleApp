// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as ExGlobals


EaCharts.Plotly1dMeasVsCalc {

    xAxisTitle: "x"
    yAxisTitle: "y"

    calculatedXYData: ExGlobals.Proxies.mainProxy.model.calculatedDataObj

}

