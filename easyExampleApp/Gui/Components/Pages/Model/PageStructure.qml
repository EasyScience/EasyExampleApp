// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.ContentPage {
    defaultInfo: ExGlobals.Proxies.mainProxy.project.modelsAdded ?
                     "" :
                     qsTr("No Models Added")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton { text: qsTr("Structure View") }
        ]

        items: [
            Loader { source: 'MainContent/StructureView3dTab.qml' }
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

        continueButton.enabled: ExGlobals.Proxies.mainProxy.project.modelsAdded

        continueButton.onClicked: {
            ExGlobals.Variables.experimentPageEnabled = true
            ExGlobals.References.experimentAppbarButton.toggle()
        }
    }

    Component.onCompleted: print("Model page loaded:", this)
    Component.onDestruction: print("Model page destroyed:", this)
}
