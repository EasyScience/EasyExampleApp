pragma Singleton

import QtQuick 2.13

QtObject {
    property var proxy: _pyQmlProxyObj

    // Debug mode
    property bool isDebugMode: false

    // Initial application components accessibility
    property bool homePageEnabled: isDebugMode ? true : true
    property bool projectPageEnabled: isDebugMode ? true : false
    property bool samplePageEnabled: isDebugMode ? true : false
    property bool experimentPageEnabled: isDebugMode ? true : false
    property bool analysisPageEnabled: isDebugMode ? true : false
    property bool summaryPageEnabled: isDebugMode ? true : false

    // Workflow states
    property bool projectCreated: false
    property bool sampleLoaded: false
    property bool experimentLoaded: false

    // References to GUI elements
    property var homeTabButton
    property var projectTabButton
    property var sampleTabButton
    property var experimentTabButton
    property var analysisTabButton
    property var summaryTabButton

    property var preferencesButton

    property var addNewSampleButton
    property var generateMeasuredDataButton
    property var startFittingButton

    property var amplitudeTextInput
    property var periodTextInput
    property var xShiftTextInput
    property var yShiftTextInput

    property var themeSelector
}
