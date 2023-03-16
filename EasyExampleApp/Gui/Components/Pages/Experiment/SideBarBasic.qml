// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Experimental data explorer")
        collapsible: false

        Loader { source: 'SideBarBasic/ExperimentalDataExplorerGroup.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Experiment ranges")
        visible: Globals.Proxies.main.experiment.created

        Loader { source: 'SideBarBasic/ExperimentRangesGroup.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Experiment background")
        visible: Globals.Proxies.main.experiment.created
        last: true

        Loader { source: 'SideBarBasic/ExperimentBackgroundGroup.qml' }
    }

}
