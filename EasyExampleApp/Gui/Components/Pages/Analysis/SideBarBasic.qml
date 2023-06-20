// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Parameters")
        collapsible: false

        Loader { source: 'SideBarBasic/Fittables.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Fitting")
        collapsible: false
        last: true

        Loader { source: 'SideBarBasic/Fitting.qml' }
    }

}
