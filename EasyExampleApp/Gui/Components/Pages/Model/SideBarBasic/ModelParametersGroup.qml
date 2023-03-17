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
        title: qsTr('Slope')
        width: parameterFieldWidth()
        text: parameterValue('slope')
        onEditingFinished: setParameterValue('slope', text)
        Component.onCompleted: Globals.Refs.app.modelPage.slopeParameter = this
    }

    EaElements.Parameter {
        title: qsTr('y-Intercept')
        width: parameterFieldWidth()
        text: parameterValue('yIntercept')
        onEditingFinished: setParameterValue('yIntercept', text)
        Component.onCompleted: Globals.Refs.app.modelPage.yInterceptParameter = this
    }

    // Logic

    function parameterFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 2
    }

    function parameterValue(name) {
        if (!Globals.Proxies.main.model.created) {
            return ''
        }
        const currentModelIndex = Globals.Proxies.main.model.currentIndex
        const item = 'value'
        const value = Globals.Proxies.main.model.data[currentModelIndex].params[name][item]
        const formattedValue = value.toFixed(4)
        return formattedValue
    }

    function setParameterValue(name, value) {
        const currentModelIndex = Globals.Proxies.main.model.currentIndex
        const item = 'value'
        const needSetFittables = true
        Globals.Proxies.main.model.editParameter(currentModelIndex,
                                                 name,
                                                 item,
                                                 value,
                                                 needSetFittables)
    }

}
