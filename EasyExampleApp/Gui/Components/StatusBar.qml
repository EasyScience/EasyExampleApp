// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import Gui.Globals as Globals


EaElements.StatusBar {

    visible: EaGlobals.Vars.appBarCurrentIndex !== 0
    //fittingInProgress: Globals.Proxies.main.fitting.isFittingNow

    //model: EaComponents.JsonListModel {
    //    json: JSON.stringify(Globals.Proxies.main.status.asJson)
    //    query: "$[*]"
    //}

}


