// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


EaCharts.Plotly1dMeasVsCalc {
    useWebGL: EaGlobals.Variables.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

    xAxisTitle: "x"
    yAxisTitle: "y"

    // Data is set in python backend

    onLoadSucceededStatusChanged: {
        if (loadSucceededStatus) {
            Globals.Proxies.main.analysis.created = true
        }
    }

    Component.onCompleted: {
        Globals.Refs.app.analysisPage.plotView = this
        Globals.Proxies.main.plotting.setAppPlotlyChartRef('analysisPage', this)
    }

}

