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

/*
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
*/

    //Column {
    Rectangle {


        id: container
        //width:500
        //height:500

        property alias measSerie: measSerie
        property alias bkgSerie: bkgSerie
        property alias calcSerie: calcSerie
        property alias residSerie: residSerie

        property string calcSerieColor: EaStyle.Colors.chartForegrounds[0]

        property int extraMargin: -12
        property real residualToMainChartHeightRatio: 0.5//0.33
        property real mainChartHeightCoeff: 1 - residualToMainChartHeightRatio

        property bool useOpenGL: EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d



        //width: parent.width
        //height: parent.height - 3 * EaStyle.Sizes.fontPixelSize + 2

        width: 500
        height: 500

        //anchors.fill: parent

        ///////////////////////////////////////////
        // Main chart container: Imeas, Icalc, Ibkg
        ///////////////////////////////////////////

//        Item {
//            width: parent.width
//            height: parent.height * mainChartHeightCoeff -
//                    braggPeaksChart.parent.height * 0.5

            EaCharts.QtCharts1dBase {
                id: mainChart

//                anchors.bottomMargin: -12 - EaStyle.Sizes.fontPixelSize
//                width: parent.width
                height: parent.height * mainChartHeightCoeff -
                        braggPeaksChart.height * 0.5
//                height: 200


                anchors.top: parent.top
                anchors.bottom: braggPeaksChart.top
                anchors.left: parent.left
                anchors.right: parent.right

//                 anchors.margins: -12
//                 anchors.bottomMargin: -12

                anchors.topMargin: -12
                anchors.leftMargin: -12
                anchors.rightMargin: -12
                anchors.bottomMargin: -12


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

                backgroundColor: 'red'//"transparent"
                plotAreaColor: 'red'//"transparent"

                // Measured curve
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
//        }

        //////////////////////////////////////
        // Bragg peaks chart container: Ibragg
        //////////////////////////////////////

//        Item {
//            z: -1
//            width: parent.width
//            height: 30
            //visible: false

            EaCharts.QtCharts1dBase {
                id: braggPeaksChart

                //visible: false

                width: parent.width
                height: 80

//                anchors.topMargin: -12 - EaStyle.Sizes.fontPixelSize * 1.5
//                anchors.bottomMargin: -12 - EaStyle.Sizes.fontPixelSize * 1.5

//                anchors.top: mainChart.bottom
                anchors.bottom: residualChart.top
                anchors.left: parent.left
                anchors.right: parent.right

                anchors.leftMargin: -12
                anchors.rightMargin: -12
                anchors.bottomMargin: -12

//                 anchors.margins: -12
//                anchors.bottomMargin: -12//-12

                useOpenGL: container.useOpenGL

                axisX.min: mainChart.axisX.min
                axisX.max: mainChart.axisX.max
                axisX.titleVisible: false
                axisX.labelsVisible: false

                axisY.min: -1
                axisY.max: 1
                axisY.titleVisible: false
                axisY.labelsVisible: false
                axisY.tickCount: 2

                backgroundColor: 'green'//"transparent"
                plotAreaColor: 'green'//"transparent"

                ScatterSeries {
                    id: braggPeaksSerie

                    axisX: braggPeaksChart.axisX
                    axisY: braggPeaksChart.axisY

                    useOpenGL: braggPeaksChart.useOpenGL

                    color: EaStyle.Colors.chartForegroundsExtra[0]

                    XYPoint {x: 0.6; y: 0}
                }
            }
//        }

        //////////////////////////////////////////
        // Residual chart container: Imeas - Icalc
        //////////////////////////////////////////

//        Item {
//            width: parent.width
//            height: parent.height * residualToMainChartHeightRatio -
//                    braggPeaksChart.parent.height * 0.5

            EaCharts.QtCharts1dBase {
                id: residualChart

//                anchors.topMargin: -12 - EaStyle.Sizes.fontPixelSize
//                width: parent.width
                height: parent.height * residualToMainChartHeightRatio -
                        braggPeaksChart.height * 0.5
//                height: 200

//                anchors.top: braggPeaksChart.bottom
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right

//                anchors.margins: -12

                anchors.bottomMargin: -12
                anchors.leftMargin: -12
                anchors.rightMargin: -12


                useOpenGL: container.useOpenGL

                axisX.min: mainChart.axisX.min
                axisX.max: mainChart.axisX.max
                axisX.titleVisible: false
                axisX.labelsVisible: false

                axisY.min: Globals.Proxies.main.plotting.chartRanges.yMin
                axisY.max: Globals.Proxies.main.plotting.chartRanges.yMax
                axisY.tickType: ValueAxis.TicksFixed
                axisY.tickCount: 3
                axisY.title: 'Imeas - Icalc'

                backgroundColor: 'blue'//"transparent"
                plotAreaColor: 'blue'//"transparent"

                LineSeries {
                    id: residSerie

                    axisX: residualChart.axisX
                    axisY: residualChart.axisY

                    useOpenGL: residualChart.useOpenGL

                    color: EaStyle.Colors.chartForegrounds[2]
                }
            }
//        }
    /*
    }
    */

    /////////////////////////
    // X-axis chart container
    /////////////////////////
/*
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
*/
    /////////
    // Legend
    /////////
/*
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
                text: '━  Imeas (measured)'
                color: measSerie.color
            }
            EaElements.Label {
                text: '━  Icalc (total calculated)'
                color: calcSerie.color
            }
            EaElements.Label {
                text: '─  Ibkg (background)'
                color: bkgSerie.color
            }
            EaElements.Label {
                text: '━  Imeas - Icalc (residual)'
                color: residSerie.color
            }
            EaElements.Label {
                text: '│  Ibragg (Bragg peaks)'
                color: braggPeaksSerie.color
            }
        }
    }
*/

    // Save references to chart series to be accessible from Python for updating data
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
        Globals.Proxies.main.plotting.setQtChartsSerieRef('analysisPage',
                                                          'braggSerie',
                                                          this.braggSerie)
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
        braggPeaksChart.plotArea.width = xAxisChart.plotArea.width
        braggPeaksChart.plotArea.x = mainChart.plotArea.x
        mainChart.plotArea.width = xAxisChart.plotArea.width
        console.debug('All charts have been aligned')
    }

}
