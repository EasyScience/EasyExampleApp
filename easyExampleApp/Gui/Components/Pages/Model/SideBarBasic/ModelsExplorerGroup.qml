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

        defaultInfoText: qsTr("No models loaded")

        // Table model

        model: EaComponents.JsonListModel {
            json: ExGlobals.Proxies.mainProxy.model.modelsAdded ?
                      JSON.stringify(ExGlobals.Proxies.mainProxy.model.modelsAsJson) :
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
                backgroundColor: model.color
            }

            EaComponents.TableViewButton {
                id: deleteRowColumn
                headerText: "Del."
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this model")
                onClicked: {
                    ExGlobals.Proxies.mainProxy.experiment.emptyMeasuredDataObj()
                    ExGlobals.Proxies.mainProxy.experiment.experimentsLoaded = false
                    ExGlobals.Proxies.mainProxy.model.modelsAdded = false
                    ExGlobals.Variables.experimentPageEnabled = false
                    ExGlobals.Variables.analysisPageEnabled = false
                    ExGlobals.Variables.summaryPageEnabled = false
                }
            }

        }

    }

    // Control buttons below table

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            enabled: false
            fontIcon: "upload"
            text: qsTr("Load new model from file")
        }

        EaElements.SideBarButton {
            enabled: !ExGlobals.Proxies.mainProxy.model.modelsAdded
            fontIcon: "plus-circle"
            text: qsTr("Add new model manually")
            onClicked: {
                ExGlobals.Proxies.mainProxy.model.modelsAdded = true
            }
        }
    }

}
