import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Sample data")
        collapsible: false

        EaElements.SideBarButton {
            id: addNewSampleButton
            fontIcon: "plus-circle"
            text: "Add new sample"
            onClicked: {
                ExGlobals.Variables.experimentPageEnabled = true
                ExGlobals.Variables.sampleLoaded = true
            }
            Component.onCompleted: ExGlobals.Variables.addNewSampleButton = addNewSampleButton
        }
    }

    EaElements.GroupBox {
        id: sampleParametersGroup
        title: qsTr("Sample parameters")
        //visible: ExGlobals.Variables.experimentPageEnabled
        enabled: ExGlobals.Variables.sampleLoaded
        //collapsed: false

        Component.onCompleted: ExGlobals.Variables.sampleParametersGroup = sampleParametersGroup

        Grid {
            columns: 4
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label {
                text: "Amplitude"
            }

            EaElements.TextField {
                id: amplitudeTextInput
                width: 130
                text: parseFloat(ExGlobals.Constants.proxy.amplitude).toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.amplitude = text
                Component.onCompleted: ExGlobals.Variables.amplitudeTextInput = amplitudeTextInput
            }

            EaElements.Label {
                text: "Period"
            }

            EaElements.TextField {
                id: periodTextInput
                width: 130
                text: parseFloat(ExGlobals.Constants.proxy.period).toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.period = text
                Component.onCompleted: ExGlobals.Variables.periodTextInput = periodTextInput
            }
        }


        Grid {
            columns: 4
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label {
                text: "amplitude"
            }

            EaElements.TextField {
                width: 130
                text: ExGlobals.Constants.proxy.fitablesDict.amplitude.toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.editFitableValueByName("amplitude", text)
            }

            EaElements.Label {
                text: "period"
            }

            EaElements.TextField {
                width: 130
                text: ExGlobals.Constants.proxy.fitablesDict.period.toFixed(4)
                onEditingFinished: ExGlobals.Constants.proxy.editFitableValueByName("period", text)
            }
        }
    }


}
