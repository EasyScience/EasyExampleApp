// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick 2.15

QtObject {
    // Debug mode
    property bool isDebugMode: typeof _pyQmlProxyObj === "undefined"

    // Initial application pages accessibility
    property bool homePageEnabled: isDebugMode ? true : true
    property bool projectPageEnabled: isDebugMode ? true : false
    property bool step1PageEnabled: isDebugMode ? true : false
    property bool step2PageEnabled: isDebugMode ? true : false
    property bool step3PageEnabled: isDebugMode ? true : false
    property bool step4PageEnabled: isDebugMode ? true : false
    property bool step5PageEnabled: isDebugMode ? true : false
    property bool summaryPageEnabled: isDebugMode ? true : false

    // //////////////////////////
    // References to GUI elements
    // //////////////////////////

    // Application bar
    property var appBarCentralTabs

    // Application bar tab buttons
    property var homeTabButton
    property var projectTabButton
    property var step1TabButton
    property var step2TabButton
    property var step3TabButton
    property var step4TabButton
    property var step5TabButton
    property var summaryTabButton

    // Charts
    property var chartViewSimple1dPlotly
    property var chartViewHeatmap2dPlotly
}
