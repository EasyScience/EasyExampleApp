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
    readonly property int innerSpacing: 0.75 * EaStyle.Sizes.fontPixelSize
    readonly property int outterSpacing: 1.5 * EaStyle.Sizes.fontPixelSize
    readonly property int nameColumnWidth: 9 * EaStyle.Sizes.fontPixelSize

    color: EaStyle.Colors.mainContentBackground

    // Main column
    Column {
        anchors.top: parent.top
        anchors.left: parent.left

        anchors.topMargin: outterSpacing
        anchors.leftMargin: outterSpacing * 1.5

        spacing: innerSpacing

        // Title
        EaElements.TextInput {
            font.family: EaStyle.Fonts.secondFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
            font.weight: Font.ExtraLight
            text: Globals.Proxies.main.project.data.name
            onEditingFinished: Globals.Proxies.main.project.editData('name', text)
        }
        // Title

        // Extra spacer
        Item { height: 1; width: 1 }
        // Extra spacer

        // Description
        Column {
            Row {
                property var parameter: Globals.Proxies.projectMainParam('_description')
                EaElements.Label {
                    width: nameColumnWidth
                    font.bold: true
                    text: parent.parameter.prettyName ?? ''
                }
                EaElements.TextInput {
                    text: parent.parameter.value ?? ''
                    //onEditingFinished: Globals.Proxies.main.project.editData('description', text)
                }
            }
        }
        // Description

        // Date
        Column {
            Row {
                property var parameter: Globals.Proxies.projectMainParam('_date_created')
                EaElements.Label {
                    width: nameColumnWidth
                    font.bold: true
                    text: parent.parameter.prettyName ?? ''
                }
                EaElements.Label {
                    text: parent.parameter.value ?? ''
                }
            }
            Row {
                property var parameter: Globals.Proxies.projectMainParam('_date_last_modified')
                EaElements.Label {
                    width: nameColumnWidth
                    font.bold: true
                    text: parent.parameter.prettyName ?? ''
                }
                EaElements.Label {
                    text: parent.parameter.value ?? ''
                }
            }
        }
        // Date

        // Models
        Column {
            Repeater {
                id: modelRepeater
                model: typeof Globals.Proxies.main.project.data.loops !== 'undefined' ?
                           Globals.Proxies.main.project.data.loops._model :
                           {}
                Row {
                    //property var parameter: Globals.Proxies.projectMainParam('_description')
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: index ? '' : modelRepeater.model[index]._file_name.prettyName
                    }
                    EaElements.Label {
                        text: modelRepeater.model[index]._dir_name.value +
                              '/' +
                              modelRepeater.model[index]._file_name.value
                    }
                }
            }
        }
        // Models

        // Experiments
        Column {
            Repeater {
                id: experimentRepeater
                model: typeof Globals.Proxies.main.project.data.loops !== 'undefined' ?
                           Globals.Proxies.main.project.data.loops._experiment :
                           {}
                Row {
                    //property var parameter: Globals.Proxies.projectMainParam('_description')
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: index ? '' : experimentRepeater.model[index]._file_name.prettyName
                    }
                    EaElements.Label {
                        text: experimentRepeater.model[index]._dir_name.value +
                              '/' +
                              experimentRepeater.model[index]._file_name.value
                    }
                }
            }
        }
        // Experiments

        // Project image
        Image {
            //visible: Globals.Proxies.main.fitting.isFitFinished

            //source: Globals.Proxies.main.project.image
            width: EaStyle.Sizes.fontPixelSize * 25
            fillMode: Image.PreserveAspectFit
        }

    }
    // Main column

}
