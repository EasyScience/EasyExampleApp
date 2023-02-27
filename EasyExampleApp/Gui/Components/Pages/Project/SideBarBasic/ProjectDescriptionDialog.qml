// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    onAccepted: {
        Globals.Proxies.main.project.currentProjectName = projectName
        Globals.Proxies.main.project.currentProjectDescription = projectDescription
        Globals.Proxies.main.project.currentProjectLocation = projectLocation
        Globals.Proxies.main.project.create()
    }

    Component.onCompleted: {
        projectName = Globals.Proxies.main.project.currentProjectName
        projectDescription = Globals.Proxies.main.project.currentProjectDescription
        projectLocation = Globals.Proxies.main.project.currentProjectLocation
    }
}


