// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals
import Gui.Components as Components


EaComponents.ContentPage {
    defaultInfo: Globals.Proxies.main.experiment.created ?
                     "" :
                     qsTr("No experiments loaded")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton { text: qsTr("Chart view") }
        ]

        items: [
            Loader { source: `MainContent/${EaGlobals.Vars.currentLib1d}1dTab.qml` }
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

        continueButton.text: Globals.Proxies.main.experiment.created ?
                                 qsTr("Continue") :
                                 qsTr("Continue without experiment data")

        continueButton.onClicked: {
            Globals.Vars.modelPageEnabled = true
            Globals.Refs.app.appbar.modelButton.toggle()
        }

        Component.onCompleted: Globals.Refs.app.experimentPage.continueButton = continueButton
    }

    Component.onCompleted: print("Experiment page loaded:", this)
    Component.onDestruction: print("Experiment page destroyed:", this)
}
