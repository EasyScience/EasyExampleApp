// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
import QtCharts

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
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
    property real residualToMainChartHeightRatio: 0.33
    property real mainChartHeightCoeff: 1 - residualToMainChartHeightRatio

    property bool useOpenGL: EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

    //property alias

    Column {
        width: parent.width
        height: parent.height - 3 * EaStyle.Sizes.fontPixelSize + 2

        // Main chart container
        Item {
            width: parent.width
            height: parent.height * mainChartHeightCoeff

            EaCharts.QtCharts1dBase {
                id: mainChart

                useOpenGL: container.useOpenGL

                axisX.title: "2θ (degree)"
                axisX.titleVisible: false
                axisX.labelsVisible: false
                axisX.min: parameterValue('xMin')
                axisX.max: parameterValue('xMax')
                axisX.onRangeChanged: alignAllCharts()

                axisY.title: "Imeas, Icalc, Ibkg"
                axisY.min: parameterValue('yMin')
                axisY.max: parameterValue('yMax')
                axisY.onRangeChanged: adjustResidualChartRangeY()

                backgroundColor: "transparent"
                plotAreaColor: "transparent"

                // Measured points
                /*
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
                */
                LineSeries {
                    id: measSerie

                    axisX: mainChart.axisX
                    axisY: mainChart.axisY

                    useOpenGL: mainChart.useOpenGL

                    color: EaStyle.Colors.chartForegroundsExtra[2]
                    width: 2
                }

                // Background curve
                LineSeries {
                    id: bkgSerie

                    axisX: mainChart.axisX
                    axisY: mainChart.axisY

                    useOpenGL: mainChart.useOpenGL

                    color: EaStyle.Colors.chartForegrounds[1]
                    width: 1
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
            width: parent.width
            height: parent.height * residualToMainChartHeightRatio

            EaCharts.QtCharts1dBase {
                id: residualChart

                useOpenGL: container.useOpenGL

                axisX.min: mainChart.axisX.min
                axisX.max: mainChart.axisX.max
                axisY.min: Globals.Proxies.main.plotting.chartRanges.yMin
                axisY.max: Globals.Proxies.main.plotting.chartRanges.yMax

                axisX.titleVisible: false
                axisX.labelsVisible: false
                axisY.title: 'Imeas - Icalc'

                axisY.tickType: ValueAxis.TicksFixed
                axisY.tickCount: 3

                backgroundColor: "transparent"
                plotAreaColor: "transparent"

                LineSeries {
                    id: residSerie

                    axisX: residualChart.axisX
                    axisY: residualChart.axisY

                    useOpenGL: residualChart.useOpenGL

                    color: EaStyle.Colors.chartForegrounds[2]
                }
            }
        }
    }

    // X-axis chart container
    Item {
        z: -1
        width: parent.width
        height: container.height
        parent: container.parent

        EaCharts.QtCharts1dBase {
            id: xAxisChart

            axisX.title: mainChart.xAxisTitle
            axisX.min: mainChart.axisX.min
            axisX.max: mainChart.axisX.max
            axisX.lineVisible: false
            axisX.gridVisible: false

            axisY.titleVisible: false
            axisY.labelsVisible: false
            axisY.visible: false

            LineSeries {
                axisX: xAxisChart.axisX
                axisY: xAxisChart.axisY

                Component.onCompleted: initialChartsSetupTimer.start()

                Timer {
                    id: initialChartsSetupTimer
                    interval: 50
                    onTriggered: {
                        alignAllCharts()
                        adjustResidualChartRangeY()
                    }
                }
            }
        }
    }

    // Legend
    Rectangle {
        parent: container.parent

        x: mainChart.plotArea.x + mainChart.plotArea.width - width - 12 - EaStyle.Sizes.fontPixelSize
        y: mainChart.plotArea.y - 12 + EaStyle.Sizes.fontPixelSize
        width: childrenRect.width
        height: childrenRect.height

        color: EaStyle.Colors.mainContentBackgroundHalfTransparent
        border.color: EaStyle.Colors.chartGridLine

        Column {
            leftPadding: EaStyle.Sizes.fontPixelSize
            rightPadding: EaStyle.Sizes.fontPixelSize
            topPadding: EaStyle.Sizes.fontPixelSize * 0.5
            bottomPadding: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.Label {
                text: '▬ Imeas (measured)'
                color: measSerie.color
            }
            EaElements.Label {
                text: '▬ Icalc (calculated)'
                color: calcSerie.color
            }
            EaElements.Label {
                text: '▬ Ibkg (background)'
                color: bkgSerie.color
            }
            EaElements.Label {
                text: '▬ Imeas - Icalc (residual)'
                color: residSerie.color
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

    function residualChartMeanY() {
        return 0
    }

    function residualChartHalfRangeY() {
        if (mainChart.plotArea.height === 0) {
            return 0.5
        }

        const mainChartRangeY = mainChart.axisY.max - mainChart.axisY.min
        const residualToMainChartHeightRatio = residualChart.plotArea.height / mainChart.plotArea.height
        const residualChartRangeY = mainChartRangeY * residualToMainChartHeightRatio
        return 0.5 * residualChartRangeY
    }

    function adjustResidualChartRangeY() {
        residualChart.axisY.min = residualChartMeanY() - residualChartHalfRangeY()
        residualChart.axisY.max = residualChartMeanY() + residualChartHalfRangeY()
        console.debug('Residual chart Y-range has been adjusted')
    }

    function alignAllCharts() {
        xAxisChart.plotArea.width -= mainChart.plotArea.x - xAxisChart.plotArea.x
        xAxisChart.plotArea.x = mainChart.plotArea.x
        residualChart.plotArea.width = xAxisChart.plotArea.width
        residualChart.plotArea.x = mainChart.plotArea.x
        mainChart.plotArea.width = xAxisChart.plotArea.width
        console.debug('All charts have been aligned')
    }

}
