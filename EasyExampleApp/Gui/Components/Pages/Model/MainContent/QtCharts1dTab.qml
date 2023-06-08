// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


EaCharts.QtCharts1dMeasVsCalc {
    useOpenGL: EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

    xAxisTitle: "x"
    yAxisTitle: "y"

    xMin: parameterValue('xMin')
    xMax: parameterValue('xMax')
    yMin: parameterValue('yMin')
    yMax: parameterValue('yMax')

    calcSerieColor: EaStyle.Colors.chartForegroundsExtra[Globals.Proxies.main.model.currentIndex]

    // Data is set in python backend

    Component.onCompleted: {
        Globals.Refs.app.modelPage.plotView = this
        Globals.Proxies.main.plotting.setQtChartsSerieRef('modelPage',
                                                          'calcSerie',
                                                          this.calcSerie)
    }

    // Logic

    function parameterValue(name) {
        if (!Globals.Proxies.main.experiment.defined) {
            return ''
        }
        const currentExperimentIndex = Globals.Proxies.main.experiment.currentIndex
        const value = Globals.Proxies.main.experiment.chartRanges[currentExperimentIndex][name].value
        const formattedValue = value.toFixed(4)
        return formattedValue
    }

}
