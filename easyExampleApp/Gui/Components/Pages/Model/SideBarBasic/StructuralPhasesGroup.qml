// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Column {
    spacing: EaStyle.Sizes.fontPixelSize

    EaComponents.TableView {

        defaultInfoText: qsTr("No Phases Added/Loaded")

        // Table model

        model: XmlListModel {
            xml: ExGlobals.Proxies.mainProxy.project.modelsAdded ?
                     ExGlobals.Proxies.mainProxy.phase.phasesAsXml :
                     ""
            query: "/root/item"

            XmlRole { name: "label"; query: "name/string()" }
        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                headerText: "No."
                text: model.index + 1
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignLeft
                width: EaStyle.Sizes.fontPixelSize * 27.9
                headerText: "Label"
                text: model.label
            }

            EaComponents.TableViewLabel {
                headerText: "Color"
                //backgroundColor: model.color ? model.color : "transparent"
                backgroundColor: EaStyle.Colors.chartForegroundsExtra[model.index]
            }

            EaComponents.TableViewButton {
                id: deleteRowColumn
                headerText: "Del."
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this phase")
            }

        }

    }

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            fontIcon: "upload"
            text: qsTr("Add new phase from CIF")
            onClicked: ExGlobals.Proxies.mainProxy.project.modelsAdded = true
        }

        EaElements.SideBarButton {
            enabled: false
            fontIcon: "plus-circle"
            text: qsTr("Add new phase manually")
        }
    }

}
