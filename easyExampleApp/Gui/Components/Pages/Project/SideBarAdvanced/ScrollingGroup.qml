// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick 2.15

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}
    EaElements.Label {}

    Component.onCompleted: {
        for (let i = 0; i < visibleChildren.length; ++i) {
            visibleChildren[i].text = `Label ${i+1} of ${visibleChildren.length}`
        }
    }

}

