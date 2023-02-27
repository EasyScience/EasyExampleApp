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

import Gui.Globals as Globals
import Gui.Components as Components


EaComponents.ContentPage {
    defaultInfo: Globals.Proxies.main.model.isCreated ?
                     "" :
                     qsTr("No analysis done")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton {
                text: Globals.Proxies.main.experiment.isCreated ?
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
            Globals.Vars.summaryPageEnabled = true
            Globals.Refs.app.appbar.summaryButton.toggle()
        }

        Component.onCompleted: Globals.Refs.app.analysisPage.continueButton = continueButton
    }

    Component.onCompleted: print("Analysis page loaded:", this)
    Component.onDestruction: print("Analysis page destroyed:", this)
}
