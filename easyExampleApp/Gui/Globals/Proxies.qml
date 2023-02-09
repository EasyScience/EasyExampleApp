// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick

import EasyApp.Gui.Style as EaStyle


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    readonly property var mainProxy: typeof pyProxy !== 'undefined' ?
                                         pyProxy:
                                         qmlProxy

    readonly property var qmlProxy: QtObject {

        readonly property var model: QtObject {
            readonly property var modelsAsJson: [
                {
                    label: 'Sine wave',
                    color: EaStyle.Colors.chartForegrounds[0]
                }
              ]
            property bool modelsAdded: false

            property real amplitude: 1
            property real period: Math.PI
            property real verticalShift: 0
            property real phaseShift: 0

            property var calculatedDataObj: ({})

            onAmplitudeChanged: setCalculatedDataObj()
            onPeriodChanged: setCalculatedDataObj()
            onVerticalShiftChanged: setCalculatedDataObj()
            onPhaseShiftChanged: setCalculatedDataObj()

            function setCalculatedDataObj() {
                let xArray = []
                let yArray = []
                for (let x = 0; x < 2 * Math.PI; x += 0.1) {
                    const y = qmlProxy.fitting.sineFunction(x, amplitude, period, phaseShift, verticalShift)
                    xArray.push(x)
                    yArray.push(y)
                }
                calculatedDataObj = {
                    'x': xArray,
                    'y': yArray
                }
            }

        }

        readonly property var experiment: QtObject {
            readonly property var experimentDataAsJson: [
                    {
                        label: 'D1A@ILL',
                        color: EaStyle.Colors.chartForegroundsExtra[2]
                    }
                  ]
            property bool experimentsLoaded: false

            property real amplitude: Math.abs(Math.random())
            property real period: Math.abs(Math.random()) * Math.PI * (4 - 3) + 3
            property real verticalShift: Math.random()
            property real phaseShift: Math.random() * Math.PI

            property int measuredDataLength: 7
            property var measuredDataObj: ({})

            function setMeasuredDataObj() {
                let xArray = []
                let yArray = []
                for (let x = 0; x < 2 * Math.PI; x += 0.1) {
                    const randomShift = Math.random() * 0.1 - 0.05
                    const y = qmlProxy.fitting.sineFunction(x, amplitude, period, phaseShift, verticalShift + randomShift)
                    xArray.push(x)
                    yArray.push(y)
                }
                measuredDataObj = {
                    'x': xArray,
                    'y': yArray
                }
            }            
            function emptyMeasuredDataObj() {
                measuredDataObj = {
                    'x': [],
                    'y': []
                }
            }
        }

        readonly property var fitting: QtObject {
            property bool isFitFinished: false

            function sineFunction(x, amplitude, period, phaseShift, verticalShift) {
                const res = amplitude * Math.sin( 2 * Math.PI / period * (x + phaseShift) ) + verticalShift
                return res
            }

            function fit() {
                qmlProxy.model.amplitude = qmlProxy.experiment.amplitude
                qmlProxy.model.period = qmlProxy.experiment.period
                qmlProxy.model.phaseShift = qmlProxy.experiment.phaseShift
                qmlProxy.model.verticalShift = qmlProxy.experiment.verticalShift

                qmlProxy.model.setCalculatedDataObj()

                isFitFinished = true
            }
        }

        readonly property var parameters: QtObject {
            property var parametersAsJson: [
                {
                    id: 4538458360,
                    number: 1,
                    label: 'Amplitude',
                    value: qmlProxy.model.amplitude,
                    unit: '',
                    error: 0.1131,
                    fit: true
                },
                {
                    id: 4092346238,
                    number: 2,
                    label: 'Period',
                    value: qmlProxy.model.period,
                    unit: 'rad',
                    error: 0.2573,
                    fit: true
                },
                {
                    id: 9834542745,
                    number: 2,
                    label: 'Vertical shift',
                    value: qmlProxy.model.verticalShift,
                    unit: '',
                    error: 0.0212,
                    fit: true
                },
                {
                    id: 8655377643,
                    number: 2,
                    label: 'Phase shift',
                    value: qmlProxy.model.phaseShift,
                    unit: 'rad',
                    error: 0.2238,
                    fit: true
                }
            ]
            function editParameterValue(pid, value) {
                if (typeof pid === 'undefined') {
                    return
                }
                if (pid === 4538458360) {
                    qmlProxy.model.amplitude = parseFloat(value)
                } else if (pid === 4092346238) {
                    qmlProxy.model.period = value
                } else if (pid === 9834542745) {
                    qmlProxy.model.verticalShift = value
                } else if (pid === 8655377643) {
                    qmlProxy.model.phaseShift = value
                }
                qmlProxy.model.setCalculatedDataObj()
            }
        }

        readonly property var statusBar: QtObject {
            property string modelAsXml:
                `<root>
                  <item>
                    <label>Calculations</label>
                    <value>CrysPy</value>
                  </item>
                  <item>
                    <label>Minimization</label>
                    <value>lmfit</value>
                  </item>
                </root>`
            property var modelAsJson: [
                {
                    label: 'Calculations',
                    value: 'CrysPy'
                },
                {
                    label: 'Minimization',
                    value: 'lmfit'
                }
              ]
        }

    }

    readonly property var miscProxy: QtObject {

        readonly property var project: QtObject {
            property bool projectCreated: false
            property bool summaryGenerated: false
            property string currentProjectPath: '_path_'
            property var projectInfoAsJson: QtObject {
                property string name: '_name_'
                property string short_description: '_short_description_'
                property string modified: '_modified_'
            }
            property var projectExamplesAsJson: [
                {
                    name: 'PbSO4',
                    description: 'neutrons, powder, constant wavelength, D1A@ILL',
                    path: '../Resources/Examples/PbSO4/project.json'
                },
                {
                    name: 'Co2SiO4',
                    description: 'neutrons, powder, constant wavelength, D20@ILL',
                    path: '../Resources/Examples/Co2SiO4/project.json'
                },
                {
                    name: 'Dy3Al5O12',
                    description: 'neutrons, powder, constant wavelength, G41@LLB',
                    path: '../Resources/Examples/Dy3Al5O12/project.json'
                }
              ]
            function createProject() { projectCreated = true }
            function loadExampleProject(fileUrl) {}
        }

        readonly property var plotting1d: QtObject {
            property var libs: ['Plotly']
            property string currentLib: 'Plotly'
        }
    }

}
