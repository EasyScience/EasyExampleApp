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

        model: Globals.Proxies.main.model.dataBlocks[Globals.Proxies.main.model.currentIndex].loops._atom_site.length

        // Header row

        header: EaComponents.TableViewHeader {

            EaComponents.TableViewLabel {
                enabled: false
                width: EaStyle.Sizes.fontPixelSize * 2.5
                //text: qsTr("No.")
            }

            EaComponents.TableViewLabel {
                id: atomSiteLabel
                width: EaStyle.Sizes.fontPixelSize * 4.39
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("label")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("type")
            }

            EaComponents.TableViewLabel {
                width: atomSiteLabel.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("fract x")
            }

            EaComponents.TableViewLabel {
                width: atomSiteLabel.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("fract y")
            }

            EaComponents.TableViewLabel {
                width: atomSiteLabel.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("fract z")
            }

            EaComponents.TableViewLabel {
                width: atomSiteLabel.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("occ.")
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

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                text: index + 1
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.modelLoopParameterValue('_atom_site', '_label', index)
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.modelLoopParameterValue('_atom_site', '_type_symbol', index)
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.modelLoopParameterValue('_atom_site', '_fract_x', index)
                onEditingFinished: Globals.Proxies.setModelLoopParameterValue('_atom_site', '_fract_x', index, text)
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.modelLoopParameterValue('_atom_site', '_fract_y', index)
                onEditingFinished: Globals.Proxies.setModelLoopParameterValue('_atom_site', '_fract_y', index, text)
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.modelLoopParameterValue('_atom_site', '_fract_z', index)
                onEditingFinished: Globals.Proxies.setModelLoopParameterValue('_atom_site', '_fract_z', index, text)
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.modelLoopParameterValue('_atom_site', '_occupancy', index)
                onEditingFinished: Globals.Proxies.setModelLoopParameterValue('_atom_site', '_occupancy', index, text)
            }

            EaComponents.TableViewLabel {
                backgroundColor: Globals.Proxies.atomColor(Globals.Proxies.modelLoopParameterValue('_atom_site', '_type_symbol', index))
            }

            EaComponents.TableViewButton {
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this atom")
                //onClicked: Globals.Proxies.main.model.removeModel(index)
            }

        }

        onCurrentIndexChanged: Globals.Proxies.main.model.currentIndex = currentIndex
    }

}
