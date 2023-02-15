// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as ExGlobals


Grid {
    columns: 2
    spacing: EaStyle.Sizes.fontPixelSize

    EaElements.Parameter {
        title: qsTr('Amplitude')
        width: parameterFieldWidth()
        text: ExGlobals.Proxies.mainProxy.model.amplitude.toFixed(4)
        onEditingFinished: ExGlobals.Proxies.mainProxy.model.amplitude = text
    }

    EaElements.Parameter {
        title: qsTr('Period')
        width: parameterFieldWidth()
        text: ExGlobals.Proxies.mainProxy.model.period.toFixed(4)
        onEditingFinished: ExGlobals.Proxies.mainProxy.model.period = text
    }

    EaElements.Parameter {
        title: qsTr('Vertical shift')
        width: parameterFieldWidth()
        text: ExGlobals.Proxies.mainProxy.model.verticalShift.toFixed(4)
        onEditingFinished: ExGlobals.Proxies.mainProxy.model.verticalShift = text
    }

    EaElements.Parameter {
        title: qsTr('Phase shift')
        width: parameterFieldWidth()
        text: ExGlobals.Proxies.mainProxy.model.phaseShift.toFixed(4)
        onEditingFinished: ExGlobals.Proxies.mainProxy.model.phaseShift = text
    }

    // Logic

    function parameterFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 2
    }

}
