// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Models explorer")
        collapsible: false
        last: true//!Globals.Proxies.main.model.defined

        Loader { source: 'SideBarText/ModelsExplorer.qml' }
    }

    EaElements.GroupBox {
        title: ''//qsTr("Models explorer")
        collapsible: false
        last: true//!Globals.Proxies.main.model.defined

        //ScrollView {
            //anchors.fill: parent

            EaElements.TextArea {
                text: Globals.Proxies.main.model.dataBlocksCif

                //textFormat: TextEdit.RichText
                font.family: EaStyle.Fonts.monoFontFamily
                backgroundOpacity: 0
                readOnly: true
            }
        //}

    }



}
