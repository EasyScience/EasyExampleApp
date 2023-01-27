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
import Gui.Components.Pages.Home 1.0 as ExHomePage

//import Gui.Pages.Home 1.0 as ExHomePage
//import Gui.Pages.Project 1.0 as ExProjectPage
//import Gui.Pages.Step1 1.0 as ExStep1
//import Gui.Pages.Step2 1.0 as ExStep2
//import Gui.Pages.Step3 1.0 as ExStep3
//import Gui.Pages.Summary 1.0 as ExLiveViewPage

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
        },

        // Project tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.projectPageEnabled
            fontIcon: "archive"
            text: qsTr("Project")
            ToolTip.text: qsTr("Project description page")
        },

        // Model tab
        EaElements.AppBarTabButton {
  //          enabled: ExGlobals.Variables.modelPageEnabled
            fontIcon: "gem"
            text: qsTr("Model")
            ToolTip.text: qsTr("Model description page")
        },

        // Experiment tab
        EaElements.AppBarTabButton {
 //           enabled: ExGlobals.Variables.experimentPageEnabled
            fontIcon: "microscope"
            text: qsTr("Experiment")
            ToolTip.text: qsTr("Experimental settings and measured data page")
        },

        // Analysis tab
        EaElements.AppBarTabButton {
 //           enabled: ExGlobals.Variables.analysisPageEnabled
            fontIcon: "calculator"
            text: qsTr("Analysis")
            ToolTip.text: qsTr("Simulation and fitting page")
        },

        // Summary tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.summaryPageEnabled
            fontIcon: "clipboard-list"
            text: qsTr("Summary")
            ToolTip.text: qsTr("Summary of the work done")
        }

    ]

    /////////////////////////
    // MAIN CONTENT + SIDEBAR
    /////////////////////////

    // Pages for the tab buttons described above
    contentArea: [

        // Home page
        ExHomePage.MainContent {},
        //Loader { source: 'Pages/Project/MainContent.qml' },
        Loader { source: 'Pages/Project/MainContent.qml' },
        Loader { source: 'Pages/Model/MainContent.qml' },
        Loader { source: 'Pages/Experiment/MainContent.qml' },
        Loader { source: 'Pages/Analysis/MainContent.qml' },
        Loader { source: 'Pages/Summary/MainContent.qml' }

    ]

    /////////////
    // STATUS BAR
    /////////////

    statusBar: EaElements.StatusBar {
        visible: EaGlobals.Variables.appBarCurrentIndex !== 0

        model: XmlListModel {
            ///xml: ExGlobals.Constants.proxy.project.statusModelAsXml
            query: "/root/item"

            XmlRole { name: "label"; query: "label/string()" }
            XmlRole { name: "value"; query: "value/string()" }
        }
    }

    ///////////////
    // Init dialogs
    ///////////////

    // Application dialogs (invisible at the beginning)

    ExComponents.CloseDialog {
        id: closeDialog
    }

    EaElements.Dialog {
        id: resetStateDialog

        title: qsTr("Reset state")

        EaElements.Label {
            horizontalAlignment: Text.AlignHCenter
            text: qsTr("Are you sure you want to reset the application to its\noriginal state without project, phases and data?\n\nThis operation cannot be undone.")
        }

        footer: EaElements.DialogButtonBox {
            EaElements.Button {
                text: qsTr("Cancel")
                onClicked: resetStateDialog.close()
            }

            EaElements.Button {
                text: qsTr("OK")
                onClicked: {
                    EaGlobals.Variables.appBarCurrentIndex = 0
                    ExGlobals.Variables.projectPageEnabled = false
                    ExGlobals.Variables.step1PageEnabled = false
                    ExGlobals.Constants.proxy.project.resetState()
                    resetStateDialog.close()
                }
                Component.onCompleted: ExGlobals.Variables.resetStateOkButton = this
            }
        }
    }

    ////////
    // Misc
    ////////

    onClosing: {
        window.quit()
    }

    Component.onCompleted: {
        ExGlobals.Variables.appBarCentralTabs = appBarCentralTabs

        // DEBUG:
        //EaStyle.Sizes.defaultScale = parseInt("150%")
    }

}
