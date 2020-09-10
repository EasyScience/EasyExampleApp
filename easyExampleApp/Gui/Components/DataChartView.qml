import QtQuick 2.13
import QtQuick.Controls 2.13
import QtCharts 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    property bool showMeasured: false
    property bool showCalculated: false
    property bool showDifference: false

    color: EaStyle.Colors.mainContentBackground

    EaCharts.ChartView {
        anchors.fill: parent

        EaCharts.ValueAxis {
            id: axisX

            titleText: "Time (s)"

            tickCount: 4

            min: 0
            max: Math.PI * (tickCount - 1)
        }

        EaCharts.ValueAxis {
            id: axisY

            titleText: "Signal (arb. units)"

            min: -6
            max: 6
        }

        EaCharts.AreaSeries {
            visible: showMeasured

            axisX: axisX
            axisY: axisY

            lowerSeries: LineSeries {
                id: lowerMeasuredSeries

                Component.onCompleted: ExGlobals.Variables.proxy.addLowerMeasuredSeriesRef(lowerMeasuredSeries)
            }

            upperSeries: LineSeries {
                id: upperMeasuredSeries

                Component.onCompleted: ExGlobals.Variables.proxy.addUpperMeasuredSeriesRef(upperMeasuredSeries)
            }
        }

        EaCharts.LineSeries {
            id: calculatedSeries

            visible: showCalculated

            axisX: axisX
            axisY: axisY

            Component.onCompleted: {
                if (visible) {
                    ExGlobals.Variables.proxy.setCalculatedSeriesRef(calculatedSeries)
                }
            }
        }
    }
}


