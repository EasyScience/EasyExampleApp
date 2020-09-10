import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Get started")
        collapsible: false

        EaElements.SideBarButton {
            fontIcon: "plus-circle"
            text: qsTr("Create a new project")
            onClicked: {
                ExGlobals.Variables.samplePageEnabled = true
                ExGlobals.Variables.projectCreated = true
            }
        }
    }

    EaElements.GroupBox {
        title: qsTr("Test Group")
        collapsed: false

        Grid {
            columns: 1
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label { text: "First Parameter: 200" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Parameter: 100" }
            EaElements.Label { text: "Last Parameter: 300" }
        }
    }

}

