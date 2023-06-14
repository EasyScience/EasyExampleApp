// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    // Table

    EaComponents.TableView {
        id: table

        property var currentValueTextInput: null

        enabled: !Globals.Proxies.main.fitting.isFittingNow
        defaultInfoText: qsTr("No parameters found")

        // Table mode

        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.

        model: Globals.Proxies.main.fittables.data.length

        // Header row

        header: EaComponents.TableViewHeader {
            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                //text: qsTr("No.")
            }

            EaComponents.TableViewLabel {
                flexibleWidth: true
                horizontalAlignment: Text.AlignLeft
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("name")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 4.0
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("value")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.0
                horizontalAlignment: Text.AlignLeft
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 4.0
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("error")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 3.0
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("vary")
            }
        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            property bool isCurrentItem: ListView.isCurrentItem
            property var item: Globals.Proxies.main.fittables.data[index]

            onIsCurrentItemChanged: {
                if (table.currentValueTextInput != valueColumn) {
                   table.currentValueTextInput = valueColumn
                }
            }

            EaComponents.TableViewLabel {
                color: EaStyle.Colors.themeForegroundMinor
                text: index + 1
            }

            EaComponents.TableViewLabel {
                text: `${item.group}.${item.parentName}.${item.name}`
                textFormat: Text.PlainText
                elide: Text.ElideMiddle
            }

            EaComponents.TableViewTextInput {
                id: valueColumn
                text: item.value.toFixed(4)
                onEditingFinished: {
                    focus = false
                    console.debug('-------------------- Fittable editing on Analysis page finished --------------------')
                    Globals.Proxies.main.fittables.edit(item.group,
                                                        item.parentIndex,
                                                        item.name,
                                                        'value',
                                                        text)
                }
            }

            EaComponents.TableViewLabel {
                text: item.unit
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewLabel {
                elide: Text.ElideNone
                text: item.error === 0 ? '' : item.error.toFixed(4)
            }

            EaComponents.TableViewCheckBox {
                id: fitColumn
                enabled: Globals.Proxies.main.experiment.defined
                checked: item.fit
                onToggled: Globals.Proxies.main.fittables.edit(item.group,
                                                               item.parentIndex,
                                                               item.name,
                                                               'fit',
                                                               checked)
            }
        }

    }

    // Parameter change slider

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.TextField {
            width: EaStyle.Sizes.fontPixelSize * 6
            text: slider.from.toFixed(4)
        }

        EaElements.Slider {
            id: slider

            enabled: !Globals.Proxies.main.fitting.isFittingNow
            width: table.width - EaStyle.Sizes.fontPixelSize * 14


            from: Globals.Proxies.main.fittables.data[table.currentIndex].min
            to: Globals.Proxies.main.fittables.data[table.currentIndex].max
            value: table.currentValueTextInput.text

            onMoved: {
                enableOpenGL()
                table.currentValueTextInput.text = value.toFixed(4)
                table.currentValueTextInput.editingFinished()
                disableOpenGL()
            }
        }

        EaElements.TextField {
            width: EaStyle.Sizes.fontPixelSize * 6
            text: slider.to.toFixed(4)
        }

    }

    // Use OpenGL on slider move only

    Timer {
        id: disableOpenGLTimer
        interval: 500
        onTriggered: disableOpenGLFromTimer()
    }

    // Logic

    function enableOpenGL() {
        if (Globals.Proxies.main.plotting.currentLib1d === 'QtCharts') {
            Globals.Refs.app.experimentPage.plotView.useOpenGL = true
            Globals.Refs.app.modelPage.plotView.useOpenGL = true
            Globals.Refs.app.analysisPage.plotView.useOpenGL = true
        }
    }

    function disableOpenGL() {
        if (Globals.Proxies.main.plotting.currentLib1d === 'QtCharts') {
            disableOpenGLTimer.restart()
        }
    }

    function disableOpenGLFromTimer() {
        Globals.Refs.app.experimentPage.plotView.useOpenGL = false
        Globals.Refs.app.modelPage.plotView.useOpenGL = false
        Globals.Refs.app.analysisPage.plotView.useOpenGL = false
    }

}
