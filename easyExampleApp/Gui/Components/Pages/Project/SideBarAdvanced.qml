// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Scrolling")
        collapsed: false
        last: true

        Loader { source: 'SideBarAdvanced/ScrollingGroup.qml' }
    }

}

