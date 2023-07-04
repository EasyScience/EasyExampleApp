// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls
import QtCharts

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    // Filter parameters widget
    Row {
        spacing: EaStyle.Sizes.fontPixelSize * 0.5

        // Filter criteria
        EaElements.TextField {
            id: filterCriteriaField

            width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

            placeholderText: qsTr("Filter criteria")

            onTextChanged: {
                nameFilterSelector.currentIndex = nameFilterSelector.indexOfValue(text)
                Globals.Proxies.main.fittables.nameFilterCriteria = text
            }
        }
        // Filter criteria

        // Filter by name
        EaElements.ComboBox {
            id: nameFilterSelector

            topInset: 0
            bottomInset: 0

            width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

            valueRole: "value"
            textRole: "text"

            displayText: currentIndex === -1 ? qsTr("Filter by name") : currentText

            model: [
                { value: "", text: qsTr("All types") },
                { value: "cell", text: "Unit cell" },
                { value: "fract", text: "Atomic coordinates" },
                { value: "B_iso", text: "Atomic displacement" },
                { value: "occupancy", text: "Atomic occupancies" },
                { value: "resolution", text: "Instrument resolution" },
                { value: "asymmetry", text: "Peak asymmetry" }
            ]

            onActivated: filterCriteriaField.text = currentValue
        }
        // Filter by name

        // Filter by variability
        EaElements.ComboBox {
            id: variabilityFilterSelector

            property int lastIndex: -1

            topInset: 0
            bottomInset: 0

            width: (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 3

            displayText: currentIndex === -1 ? qsTr("Filter by variability") : currentText

            valueRole: "value"
            textRole: "text"

            model: [
                { value: 'all', text: `All parameters (${Globals.Proxies.main.fittables.freeParamsCount +
                                                       Globals.Proxies.main.fittables.fixedParamsCount})` },
                { value: 'free', text: `Free parameters (${Globals.Proxies.main.fittables.freeParamsCount})` },
                { value: 'fixed', text: `Fixed parameters (${Globals.Proxies.main.fittables.fixedParamsCount})` }
            ]
            onModelChanged: currentIndex = lastIndex

            onActivated: {
                lastIndex = currentIndex
                Globals.Proxies.main.fittables.variabilityFilterCriteria = currentValue
            }
        }
        // Filter by variability

    }
    // Filter parameters widget

    // Table
    EaComponents.TableView {
        id: table

        property var currentValueTextInput: null

        enabled: !Globals.Proxies.main.fitting.isFittingNow
        defaultInfoText: qsTr("No parameters found")

        maxRowCountShow: 6 +
                         Math.trunc((applicationWindow.height - EaStyle.Sizes.appWindowMinimumHeight) /
                                    EaStyle.Sizes.tableRowHeight)

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
                width: EaStyle.Sizes.fontPixelSize * 4.5
                horizontalAlignment: Text.AlignRight
                color: EaStyle.Colors.themeForegroundMinor
                text: qsTr("value")
            }

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.0
                horizontalAlignment: Text.AlignLeft
                //text: qsTr("units")
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
        // Header row

        // Table content row
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
                text: parameterName(item)
                textFormat: Text.PlainText
                elide: Text.ElideMiddle
            }

            EaComponents.TableViewParameter {
                id: valueColumn
                enabled: item.enabled ?? true  // NEED FIX
                fit: item.fit
                text: item.value.toFixed(4)
                onEditingFinished: {
                    focus = false
                    console.debug("-------------------- Editing 'value' field of fittable on Analysis page --------------------")
                    Globals.Proxies.main.fittables.edit(item.blockType,
                                                        item.blockIndex,
                                                        item.loopName,
                                                        item.paramIndex,
                                                        item.paramName,
                                                        'value',
                                                        text)
                }
            }

            EaComponents.TableViewLabel {
                text: item.units
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
                onToggled: {
                    console.debug("-------------------- Editing 'fit' field of fittable on Analysis page --------------------")
                    Globals.Proxies.main.fittables.edit(item.blockType,
                                                        item.blockIndex,
                                                        item.loopName,
                                                        item.paramIndex,
                                                        item.paramName,
                                                        'fit',
                                                        checked)
                }
            }
        }
        // Table content row
    }
    // Table

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

            onMoved: moveDelayTimer.restart()
        }

        EaElements.TextField {
            width: EaStyle.Sizes.fontPixelSize * 6
            text: slider.to.toFixed(4)
        }

    }
    // Slider

    // Move delay timer

    Timer {
        id: moveDelayTimer
        interval: 50
        onTriggered: {
            if (table.currentValueTextInput.text !== slider.value.toFixed(4)) {
                //enableOpenGL()
                table.currentValueTextInput.text = slider.value.toFixed(4)
                table.currentValueTextInput.editingFinished()
                //disableOpenGL()
            }
        }
    }

    // Use OpenGL on slider move only

    Timer {
        id: disableOpenGLTimer
        interval: 1500
        onTriggered: disableOpenGLFromTimer()
    }

    // Logic

    function parameterName(item) {
        let name
        if (typeof item.loopName === 'undefined') {
            name = `${item.blockType}[${item.blockIndex}].${item.paramName}`
        } else {
            name = `${item.blockType}[${item.blockIndex}].${item.loopName}[${item.paramIndex}].${item.paramName}`
        }
        name = name.replace(/\._/g, ".")  // replace all '._' to '.' for prettier name
        return name
    }

    function enableOpenGL() {
        if (Globals.Proxies.main.plotting.currentLib1d === 'QtCharts') {
            Globals.Refs.app.experimentPage.plotView.useOpenGL = true
            //Globals.Refs.app.modelPage.plotView.useOpenGL = true
            Globals.Refs.app.analysisPage.plotView.useAnimation = false
            Globals.Refs.app.analysisPage.plotView.useOpenGL = true
        }
    }

    function disableOpenGL() {
        if (Globals.Proxies.main.plotting.currentLib1d === 'QtCharts') {
            ////Globals.Proxies.main.plotting.chartRefs.QtCharts.analysisPage.totalCalcSerie.pointsReplaced()
            disableOpenGLTimer.restart()
        }
    }

    function disableOpenGLFromTimer() {
        Globals.Refs.app.experimentPage.plotView.useOpenGL = false
        //Globals.Refs.app.modelPage.plotView.useOpenGL = false
        ////Globals.Proxies.main.plotting.chartRefs.QtCharts.analysisPage.totalCalcSerie.pointsReplaced()
        ///console.error(Globals.Proxies.main.plotting.chartRefs.QtCharts.analysisPage.totalCalcSerie)
        Globals.Refs.app.analysisPage.plotView.useAnimation = true
        Globals.Refs.app.analysisPage.plotView.useOpenGL = false
    }

}
