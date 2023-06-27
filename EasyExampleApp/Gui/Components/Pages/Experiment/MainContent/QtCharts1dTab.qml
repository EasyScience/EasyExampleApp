// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


Rectangle {
    color: EaStyle.Colors.chartBackground

    EaCharts.QtCharts1dMeasVsCalc {
        id: chartView

        anchors.topMargin: EaStyle.Sizes.toolButtonHeight - EaStyle.Sizes.fontPixelSize - 1

        useOpenGL: EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

        axisX.title: "2θ (degree)"
        axisX.min: parameterValue('xMin')
        axisX.max: parameterValue('xMax')
        axisX.minAfterReset: parameterValue('xMin')
        axisX.maxAfterReset: parameterValue('xMax')

        axisY.title: "Imeas, Ibkg"
        axisY.min: parameterValue('yMin')
        axisY.max: parameterValue('yMax')
        axisY.minAfterReset: parameterValue('yMin')
        axisY.maxAfterReset: parameterValue('yMax')

        measSerie.onHovered: (point, state) => showMainTooltip(chartView, point, state)
        bkgSerie.onHovered: (point, state) => showMainTooltip(chartView, point, state)

        // Tool buttons
        Row {
            id: toolButtons

            x: chartView.plotArea.x + chartView.plotArea.width - width
            y: chartView.plotArea.y - height - EaStyle.Sizes.fontPixelSize

            spacing: 0.25 * EaStyle.Sizes.fontPixelSize

            EaElements.TabButton {
                checked: Globals.Vars.showLegendOnExperimentPage
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "align-left"
                ToolTip.text: Globals.Vars.showLegendOnExperimentPage ?
                                  qsTr("Hide legend") :
                                  qsTr("Show legend")
                onClicked: Globals.Vars.showLegendOnExperimentPage = checked
            }

            EaElements.TabButton {
                checked: chartView.allowHover
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "comment-alt"
                ToolTip.text: qsTr("Show coordinates tooltip on hover")
                onClicked: chartView.allowHover = !chartView.allowHover
            }

            Item { height: 1; width: 0.5 * EaStyle.Sizes.fontPixelSize }  // spacer

            EaElements.TabButton {
                checked: !chartView.allowZoom
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "arrows-alt"
                ToolTip.text: qsTr("Enable pan")
                onClicked: chartView.allowZoom = !chartView.allowZoom
            }

            EaElements.TabButton {
                checked: chartView.allowZoom
                autoExclusive: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "expand"
                ToolTip.text: qsTr("Enable box zoom")
                onClicked: chartView.allowZoom = !chartView.allowZoom
            }

            EaElements.TabButton {
                checkable: false
                height: EaStyle.Sizes.toolButtonHeight
                width: EaStyle.Sizes.toolButtonHeight
                borderColor: EaStyle.Colors.chartAxis
                fontIcon: "backspace"
                ToolTip.text: qsTr("Reset axes")
                onClicked: chartView.resetAxes()
            }

        }
        // Tool buttons

        // Legend
        Rectangle {
            visible: Globals.Vars.showLegendOnExperimentPage

            x: chartView.plotArea.x + chartView.plotArea.width - width - EaStyle.Sizes.fontPixelSize
            y: chartView.plotArea.y + EaStyle.Sizes.fontPixelSize
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
                    color: chartView.measSerie.color
                }
                EaElements.Label {
                    text: '─  Ibkg (background)'
                    color: chartView.bkgSerie.color
                }
            }
        }
        // Legend

        // ToolTips
        EaElements.ToolTip {
            id: dataToolTip

            arrowLength: 0
            textFormat: Text.RichText
        }
        // ToolTips

        // Data is set in python backend

        Component.onCompleted: {
            Globals.Refs.app.experimentPage.plotView = chartView
            Globals.Proxies.main.plotting.setQtChartsSerieRef('experimentPage',
                                                              'measSerie',
                                                              chartView.measSerie)
            Globals.Proxies.main.plotting.setQtChartsSerieRef('experimentPage',
                                                              'bkgSerie',
                                                              chartView.bkgSerie)
        }

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

    function showMainTooltip(chart, point, state) {
        if (!chartView.allowHover) {
            return
        }
        const pos = chart.mapToPosition(Qt.point(point.x, point.y))
        dataToolTip.x = pos.x
        dataToolTip.y = pos.y
        dataToolTip.text = `<p align="left">x: ${point.x.toFixed(2)}<br\>y: ${point.y.toFixed(2)}</p>`
        dataToolTip.parent = chart
        dataToolTip.visible = state
    }

}

