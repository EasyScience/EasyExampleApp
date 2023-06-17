// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style 1.0 as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.Dialog {
    id: dialog

    visible: !Globals.Proxies.main.fitting.isFittingNow && Globals.Proxies.main.status.fitStatus
    title: qsTr("Status")
    standardButtons: Dialog.Ok

    EaElements.Label {
        text: {
            if (Globals.Proxies.main.status.fitStatus === 'Success') {
                return 'Fitting is successfully completed.'
            } else if (Globals.Proxies.main.status.fitStatus === 'Failure') {
                return 'Fitting is failed.'
            } else if (Globals.Proxies.main.status.fitStatus === 'Cancelled') {
                return 'Fitting is cancelled.'
            } else {
                return ''
            }
        }
    }
}
