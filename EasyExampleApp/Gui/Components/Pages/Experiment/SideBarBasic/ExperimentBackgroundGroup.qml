// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


Row {
    spacing: EaStyle.Sizes.fontPixelSize

    EaElements.ComboBox {
        y: EaStyle.Sizes.fontPixelSize * 1.5
        model: ["Point background"]

        EaElements.Label {
            y: -parent.y
            enabled: false
            text: qsTr('Type')
        }
        width: parameterFieldWidth() * 2 + EaStyle.Sizes.fontPixelSize
    }

    EaElements.Parameter {
        title: qsTr('Value')
        width: parameterFieldWidth()
        text: parameterValue('background')
        onEditingFinished: setParameterValue('background', text)
    }

    // Logic

    function parameterFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - 2 * EaStyle.Sizes.fontPixelSize) / 3
    }

    function parameterValue(name) {
        if (!Globals.Proxies.main.experiment.created) {
            return ''
        }
        const currentExperimentIndex = 0
        const item = 'value'
        const value = Globals.Proxies.main.experiment.data[currentExperimentIndex].params[name][item]
        const formattedValue = value.toFixed(4)
        return formattedValue
    }

    function setParameterValue(name, value) {
        const currentExperimentIndex = 0
        const item = 'value'
        const needSetFittables = true
        Globals.Proxies.main.experiment.editParameter(currentExperimentIndex,
                                                      name,
                                                      item,
                                                      value,
                                                      needSetFittables)
    }
}
