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

        defaultInfoText: qsTr("No experiments defined")

        // Table model

        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.

        model: Globals.Proxies.main.experiment.dataBlocks.length

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                headerText: "No."
                text: index + 1
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignLeft
                width: EaStyle.Sizes.fontPixelSize * 27.9
                headerText: "Name"
                text: Globals.Proxies.main.experiment.dataBlocks[index].name
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
                onClicked: Globals.Proxies.main.experiment.removeExperiment(index)
            }
        }

        onCurrentIndexChanged: Globals.Proxies.main.experiment.currentIndex = currentIndex

    }

    // Control buttons below table

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            enabled: !Globals.Proxies.main.experiment.defined
            fontIcon: "upload"
            text: qsTr("Import data from local drive")
            onClicked: Globals.Proxies.main.experiment.loadExperimentFromFile('examples/PicoScope.json')
            Component.onCompleted: Globals.Refs.app.experimentPage.importDataFromLocalDriveButton = this
        }

        EaElements.SideBarButton {
            enabled: !Globals.Proxies.main.experiment.defined
            fontIcon: "upload"
            text: qsTr("Add default experimental data")
            onClicked: Globals.Proxies.main.experiment.addDefaultExperiment()
            Component.onCompleted: Globals.Refs.app.experimentPage.addDefaultExperimentDataButton = this
        }
    }

}
