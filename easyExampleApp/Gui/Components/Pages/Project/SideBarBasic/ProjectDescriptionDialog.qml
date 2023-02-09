// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals


EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    onAccepted: {
        ExGlobals.Proxies.miscProxy.project.currentProjectPath = projectLocation
        ExGlobals.Proxies.miscProxy.project.createProject()

    }

    Component.onCompleted: {
        projectName = ExGlobals.Proxies.miscProxy.project.projectInfoAsJson.name
        projectShortDescription = ExGlobals.Proxies.miscProxy.project.projectInfoAsJson.short_description
    }
}


