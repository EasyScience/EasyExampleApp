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
        title: qsTr('u')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_resolution_u')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_resolution_u')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_resolution_u', text)
    }

    EaElements.Parameter {
        title: qsTr('v')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_resolution_v')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_resolution_v')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_resolution_v', text)
    }

    EaElements.Parameter {
        title: qsTr('w')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_resolution_w')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_resolution_w')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_resolution_w', text)
    }

    EaElements.Parameter {
        title: qsTr('x')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_resolution_x')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_resolution_x')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_resolution_x', text)
    }

    EaElements.Parameter {
        title: qsTr('y')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_resolution_y')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_resolution_y')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_resolution_y', text)
    }

}
