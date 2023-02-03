// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import Gui.Globals as ExGlobals
import Gui.Components as ExComponents


ExComponents.ApplicationWindow {
    id: window

    appName: ExGlobals.Configs.appConfig.name
    appVersion: ExGlobals.Configs.appConfig.version
    appDate: ExGlobals.Configs.appConfig.date
}
