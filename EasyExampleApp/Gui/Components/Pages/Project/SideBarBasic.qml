// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Get started")
        collapsible: false

        Loader { source: 'SideBarBasic/GetStartedGroup.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Examples")
        collapsed: true
        last: true

        Loader { source: 'SideBarBasic/ExamplesGroup.qml' }
    }

}

