pragma Singleton

import QtQuick 2.13

QtObject {
    readonly property var proxy: _projectConfig

    readonly property string appName: _projectConfig.tool.poetry.name
    readonly property string appPrefixName: "easy"
    readonly property string appSuffixName: appName.replace(appPrefixName, "")
    readonly property string appVersion: _projectConfig.tool.poetry.version
    readonly property string appDate: new Date().toISOString().slice(0,10) // TODO: Get from phython logic formatted as "9 Apr 2020"
    readonly property string appLogo: Qt.resolvedUrl("../Resources/Logo/App.svg")
}
