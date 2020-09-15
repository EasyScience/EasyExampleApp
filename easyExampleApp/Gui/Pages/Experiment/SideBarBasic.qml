import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Measured data")
        collapsible: false

        EaElements.SideBarButton {
            id: generateMeasuredDataButton
            fontIcon: "plus-circle"
            text: "Generate measured data"
            onClicked: {
                ExGlobals.Variables.analysisPageEnabled = true
                ExGlobals.Variables.experimentLoaded = true
                ExGlobals.Variables.proxy.generateMeasuredData()
            }
            Component.onCompleted: ExGlobals.Variables.generateMeasuredDataButton = generateMeasuredDataButton
        }
    }

    EaElements.GroupBox {
        title: qsTr("Instrumental parameters")
        //visible: ExGlobals.Variables.analysisPageEnabled
        enabled: ExGlobals.Variables.experimentLoaded
        //collapsed: false

        Grid {
            columns: 4
            columnSpacing: 20
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.Label {
                text: "X-shift"
            }

            EaElements.TextField {
                width: 140
                text: parseFloat(ExGlobals.Variables.proxy.xShift).toFixed(2)
                onEditingFinished: ExGlobals.Variables.proxy.xShift = text
            }

            EaElements.Label {
                text: "Y-shift"
            }

            EaElements.TextField {
                width: 140
                text: parseFloat(ExGlobals.Variables.proxy.yShift).toFixed(2)
                onEditingFinished: ExGlobals.Variables.proxy.yShift = text
            }
        }
    }

}

