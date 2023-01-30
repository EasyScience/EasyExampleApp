// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick 2.15

import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Get started")
        collapsible: false

        Loader { source: 'SideBarBasic/GetStartedGroup.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Examples")
        last: true

        Loader { source: 'SideBarBasic/ExamplesGroup.qml' }
    }

}

