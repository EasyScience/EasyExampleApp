// SPDX-FileCopyrightText: 2022 EasyTexture contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyTexture project <https://github.com/EasyScience/EasyTextureApp>

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.XmlListModel 2.15

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals


Grid {
    columns: 2
    spacing: EaStyle.Sizes.fontPixelSize

    EaElements.SideBarButton {
        //enabled: false
        fontIcon: "plus-circle"
        text: qsTr("Create a new project")

        onClicked: EaGlobals.Variables.showProjectDescriptionDialog = true

        //Loader { source: 'ProjectDescriptionDialog.qml' }
    }

    EaElements.SideBarButton {
        fontIcon: "arrow-circle-right"
        text: qsTr("Continue without a project")

        onClicked: {
            ExGlobals.Variables.step1PageEnabled = true
            ExGlobals.Variables.step1TabButton.toggle()
        }
    }

    EaElements.SideBarButton {
        enabled: false
        fontIcon: "upload"
        text: qsTr("Open an existing project")

        onClicked: fileDialogLoadProject.open()
        Component.onCompleted: ExGlobals.Variables.openProjectButton = this
    }

    EaElements.SideBarButton {
        enabled: false

        fontIcon: "download"
        text: qsTr("Save project as...")
    }
}

