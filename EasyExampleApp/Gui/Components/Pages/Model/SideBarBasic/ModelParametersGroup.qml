// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


Grid {
    columns: 2
    spacing: EaStyle.Sizes.fontPixelSize

    EaElements.Parameter {
        title: qsTr('Slope')
        width: parameterFieldWidth()
        text: Globals.Proxies.main.model.parameters.slope.value.toFixed(4)
        onEditingFinished: Globals.Proxies.main.model.editParameter('slope', 'value', text, true)
    }

    EaElements.Parameter {
        title: qsTr('y-Intercept')
        width: parameterFieldWidth()
        text: Globals.Proxies.main.model.parameters.yIntercept.value.toFixed(4)
        onEditingFinished: Globals.Proxies.main.model.editParameter('yIntercept', 'value', text, true)
    }

    // Logic

    function parameterFieldWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - EaStyle.Sizes.fontPixelSize) / 2
    }

}
