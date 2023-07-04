// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import Gui.Globals as Globals


EaElements.StatusBar {
    visible: EaGlobals.Vars.appBarCurrentIndex !== 0

    EaElements.StatusBarItem {
        key: qsTr('Project')
        value: Globals.Proxies.main.status.project
    }

    EaElements.StatusBarItem {
        key: qsTr('Models')
        value: Globals.Proxies.main.status.phaseCount
    }

    EaElements.StatusBarItem {
        key: qsTr('Data points')
        value: Globals.Proxies.main.status.dataPoints
    }

    EaElements.StatusBarItem {
        key: qsTr('Calculate')
        value: Globals.Proxies.main.status.calculator
    }

    EaElements.StatusBarItem {
        key: qsTr('Minimize')
        value: Globals.Proxies.main.status.minimizer
    }

    EaElements.StatusBarItem {
        key: qsTr('Parameters')
        value: Globals.Proxies.main.status.variables
    }

    EaElements.StatusBarItem {
        key: qsTr('Fit iteration')
        value: Globals.Proxies.main.status.fitIteration
    }

    EaElements.StatusBarItem {
        key: qsTr('Goodness-of-fit')
        value: Globals.Proxies.main.status.goodnessOfFit
    }

    EaElements.StatusBarItem {
        key: qsTr('Fit status')
        value: Globals.Proxies.main.status.fitStatus
    }

}
