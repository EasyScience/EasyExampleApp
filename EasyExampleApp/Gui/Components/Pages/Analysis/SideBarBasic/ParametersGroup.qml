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

        model: EaComponents.JsonListModel {
            json: JSON.stringify(Globals.Proxies.main.fittables.data)
            query: "$[*]"
        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {
            property bool isCurrentItem: ListView.isCurrentItem
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
                text: `${model.group}.${model.parentName}.${model.name}`
                textFormat: Text.PlainText
                elide: Text.ElideMiddle
            }

            EaComponents.TableViewTextInput {
                id: valueColumn
                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 4
                headerText: qsTr("Value")
                text: model.value.toFixed(4)
                onEditingFinished: Globals.Proxies.main.fittables.edit(model.group,
                                                                       model.parentIndex,
                                                                       model.name,
                                                                       'value',
                                                                       text)
            }

            EaComponents.TableViewLabel {
                id: unitColumn
                horizontalAlignment: Text.AlignLeft
                width: EaStyle.Sizes.fontPixelSize * 2
                text: model.unit
                color: EaStyle.Colors.themeForegroundMinor
            }

            EaComponents.TableViewLabel {
                id: errorColumn
                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 4
                elide: Text.ElideNone
                headerText: qsTr("Error")
                text: model.error === 0 ? '' :  model.error.toFixed(4)
            }

            EaComponents.TableViewCheckBox {
                id: fitColumn
                enabled: Globals.Proxies.main.experiment.created
                headerText: qsTr("Fit")
                checked: model.fit
                onCheckedChanged: Globals.Proxies.main.fittables.edit(model.group,
                                                                      model.parentIndex,
                                                                      model.name,
                                                                      'fit',
                                                                      checked)
            }
        }

    }

    // Parameter change slider

    EaElements.Slider {
        id: slider

        width: table.width

        from: table.model.get(table.currentIndex).min
        to: table.model.get(table.currentIndex).max
        value: table.currentValueTextInput.text

        onMoved: {
            const calcSerie = Globals.Proxies.main.plotting.appChartRefs.QtCharts.analysisPage.calcSerie
            if (!EaGlobals.Variables.useOpenGL && typeof calcSerie !== 'undefined') {
                calcSerie.useOpenGL = true
            }
            table.currentValueTextInput.text = value.toFixed(4)
            table.currentValueTextInput.editingFinished()
            if (!EaGlobals.Variables.useOpenGL && typeof calcSerie !== 'undefined') {
                disableOpenGLTimer.restart()
            }
        }
    }

    // Use OpenGL on slider move only

    Timer {
        id: disableOpenGLTimer
        interval: 500
        onTriggered: calcSerie.useOpenGL = false
    }

    // Control buttons below table

    EaElements.SideBarButton {
        enabled: Globals.Proxies.main.experiment.created
        wide: true

        fontIcon: 'play-circle'
        text: qsTr('Start fitting')

        onClicked: Globals.Proxies.main.fitting.fit()

        Component.onCompleted: Globals.Refs.app.analysisPage.startFittingButton = this
    }

}
