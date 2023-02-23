// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick

import EasyApp.Gui.Style as EaStyle

import Gui.Globals as Globals
import Gui.Logic as Logic


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    property var mainProxy: typeof pyProxy !== 'undefined' && pyProxy !== null ?
                                         pyProxy:
                                         qmlProxy

    readonly property var qmlProxy: QtObject {

        readonly property var project: QtObject {
            property var examplesAsJson: [
                {
                    'name': 'Horizontal line',
                    'description': 'Straight line, horizontal, PicoScope 2204A',
                    'path': '../Resources/Examples/HorizontalLine/project.json'
                },
                {
                    'name': 'Slanting line 1',
                    'description': 'Straight line, positive slope, Tektronix 2430A',
                    'path': '../Resources/Examples/SlantingLine1/project.json'
                },
                {
                    'name': 'Slanting line 2',
                    'description': 'Straight line, negative slope, Siglent SDS1202X-E',
                    'path': '../Resources/Examples/SlantingLine2/project.json'
                }
            ]

            property bool isCreated: false
            property bool needSave: false

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
                    'label': 'Line'
                }
            ]

            property bool isCreated: false

            property real slope: 1.0
            property real yIntercept: 0

            property var xArray: []
            property var yArray: []
            property var calculatedData: ({})

            onSlopeChanged: generateCalculatedData()
            onYInterceptChanged: generateCalculatedData()

            function setXArray() {
                const length = qmlProxy.experiment.measuredDataLength
                xArray = Array.from({ length: length }, (_, i) => i / (length - 1))
            }

            function setYArray() {
                yArray = Logic.Calculator.line(xArray, slope, yIntercept)
            }

            function generateCalculatedData() {
                if (xArray.length !== qmlProxy.experiment.measuredDataLength) {
                    setXArray()
                }
                setYArray()

                calculatedData = {'x': xArray, 'y': yArray}
                isCreated = true
            }

            function emptyCalculatedData() {
                calculatedData = {'x': [], 'y': []}
                isCreated = false
            }
        }

        readonly property var experiment: QtObject {
            readonly property var asJson: [
                    {
                        'label': 'PicoScope'
                    }
                  ]
            property bool isCreated: false

            property real slope: -3
            property real yIntercept: 1.5

            property int measuredDataLength: 300
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
                const length = measuredDataLength
                const xArray = Array.from({ length: length }, (_, i) => i / (length - 1))
                const yArray = Logic.Calculator.lineMeas(xArray, slope, yIntercept)
                measuredData = {'x': xArray, 'y': yArray}
                isCreated = true
            }            

            function emptyMeasuredData() {
                measuredData = {'x': [], 'y': []}
                isCreated = false
            }
        }

        readonly property var fitting: QtObject {
            property bool isFitFinished: false

            function fit() {
                qmlProxy.model.slope = qmlProxy.experiment.slope
                qmlProxy.model.yIntercept = qmlProxy.experiment.yIntercept
                isFitFinished = true
            }
        }

        readonly property var parameters: QtObject {
            property var asJson: []

            Component.onCompleted: generateAsJson()

            function generateAsJson() {
                asJson = [
                    {
                        'id': '4538458360',
                        'number': 1,
                        'label': 'Slope',
                        'value': qmlProxy.model.slope,
                        'min': -5,
                        'max': 5,
                        'unit': '',
                        'error': 0.1131,
                        'fit': true
                    },
                    {
                        'id': '4092346238',
                        'number': 2,
                        'label': 'y-Intercept',
                        'value': qmlProxy.model.yIntercept,
                        'min': -5,
                        'max': 5,
                        'unit': '',
                        'error': 0.2573,
                        'fit': true
                    }
                ]
            }

            function editParameterValue(pid, value) {
                if (typeof pid === 'undefined') {
                    return
                }
                if (pid === '4538458360') {
                    qmlProxy.model.slope = parseFloat(value)
                } else if (pid === '4092346238') {
                    qmlProxy.model.yIntercept = parseFloat(value)
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
