// SPDX-FileCopyrightText: 2022 EasyTexture contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyTexture project <https://github.com/EasyScience/EasyTextureApp>

import QtQuick 2.15

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.AboutDialog {
    visible: EaGlobals.Variables.showAppAboutDialog
    onClosed: EaGlobals.Variables.showAppAboutDialog = false

    appIconPath: ExGlobals.Constants.appLogo
    appUrl: ExGlobals.Constants.appUrl

    appPrefixName: ExGlobals.Constants.appPrefixNameLogo
    appSuffixName: ExGlobals.Constants.appSuffixNameLogo
    appVersion: ExGlobals.Constants.appVersion
    appDate: ExGlobals.Constants.appDate

    commit: ExGlobals.Constants.commit
    commitUrl: ExGlobals.Constants.commitUrl

    branch: ExGlobals.Constants.branch
    branchUrl: ExGlobals.Constants.branchUrl

    eulaUrl: ExGlobals.Constants.eulaUrl
    oslUrl: ExGlobals.Constants.oslUrl

    description: ExGlobals.Constants.description

    essIconPath: ExGlobals.Constants.essLogo
}
