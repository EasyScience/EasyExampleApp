// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import QtQuick.Window

import EasyApp.Gui.Style as EaStyle

import Gui.Globals as ExGlobals
import Gui.Components as ExComponents


Window {
    id: baseWindow

    property bool initialGuiCompleted: ExGlobals.Variables.applicationWindowCompleted &&
                                       ExGlobals.Variables.homePageCompleted
    onInitialGuiCompletedChanged: loadingLogoAnimo.stop()

    visible: true

    //x: Screen.width / 2 - width / 2
    //y: Screen.height / 2 - height / 2

    height: EaStyle.Sizes.fontPixelSize * 11
    width: EaStyle.Sizes.fontPixelSize * 11

    flags: Qt.FramelessWindowHint //Qt.Popup

    color: "transparent"

    Component.onCompleted: {
        print("Base window loaded:", this)
        applicationWindoeLoader.source = "Components/ApplicationWindow.qml"
    }
    Component.onDestruction: print("Base window destroyed:", this)

    // Start logo with animation

    Rectangle {
        anchors.fill: parent

        color: EaStyle.Colors.appBarBackground
        radius: EaStyle.Sizes.fontPixelSize

        Image {
            id: loadingLogo

            anchors.fill: parent
            anchors.margins: EaStyle.Sizes.fontPixelSize * 1.5

            source: ExGlobals.Configs.appConfig.icon
            fillMode: Image.PreserveAspectFit
            antialiasing: true

            RotationAnimation {
                id: loadingLogoAnimo

                target: loadingLogo

                running: true
                alwaysRunToEnd: true

                loops: Animation.Infinite
                from: 0
                to: 360 * 4
                duration: 2000

                easing.type: Easing.OutInElastic

                onFinished: {
                    baseWindow.visible = false
                    ExGlobals.Variables.applicationWindowOpacity = 1.0
                }
            }
        }
    }

    // Application window loader

    Loader {
        id: applicationWindoeLoader
        visible: status === Loader.Ready
        asynchronous: true
    }

}
