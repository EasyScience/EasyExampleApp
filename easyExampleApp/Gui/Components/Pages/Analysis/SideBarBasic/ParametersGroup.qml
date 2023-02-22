// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    // Table

    EaComponents.TableView {
        id: table

        defaultInfoText: qsTr("No parameters found")

        // Table model

        model: EaComponents.JsonListModel {
            json: JSON.stringify(Globals.Proxies.mainProxy.parameters.asJson)
            query: "$[*]"
        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                id: numberColumn
                width: EaStyle.Sizes.fontPixelSize * 2.5
                headerText: "No."
                text: model.number
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
                headerText: "Label"
                text: model.label
                textFormat: Text.PlainText
                elide: Text.ElideMiddle
            }

            EaComponents.TableViewTextInput {
                id: valueColumn
                horizontalAlignment: Text.AlignRight
                width: EaStyle.Sizes.fontPixelSize * 4
                headerText: "Value"
                text: model.value.toFixed(4)
                onEditingFinished: Globals.Proxies.mainProxy.parameters.editParameterValue(model.id, text)
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
                headerText: "Error"
                text: Globals.Proxies.mainProxy.fitting.isFitFinished ? model.error.toFixed(4) : ''
            }

            EaComponents.TableViewCheckBox {
                id: fitColumn
                enabled: Globals.Proxies.mainProxy.experiment.isCreated
                headerText: "Fit"
                checked: model.fit
                //onCheckedChanged: Globals.Proxies.mainProxy.parameters.editParameterFit(model.id, checked)
            }
        }

    }

    // Parameter change slider

    EaElements.Slider {
        id: slider

        width: table.width

        from: table.model.get(table.currentIndex).min
        to: table.model.get(table.currentIndex).max
        value: table.model.get(table.currentIndex).value

        onMoved: Globals.Proxies.mainProxy.parameters.editParameterValue(
                     table.model.get(table.currentIndex).id,
                     value)

        onPressedChanged: {
            if (!pressed) {
                Globals.Proxies.mainProxy.parameters.generateAsJson()
            }
        }
    }

    // Control buttons below table

    EaElements.SideBarButton {
        enabled: Globals.Proxies.mainProxy.experiment.isCreated
        wide: true

        fontIcon: 'play-circle'
        text: qsTr('Start fitting')

        onClicked: Globals.Proxies.mainProxy.fitting.fit()

        Component.onCompleted: Globals.Refs.app.analysisPage.startFittingButton = this
    }

}
