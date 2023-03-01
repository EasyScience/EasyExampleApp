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

        defaultInfoText: qsTr("No experiments loaded")

        // Table model

        model: EaComponents.JsonListModel {
            json: Globals.Proxies.main.experiment.isCreated ?
                      JSON.stringify([Globals.Proxies.main.experiment.description]) :
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
                headerText: "Name"
                text: model.name
            }

            EaComponents.TableViewLabel {
                headerText: "Color"
                backgroundColor: EaStyle.Colors.chartForegroundsExtra[2]
            }

            EaComponents.TableViewButton {
                id: deleteRowColumn
                headerText: "Del."
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this dataset")
                onClicked: Globals.Proxies.main.experiment.emptyData()
            }
        }

    }

    // Control buttons below table

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            enabled: !Globals.Proxies.main.experiment.isCreated
            fontIcon: "upload"
            text: qsTr("Import data from local drive")
            onClicked: Globals.Proxies.main.experiment.loadData()
            Component.onCompleted: Globals.Refs.app.experimentPage.importDataFromLocalDriveButton = this
        }

        EaElements.SideBarButton {
            enabled: false
            fontIcon: "download"
            text: qsTr("Download data from SciCat")
        }
    }

}
