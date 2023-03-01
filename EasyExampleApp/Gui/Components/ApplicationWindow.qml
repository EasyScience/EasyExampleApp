// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Animations as EaAnimations
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals
import Gui.Components as Components


EaComponents.ApplicationWindow {

    appName: Globals.Configs.appConfig.name
    appVersion: Globals.Configs.appConfig.version
    appDate: Globals.Configs.appConfig.date

    //opacity: Globals.Vars.splashScreenAnimoFinished ? 1 : 0
    //Behavior on opacity { EaAnimations.ThemeChange {} }

    onClosing: Qt.quit()

    Component.onCompleted: {
        print("Application window loaded:", this)
        Globals.Vars.applicationWindowCreated = true
    }
    Component.onDestruction: print("Application window destroyed:", this)

    ///////////////////
    // APPLICATION BAR
    ///////////////////

    // Left group of application bar tool buttons
    appBarLeftButtons: [

        EaElements.ToolButton {
            enabled: Globals.Proxies.main.project.isCreated &&
                    Globals.Proxies.main.project.needSave
            highlighted: true
            fontIcon: "save"
            ToolTip.text: qsTr("Save current state of the project")
            onClicked: Globals.Proxies.main.project.save()
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
            enabled: Globals.Vars.homePageEnabled
            fontIcon: "backspace"
            ToolTip.text: qsTr("Reset to initial state without project, model and data")
            onClicked: {
                appBarCentralTabs.setCurrentIndex(0)
                Globals.Vars.projectPageEnabled = false
                Globals.Vars.modelPageEnabled = false
                Globals.Vars.experimentPageEnabled = false
                Globals.Vars.analysisPageEnabled = false
                Globals.Vars.summaryPageEnabled = false
            }
            Component.onCompleted: Globals.Refs.app.appbar.resetStateButton = this
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
            onClicked: Qt.openUrlExternally(Globals.Configs.appConfig.homePageUrl)
        },

        EaElements.ToolButton {
            fontIcon: "bug"
            ToolTip.text: qsTr("Report a bug or issue")
            onClicked: Qt.openUrlExternally(Globals.Configs.appConfig.issuesUrl)
        }

    ]

    // Central group of application bar tab buttons (workflow tabs)
    // Tab buttons for the pages described below
    appBarCentralTabs.contentData: [

        // Home tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.homePageEnabled
            fontIcon: "home"
            text: qsTr("Home")
            ToolTip.text: qsTr("Home page")
            Component.onCompleted: {
                homePageLoader.source = 'Pages/Home/Page.qml'
                Globals.Refs.app.appbar.homeButton = this
            }
        },

        // Project tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.projectPageEnabled
            fontIcon: "archive"
            text: qsTr("Project")
            ToolTip.text: qsTr("Project description page")
            onEnabledChanged: enabled ?
                                  projectPageLoader.source = 'Pages/Project/PageStructure.qml' :
                                  projectPageLoader.source = ''
            Component.onCompleted: Globals.Refs.app.appbar.projectButton = this
        },

        // Experiment tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.experimentPageEnabled
            fontIcon: "microscope"
            text: qsTr("Experiment")
            ToolTip.text: qsTr("Experimental settings and measured data page")
            onEnabledChanged: enabled ?
                                  experimentPageLoader.source = 'Pages/Experiment/PageStructure.qml' :
                                  experimentPageLoader.source = ''
            Component.onCompleted: Globals.Refs.app.appbar.experimentButton = this
        },

        // Model tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.modelPageEnabled
            fontIcon: "gem"
            text: qsTr("Model")
            ToolTip.text: qsTr("Model description page")
            onEnabledChanged: enabled ?
                                  modelPageLoader.source = 'Pages/Model/PageStructure.qml' :
                                  modelPageLoader.source = ''
            Component.onCompleted: Globals.Refs.app.appbar.modelButton = this
        },

        // Analysis tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.analysisPageEnabled
            fontIcon: "calculator"
            text: qsTr("Analysis")
            ToolTip.text: qsTr("Simulation and fitting page")
            onEnabledChanged: enabled ?
                                  analysisPageLoader.source = 'Pages/Analysis/PageStructure.qml' :
                                  analysisPageLoader.source = ''
            Component.onCompleted: Globals.Refs.app.appbar.analysisButton = this
        },

        // Summary tab
        EaElements.AppBarTabButton {
            enabled: Globals.Vars.summaryPageEnabled
            fontIcon: "clipboard-list"
            text: qsTr("Summary")
            ToolTip.text: qsTr("Summary of the work done")
            onEnabledChanged: enabled ?
                                  summaryPageLoader.source = 'Pages/Summary/PageStructure.qml' :
                                  summaryPageLoader.source = ''
            onCheckedChanged: checked ?
                                  Globals.Proxies.main.summary.isCreated = true :
                                  Globals.Proxies.main.summary.isCreated = false
            Component.onCompleted: Globals.Refs.app.appbar.summaryButton = this
        }

    ]

    //////////////////////
    // MAIN VIEW + SIDEBAR
    //////////////////////

    // Pages for the tab buttons described above
    contentArea: [
        Loader { id: homePageLoader },
        Loader { id: projectPageLoader },
        Loader { id: experimentPageLoader },
        Loader { id: modelPageLoader },
        Loader { id: analysisPageLoader },
        Loader { id: summaryPageLoader }
    ]

    /////////////
    // STATUS BAR
    /////////////

    statusBar: Components.StatusBar {}

    ////////////
    // GUI TESTS
    ////////////

    Loader {
        source: Globals.Vars.isTestMode ? 'GuiTestsController.qml' : ""
    }

}
