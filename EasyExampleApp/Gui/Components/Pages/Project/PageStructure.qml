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
    defaultInfo: Globals.Proxies.main.project.isCreated ?
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

        continueButton.text: Globals.Proxies.main.project.isCreated ?
                                 qsTr("Continue") :
                                 qsTr("Continue without project")

        continueButton.onClicked: {            
            Globals.Vars.experimentPageEnabled = true
            Globals.Refs.app.appbar.experimentButton.toggle()
        }

        Component.onCompleted: Globals.Refs.app.projectPage.continueButton = continueButton
    }

    Component.onCompleted: print("Project page loaded:", this)
    Component.onDestruction: print("Project page destroyed:", this)
}
