// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick 2.15

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.AboutDialog {
    visible: EaGlobals.Variables.showAppAboutDialog
    onClosed: EaGlobals.Variables.showAppAboutDialog = false

    appIconPath: ExGlobals.Configs.appConfig.icon
    appUrl: ExGlobals.Configs.appConfig.homePageUrl

    appPrefixName: ExGlobals.Configs.appConfig.namePrefixForLogo
    appSuffixName: ExGlobals.Configs.appConfig.nameSuffixForLogo
    appVersion: ExGlobals.Configs.appConfig.version
    appDate: ExGlobals.Configs.appConfig.date

    commit: ExGlobals.Configs.appConfig.commit
    commitUrl: ExGlobals.Configs.appConfig.commitUrl
    branch: ExGlobals.Configs.appConfig.branch
    branchUrl: ExGlobals.Configs.appConfig.branchUrl

    eulaUrl: ExGlobals.Configs.appConfig.licenseUrl
    oslUrl: ExGlobals.Configs.appConfig.dependenciesUrl

    description: ExGlobals.Configs.appConfig.description
    developerIcons: ExGlobals.Configs.appConfig.developerIcons
    developerYearsFrom: ExGlobals.Configs.appConfig.developerYearsFrom
    developerYearsTo: ExGlobals.Configs.appConfig.developerYearsTo
}
