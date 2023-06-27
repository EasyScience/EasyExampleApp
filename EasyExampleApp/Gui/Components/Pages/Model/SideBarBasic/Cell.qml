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
        title: qsTr('length a')
        enabled: Globals.Proxies.modelMainParameterEnabled('_cell_length_a')
        fit: Globals.Proxies.modelMainParameterFit('_cell_length_a')
        text: Globals.Proxies.modelMainParameterValue('_cell_length_a')
        onEditingFinished: Globals.Proxies.setModelMainParameterValue('_cell_length_a', text)
    }

    EaElements.Parameter {
        title: qsTr('length b')
        enabled: Globals.Proxies.modelMainParameterEnabled('_cell_length_b')
        fit: Globals.Proxies.modelMainParameterFit('_cell_length_b')
        text: Globals.Proxies.modelMainParameterValue('_cell_length_b')
        onEditingFinished: Globals.Proxies.setModelMainParameterValue('_cell_length_b', text)
    }

    EaElements.Parameter {
        title: qsTr('length c')
        enabled: Globals.Proxies.modelMainParameterEnabled('_cell_length_c')
        fit: Globals.Proxies.modelMainParameterFit('_cell_length_b')
        text: Globals.Proxies.modelMainParameterValue('_cell_length_c')
        onEditingFinished: Globals.Proxies.setModelMainParameterValue('_cell_length_c', text)
    }

    EaElements.Parameter {
        title: qsTr('angle α')
        enabled: Globals.Proxies.modelMainParameterEnabled('_cell_angle_alpha')
        fit: Globals.Proxies.modelMainParameterFit('_cell_angle_alpha')
        text: Globals.Proxies.modelMainParameterValue('_cell_angle_alpha')
        onEditingFinished: Globals.Proxies.setModelMainParameterValue('_cell_angle_alpha', text)
    }

    EaElements.Parameter {
        title: qsTr('angle β')
        enabled: Globals.Proxies.modelMainParameterEnabled('_cell_angle_beta')
        fit: Globals.Proxies.modelMainParameterFit('_cell_angle_beta')
        text: Globals.Proxies.modelMainParameterValue('_cell_angle_beta')
        onEditingFinished: Globals.Proxies.setModelMainParameterValue('_cell_angle_beta', text)
    }

    EaElements.Parameter {
        title: qsTr('angle γ')
        enabled: Globals.Proxies.modelMainParameterEnabled('_cell_angle_gamma')
        fit: Globals.Proxies.modelMainParameterFit('_cell_angle_gamma')
        text: Globals.Proxies.modelMainParameterValue('_cell_angle_gamma')
        onEditingFinished: Globals.Proxies.setModelMainParameterValue('_cell_angle_gamma', text)
    }

}
