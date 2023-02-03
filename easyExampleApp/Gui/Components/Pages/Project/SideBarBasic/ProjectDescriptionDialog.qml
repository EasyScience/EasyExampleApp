// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import easyApp.Gui.Globals as EaGlobals
import easyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals


EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    onAccepted: {
        ExGlobals.Proxies.mainProxy.project.currentProjectPath = projectLocation
        ExGlobals.Proxies.mainProxy.project.createProject()

    }

    Component.onCompleted: {
        projectName = ExGlobals.Proxies.mainProxy.project.projectInfoAsJson.name
        projectShortDescription = ExGlobals.Proxies.mainProxy.project.projectInfoAsJson.short_description
    }
}


