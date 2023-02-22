// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.BasicReport {

    xAxisTitle: "x"
    yAxisTitle: "y"

    measuredXYData: Globals.Proxies.mainProxy.summary.isCreated ?
                        Globals.Proxies.mainProxy.experiment.measuredData :
                        {}
    calculatedXYData: Globals.Proxies.mainProxy.summary.isCreated ?
                          Globals.Proxies.mainProxy.model.calculatedData :
                          {}

    Component.onCompleted: Globals.Refs.summaryReportWebEngine = this

}

