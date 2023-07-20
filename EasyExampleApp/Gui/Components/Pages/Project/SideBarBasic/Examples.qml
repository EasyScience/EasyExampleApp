// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


EaComponents.TableView {
    id: tableView

    showHeader: false
    tallRows: true
    maxRowCountShow: 6

    defaultInfoText: qsTr("No examples available")

    // Table model
    model: Globals.Proxies.main.project.examples
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
            text: qsTr("name / description")
        }
    }
    // Header row


    // Table rows
    delegate: EaComponents.TableViewDelegate {

        mouseArea.onPressed: {
            const filePath = tableView.model[index].path
            const fileUrl = Qt.resolvedUrl(filePath)
            Globals.Proxies.main.project.loadProjectFromFile(fileUrl)
        }

        EaComponents.TableViewLabel {
            text: index + 1
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewTwoRowsAdvancedLabel {
            fontIcon: 'archive'
            text: tableView.model[index].name
            minorText: tableView.model[index].description
            ToolTip.text: tableView.model[index].description
        }
    }
    // Table rows

}
