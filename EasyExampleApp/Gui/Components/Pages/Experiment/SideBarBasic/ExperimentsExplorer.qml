// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

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

        // Header row

        header: EaComponents.TableViewHeader {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                //text: qsTr("no.")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
                //text: qsTr("color")
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("label")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.tableRowHeight
                //text: qsTr("del.")
            }

        }

        // Table rows
        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                text: index + 1
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewButton {
                fontIcon: "tint"
                ToolTip.text: qsTr("Measured pattern color")
                outlineIcon: true
                backgroundColor: "transparent"
                borderColor: "transparent"
                iconColor: EaStyle.Colors.chartForegroundsExtra[2]
            }

            EaComponents.TableViewParameter {
                text: Globals.Proxies.main.experiment.dataBlocks[index].name
            }

            EaComponents.TableViewButton {
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
            text: qsTr("Load experiment from file")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                if (Globals.Vars.isTestMode) {
                    console.debug(`---------- Loading experiment from file (test mode) ----------`)
                    const fpath = '../examples/Co2SiO4_experiment.cif'
                    Globals.Proxies.main.experiment.loadExperimentFromFile(fpath)
                } else {
                    openCifFileDialog.open()
                }
            }
            Component.onCompleted: Globals.Refs.app.experimentPage.importDataFromLocalDriveButton = this
        }

        EaElements.SideBarButton {
            enabled: !Globals.Proxies.main.experiment.defined
            fontIcon: "plus-circle"
            text: qsTr("Define experiment manually")
            onClicked: {
                console.debug(`Clicking '${text}' button: ${this}`)
                console.debug(`---------- Adding default experiment ----------`)
                Globals.Proxies.main.experiment.addDefaultExperiment()
            }
            Component.onCompleted: Globals.Refs.app.experimentPage.addDefaultExperimentDataButton = this
        }
    }

    // Misc

    FileDialog{
        id: openCifFileDialog
        //selectMultiple: true
        nameFilters: [ "CIF files (*.cif)"]
        onAccepted: {
            console.debug(`---------- Loading experiment from file ----------`)
            Globals.Proxies.main.experiment.loadExperimentFromFile(selectedFile)
        }
    }

}
