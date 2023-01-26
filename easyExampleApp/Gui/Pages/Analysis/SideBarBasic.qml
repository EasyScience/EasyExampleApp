import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        id: groupBox

        title: qsTr("Fit parameters")
        visible: ExGlobals.Variables.analysisPageEnabled
        collapsible: false

        ExComponents.FitablesView {}

        EaElements.SideBarButton {
            id: startFittingButton
            fontIcon: "play-circle"
            text: qsTr("Start fitting")
            onClicked: {
                ExGlobals.Variables.summaryPageEnabled = true
                ExGlobals.Constants.proxy.startFitting()
            }
            Component.onCompleted: ExGlobals.Variables.startFittingButton = startFittingButton
        }
    }

    Component.onCompleted: ExGlobals.Constants.proxy.updateCalculatedData()

}
