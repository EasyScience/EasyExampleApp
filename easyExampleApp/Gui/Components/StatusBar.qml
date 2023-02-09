// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
//import QtQuick.XmlListModel 2.15

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals


EaElements.StatusBar {
    visible: EaGlobals.Variables.appBarCurrentIndex !== 0

    /*
    model: XmlListModel {
        xml: ExGlobals.Proxies.miscProxy.statusBar.modelAsXml
        query: "/root/item"

        XmlRole { name: "label"; query: "label/string()" }
        XmlRole { name: "value"; query: "value/string()" }
    }
    */

    model: EaComponents.JsonListModel {
        json: JSON.stringify(ExGlobals.Proxies.mainProxy.statusBar.modelAsJson)
        query: "$[*]"
    }

}


