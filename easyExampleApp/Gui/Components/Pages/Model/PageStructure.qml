// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals
import Gui.Components as ExComponents


EaComponents.ContentPage {
    defaultInfo: ExGlobals.Proxies.mainProxy.model.isCreated ?
                     "" :
                     qsTr("No models added")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton { text: qsTr("Model view 1D") }
        ]

        items: [
            Loader { source: 'MainContent/ModelView1dTab.qml' }
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

        continueButton.enabled: ExGlobals.Proxies.mainProxy.model.isCreated

        continueButton.onClicked: {
            ExGlobals.Variables.experimentPageEnabled = true
            ExGlobals.References.experimentAppbarButton.toggle()
        }
    }

    Component.onCompleted: print("Model page loaded:", this)
    Component.onDestruction: print("Model page destroyed:", this)
}
