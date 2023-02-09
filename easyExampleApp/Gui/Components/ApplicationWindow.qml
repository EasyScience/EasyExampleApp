// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Animations as EaAnimations
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals
import Gui.Components as ExComponents


EaComponents.ApplicationWindow {

    appName: ExGlobals.Configs.appConfig.name
    appVersion: ExGlobals.Configs.appConfig.version
    appDate: ExGlobals.Configs.appConfig.date

    opacity: ExGlobals.Variables.splashScreenAnimoFinished ? 1 : 0
    Behavior on opacity { EaAnimations.ThemeChange {} }

    onClosing: Qt.quit()

    Component.onCompleted: {
        print("Application window loaded:", this)
        ExGlobals.Variables.applicationWindowCreated = true
    }
    Component.onDestruction: print("Application window destroyed:", this)

    ///////////////////
    // APPLICATION BAR
    ///////////////////

    // Left group of application bar tool buttons
    appBarLeftButtons: [

        EaElements.ToolButton {
            enabled: false
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
            enabled: ExGlobals.Variables.homePageEnabled
            fontIcon: "backspace"
            ToolTip.text: qsTr("Reset to initial state without project, model and data")
            onClicked: {
                appBarCentralTabs.setCurrentIndex(0)
                ExGlobals.Variables.projectPageEnabled = false
                ExGlobals.Variables.modelPageEnabled = false
                ExGlobals.Variables.experimentPageEnabled = false
                ExGlobals.Variables.analysisPageEnabled = false
                ExGlobals.Variables.summaryPageEnabled = false
            }
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
            fontIcon: "question-circle"
            ToolTip.text: qsTr("Get online help")
            onClicked: Qt.openUrlExternally(ExGlobals.Configs.appConfig.homePageUrl)
        },

        EaElements.ToolButton {
            fontIcon: "bug"
            ToolTip.text: qsTr("Report a bug or issue")
            onClicked: Qt.openUrlExternally(ExGlobals.Configs.appConfig.issuesUrl)
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
            Component.onCompleted: homePageLoader.source = 'Pages/Home/Page.qml'
        },

        // Project tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.projectPageEnabled
            fontIcon: "archive"
            text: qsTr("Project")
            ToolTip.text: qsTr("Project description page")
            onEnabledChanged: enabled ?
                                  projectPageLoader.source = 'Pages/Project/PageStructure.qml' :
                                  projectPageLoader.source = ''
            Component.onCompleted: ExGlobals.References.projectAppbarButton = this
        },

        // Model tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.modelPageEnabled
            fontIcon: "gem"
            text: qsTr("Model")
            ToolTip.text: qsTr("Model description page")
            onEnabledChanged: enabled ?
                                  modelPageLoader.source = 'Pages/Model/PageStructure.qml' :
                                  modelPageLoader.source = ''
            Component.onCompleted: ExGlobals.References.modelAppbarButton = this
        },

        // Experiment tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.experimentPageEnabled
            fontIcon: "microscope"
            text: qsTr("Experiment")
            ToolTip.text: qsTr("Experimental settings and measured data page")
            onEnabledChanged: enabled ?
                                  experimentPageLoader.source = 'Pages/Experiment/PageStructure.qml' :
                                  experimentPageLoader.source = ''
            Component.onCompleted: ExGlobals.References.experimentAppbarButton = this
        },

        // Analysis tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.analysisPageEnabled
            fontIcon: "calculator"
            text: qsTr("Analysis")
            ToolTip.text: qsTr("Simulation and fitting page")
            onEnabledChanged: enabled ?
                                  analysisPageLoader.source = 'Pages/Analysis/PageStructure.qml' :
                                  analysisPageLoader.source = ''
            Component.onCompleted: ExGlobals.References.analysisAppbarButton = this
        },

        // Summary tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.summaryPageEnabled
            fontIcon: "clipboard-list"
            text: qsTr("Summary")
            ToolTip.text: qsTr("Summary of the work done")
            onEnabledChanged: enabled ?
                                  summaryPageLoader.source = 'Pages/Summary/PageStructure.qml' :
                                  summaryPageLoader.source = ''
            onCheckedChanged: checked ?
                                  ExGlobals.Proxies.miscProxy.project.summaryGenerated = true :
                                  ExGlobals.Proxies.miscProxy.project.summaryGenerated = false
            Component.onCompleted: ExGlobals.References.summaryAppbarButton = this
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
