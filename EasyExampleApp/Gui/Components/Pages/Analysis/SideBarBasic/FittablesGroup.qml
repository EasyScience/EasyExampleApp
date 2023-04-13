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

        defaultInfoText: qsTr("No parameters found")

        // Table mode

        // We only use the length of the model object defined in backend logic and
        // directly access that model in every row using the TableView index property.

        model: Globals.Proxies.main.fittables.data.length

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
                id: numberColumn
                width: EaStyle.Sizes.fontPixelSize * 2.5
                headerText: qsTr("No.")
                text: index + 1
            }

            EaComponents.TableViewLabel {
                id: labelColumn
                horizontalAlignment: Text.AlignLeft
                width: table.width -
                       (parent.children.length - 1) * EaStyle.Sizes.tableColumnSpacing -
                       numberColumn.width -
                       valueColumn.width -
                       unitColumn.width -
                       errorColumn.width -
                       fitColumn.width
                headerText: qsTr("Name")
                text: `${item.group}.${item.parentName}.${item.name}`
                textFormat: Text.PlainText
                elide: Text.ElideMiddle
            }

            EaComponents.TableViewTextInput {
                id: valueColumn
                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 4
                headerText: qsTr("Value")
                text: item.value.toFixed(4)
                onEditingFinished: {
                    focus = false
                    Globals.Proxies.main.fittables.edit(item.group,
                                                        item.parentIndex,
                                                        item.name,
                                                        'value',
                                                        text)
                }
            }

            EaComponents.TableViewLabel {
                id: unitColumn
                horizontalAlignment: Text.AlignLeft
                width: EaStyle.Sizes.fontPixelSize * 2
                text: item.unit
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewLabel {
                id: errorColumn
                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 4
                elide: Text.ElideNone
                headerText: qsTr("Error")
                text: item.error === 0 ? '' : item.error.toFixed(4)
            }

            EaComponents.TableViewCheckBox {
                id: fitColumn
                enabled: Globals.Proxies.main.experiment.defined
                headerText: qsTr("Fit")
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

    EaElements.Slider {
        id: slider

        width: table.width

        from: Globals.Proxies.main.fittables.data[table.currentIndex].min
        to: Globals.Proxies.main.fittables.data[table.currentIndex].max
        value: table.currentValueTextInput.text

        onMoved: {
            if (!EaGlobals.Vars.useOpenGL && typeof totalCalcSerie() !== 'undefined') {
                totalCalcSerie().useOpenGL = true
            }
            if (!EaGlobals.Vars.useOpenGL && typeof bkgSerie() !== 'undefined') {
                bkgSerie().useOpenGL = true
            }
            table.currentValueTextInput.text = value.toFixed(4)
            table.currentValueTextInput.editingFinished()
            if (!EaGlobals.Vars.useOpenGL && typeof totalCalcSerie() !== 'undefined') {
                disableOpenGLTimer.restart()
            }
            if (!EaGlobals.Vars.useOpenGL && typeof bkgSerie() !== 'undefined') {
                disableOpenGLTimer.restart()
            }
        }
    }

    // Use OpenGL on slider move only

    Timer {
        id: disableOpenGLTimer
        interval: 500
        onTriggered: {
            bkgSerie().useOpenGL = false
            totalCalcSerie().useOpenGL = false
        }
    }

    // Control buttons below table

    EaElements.SideBarButton {
        enabled: Globals.Proxies.main.experiment.defined
        wide: true

        fontIcon: 'play-circle'
        text: qsTr('Start fitting')

        onClicked: Globals.Proxies.main.fitting.fit()

        Component.onCompleted: Globals.Refs.app.analysisPage.startFittingButton = this
    }

    // Logic

    function bkgSerie() {
        return Globals.Proxies.main.plotting.chartRefs.QtCharts.analysisPage.bkgSerie
    }

    function totalCalcSerie() {
        return Globals.Proxies.main.plotting.chartRefs.QtCharts.analysisPage.totalCalcSerie
    }

}
