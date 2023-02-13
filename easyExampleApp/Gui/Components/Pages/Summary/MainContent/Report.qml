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

    measuredXYData: ExGlobals.Proxies.miscProxy.project.summaryGenerated ?
                        ExGlobals.Proxies.mainProxy.experiment.measuredDataObj :
                        {}
    calculatedXYData: ExGlobals.Proxies.miscProxy.project.summaryGenerated ?
                          ExGlobals.Proxies.mainProxy.model.calculatedDataObj :
                          {}

    Component.onCompleted: ExGlobals.References.summaryReportWebEngine = this

}

