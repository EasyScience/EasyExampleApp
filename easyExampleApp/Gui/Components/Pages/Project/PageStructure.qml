// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.3 as Dialogs1
import QtQuick.XmlListModel 2.15

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.ContentPage {
    defaultInfo: ExGlobals.Proxies.mainProxy.project.projectCreated ?
                     "" :
                     qsTr("No Project Created/Opened")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton { text: qsTr("Description") }
        ]

        items: [
            Loader { source: 'MainContent/DescriptionTab.qml' }
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
            ExGlobals.Variables.modelPageEnabled = true
            ExGlobals.References.modelAppbarButton.toggle()
        }
    }

    Component.onCompleted: print("Project page loaded:", this)
    Component.onDestruction: print("Project page destroyed:", this)
}
