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
        title: qsTr('Shift')
        width: parameterFieldWidth()
        text: parameterValue('shift')
        onEditingFinished: {
            focus = false
            setParameterValue('shift', text)
        }
        Component.onCompleted: Globals.Refs.app.modelPage.shiftParameter = this
    }

    EaElements.Parameter {
        title: qsTr('Width')
        width: parameterFieldWidth()
        text: parameterValue('width')
        onEditingFinished: {
            focus = false
            setParameterValue('width', text)
        }
        Component.onCompleted: Globals.Refs.app.modelPage.widthParameter = this
    }

    EaElements.Parameter {
        title: qsTr('Scale')
        width: parameterFieldWidth()
        text: parameterValue('scale')
        onEditingFinished: {
            focus = false
            setParameterValue('scale', text)
        }
        Component.onCompleted: Globals.Refs.app.modelPage.scaleParameter = this
    }

    // Logic

    function parameterFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - 2 * EaStyle.Sizes.fontPixelSize) / 3
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
