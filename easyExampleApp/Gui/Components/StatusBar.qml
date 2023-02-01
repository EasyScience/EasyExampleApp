// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.XmlListModel 2.15

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals


EaElements.StatusBar {
    visible: EaGlobals.Variables.appBarCurrentIndex !== 0

    /*
    model: XmlListModel {
        xml: ExGlobals.Proxies.mainProxy.statusBar.modelAsXml
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


