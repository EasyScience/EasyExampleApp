import QtQuick 2.15

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Components 1.0 as EaComponents

// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import Gui.Globals 1.0 as ExGlobals

EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    ///onProjectNameChanged: ExGlobals.Proxies.mainProxy.project.editProjectInfo("name", projectName)
    ///onProjectShortDescriptionChanged: ExGlobals.Proxies.mainProxy.project.editProjectInfo("short_description", projectShortDescription)
    ///onProjectLocationChanged: ExGlobals.Proxies.mainProxy.project.currentProjectPath = projectLocation

    onAccepted: {
        ExGlobals.Proxies.mainProxy.project.currentProjectPath = projectLocation
        ExGlobals.Proxies.mainProxy.project.createProject()

    }

    Component.onCompleted: {
        projectName = ExGlobals.Proxies.mainProxy.project.projectInfoAsJson.name
        projectShortDescription = ExGlobals.Proxies.mainProxy.project.projectInfoAsJson.short_description
        ///projectLocation = ExGlobals.Proxies.mainProxy.project.currentProjectPath

        console.log("!!!!", this)
    }
}


