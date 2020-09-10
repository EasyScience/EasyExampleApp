import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

Item {
    id: root

    Column {
        anchors.centerIn: parent
        spacing: EaStyle.Sizes.fontPixelSize * 2

        // Application logo, name and version
        Column {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 0

            // Application logo
            Image {
                source: ExGlobals.Constants.appLogo
                anchors.horizontalCenter: parent.horizontalCenter
                width: EaStyle.Sizes.fontPixelSize * 6
                fillMode: Image.PreserveAspectFit
                antialiasing: true
            }

            // Application name
            Row {
                property var fontFamily: EaStyle.Fonts.secondCondensedFontFamily
                property var fontPixelSize: EaStyle.Sizes.fontPixelSize * 4

                anchors.horizontalCenter: parent.horizontalCenter

                EaElements.Label {
                    font.family: parent.fontFamily
                    font.pixelSize: parent.fontPixelSize
                    font.weight: Font.ExtraLight
                    text: ExGlobals.Constants.appPrefixName
                }
                EaElements.Label {
                    font.family: parent.fontFamily
                    font.pixelSize: parent.fontPixelSize
                    text: ExGlobals.Constants.appSuffixName
                }
            }

            // Application version
            EaElements.Label {
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: EaStyle.Fonts.secondExpandedFontFamily
                text: "Version %1 (%2)".arg(ExGlobals.Constants.appVersion).arg(ExGlobals.Constants.appDate)
            }
        }

        // Start button
        Button {
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTr("Start")
            onClicked: {
                ExGlobals.Variables.projectPageEnabled = true
                ExGlobals.Variables.projectTabButton.toggle()
            }
        }

        // Links
        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: EaStyle.Sizes.fontPixelSize * 3

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    text: qsTr("About %1".arg(ExGlobals.Constants.appName))
                }
                EaElements.Button {
                    text: qsTr("Online documentation")
                }
                EaElements.Button {
                    text: qsTr("Get in touch online")
                }
            }

            Column {
                spacing: EaStyle.Sizes.fontPixelSize

                EaElements.Button {
                    text: qsTr("Tutorial 1: Data fitting")
                    onClicked: runTutorial1()
                }
                EaElements.Button {
                    text: qsTr("Tutorial 2: App settings")
                    onClicked: runTutorial2()
                }
            }
        }

    }

    EaElements.RemoteController {
        id: rc
    }

    Timer {
        id: quit
        interval: 1000
        onTriggered: {
            print("* closing app")
            Qt.quit()
        }
    }

    Component.onCompleted: {
        if (EaGlobals.Variables.isTestMode) {
            print('TEST MODE')
            runTutorial0()
            quit.start()
        }
    }

    // Tutorials

    function startSavingScreenshots(message) {
        if (EaGlobals.Variables.isTestMode) {
            print(message)
            EaGlobals.Variables.saveScreenshotsRunning = true
        }
    }

    function endSavingScreenshots() {
        if (EaGlobals.Variables.isTestMode) {
            EaGlobals.Variables.saveScreenshotsRunning = false
        }
    }

    function runTutorial0() {
        startSavingScreenshots("* run Tutorial 0")
        rc.wait(1000)
        rc.show()
        rc.wait(1000)
        rc.hide()
        rc.wait(1000)
        endSavingScreenshots()
    }

    function runTutorial1() {
        startSavingScreenshots("* run Tutorial 1")

        rc.wait(1000)
        rc.show()

        rc.mouseClick(ExGlobals.Variables.sampleTabButton)
        rc.mouseClick(ExGlobals.Variables.addNewSampleButton)
        rc.mouseClick(ExGlobals.Variables.amplitudeTextInput)
        rc.clearText(4)
        rc.typeText("2.10")
        rc.mouseClick(ExGlobals.Variables.periodTextInput)
        rc.clearText(2)
        rc.typeText("30")
        rc.keyClick(Qt.Key_Enter)

        rc.wait(2000)
        rc.mouseClick(ExGlobals.Variables.experimentTabButton)
        rc.mouseClick(ExGlobals.Variables.generateMeasuredDataButton)

        rc.wait(1000)
        rc.mouseClick(ExGlobals.Variables.analysisTabButton)
        rc.mouseClick(ExGlobals.Variables.xShiftTextInput)
        rc.clearText(4)
        rc.typeText("-0.30")
        rc.mouseClick(ExGlobals.Variables.yShiftTextInput)
        rc.clearText(2)
        rc.typeText("40")
        rc.keyClick(Qt.Key_Enter)
        rc.wait(1000)
        rc.mouseClick(ExGlobals.Variables.startFittingButton)

        rc.wait(1000)
        rc.hide()

        rc.wait(1000)
        endSavingScreenshots()
    }

    function runTutorial2() {
        startSavingScreenshots("* run Tutorial 2")

        rc.wait(1000)
        rc.show()

        rc.mouseClick(ExGlobals.Variables.preferencesButton)
        rc.mouseClick(ExGlobals.Variables.themeSelector)

        const x_pos = undefined
        let y_pos = EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        rc.wait(1000)
        rc.mouseClick(ExGlobals.Variables.themeSelector)
        y_pos = EaStyle.Colors.isDarkTheme ? EaStyle.Sizes.comboBoxHeight * 1.5 : undefined
        rc.mouseClick(ExGlobals.Variables.themeSelector, x_pos, y_pos)

        rc.wait(1000)
        rc.keyClick(Qt.Key_Escape)

        rc.wait(1000)
        rc.hide()

        rc.wait(1000)
        endSavingScreenshots()
    }

    function runTutorial3() {
        startSavingScreenshots("* run Tutorial 3")
        rc.wait(1000)
        rc.show()
        rc.mouseClick(ExGlobals.Variables.sampleTabButton)
        rc.wait(1000)
        rc.hide()
        rc.wait(1000)
        endSavingScreenshots()
    }

}
