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
    defaultInfo: ExGlobals.Proxies.mainProxy.project.experimentsLoaded ?
                     "" :
                     qsTr("No Experiments Loaded")

    mainView: EaComponents.MainContent {
        tabs: [
            EaElements.TabButton { text: qsTr("Plot View 1D") },
            EaElements.TabButton { text: qsTr("Plot View 2D") },
            EaElements.TabButton { text: qsTr("Plot View 3D (surface)") },
            EaElements.TabButton { text: qsTr("Plot View 3D (scatter)") }
        ]

        items: [
            Loader { source: 'MainContent/PlotView1dTab.qml' },
            Loader { source: 'MainContent/PlotView2dTab.qml' },
            Loader { source: 'MainContent/PlotViewSurface3dTab.qml' },
            Loader { source: 'MainContent/PlotViewScatter3dTab.qml' }
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

        continueButton.text: ExGlobals.Proxies.mainProxy.project.experimentsLoaded ?
                                 qsTr("Continue") :
                                 qsTr("Continue without experiment data")

        continueButton.onClicked: {
            ExGlobals.Variables.analysisPageEnabled = true
            ExGlobals.References.analysisAppbarButton.toggle()
        }
    }

    Component.onCompleted: print("Experiment page loaded:", this)
    Component.onDestruction: print("Experiment page destroyed:", this)
}
