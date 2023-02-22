// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaElements.RemoteController {
    id: rc

    property var res: []

    Timer {
        running: true
        interval: 1000
        onTriggered: {
            runBasicGuiTest()
            processTestResults()
        }
    }

    // Tests

    function processTestResults() {
        let success = 0
        let okTests = 0
        let failedTests = 0

        print("========================================")
        print("GUI tests")
        print("----------------------------------------")
        for (let i in res) {
            if (res[i].startsWith('FAIL')) {
                success = -1
                failedTests += 1
                print(res[i])
            } else {
                okTests +=1
            }
        }

        if (success === 0) {
            print(`All ${res.length} GUI tests are OK`)
        } else {
            print("----------------------------------------")
            print(`${failedTests} of ${res.length} GUI tests are FAILED`)
        }
        print("========================================")

        print("Closing app after test mode.")
        Qt.exit(success)
    }

    function runBasicGuiTest() {
        // Set up testing process

        print('Run basic suit of GUI tests ')

        rc.posToCenter()
        rc.showPointer()

        // Home Page

        res.push( rc.compare(Globals.Refs.app.appbar.homeButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.projectButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.modelButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.experimentButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.analysisButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.summaryButton.enabled, false) )

        res.push( rc.compare(Globals.Refs.app.homePage.startButton.text, 'Start') )
        res.push( rc.compare(Globals.Refs.app.homePage.startButton.enabled, true) )

        return

        rc.mouseClick(Globals.Refs.app.homePage.startButton)

        // Project Page

        res.push( rc.compare(Globals.Refs.app.appbar.homeButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.projectButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.modelButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.experimentButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.analysisButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.summaryButton.enabled, false) )

        res.push( rc.compare(Globals.Refs.app.projectPage.continueButton.text, 'Continue without project') )
        res.push( rc.compare(Globals.Refs.app.projectPage.continueButton.enabled, true) )

        rc.mouseClick(Globals.Refs.app.projectPage.continueButton)

        // Model Page

        res.push( rc.compare(Globals.Refs.app.appbar.homeButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.projectButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.modelButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.experimentButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.analysisButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.summaryButton.enabled, false) )

        res.push( rc.compare(Globals.Refs.app.modelPage.addNewModelManuallyButton.text, 'Add new model manually') )
        res.push( rc.compare(Globals.Refs.app.modelPage.addNewModelManuallyButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.modelPage.continueButton.text, 'Continue') )
        res.push( rc.compare(Globals.Refs.app.modelPage.continueButton.enabled, false) )

        rc.mouseClick(Globals.Refs.app.modelPage.addNewModelManuallyButton)

        res.push( rc.compare(Globals.Refs.app.modelPage.addNewModelManuallyButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.modelPage.continueButton.enabled, true) )

        rc.mouseClick(Globals.Refs.app.modelPage.continueButton)

        // Experiment page

        res.push( rc.compare(Globals.Refs.app.appbar.homeButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.projectButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.modelButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.experimentButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.analysisButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.appbar.summaryButton.enabled, false) )

        res.push( rc.compare(Globals.Refs.app.experimentPage.importDataFromLocalDriveButton.text, 'Import data from local drive') )
        res.push( rc.compare(Globals.Refs.app.experimentPage.importDataFromLocalDriveButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.experimentPage.continueButton.text, 'Continue without experiment data') )
        res.push( rc.compare(Globals.Refs.app.experimentPage.continueButton.enabled, true) )

        rc.mouseClick(Globals.Refs.app.experimentPage.importDataFromLocalDriveButton)

        res.push( rc.compare(Globals.Refs.app.experimentPage.importDataFromLocalDriveButton.enabled, false) )
        res.push( rc.compare(Globals.Refs.app.experimentPage.continueButton.text, 'Continue') )

        rc.mouseClick(Globals.Refs.app.experimentPage.continueButton)

        // Analysis page

        res.push( rc.compare(Globals.Refs.app.appbar.homeButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.projectButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.modelButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.experimentButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.analysisButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.appbar.summaryButton.enabled, false) )

        res.push( rc.compare(Globals.Refs.app.analysisPage.startFittingButton.text, 'Start fitting') )
        res.push( rc.compare(Globals.Refs.app.analysisPage.startFittingButton.enabled, true) )
        res.push( rc.compare(Globals.Refs.app.analysisPage.continueButton.text, 'Continue') )
        res.push( rc.compare(Globals.Refs.app.analysisPage.continueButton.enabled, true) )

        rc.mouseClick(Globals.Refs.app.analysisPage.startFittingButton)
        rc.mouseClick(Globals.Refs.app.analysisPage.continueButton)

        // Summary page

        //...

        // Complete testing process

        rc.hidePointer()
    }

}
