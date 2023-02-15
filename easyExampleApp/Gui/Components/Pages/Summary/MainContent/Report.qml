// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Components as EaComponents

import Gui.Globals as ExGlobals


EaComponents.BasicReport {

    xAxisTitle: "x"
    yAxisTitle: "y"

    measuredXYData: ExGlobals.Proxies.mainProxy.summary.isCreated ?
                        ExGlobals.Proxies.mainProxy.experiment.measuredData :
                        {}
    calculatedXYData: ExGlobals.Proxies.mainProxy.summary.isCreated ?
                          ExGlobals.Proxies.mainProxy.model.calculatedData :
                          {}

    Component.onCompleted: ExGlobals.References.summaryReportWebEngine = this

}

