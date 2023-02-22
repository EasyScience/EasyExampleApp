// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
import QtTest

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals
import Gui.Components as Components


Item {
    id: root

    Column {
        anchors.centerIn: parent

        // Application logo
        Image {
            id: appLogo

            source: Globals.Configs.appConfig.icon
            anchors.horizontalCenter: parent.horizontalCenter
            width: EaStyle.Sizes.fontPixelSize * 5
            fillMode: Image.PreserveAspectFit
            antialiasing: true
        }

        // Application name
        Row {
            id: appName

            property string fontFamily: EaStyle.Fonts.thirdFontFamily
            property string fontPixelSize: EaStyle.Sizes.fontPixelSize * 4

            anchors.horizontalCenter: parent.horizontalCenter

            EaElements.Label {
                font.family: parent.fontFamily
                font.pixelSize: parent.fontPixelSize
                font.weight: Font.Light
                text: Globals.Configs.appConfig.namePrefixForLogo
            }
            EaElements.Label {
                font.family: parent.fontFamily
                font.pixelSize: parent.fontPixelSize
                font.weight: Font.DemiBold
                text: Globals.Configs.appConfig.nameSuffixForLogo
            }
        }

        // Application version
        EaElements.Label {
            id: appVersion

            anchors.horizontalCenter: parent.horizontalCenter

            text: qsTr('Version') + ` ${Globals.Configs.appConfig.version} (${Globals.Configs.appConfig.date})`
        }

        // Github branch
        EaElements.Label {
            id: githubBranch

            visible: Globals.Configs.appConfig.branch && Globals.Configs.appConfig.branch !== 'master'
            topPadding: EaStyle.Sizes.fontPixelSize * 0.5
            anchors.horizontalCenter: parent.horizontalCenter
            opacity: 0

            text: qsTr('Branch') + ` <a href="${Globals.Configs.appConfig.branchUrl}">${Globals.Configs.appConfig.branch}</a>`
        }

        // Vertical spacer
        Item { width: 1; height: EaStyle.Sizes.fontPixelSize * 2.5 }

        // Start button
        EaElements.SideBarButton {
            id: startButton

            anchors.horizontalCenter: parent.horizontalCenter

            fontIcon: "rocket"
            text: qsTr("Start")
            onClicked: {
                Globals.Vars.projectPageEnabled = true
                Globals.Refs.app.appbar.projectButton.toggle()
            }
            Component.onCompleted: Globals.Refs.app.homePage.startButton = this
        }

        // Vertical spacer
        Item { width: 1; height: EaStyle.Sizes.fontPixelSize * 2.5 }

        // Links
        Row {
            id: links

            anchors.horizontalCenter: parent.horizontalCenter
            spacing: EaStyle.Sizes.fontPixelSize * 3

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    text: qsTr("About %1".arg(Globals.Configs.appConfig.name))
                    onClicked: EaGlobals.Variables.showAppAboutDialog = true
                    Loader { id: aboutDialogLoader }
                    Component.onCompleted: aboutDialogLoader.source = "AboutDialog.qml"
                }
                EaElements.Button {
                    text: qsTr("Online documentation")
                    onClicked: Qt.openUrlExternally("https://github.com/EasyScience/EasyExampleApp")
                }
                EaElements.Button {
                    enabled: false
                    text: qsTr("Get in touch online")
                }
            }

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    enabled: false
                    text: qsTr("Tutorial") + " 1: " + qsTr("App interface")
                    onClicked: print("Tutorial 1 button clicked")
                }
                EaElements.Button {
                    enabled: false
                    text: qsTr("Tutorial") + " 2: " + qsTr("Basic usage")
                    onClicked: print("Tutorial 2 button clicked")
                }
                EaElements.Button {
                    //enabled: false
                    text: qsTr("Tutorial") + " 3: " + qsTr("Advanced usage")
                    onClicked: {
                        print("Tutorial 3 button clicked")
                        dataFittingTutorialTimer.start()
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        print("Home page loaded:", this)
        Globals.Vars.homePageCreated = true
    }
    Component.onDestruction: print("Home page destroyed:", this)

    // User tutorials

    Components.UserTutorialsController {
        id: tutorialsController
    }

    Timer {
        id: dataFittingTutorialTimer
        interval: 100
        onTriggered: tutorialsController.runDataFittingTutorial()
    }

}
