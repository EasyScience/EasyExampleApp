// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Animations as EaAnimations
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


Rectangle {
    id: container

    width: EaStyle.Sizes.sideBarContentWidth
    height: 11 * EaStyle.Sizes.tableRowHeight -
            EaStyle.Sizes.fontPixelSize * (Globals.Proxies.main.model.dataBlocks.length - 1) -
            1.4 * EaStyle.Sizes.fontPixelSize +
            (applicationWindow.height - EaStyle.Sizes.appWindowMinimumHeight)

    color: enabled ? EaStyle.Colors.textViewBackground : EaStyle.Colors.textViewBackgroundDisabled
    Behavior on color { EaAnimations.ThemeChange {} }

    border.color: EaStyle.Colors.appBarComboBoxBorder

    // ListView
    ListView {
        id: listView

        property var firstDelegateRef: null
        property bool cifEdited: listView.firstDelegateRef === null ?
                                     false :
                                     listView.firstDelegateRef.text !== Globals.Proxies.main.model.dataBlocksCif[0]

        anchors.fill: parent
        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.bottomMargin: EaStyle.Sizes.fontPixelSize
        anchors.leftMargin: EaStyle.Sizes.fontPixelSize

        clip: true

        ScrollBar.vertical: EaElements.ScrollBar {
            policy: ScrollBar.AsNeeded
            interactive: false
        }

        model: Globals.Proxies.main.model.dataBlocksCif

        // ListView Delegate
        delegate: TextEdit {
            font.family: EaStyle.Fonts.monoFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize

            color: enabled ?
                       EaStyle.Colors.themeForeground :
                       EaStyle.Colors.themeForegroundDisabled
            Behavior on color { EaAnimations.ThemeChange {} }

            text: Globals.Proxies.main.model.dataBlocksCif[index]

            Component.onCompleted: {
                if (index === 0) {
                    listView.firstDelegateRef = this
                }
            }
       }
        // ListView Delegate

    }
    // ListView

    // Tool buttons
    Row {
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.rightMargin: EaStyle.Sizes.fontPixelSize
        spacing: 0.25 * EaStyle.Sizes.fontPixelSize

        EaElements.TabButton {
            enabled: listView.cifEdited
            highlighted: listView.cifEdited
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "check"
            ToolTip.text: qsTr("Apply changes")
            //onClicked: forceActiveFocus()
            onClicked: {
                Globals.Proxies.main.model.loadModelFromEdCif(listView.firstDelegateRef.text)
                forceActiveFocus()
            }
        }

        EaElements.TabButton {
            enabled: listView.cifEdited
            highlighted: listView.cifEdited
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "undo"
            ToolTip.text: qsTr("Undo all changes")
            onClicked: {
                listView.firstDelegateRef.text = Globals.Proxies.main.model.dataBlocksCif[0]
                forceActiveFocus()
            }
        }

    }
    // Tool buttons
}
