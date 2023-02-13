// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Experimental data")
        visible: ExGlobals.Proxies.mainProxy.experiment.experimentsLoaded
        last: true

        Loader { source: 'SideBarAdvanced/GenerateDataGroup.qml' }
    }

}
