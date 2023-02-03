// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import easyApp.Gui.Style as EaStyle
import easyApp.Gui.Globals as EaGlobals
import easyApp.Gui.Elements as EaElements

import Gui.Globals as ExGlobals


Item {
    id: root

    Column {
        anchors.centerIn: parent

        // Application logo
        Image {
            id: appLogo

            source: ExGlobals.Configs.appConfig.icon
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
                text: ExGlobals.Configs.appConfig.namePrefixForLogo
            }
            EaElements.Label {
                font.family: parent.fontFamily
                font.pixelSize: parent.fontPixelSize
                font.weight: Font.DemiBold
                text: ExGlobals.Configs.appConfig.nameSuffixForLogo
            }
        }

        // Application version
        EaElements.Label {
            id: appVersion

            anchors.horizontalCenter: parent.horizontalCenter

            text: ExGlobals.Configs.branch && ExGlobals.Configs.branch !== 'master'
                  ? qsTr('Version') + ` <a href="${ExGlobals.Configs.appConfig.commitUrl}">${ExGlobals.Configs.appConfig.version}-${ExGlobals.Configs.appConfig.commit}</a> (${ExGlobals.Configs.appConfig.date})`
                  : qsTr('Version') + ` ${ExGlobals.Configs.appConfig.version} (${ExGlobals.Configs.appConfig.date})`
        }

        // Github branch
        EaElements.Label {
            id: githubBranch

            visible: ExGlobals.Configs.appConfig.branch && ExGlobals.Configs.appConfig.branch !== 'master'
            topPadding: EaStyle.Sizes.fontPixelSize * 0.5
            anchors.horizontalCenter: parent.horizontalCenter
            opacity: 0

            text: qsTr('Branch') + ` <a href="${ExGlobals.Configs.appConfig.branchUrl}">${ExGlobals.Configs.appConfig.branch}</a>`
        }

        // Vertical spacer
        Item { width: 1; height: EaStyle.Sizes.fontPixelSize * 2.5 }

        // Start button
        EaElements.SideBarButton {
            id: startButton

            width: EaStyle.Sizes.fontPixelSize * 15
            anchors.horizontalCenter: parent.horizontalCenter

            fontIcon: "rocket"
            text: qsTr("Start")
            onClicked: {
                ExGlobals.Variables.projectPageEnabled = true
                ExGlobals.References.projectAppbarButton.toggle()
            }
            Component.onCompleted: ExGlobals.Variables.startButton = this
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
                    text: qsTr("About %1".arg(ExGlobals.Configs.appConfig.name))
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
                    enabled: false
                    text: qsTr("Tutorial") + " 3: " + qsTr("Advanced usage")
                    onClicked: print("Tutorial 3 button clicked")
                }
            }
        }
    }

    Component.onCompleted: print("Home page loaded:", this)
    Component.onDestruction: print("Home page destroyed:", this)
}
