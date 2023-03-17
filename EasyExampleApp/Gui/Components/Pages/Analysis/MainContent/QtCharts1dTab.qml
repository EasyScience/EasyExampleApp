// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


EaCharts.QtCharts1dMeasVsCalc {
    useOpenGL: EaGlobals.Variables.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

    xAxisTitle: "x"
    yAxisTitle: "y"

    xMin: 0
    xMax: 1
    yMin: -2
    yMax: 2

    // Data is set in python backend

    Component.onCompleted: {
        Globals.Refs.app.experimentPage.plotView = this
        Globals.Proxies.main.plotting.setAppQtChartsSerieRef('analysisPage',
                                                             'measSerie',
                                                             this.measSerie)
        Globals.Proxies.main.plotting.setAppQtChartsSerieRef('analysisPage',
                                                             'calcSerie',
                                                             this.calcSerie)

        Globals.Proxies.main.analysis.created = true
    }
}
