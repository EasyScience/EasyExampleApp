// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
//import QtQuick.XmlListModel 2.15

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals
import Gui.Components as ExComponents


EaComponents.ContentPage {
    defaultInfo: ExGlobals.Proxies.mainProxy.model.modelsAdded ?
                     "" :
                     qsTr("No analysis done")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton {
                text: ExGlobals.Proxies.mainProxy.experiment.experimentsLoaded ?
                          qsTr("Fitting") :
                          qsTr("Simulation")
            }
        ]

        items: [
            Loader { source: 'MainContent/AnalysisTab.qml' }
        ]
    }

    sideBar: EaComponents.SideBar {
        tabs: [
            EaElements.TabButton { text: qsTr("Basic controls") },
            EaElements.TabButton { text: qsTr("Advanced controls") }
        ]

        items: [
            Loader { source: 'SideBarBasic.qml' },
            Loader { source: 'SideBarAdvanced.qml' }
        ]

        continueButton.onClicked: {
            ExGlobals.Variables.summaryPageEnabled = true
            ExGlobals.References.summaryAppbarButton.toggle()
        }
    }

    Component.onCompleted: print("Analysis page loaded:", this)
    Component.onDestruction: print("Analysis page destroyed:", this)
}
