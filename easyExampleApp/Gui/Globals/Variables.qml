// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    // Debug mode
    property bool isDebugMode: false

    // Initial application pages accessibility
    property bool homePageEnabled: isDebugMode ? true : true
    property bool projectPageEnabled: isDebugMode ? true : false
    property bool modelPageEnabled: isDebugMode ? true : false
    property bool experimentPageEnabled: isDebugMode ? true : false
    property bool analysisPageEnabled: isDebugMode ? true : false
    property bool summaryPageEnabled: isDebugMode ? true : false

    // Misc
    property real applicationWindowOpacity: 0.0
    property bool applicationWindowCompleted: false
    property bool homePageCompleted: false

}
