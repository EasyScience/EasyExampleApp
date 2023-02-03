// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals


Rectangle {
    readonly property int commonSpacing: EaStyle.Sizes.fontPixelSize * 1.5

    color: EaStyle.Colors.mainContentBackground

    Column {

        anchors.left: parent.left
        anchors.leftMargin: commonSpacing
        anchors.top: parent.top
        anchors.topMargin: commonSpacing * 0.5
        spacing: commonSpacing

        EaElements.TextInput {
            font.family: EaStyle.Fonts.secondFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
            font.weight: Font.ExtraLight
            text: ExGlobals.Proxies.mainProxy.project.projectInfoAsJson.name
        }

        Grid {
            columns: 2
            rowSpacing: 0
            columnSpacing: commonSpacing

            EaElements.Label {
                font.bold: true
                text: qsTr("Short description:")
            }
            EaElements.TextInput {
                text: ExGlobals.Proxies.mainProxy.project.projectInfoAsJson.short_description
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Location:")
            }
            EaElements.Label {
                text: ExGlobals.Proxies.mainProxy.project.currentProjectPath
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Modified:")
            }
            EaElements.Label {
                text: ExGlobals.Proxies.mainProxy.project.projectInfoAsJson.modified
            }
        }

    }

}
