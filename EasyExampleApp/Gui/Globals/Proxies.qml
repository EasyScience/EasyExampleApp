// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick

import EasyApp.Gui.Style as EaStyle

import Gui.Globals as Globals


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    readonly property var mainProxy: typeof pyProxy !== 'undefined' ?
                                         pyProxy:
                                         qmlProxy

    readonly property var qmlProxy: QtObject {

        readonly property var project: QtObject {
            property var examplesAsJson: [
                {
                    name: 'Example1',
                    description: 'Sine wave, PicoScope 2204A',
                    path: '../Resources/Examples/Example1/project.json'
                },
                {
                    name: 'Example2',
                    description: 'Sine wave, Tektronix 2430A',
                    path: '../Resources/Examples/Example2/project.json'
                },
                {
                    name: 'Example3',
                    description: 'Sine wave, Siglent SDS1202X-E',
                    path: '../Resources/Examples/Example3/project.json'
                }
            ]

            property bool isCreated: false

            property string currentProjectName: 'Default project'
            property string currentProjectDescription: 'Default project description'
            property string currentProjectLocation: ''
            property string currentProjectCreatedDate: ''
            property string currentProjectImage: Qt.resolvedUrl('../Resources/Project/Sine.svg')

            function create() {
                currentProjectCreatedDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
                isCreated = true
            }
        }

        readonly property var model: QtObject {
            readonly property var asJson: [
                {
                    label: 'Sine wave'
                }
            ]

            property bool isCreated: false

            property real amplitude: 1
            property real period: 3.141592653589793
            property real verticalShift: 0
            property real phaseShift: 0

            property var calculatedData: ({})

            onAmplitudeChanged: generateCalculatedData()
            onPeriodChanged: generateCalculatedData()
            onVerticalShiftChanged: generateCalculatedData()
            onPhaseShiftChanged: generateCalculatedData()

            function generateCalculatedData() {
                let xArray = []
                let yArray = []
                for (let i = 0; i < qmlProxy.experiment.measuredDataLength; ++i) {
                    const xStep = 10 * Math.PI / (qmlProxy.experiment.measuredDataLength - 1)
                    const x = i * xStep
                    const y = qmlProxy.calculator.sine(x,
                                                       amplitude,
                                                       period,
                                                       phaseShift,
                                                       verticalShift
                                                       )
                    xArray.push(x)
                    yArray.push(y)
                }
                calculatedData = { 'x': xArray, 'y': yArray }
                isCreated = true
            }
            function emptyCalculatedData() {
                calculatedData = { 'x': [], 'y': [] }
                isCreated = false
            }
        }

        readonly property var experiment: QtObject {
            readonly property var asJson: [
                    {
                        label: 'PicoScope'
                    }
                  ]
            property bool isCreated: false

            property real amplitude: Math.abs(Math.random())  // [0, 1)
            property real period: Math.abs(Math.random()) * Math.PI * (4 - 3) + 3  // (3, 4) * pi
            property real verticalShift: Math.random()  // (-1, 1)
            property real phaseShift: Math.random() * Math.PI  // (-1, 1) * pi

            property int measuredDataLength: 100
            property var measuredData: ({})

            onMeasuredDataLengthChanged: {
                if (qmlProxy.model.isCreated) {
                    qmlProxy.model.generateCalculatedData()
                }
                if (qmlProxy.experiment.isCreated) {
                    qmlProxy.experiment.loadMeasuredData()
                }
                if (qmlProxy.fitting.isFitFinished) {
                    qmlProxy.fitting.fit()
                }
            }

            function loadMeasuredData() {
                let xArray = []
                let yArray = []
                for (let i = 0; i < measuredDataLength; ++i) {
                    const xStep = 10 * Math.PI / (measuredDataLength - 1)
                    const x = i * xStep
                    const randomVerticalShift = Math.random() * 0.1 - 0.05  // [-0.05, 0.05)
                    const y = qmlProxy.calculator.sine(x,
                                                       amplitude,
                                                       period,
                                                       phaseShift,
                                                       verticalShift + randomVerticalShift
                                                       )
                    xArray.push(x)
                    yArray.push(y)
                }
                measuredData = { 'x': xArray, 'y': yArray }
                isCreated = true
            }            
            function emptyMeasuredData() {
                measuredData = { 'x': [], 'y': [] }
                isCreated = false
            }
        }

        readonly property var calculator: QtObject {
            function sine(x, amplitude, period, phaseShift, verticalShift) {
                const res = amplitude * Math.sin( 2 * Math.PI / period * (x + phaseShift) ) + verticalShift
                return res
            }
        }


        readonly property var fitting: QtObject {
            property bool isFitFinished: false

            function fit() {
                qmlProxy.model.amplitude = qmlProxy.experiment.amplitude
                qmlProxy.model.period = qmlProxy.experiment.period
                qmlProxy.model.phaseShift = qmlProxy.experiment.phaseShift
                qmlProxy.model.verticalShift = qmlProxy.experiment.verticalShift

                isFitFinished = true
            }
        }

        readonly property var parameters: QtObject {
            property var asJson: [
                {
                    id: '4538458360',
                    number: 1,
                    label: 'Amplitude',
                    value: qmlProxy.model.amplitude,
                    unit: '',
                    error: 0.1131,
                    fit: true
                },
                {
                    id: '4092346238',
                    number: 2,
                    label: 'Period',
                    value: qmlProxy.model.period,
                    unit: 'rad',
                    error: 0.2573,
                    fit: true
                },
                {
                    id: '9834542745',
                    number: 2,
                    label: 'Vertical shift',
                    value: qmlProxy.model.verticalShift,
                    unit: '',
                    error: 0.0212,
                    fit: true
                },
                {
                    id: '8655377643',
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
                if (pid === '4538458360') {
                    qmlProxy.model.amplitude = parseFloat(value)
                } else if (pid === '4092346238') {
                    qmlProxy.model.period = parseFloat(value)
                } else if (pid === '9834542745') {
                    qmlProxy.model.verticalShift = parseFloat(value)
                } else if (pid === '8655377643') {
                    qmlProxy.model.phaseShift = parseFloat(value)
                }
            }
        }

        readonly property var summary: QtObject {
            property bool isCreated: false

            // https://stackoverflow.com/questions/17882518/reading-and-writing-files-in-qml-qt
            // https://stackoverflow.com/questions/57351643/how-to-save-dynamically-generated-web-page-in-qwebengineview
            function saveFile(fileUrl, text) {
                const request = new XMLHttpRequest()
                request.open("PUT", fileUrl, false)
                request.send(text)
                return request.status
            }
            function saveHtmlReport(fileUrl) {
                const webEngine = ExGlobals.References.summaryReportWebEngine
                webEngine.runJavaScript("document.documentElement.outerHTML",
                                        function(htmlContent) {
                                            print('!!!!!!!', htmlContent)
                                            const status = saveFile(fileUrl, htmlContent)
                                            print(`Save report '${fileUrl}' status: ${status}`)
                                        })
            }
        }

        readonly property var status: QtObject {
            property string asXml:
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
            property var asJson: [
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

        readonly property var plotting: QtObject {
            readonly property bool useWebGL1d: false
            readonly property var libs1d: ['Plotly']
            property string currentLib1d: 'Plotly'
        }

    }

}
