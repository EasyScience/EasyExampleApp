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
        ExGlobals.Proxies.mainProxy.project.currentProjectName = projectName
        ExGlobals.Proxies.mainProxy.project.currentProjectDescription = projectDescription
        ExGlobals.Proxies.mainProxy.project.currentProjectLocation = projectLocation
        ExGlobals.Proxies.mainProxy.project.create()
    }

    Component.onCompleted: {
        projectName = ExGlobals.Proxies.mainProxy.project.currentProjectName
        projectDescription = ExGlobals.Proxies.mainProxy.project.currentProjectDescription
        projectLocation = ExGlobals.Proxies.mainProxy.project.currentProjectLocation
    }
}


