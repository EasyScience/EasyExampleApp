// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs
//import QtQuick.XmlListModel 2.15

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


Grid {
    columns: 2
    spacing: EaStyle.Sizes.fontPixelSize

    EaElements.SideBarButton {
        fontIcon: "plus-circle"
        text: qsTr("Create a new project")

        onClicked: {
            console.debug(`Clicking '${text}' button: ${this}`)
            projectDescriptionDialog.source = 'ProjectDescriptionDialog.qml'
            EaGlobals.Vars.showProjectDescriptionDialog = true
        }

        Loader {
            id: projectDescriptionDialog
        }
    }

    EaElements.SideBarButton {
        fontIcon: "upload"
        text: qsTr("Open an existing project")

        onClicked: {
            console.debug(`Clicking '${text}' button: ${this}`)
            if (Globals.Vars.isTestMode) {
                console.debug('*** Open an existing project (test mode) ***')
                Globals.Vars.modelPageEnabled = true
                const fpath = Qt.resolvedUrl('../../../../../../examples/1-model_1-experiment/project.cif')
                Globals.Proxies.main.project.loadProjectFromFile(fpath)
                Globals.Vars.summaryPageEnabled = true
            } else {
                openCifFileDialog.open()
            }
        }
    }

    EaElements.SideBarButton {
        enabled: false

        fontIcon: "download"
        text: qsTr("Save project as...")
    }

    EaElements.SideBarButton {
        enabled: false

        fontIcon: "times-circle"
        text: qsTr("Close current project")
    }

    // Misc

    FileDialog{
        id: openCifFileDialog
        fileMode: FileDialog.OpenFile
        nameFilters: [ "CIF files (*.cif)"]
        onAccepted: {
            console.debug('*** Loading model(s) from file(s) ***')
            Globals.Vars.modelPageEnabled = true
            Globals.Proxies.main.project.loadProjectFromFile(selectedFile)
            Globals.Vars.summaryPageEnabled = true
        }
    }

}

