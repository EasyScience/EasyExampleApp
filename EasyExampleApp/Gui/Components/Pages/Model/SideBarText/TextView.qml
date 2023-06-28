// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.TextArea {
    text: Globals.Proxies.main.model.dataBlocksCif

    //textFormat: TextEdit.RichText
    font.family: EaStyle.Fonts.monoFontFamily
    backgroundOpacity: 0
    readOnly: true
}
