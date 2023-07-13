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


EaComponents.TableView {
    id: tableView

    property int modelCurrentIndex: Globals.Proxies.main.model.currentIndex

    defaultInfoText: qsTr("No models defined")

    maxRowCountShow: 3
    onModelCurrentIndexChanged: currentIndex = Globals.Proxies.main.model.currentIndex
    onCurrentIndexChanged: Globals.Proxies.main.model.currentIndex = currentIndex

    model: Globals.Proxies.main.model.dataBlocks

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

    }
    // Header row

    // Table rows
    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            text: index + 1
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewButton {
            fontIcon: "layer-group"
            ToolTip.text: qsTr("Calculated pattern color")
            outlineIcon: true
            backgroundColor: "transparent"
            borderColor: "transparent"
            iconColor: EaStyle.Colors.chartForegrounds[index]
        }

        EaComponents.TableViewParameter {
            enabled: false
            text: tableView.model[index].name
        }

    }
    // Table rows

    Component.onCompleted: Globals.Refs.app.modelPage.modelsExplorer = this

}
