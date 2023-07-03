// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.TextArea {
    id: textArea

    property string fullCif: Globals.Proxies.main.experiment.dataBlocksCif +
                             Globals.Proxies.main.experiment.dataBlocksCifMeasOnly
    property bool cifEdited: textArea.text !== fullCif

    //readOnly: true

    width: EaStyle.Sizes.sideBarContentWidth
    backgroundRect.border.color: EaStyle.Colors.appBarComboBoxBorder

    font.family: EaStyle.Fonts.monoFontFamily

    text: fullCif

    // Tool buttons
    Row {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.rightMargin: EaStyle.Sizes.fontPixelSize
        spacing: 0.25 * EaStyle.Sizes.fontPixelSize

        EaElements.TabButton {
            enabled: cifEdited
            highlighted: cifEdited
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "check"
            ToolTip.text: qsTr("Apply all changes")
            //onClicked: forceActiveFocus()
            onClicked: {
                Globals.Proxies.main.experiment.loadExperimentFromCif(textArea.text)
                forceActiveFocus()
            }
        }

        EaElements.TabButton {
            enabled: cifEdited
            highlighted: cifEdited
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "undo"
            ToolTip.text: qsTr("Undo all changes")
            onClicked: {
                textArea.text = fullCif
                forceActiveFocus()
            }
        }

    }
    // Tool buttons

}
