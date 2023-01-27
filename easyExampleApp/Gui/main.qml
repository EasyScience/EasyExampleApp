// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick 2.15
import QtQuick.Controls 2.15

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents


ExComponents.ApplicationWindow {
    id: window

    appName: ExGlobals.Constants.appName
    appVersion: ExGlobals.Constants.appVersion
    appDate: ExGlobals.Constants.appDate
}
