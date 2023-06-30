// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaElements.GroupColumn {

    EaComponents.TableView {

        defaultInfoText: qsTr("No phases defined")

        // Table model

        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.

        model: {
            if (typeof Globals.Proxies.main.experiment.dataBlocks[Globals.Proxies.main.model.currentIndex] === 'undefined') {
                return 0
            }
            return Globals.Proxies.main.experiment.dataBlocks[Globals.Proxies.main.model.currentIndex].loops._phase.length
        }

        // Header row

        header: EaComponents.TableViewHeader {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                //text: qsTr("No.")
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.experimentLoopParam('_phase', '_label', 0).prettyName
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 5.0
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.experimentLoopParam('_phase', '_scale', 0).prettyName
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                //text: qsTr("Del.")
            }

        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                color: EaStyle.Colors.themeForegroundMinor
                text: index + 1
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.experimentLoopParam('_phase', '_label', index)
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.experimentLoopParam('_phase', '_scale', index)
                onEditingFinished: Globals.Proxies.setExperimentLoopParam(parameter, 'value', text)
                fitCheckBox.onToggled: Globals.Proxies.setExperimentLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewButton {
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this phase")
                onClicked: Globals.Proxies.main.model.removeModel(index)
            }

        }

        onCurrentIndexChanged: Globals.Proxies.main.model.currentIndex = currentIndex
    }

}
