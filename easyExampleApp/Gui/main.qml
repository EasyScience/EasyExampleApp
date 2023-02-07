// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import QtQuick.Window

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as ExGlobals
import Gui.Components as ExComponents


EaElements.SplashScreen {

    appNamePrefix: ExGlobals.Configs.appConfig.namePrefixForLogo
    appNameSuffix: ExGlobals.Configs.appConfig.nameSuffixForLogo
    appVersion: qsTr('Version') + ` ${ExGlobals.Configs.appConfig.version} (${ExGlobals.Configs.appConfig.date})`
    logoSource: ExGlobals.Configs.appConfig.icon

    initialGuiCompleted: ExGlobals.Variables.applicationWindowCreated &&
                         ExGlobals.Variables.homePageCreated

    onAnimationFinishedChanged: ExGlobals.Variables.splashScreenAnimoFinished = animationFinished

    Component.onCompleted: print("Splash screen loaded:", this)
    Component.onDestruction: print("Splash screen destroyed:", this)

    // Application window loader

    Loader {
        asynchronous: true
        source: "Components/ApplicationWindow.qml"
    }

}
