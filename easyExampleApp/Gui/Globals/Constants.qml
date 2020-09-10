pragma Singleton

import QtQuick 2.13

QtObject {
    readonly property string appName: _pyQmlProxyObj.appName
    readonly property string appPrefixName: "easy"
    readonly property string appSuffixName: "Example" // TODO: Get from phython logic
    readonly property string appVersion: "0.5.0" // TODO: Get from phython logic
    readonly property string appDate: "15 May 2020" // TODO: Get from phython logic
    readonly property string appLogo: Qt.resolvedUrl("../Resources/Logo/App.svg")
}
