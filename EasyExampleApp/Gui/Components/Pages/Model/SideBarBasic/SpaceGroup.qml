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
        parameter: Globals.Proxies.modelMainParam('_space_group_name_H-M_alt')
        onEditingFinished: Globals.Proxies.setModelMainParamWithFullUpdate(parameter, 'value', text)
    }

    EaElements.Parameter {
        parameter: Globals.Proxies.modelMainParam('_space_group_IT_coordinate_system_code')
        onEditingFinished: Globals.Proxies.setModelMainParamWithFullUpdate(parameter, 'value', text)
    }

}
