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

        defaultInfoText: qsTr("No atoms defined")

        // Table model

        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.

        model: {
            if (typeof Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex] === 'undefined') {
                return 0
            }
            return Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex].loops._atom_site.length
        }

        // Header row
        header: EaComponents.TableViewHeader {

            EaComponents.TableViewLabel {
                enabled: false
                width: EaStyle.Sizes.fontPixelSize * 2.5
                //text: qsTr("No.")
            }

            EaComponents.TableViewLabel {
                id: atomSiteLabel
                width: EaStyle.Sizes.fontPixelSize * 4.0
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_label', 0).prettyName
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.0
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_type_symbol', 0).prettyName
            }

            EaComponents.TableViewLabel {
                id: fractXLabel
                width: EaStyle.Sizes.fontPixelSize * 4.4
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_fract_x', 0).prettyName
            }

            EaComponents.TableViewLabel {
                width: fractXLabel.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_fract_y', 0).prettyName
            }

            EaComponents.TableViewLabel {
                width: fractXLabel.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_fract_z', 0).prettyName
            }

            EaComponents.TableViewLabel {
                width: fractXLabel.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_occupancy', 0).prettyName
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignHCenter
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("WP")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                //text: qsTr("Color")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                //text: qsTr("Del.")
            }

        }
        // Header row

        // Table rows
        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                text: index + 1
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewTextInput {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_label', index)
            }

            EaComponents.TableViewTextInput {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_type_symbol', index)
            }

            EaComponents.TableViewTextInput {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_fract_x', index)
                onEditingFinished: Globals.Proxies.setModelLoopParam(parameter, 'value', text)
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewTextInput {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_fract_y', index)
                onEditingFinished: Globals.Proxies.setModelLoopParam(parameter, 'value', text)
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewTextInput {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_fract_z', index)
                onEditingFinished: Globals.Proxies.setModelLoopParam(parameter, 'value', text)
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewTextInput {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_occupancy', index)
                onEditingFinished: Globals.Proxies.setModelLoopParam(parameter, 'value', text)
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.modelLoopParam('_atom_site', '_multiplicity', index).value +
                      Globals.Proxies.modelLoopParam('_atom_site', '_Wyckoff_symbol', index).value
            }

            EaComponents.TableViewLabel {
                backgroundColor: Globals.Proxies.atomColor(
                                     Globals.Proxies.modelLoopParam('_atom_site', '_type_symbol', index).value)
            }

            EaComponents.TableViewButton {
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this atom")
            }

        }
        // Table rows

    }

}
