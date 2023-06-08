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
        title: qsTr('a')
        width: parameterFieldWidth()
        text: parameterValue('_cell_length_a')
        onEditingFinished: {
            focus = false
            setParameterValue('_cell_length_a', text)
        }
        //Component.onCompleted: Globals.Refs.app.modelPage.shiftParameter = this
    }

    EaElements.Parameter {
        title: qsTr('b')
        width: parameterFieldWidth()
        text: parameterValue('_cell_length_b')
        onEditingFinished: {
            focus = false
            setParameterValue('_cell_length_b', text)
        }
        //Component.onCompleted: Globals.Refs.app.modelPage.shiftParameter = this
    }

    EaElements.Parameter {
        title: qsTr('c')
        width: parameterFieldWidth()
        text: parameterValue('_cell_length_c')
        onEditingFinished: {
            focus = false
            setParameterValue('_cell_length_c', text)
        }
        //Component.onCompleted: Globals.Refs.app.modelPage.shiftParameter = this
    }

    EaElements.Parameter {
        title: qsTr('alpha')
        width: parameterFieldWidth()
        text: parameterValue('_cell_angle_alpha')
        onEditingFinished: {
            focus = false
            setParameterValue('_cell_angle_alpha', text)
        }
        //Component.onCompleted: Globals.Refs.app.modelPage.shiftParameter = this
    }

    EaElements.Parameter {
        title: qsTr('beta')
        width: parameterFieldWidth()
        text: parameterValue('_cell_angle_beta')
        onEditingFinished: {
            focus = false
            setParameterValue('_cell_angle_beta', text)
        }
        //Component.onCompleted: Globals.Refs.app.modelPage.shiftParameter = this
    }

    EaElements.Parameter {
        title: qsTr('gamma')
        width: parameterFieldWidth()
        text: parameterValue('_cell_angle_gamma')
        onEditingFinished: {
            focus = false
            setParameterValue('_cell_angle_gamma', text)
        }
        //Component.onCompleted: Globals.Refs.app.modelPage.shiftParameter = this
    }


    // Logic

    function parameterFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - 5 * EaStyle.Sizes.fontPixelSize) / 6
    }

    function parameterValue(name) {
        if (!Globals.Proxies.main.model.defined) {
            return ''
        }
        const currentModelIndex = Globals.Proxies.main.model.currentIndex
        const item = 'value'
        const value = Globals.Proxies.main.model.dataBlocks[currentModelIndex].params[name][item]
        const formattedValue = value.toFixed(4)
        return formattedValue
    }

    function setParameterValue(name, value) {
        const page = 'model'
        const blockIndex = Globals.Proxies.main.model.currentIndex
        const item = 'value'
        Globals.Proxies.main.model.editParameter(page, blockIndex, name, item, value)
    }

}
