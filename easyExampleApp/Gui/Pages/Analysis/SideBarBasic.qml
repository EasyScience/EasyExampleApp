import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    /*
    EaElements.GroupBox {
        title: qsTr("Measured data")
        collapsible: false

        EaElements.SideBarButton {
            fontIcon: "plus-circle"
            text: "Generate measured data"
            onClicked: ExGlobals.Variables.proxy.generateMeasuredData()
            Component.onCompleted: ExGlobals.Variables.proxy.generateMeasuredData()
        }
    }
    */

    EaElements.GroupBox {
        title: qsTr("Fit parameters")
        visible: ExGlobals.Variables.analysisPageEnabled
        collapsed: false

        Grid {
            columns: 4
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label {
                text: "Amplitude"
            }

            EaElements.TextField {
                width: 130
                text: parseFloat(ExGlobals.Variables.proxy.amplitude).toFixed(2)
                onEditingFinished: ExGlobals.Variables.proxy.amplitude = text
            }

            EaElements.Label {
                text: "Period"
            }

            EaElements.TextField {
                width: 130
                text: parseFloat(ExGlobals.Variables.proxy.period).toFixed(2)
                onEditingFinished: ExGlobals.Variables.proxy.period = text
            }

            EaElements.Label {
                text: "X-shift"
            }

            EaElements.TextField {
                id: xShiftTextInput
                width: 130
                text: parseFloat(ExGlobals.Variables.proxy.xShift).toFixed(2)
                onEditingFinished: ExGlobals.Variables.proxy.xShift = text
                Component.onCompleted: ExGlobals.Variables.xShiftTextInput = xShiftTextInput
            }

            EaElements.Label {
                text: "Y-shift"
            }

            EaElements.TextField {
                id: yShiftTextInput
                width: 130
                text: parseFloat(ExGlobals.Variables.proxy.yShift).toFixed(2)
                onEditingFinished: ExGlobals.Variables.proxy.yShift = text
                Component.onCompleted: ExGlobals.Variables.yShiftTextInput = yShiftTextInput
            }
        }

        EaElements.SideBarButton {
            id: startFittingButton
            fontIcon: "play-circle"
            text: "Start fitting"
            onClicked: {
                ExGlobals.Variables.summaryPageEnabled = true
                ExGlobals.Variables.proxy.startFitting()
            }
            Component.onCompleted: ExGlobals.Variables.startFittingButton = startFittingButton
        }
    }

    Component.onCompleted: ExGlobals.Variables.proxy.updateCalculatedData()

}
