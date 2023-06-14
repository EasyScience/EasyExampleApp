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
        title: qsTr('min')
        text: Globals.Proxies.experimentMainParameterValue('_pd_meas_2theta_range_min')
    }

    EaElements.Parameter {
        title: qsTr('max')
        text: Globals.Proxies.experimentMainParameterValue('_pd_meas_2theta_range_max')
    }

    EaElements.Parameter {
        title: qsTr('inc')
        text: Globals.Proxies.experimentMainParameterValue('_pd_meas_2theta_range_inc')
    }

}
