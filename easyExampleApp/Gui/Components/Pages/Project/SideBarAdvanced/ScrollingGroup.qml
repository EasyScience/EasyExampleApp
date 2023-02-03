// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements


Column {
    property int numLabels: 50

    spacing: EaStyle.Sizes.fontPixelSize

    Repeater {
        model: numLabels
        EaElements.Label {
            text: `Label ${index+1} of ${numLabels}`
        }
    }

}

