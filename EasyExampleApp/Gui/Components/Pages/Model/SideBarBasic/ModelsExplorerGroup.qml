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

        defaultInfoText: qsTr("No models defined")

        // Table model

        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.

        model: Globals.Proxies.main.model.dataBlocks.length

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                headerText: qsTr("No.")
                text: index + 1
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignLeft
                width: EaStyle.Sizes.fontPixelSize * 27.9
                headerText: qsTr("Name")
                text: Globals.Proxies.main.model.dataBlocks[index].name
            }

            EaComponents.TableViewLabel {
                headerText: qsTr("Color")
                backgroundColor: EaStyle.Colors.chartForegrounds[0]
            }

            EaComponents.TableViewButton {
                id: deleteRowColumn
                headerText: qsTr("Del.")
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this model")
                onClicked: Globals.Proxies.main.model.removeModel(index)
            }

        }

        onCurrentIndexChanged: Globals.Proxies.main.model.currentIndex = currentIndex

        Component.onCompleted: Globals.Refs.app.modelPage.modelsExplorer = this

    }

    // Control buttons below table

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            fontIcon: "upload"
            text: qsTr("Load new model from file")
            onClicked: Globals.Proxies.main.model.loadModelFromFile('/Users/as/Development/GitHub/easyScience/EasyExampleApp/examples/Gaussian.json')
            Component.onCompleted: Globals.Refs.app.modelPage.loadNewModelFromFileButton = this
        }

        EaElements.SideBarButton {
            fontIcon: "plus-circle"
            text: qsTr("Add new model manually")
            onClicked: Globals.Proxies.main.model.addDefaultModel()
            Component.onCompleted: Globals.Refs.app.modelPage.addNewModelManuallyButton = this
        }
    }

}
