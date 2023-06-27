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
        title: qsTr('p1')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_reflex_asymmetry_p1')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_reflex_asymmetry_p1')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_reflex_asymmetry_p1', text)
    }

    EaElements.Parameter {
        title: qsTr('p2')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_reflex_asymmetry_p2')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_reflex_asymmetry_p2')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_reflex_asymmetry_p2', text)
    }

    EaElements.Parameter {
        title: qsTr('p3')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_reflex_asymmetry_p3')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_reflex_asymmetry_p3')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_reflex_asymmetry_p3', text)
    }

    EaElements.Parameter {
        title: qsTr('p4')
        fit: Globals.Proxies.experimentMainParameterFit('_pd_instr_reflex_asymmetry_p4')
        text: Globals.Proxies.experimentMainParameterValue('_pd_instr_reflex_asymmetry_p4')
        onEditingFinished: Globals.Proxies.setExperimentMainParameterValue('_pd_instr_reflex_asymmetry_p4', text)
    }

}
