// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Models explorer")
        collapsible: false
        last: !Globals.Proxies.main.model.defined

        Loader { source: 'SideBarBasic/ModelsExplorer.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Space group")
        visible: Globals.Proxies.main.model.defined

        Loader { source: 'SideBarBasic/SpaceGroup.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Cell")
        visible: Globals.Proxies.main.model.defined

        Loader { source: 'SideBarBasic/Cell.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Atom site")
        visible: Globals.Proxies.main.model.defined
        last: true

        Loader { source: 'SideBarBasic/AtomSite.qml' }
    }

}
