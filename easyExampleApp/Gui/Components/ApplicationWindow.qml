// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick 2.15
import QtQuick.Controls 2.15

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents


EaComponents.ApplicationWindow {

    ///////////////////
    // APPLICATION BAR
    ///////////////////

    // Left group of application bar tool buttons
    appBarLeftButtons: [

        EaElements.ToolButton {
            enabled: false
            highlighted: true
            fontIcon: "save"
            ToolTip.text: qsTr("Save current state of the project")
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: "undo"
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: "redo"
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: "backspace"
            ToolTip.text: qsTr("Reset to initial state without project, model and data")
        }

    ]

    // Right group of application bar tool buttons
    appBarRightButtons: [

        EaElements.ToolButton {
            fontIcon: "cog"
            ToolTip.text: qsTr("Application preferences")
            onClicked: EaGlobals.Variables.showAppPreferencesDialog = true
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: "question-circle"
            ToolTip.text: qsTr("Get online help")
            onClicked: Qt.openUrlExternally(ExGlobals.Constants.appUrl)
        },

        EaElements.ToolButton {
            fontIcon: "bug"
            ToolTip.text: qsTr("Report a bug or issue")
            onClicked: Qt.openUrlExternally(ExGlobals.Constants.appIssuesUrl)
        }

    ]

    // Central group of application bar tab buttons (workflow tabs)
    // Tab buttons for the pages described below
    appBarCentralTabs.contentData: [

        // Home tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.homePageEnabled
            fontIcon: "home"
            text: qsTr("Home")
            ToolTip.text: qsTr("Home page")
            Component.onCompleted: homePageLoader.source = 'Pages/Home/PageStructure.qml'
        },

        // Project tab
        EaElements.AppBarTabButton {
            id: projectTabButton

            enabled: ExGlobals.Variables.projectPageEnabled
            fontIcon: "archive"
            text: qsTr("Project")
            ToolTip.text: qsTr("Project description page")
            onCheckedChanged: checked ?
                                  projectPageLoader.source = 'Pages/Project/PageStructure.qml' :
                                  projectPageLoader.source = ''
            Component.onCompleted: ExGlobals.Variables.projectAppbarButton = this
        },

        // Model tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.modelPageEnabled
            fontIcon: "gem"
            text: qsTr("Model")
            ToolTip.text: qsTr("Model description page")
            onCheckedChanged: checked ?
                                  modelPageLoader.source = 'Pages/Model/PageStructure.qml' :
                                  modelPageLoader.source = ''
            Component.onCompleted: ExGlobals.Variables.modelAppbarButton = this
        },

        // Experiment tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.experimentPageEnabled
            fontIcon: "microscope"
            text: qsTr("Experiment")
            ToolTip.text: qsTr("Experimental settings and measured data page")
            onCheckedChanged: checked ?
                                  experimentPageLoader.source = 'Pages/Experiment/PageStructure.qml' :
                                  experimentPageLoader.source = ''
            Component.onCompleted: ExGlobals.Variables.experimentAppbarButton = this
        },

        // Analysis tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.analysisPageEnabled
            fontIcon: "calculator"
            text: qsTr("Analysis")
            ToolTip.text: qsTr("Simulation and fitting page")
            onCheckedChanged: checked ?
                                  analysisPageLoader.source = 'Pages/Analysis/PageStructure.qml' :
                                  analysisPageLoader.source = ''
            Component.onCompleted: ExGlobals.Variables.analysisAppbarButton = this
        },

        // Summary tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.summaryPageEnabled
            fontIcon: "clipboard-list"
            text: qsTr("Summary")
            ToolTip.text: qsTr("Summary of the work done")
            onCheckedChanged: checked ?
                                  summaryPageLoader.source = 'Pages/Summary/PageStructure.qml' :
                                  summaryPageLoader.source = ''
            Component.onCompleted: ExGlobals.Variables.summaryAppbarButton = this
        }

    ]

    //////////////////////
    // MAIN VIEW + SIDEBAR
    //////////////////////

    // Pages for the tab buttons described above
    contentArea: [
        Loader { id: homePageLoader },
        Loader { id: projectPageLoader },
        Loader { id: modelPageLoader },
        Loader { id: experimentPageLoader },
        Loader { id: analysisPageLoader },
        Loader { id: summaryPageLoader }
    ]

    /////////////
    // STATUS BAR
    /////////////

    statusBar: ExComponents.StatusBar {}

}
