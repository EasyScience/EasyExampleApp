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

    maxRowCountShow: 9
    defaultInfoText: qsTr("No Examples Available")

    // Table model

    model: EaComponents.JsonListModel {
        json: JSON.stringify(Globals.Proxies.main.project.examples)
        query: "$[*]"
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: indexColumn

            width: EaStyle.Sizes.fontPixelSize * 2.5

            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            width: tableView.width
                   - indexColumn.width
                   - descriptionColumn.width
                   - uploadColumn.width
                   - EaStyle.Sizes.tableColumnSpacing * 3
                   - EaStyle.Sizes.borderThickness

            horizontalAlignment: Text.AlignLeft

            headerText: "Name"
            text: model.name
        }

        EaComponents.TableViewLabelControl {
            id: descriptionColumn

            width: EaStyle.Sizes.fontPixelSize * 24

            horizontalAlignment: Text.AlignLeft

            headerText: "Description"
            text: model.description
            ToolTip.text: model.description
        }

        EaComponents.TableViewButton {
            id: uploadColumn

            fontIcon: "upload"
            ToolTip.text: qsTr("Load this example")
        }
    }

}
