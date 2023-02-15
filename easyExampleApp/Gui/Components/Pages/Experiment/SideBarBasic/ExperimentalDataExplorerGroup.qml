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

import Gui.Globals as ExGlobals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    // Table

    EaComponents.TableView {

        defaultInfoText: qsTr("No experiments loaded")

        // Table model

        model: EaComponents.JsonListModel {
            json: ExGlobals.Proxies.mainProxy.experiment.isCreated ?
                      JSON.stringify(ExGlobals.Proxies.mainProxy.experiment.asJson) :
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
                backgroundColor: EaStyle.Colors.chartForegroundsExtra[2]
            }

            EaComponents.TableViewButton {
                id: deleteRowColumn
                headerText: "Del."
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this dataset")
                onClicked: ExGlobals.Proxies.mainProxy.experiment.emptyMeasuredData()
            }
        }

    }

    // Control buttons below table

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            enabled: !ExGlobals.Proxies.mainProxy.experiment.isCreated
            fontIcon: "upload"
            text: qsTr("Import data from local drive")
            onClicked: ExGlobals.Proxies.mainProxy.experiment.loadMeasuredData()
        }

        EaElements.SideBarButton {
            enabled: false
            fontIcon: "download"
            text: qsTr("Download data from SciCat")
        }
    }

}
