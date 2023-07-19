// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
import QtCore

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


EaComponents.TableView {
    id: tableView

    maxRowCountShow: 9
    defaultInfoText: qsTr("No recent projects found")

    // Table model
    model: Globals.Proxies.main.project.recent
    Component.onCompleted: Globals.Proxies.main.project.recent = JSON.parse(settings.value('recentProjects', '[]'))
    // Table model

    // Header row
    header: EaComponents.TableViewHeader {

        EaComponents.TableViewLabel {
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 2.5
            //text: qsTr("No.")
        }

        EaComponents.TableViewLabel {
            flexibleWidth: true
            horizontalAlignment: Text.AlignLeft
            color: EaStyle.Colors.themeForegroundMinor
            text: qsTr("file")
        }

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.tableRowHeight
        }

    }
    // Header row


    // Table rows
    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            text: index + 1
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewLabelControl {
            text: tableView.model[index]
            ToolTip.text: tableView.model[index]
        }

        EaComponents.TableViewButton {
            fontIcon: "upload"
            ToolTip.text: qsTr("Load this project")
            onClicked: {
                const fpath = Qt.resolvedUrl(tableView.model[index])
                Globals.Proxies.main.project.loadProjectFromFile(fpath)
            }
        }

    }
    // Table rows

    // Persistent settings
    Settings {
        id: settings
        location: EaGlobals.Vars.settingsFile // Gives WASM error on run
        category: 'Project.Recent'
    }

}
