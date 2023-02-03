// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls
//import QtQuick.XmlListModel 2.13

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as ExGlobals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    EaComponents.TableView {

        defaultInfoText: qsTr("No Phases Added/Loaded")

        // Table model

        /*
        model: XmlListModel {
            xml: ExGlobals.Proxies.mainProxy.project.modelsAdded ?
                     ExGlobals.Proxies.mainProxy.phase.phasesAsXml :
                     ""
            query: "/root/item"

            XmlRole { name: "label"; query: "name/string()" }
        }
        */

        model: EaComponents.JsonListModel {
            json: ExGlobals.Proxies.mainProxy.project.modelsAdded ?
                      JSON.stringify(ExGlobals.Proxies.mainProxy.phase.phasesAsJson) :
                      ""
            query: "$[*]"
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
