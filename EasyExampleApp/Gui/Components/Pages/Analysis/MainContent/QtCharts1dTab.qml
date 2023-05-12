// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
import QtCharts

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


Column {
    id: container
    width:500
    height:500

    property alias measSerie: measSerie
    property alias bkgSerie: bkgSerie
    property alias calcSerie: calcSerie
    property alias residSerie: residSerie

    property string calcSerieColor: EaStyle.Colors.chartForegrounds[0]

    property int extraMargin: -12
    property real residChartHeightCoeff: 0.4
    property real mainChartHeightCoeff: 1 - residChartHeightCoeff

    property bool useOpenGL: EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

    //property alias

    // Main chart container
    Item {
        width: container.width
        height: container.height * mainChartHeightCoeff

        EaCharts.QtCharts1dBase {
            id: mainChart

            useOpenGL: container.useOpenGL

            xAxisTitle: "X"
            yAxisTitle: "Imeas, Icalc"

            xMin: -10
            xMax: 10
            yMin: 0
            yMax: 4

            xAxisTitleVisible: false
            xAxisLabelsVisible: false

            // Measured points
            ScatterSeries {
                id: measSerie

                axisX: mainChart.axisX
                axisY: mainChart.axisY

                useOpenGL: mainChart.useOpenGL

                markerSize: 5
                borderWidth: 1
                color: EaStyle.Colors.chartForegroundsExtra[2]
                borderColor: this.color
            }

            // Background curve
            LineSeries {
                id: bkgSerie

                axisX: mainChart.axisX
                axisY: mainChart.axisY

                useOpenGL: mainChart.useOpenGL

                color: EaStyle.Colors.chartForegrounds[1]
                width: 2
            }

            // Calculated curve
            LineSeries {
                id: calcSerie

                axisX: mainChart.axisX
                axisY: mainChart.axisY

                useOpenGL: mainChart.useOpenGL

                color: calcSerieColor
                width: 2
            }
        }
    }

    // Residual chart container
    Item {
        width: container.width
        height: container.height * residChartHeightCoeff

        EaCharts.QtCharts1dBase {
            id: residChart

            useOpenGL: container.useOpenGL

            xAxisTitle: mainChart.xAxisTitle
            yAxisTitle: 'Imeas - Icalc'
            xMin: mainChart.xMin
            xMax: mainChart.xMax
            yMin: -1
            yMax: 1

            LineSeries {
                id: residSerie

                axisX: residChart.axisX
                axisY: residChart.axisY

                useOpenGL: residChart.useOpenGL

                color: EaStyle.Colors.chartForegroundsExtra[2]
            }
        }
    }

    // Data is set in python backend

    Component.onCompleted: {
        Globals.Refs.app.analysisPage.plotView = this
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'measSerie',
                                                          this.measSerie)
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'bkgSerie',
                                                          this.bkgSerie)
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'totalCalcSerie',
                                                          this.calcSerie)
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'residSerie',
                                                          this.residSerie)
        Globals.Proxies.main.analysis.defined = true
    }

}
