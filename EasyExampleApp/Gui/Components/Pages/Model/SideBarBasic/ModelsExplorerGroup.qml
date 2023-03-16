// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    // Table

    EaComponents.TableView {
        id: table

        defaultInfoText: qsTr("No models loaded / added")

        // Table model

        model: EaComponents.JsonListModel {
            json: Globals.Proxies.main.model.created ?
                      JSON.stringify(Globals.Proxies.main.model.data) :
                      ""
            query: "$[*]"
        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                headerText: qsTr("No.")
                text: model.index + 1
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignLeft
                width: EaStyle.Sizes.fontPixelSize * 27.9
                headerText: qsTr("Name")
                text: model.name
            }

            EaComponents.TableViewLabel {
                headerText: qsTr("Color")
                backgroundColor: EaStyle.Colors.chartForegrounds[0]
            }

            EaComponents.TableViewButton {
                id: deleteRowColumn
                enabled: false
                headerText: qsTr("Del.")
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this model")
            }

        }

        onCurrentIndexChanged: {
            if (currentIndex === -1)
                return
            Globals.Proxies.main.model.currentIndex = currentIndex
        }

        Component.onCompleted: Globals.Refs.app.modelPage.modelsExplorer = this

    }

    // Control buttons below table

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            enabled: Globals.Proxies.main.model.data.length < 2
            fontIcon: "upload"
            text: qsTr("Load new model from file")
            onClicked: {
                Globals.Proxies.main.model.load()
                table.currentIndex = 0
            }
            Component.onCompleted: Globals.Refs.app.modelPage.loadNewModelFromFileButton = this
        }

        EaElements.SideBarButton {
            enabled: false
            fontIcon: "plus-circle"
            text: qsTr("Add new model manually")
        }
    }

}
