// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


Rectangle {
    readonly property int commonSpacing: EaStyle.Sizes.fontPixelSize * 1.5

    color: EaStyle.Colors.mainContentBackground

    Column {

        anchors.top: parent.top
        anchors.left: parent.left

        anchors.topMargin: commonSpacing
        anchors.leftMargin: commonSpacing * 1.5

        spacing: commonSpacing

        // Project title

        EaElements.TextInput {
            font.family: EaStyle.Fonts.secondFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
            font.weight: Font.ExtraLight
            text: Globals.Proxies.main.project.data.name
            onEditingFinished: Globals.Proxies.main.project.editData('name', text)
        }

        // Project info

        Grid {
            columns: 2
            rowSpacing: 0
            columnSpacing: commonSpacing

            EaElements.Label {
                visible: Globals.Proxies.main.project.data.items._short_description
                font.bold: true
                text: qsTr("Short description:")
            }
            EaElements.TextInput {
                text: Globals.Proxies.main.project.data.items._short_description
                //onEditingFinished: Globals.Proxies.main.project.editData('description', text)
            }

            /*
            EaElements.Label {
                visible: Globals.Proxies.main.project.data.location
                font.bold: true
                text: qsTr("Location:")
            }
            EaElements.Label {
                text: Globals.Proxies.main.project.data.location
            }
            */

            EaElements.Label {
                visible: Globals.Proxies.main.project.data.items._modified
                font.bold: true
                text: qsTr("Modified:")
            }
            EaElements.Label {
                text: Globals.Proxies.main.project.data.items._modified
            }

            EaElements.Label {
                visible: Globals.Proxies.main.project.data.loops._model_file._name
                font.bold: true
                text: qsTr("Model file(s):")
            }
            EaElements.Label {
                text: Globals.Proxies.main.project.data.loops._model_file._name.join(', ')
            }

            EaElements.Label {
                visible: Globals.Proxies.main.project.data.loops._experiment_file._name
                font.bold: true
                text: qsTr("Experiment file(s):")
            }
            EaElements.Label {
                text: Globals.Proxies.main.project.data.loops._experiment_file._name.join(', ')
            }

        }

        // Project image

        Image {
            //visible: Globals.Proxies.main.fitting.isFitFinished

            //source: Globals.Proxies.main.project.image
            width: EaStyle.Sizes.fontPixelSize * 25
            fillMode: Image.PreserveAspectFit
        }

    }

}
