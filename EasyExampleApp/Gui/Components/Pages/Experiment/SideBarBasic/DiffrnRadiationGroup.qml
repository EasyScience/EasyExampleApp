// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.GroupRow {

    EaElements.Parameter {
        //enabled: false
        title: qsTr('probe')
        text: Globals.Proxies.experimentParameterValue('_diffrn_radiation_probe')
        //horizontalAlignment: TextField.AlignLeft
    }

    EaElements.Parameter {
        title: qsTr('wavelength')
        text: Globals.Proxies.experimentParameterValue('_diffrn_radiation_wavelength')
        onEditingFinished: Globals.Proxies.setExperimentParameterValue('_diffrn_radiation_wavelength', text)
    }

}
