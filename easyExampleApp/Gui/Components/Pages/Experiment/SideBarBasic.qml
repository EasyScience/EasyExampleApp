// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import easyApp.Gui.Elements as EaElements
import easyApp.Gui.Components as EaComponents


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Experimental data")
        collapsible: false
        last: true

        Loader { source: 'SideBarBasic/ExperimentDataGroup.qml' }
    }

}
