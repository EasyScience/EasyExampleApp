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

EaComponents.TableView {
    id: tableView

    maxRowCountShow: 9
    defaultInfoText: qsTr("No Examples Available")

    // Table model

    model: XmlListModel {
        ///xml: ExGlobals.Constants.proxy.project.projectExamplesAsXml
        query: "/root/item"

        XmlRole { name: "name"; query: "name/string()" }
        XmlRole { name: "description"; query: "description/string()" }
        XmlRole { name: "path"; query: "path/string()" }
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
                ExGlobals.Constants.proxy.project.loadExampleProject(fileUrl)

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
