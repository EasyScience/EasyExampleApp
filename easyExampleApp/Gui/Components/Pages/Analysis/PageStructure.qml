// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
//import QtQuick.XmlListModel 2.15

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.ContentPage {
    defaultInfo: ExGlobals.Proxies.mainProxy.project.projectCreated ?
                     "" :
                     qsTr("No Analysis Done")

    mainView: EaComponents.MainContent {
        tabs: [
        ]

        items: [
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
