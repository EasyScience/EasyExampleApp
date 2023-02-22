// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    // Main
    readonly property var app: {
        'appbar': {
            'homeButton': null,
            'projectButton': null,
            'modelButton': null,
            'experimentButton': null,
            'analysisButton': null,
            'summaryButton': null
        },
        'homePage': {
            'startButton': null
        },
        'projectPage': {
            'continueButton': null
        },
        'modelPage': {
            'continueButton': null,
            'addNewModelManuallyButton': null
        },
        'experimentPage': {
            'continueButton': null,
            'importDataFromLocalDriveButton': null
        },
        'analysisPage': {
            'continueButton': null,
            'startFittingButton': null
        },
        'summaryPage': {
        },
    }

    // Misc
    property var summaryReportWebEngine
    property var remoteController

}
