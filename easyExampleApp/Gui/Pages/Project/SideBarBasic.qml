import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Get started")
        collapsible: false

        EaElements.SideBarButton {
            id: createProjectButton
            fontIcon: "plus-circle"
            text: qsTr("Create a new project")
            onClicked: {
                ExGlobals.Variables.samplePageEnabled = true
                ExGlobals.Variables.projectCreated = true
            }
            Component.onCompleted: ExGlobals.Variables.createProjectButton = createProjectButton
        }
    }

    EaElements.GroupBox {
        title: qsTr("Test Group")
        //collapsed: false

        Grid {
            columns: 1
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label { text: qsTr("First Parameter: 200") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Parameter: 100") }
            EaElements.Label { text: qsTr("Last Parameter: 300") }
        }
    }

}

