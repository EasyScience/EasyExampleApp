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
    id: main

    readonly property int fullWidth: width
    readonly property int nameColumnWidth: 8 * EaStyle.Sizes.fontPixelSize
    readonly property int imageHeight: 9.5 * EaStyle.Sizes.fontPixelSize
    readonly property int innerSpacing: 0.85 * EaStyle.Sizes.fontPixelSize
    readonly property int outterSpacing: 1.5 * EaStyle.Sizes.fontPixelSize

    color: 'transparent'

    // Flickable
    Flickable {
        id: flickable

        anchors.fill: parent

        contentHeight: column.height + 2 * column.y
        contentWidth: column.width

        clip: true
        flickableDirection: Flickable.VerticalFlick

        ScrollBar.vertical: EaElements.ScrollBar {
            policy: ScrollBar.AsNeeded
            interactive: false
        }

        // Main column
        Column {
            id: column

            x: 1.5 * outterSpacing
            y: outterSpacing
            width: main.width - 2 * x

            spacing: innerSpacing

            // Title
            EaElements.TextInput {
                font.family: EaStyle.Fonts.secondFontFamily
                font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
                font.weight: Font.ExtraLight
                onAccepted: focus = false
                validator: RegularExpressionValidator { regularExpression: /^[a-zA-Z][a-zA-Z0-9]{1,30}$/ }
                placeholderText: qsTr("Enter project name here")
                text: Globals.Proxies.main.project.dataBlock.name
                onEditingFinished: Globals.Proxies.main.project.setName(text)
                onFocusChanged: {
                    if (!focus && !text) {
                        text = Globals.Proxies.main.project.dataBlock.name
                    }
                }
            }
            // Title

            // Extra spacer
            Item { height: 1; width: 1 }
            // Extra spacer

            // Description & location
            Column {
                Row {
                    property var parameter: Globals.Proxies.projectMainParam('_description')
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: parent.parameter.prettyName
                    }
                    EaElements.TextInput {
                        text: parent.parameter.value
                        placeholderText: qsTr("Enter project description here")
                        onAccepted: focus = false
                        onEditingFinished: {
                            if (text) {
                                Globals.Proxies.setProjectMainParam(parent.parameter, 'value', text)
                            } else {
                                text = parent.parameter.value
                            }
                        }
                    }
                }
                Row {
                    property var parameter: Globals.Proxies.projectMainParam('_location')
                    visible: parameter.value
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: parent.parameter.prettyName
                    }
                    EaElements.Label {
                        width: column.width - nameColumnWidth
                        elide: Text.ElideMiddle
                        text: parent.parameter.value
                    }
                }
            }
            // Description & location

            // Date
            Column {
                Row {
                    property var parameter: Globals.Proxies.projectMainParam('_date_created')
                    visible: parameter.value
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: parent.parameter.prettyName
                    }
                    EaElements.Label {
                        text: parent.parameter.value
                    }
                }
                Row {
                    property var parameter: Globals.Proxies.projectMainParam('_date_last_modified')
                    visible: parameter.value
                    spacing: innerSpacing
                    EaElements.Label {
                        width: nameColumnWidth
                        font.bold: true
                        text: parent.parameter.prettyName
                    }
                    EaElements.Label {
                        text: parent.parameter.value
                    }
                }
            }
            // Date

            // Models
            Column {
                Repeater {
                    id: modelRepeater
                    model: typeof Globals.Proxies.main.project.dataBlock.loops !== 'undefined' ?
                               Globals.Proxies.main.project.dataBlock.loops._model :
                               {}
                    Row {
                        spacing: innerSpacing
                        EaElements.Label {
                            width: nameColumnWidth
                            font.bold: true
                            text: index ? '' : modelRepeater.model[index]._cif_file_name.prettyName
                        }
                        EaElements.Label {
                            text: modelRepeater.model[index]._dir_name.value +
                                  '/' +
                                  modelRepeater.model[index]._cif_file_name.value
                        }
                    }
                }
            }
            // Models

            // Model images
            Row {
                spacing: innerSpacing
                visible: childrenRect.height > 2
                Item { height: 1; width: nameColumnWidth }
                Repeater {
                    model: modelRepeater.model
                    Rectangle {
                        visible: childrenRect.height
                        height: childrenRect.height + 2 * border.width
                        width: childrenRect.width + 2 * border.width
                        border.color: EaStyle.Colors.chartAxis
                        border.width: 1
                        Image {
                            x: parent.border.width
                            y: parent.border.width
                            height: status === Image.Ready ? imageHeight : 0
                            asynchronous: true
                            mipmap: true
                            fillMode: Image.PreserveAspectFit
                            source: typeof modelRepeater.model[index]._jpg_file_name !== 'undefined' ?
                                Globals.Proxies.projectMainParam('_location').value + '/' +
                                modelRepeater.model[index]._dir_name.value + '/' +
                                modelRepeater.model[index]._jpg_file_name.value :
                                ''
                        }
                    }
                }
            }
            // Model images

            // Experiments
            Column {
                Repeater {
                    id: experimentRepeater
                    model: typeof Globals.Proxies.main.project.dataBlock.loops !== 'undefined' ?
                               Globals.Proxies.main.project.dataBlock.loops._experiment :
                               {}
                    Row {
                        //property var parameter: Globals.Proxies.projectMainParam('_description')
                        spacing: innerSpacing
                        EaElements.Label {
                            width: nameColumnWidth
                            font.bold: true
                            text: index ? '' : experimentRepeater.model[index]._cif_file_name.prettyName
                        }
                        EaElements.Label {
                            text: experimentRepeater.model[index]._dir_name.value +
                                  '/' +
                                  experimentRepeater.model[index]._cif_file_name.value
                        }
                    }
                }
            }
            // Experiments

            // Experiment images
            Row {
                spacing: innerSpacing
                visible: childrenRect.height > 2
                Item { height: 1; width: nameColumnWidth }
                Repeater {
                    model: experimentRepeater.model
                    Rectangle {
                        visible: childrenRect.height
                        height: childrenRect.height + 2 * border.width
                        width: childrenRect.width + 2 * border.width
                        border.color: EaStyle.Colors.chartAxis
                        border.width: 1
                        Image {
                            x: parent.border.width
                            y: parent.border.width
                            height: status === Image.Ready ? imageHeight : 0
                            asynchronous: true
                            mipmap: true
                            fillMode: Image.PreserveAspectFit
                            source: typeof experimentRepeater.model[index]._jpg_file_name !== 'undefined' ?
                                Globals.Proxies.projectMainParam('_location').value + '/' +
                                experimentRepeater.model[index]._dir_name.value + '/' +
                                experimentRepeater.model[index]._jpg_file_name.value :
                                ''

                        }
                    }
                }
            }
            // Experiment images
        }
        // Main column
    }
    // Flickable
}
