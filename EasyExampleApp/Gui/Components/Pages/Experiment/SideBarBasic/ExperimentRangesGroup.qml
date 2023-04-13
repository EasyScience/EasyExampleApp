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

    EaElements.Parameter {
        enabled: false
        title: qsTr('X min')
        width: parameterFieldWidth()
        text: parameterValue('xMin')
    }

    EaElements.Parameter {
        enabled: false
        title: qsTr('X max')
        width: parameterFieldWidth()
        text: parameterValue('xMax')
    }

    EaElements.Parameter {
        enabled: Globals.Vars.allowEditExperimentalRanges
        title: qsTr('X step')
        width: parameterFieldWidth()
        text: parameterValue('xStep')
        onEditingFinished: {
            focus = false
            setParameterValue('xStep', text)
            Globals.Proxies.main.experiment.load()
        }
    }

    // Logic

    function parameterFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - 2 * EaStyle.Sizes.fontPixelSize) / 3
    }

    function parameterValue(name) {
        if (!Globals.Proxies.main.experiment.defined) {
            return ''
        }
        const currentExperimentIndex = Globals.Proxies.main.experiment.currentIndex
        const item = 'value'
        const value = Globals.Proxies.main.experiment.dataBlocks[currentExperimentIndex].params[name][item]
        const formattedValue = value.toFixed(4)
        return formattedValue
    }

    function setParameterValue(name, value) {
        const page = 'experiment'
        const blockIndex = Globals.Proxies.main.experiment.currentIndex
        const item = 'value'
        Globals.Proxies.main.experiment.editParameter(page, blockIndex, name, item, value)
    }
}
