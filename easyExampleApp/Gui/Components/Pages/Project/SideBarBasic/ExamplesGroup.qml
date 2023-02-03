// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
//import QtQuick.XmlListModel 2.15

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as ExGlobals


EaComponents.TableView {
    id: tableView

    maxRowCountShow: 9
    defaultInfoText: qsTr("No Examples Available")

    // Table model

    /*
    model: XmlListModel {
        xml: ExGlobals.Proxies.mainProxy.project.projectExamplesAsXml
        query: "/root/item"

        XmlRole { name: "name"; query: "name/string()" }
        XmlRole { name: "description"; query: "description/string()" }
        XmlRole { name: "path"; query: "path/string()" }
    }
    */

    model: EaComponents.JsonListModel {
        json: JSON.stringify(ExGlobals.Proxies.mainProxy.project.projectExamplesAsJson)
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

            onClicked: {
                const fileUrl = Qt.resolvedUrl(model.path)
                ExGlobals.Proxies.mainProxy.project.loadExampleProject(fileUrl)

                ExGlobals.Variables.step1PageEnabled = true
                ExGlobals.Variables.step2PageEnabled = true
            }

            Component.onCompleted: {
                if (model.name === 'PbSO4') {
                    ExGlobals.Variables.loadExampleProjectButton = this
                }
            }
        }
    }

}
