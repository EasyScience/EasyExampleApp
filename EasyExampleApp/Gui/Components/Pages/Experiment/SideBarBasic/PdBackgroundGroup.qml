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

        defaultInfoText: qsTr("No background points defined")

        // Table model

        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.

        model: Globals.Proxies.main.experiment.dataBlocks[Globals.Proxies.main.model.currentIndex].loops._pd_background.length

        // Header row

        header: EaComponents.TableViewHeader {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                text: qsTr("No.")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 11.0
                horizontalAlignment: Text.AlignRight
                text: qsTr("2θ")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 11.0
                horizontalAlignment: Text.AlignRight
                text: qsTr("Intensity")
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                text: qsTr("Del.")
            }

        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                text: index + 1
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.experimentLoopParameterValue('_pd_background', '_2theta', index)
            }

            EaComponents.TableViewTextInput {
                text: Globals.Proxies.experimentLoopParameterValue('_pd_background', '_intensity', index)
            }

            EaComponents.TableViewLabel {
            }

            EaComponents.TableViewButton {
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this point")
                onClicked: Globals.Proxies.main.model.removeModel(index)
            }

        }

        onCurrentIndexChanged: Globals.Proxies.main.model.currentIndex = currentIndex
    }

}
