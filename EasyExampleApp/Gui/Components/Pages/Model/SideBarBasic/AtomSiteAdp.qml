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
                width: EaStyle.Sizes.fontPixelSize * 4.0
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_label', 0).prettyName
           }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_adp_type', 0).prettyName
            }

            EaComponents.TableViewLabel {
                id: atomSiteIso
                width: EaStyle.Sizes.fontPixelSize * 3.7
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: Globals.Proxies.modelLoopParam('_atom_site', '_B_iso_or_equiv', 0).prettyName
            }

            EaComponents.TableViewLabel {
                width: atomSiteIso.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("ani11")
            }

            EaComponents.TableViewLabel {
                width: atomSiteIso.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("ani22")
            }

            EaComponents.TableViewLabel {
                width: atomSiteIso.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("ani33")
            }

            EaComponents.TableViewLabel {
                width: atomSiteIso.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("ani12")
            }

            EaComponents.TableViewLabel {
                width: atomSiteIso.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("ani13")
            }

            EaComponents.TableViewLabel {
                width: atomSiteIso.width
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("ani23")
            }

            // Temporary fix for right margin
            EaComponents.TableViewLabel {
                width: 1
            }

        }
        // Header row

        // Table rows
        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                text: index + 1
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_label', index)
            }

            EaComponents.TableViewParameter {
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_adp_type', index)
            }

            EaComponents.TableViewParameter {
                id: iso
                parameter: Globals.Proxies.modelLoopParam('_atom_site', '_B_iso_or_equiv', index)
                onEditingFinished: Globals.Proxies.setModelLoopParam(parameter, 'value', text)
                fitCheckBox.onToggled: Globals.Proxies.setModelLoopParam(parameter, 'fit', fitCheckBox.checked)
            }

            EaComponents.TableViewParameter {
                enabled: false
                text: iso.text
            }

            EaComponents.TableViewParameter {
                enabled: false
                text: iso.text
            }

            EaComponents.TableViewParameter {
                enabled: false
                text: iso.text
            }

            EaComponents.TableViewParameter {
                enabled: false
                text: '0.0000'
            }

            EaComponents.TableViewParameter {
                enabled: false
                text: '0.0000'
            }

            EaComponents.TableViewParameter {
                enabled: false
                text: '0.0000'
            }

            // Temporary fix for right margin
            EaComponents.TableViewLabel {}

        }
        // Table rows

    }

}
