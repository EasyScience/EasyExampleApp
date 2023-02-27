// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals
import Gui.Logic as Logic


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    property var main: typeof pyProxy !== 'undefined' && pyProxy !== null ?
                                         pyProxy:
                                         qmlProxy

    readonly property var qmlProxy: QtObject {

        // Project

        readonly property var project: QtObject {

            property bool isCreated: false
            property bool needSave: false

            property string currentProjectName: 'Default project'
            property string currentProjectDescription: 'Default project description'
            property string currentProjectLocation: ''
            property string currentProjectCreatedDate: ''
            property string currentProjectImage: Qt.resolvedUrl('../Resources/Project/Sine.svg')

            property var examples: [
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

            onExamplesChanged: setNeedSaveToTrue()
            onCurrentProjectNameChanged: setNeedSaveToTrue()
            onCurrentProjectDescriptionChanged: setNeedSaveToTrue()
            onCurrentProjectImageChanged: setNeedSaveToTrue()

            function setNeedSaveToTrue() {
                needSave = true
            }

            function create() {
                currentProjectCreatedDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
                isCreated = true
            }

            function save() {
                let project = {}

                if (isCreated) {
                    project['project'] = {
                        'name': currentProjectName,
                        'description': currentProjectDescription,
                        'location': currentProjectLocation,
                        'creationDate': currentProjectCreatedDate
                    }
                }

                if (qmlProxy.experiment.isCreated) {
                    project['experiment'] = {
                        'label': qmlProxy.experiment.asJson[0]['label'],
                        'isCreated': qmlProxy.experiment.isCreated,
                        'parameters': qmlProxy.experiment.parameters,
                        'dataSize': qmlProxy.experiment.dataSize,
                        'xData': qmlProxy.experiment.xData,
                        'yData': qmlProxy.experiment.yData
                    }
                }

                if (qmlProxy.model.isCreated) {
                    project['model'] = {
                        'label': qmlProxy.model.asJson[0]['label'],
                        'isCreated': qmlProxy.model.isCreated,
                        'parameters': qmlProxy.model.parameters,
                        'yData': qmlProxy.model.yData
                    }
                }

                if (qmlProxy.fitting.isFitFinished) {
                    project['fitting'] = {
                        'isFitFinished': qmlProxy.fitting.isFitFinished
                    }
                }

                if (qmlProxy.summary.isCreated) {
                    project['summary'] = {
                        'isCreated': qmlProxy.summary.isCreated
                    }
                }

                const filePath = `${currentProjectLocation}/project.json`
                EaLogic.Utils.writeFile(filePath, JSON.stringify(project))

                needSave = false
            }
        }

        // Experiment

        readonly property var experiment: QtObject {
            readonly property var description: {
                'label': 'PicoScope'
            }
            property var parameters: {
                'xMin': {
                    'value': 0.0,
                    'fittable': false,
                },
                'xMax': {
                    'value': 1.0,
                    'fittable': false,
                },
                'xStep': {
                    'value': 0.01,
                    'fittable': false,
                }
            }
            property int dataSize: 300
            property var xData: []
            property var yData: []
            property bool isCreated: false

            onDataSizeChanged: {
                if (isCreated) {
                    loadData()
                }
                if (qmlProxy.model.isCreated) {
                    qmlProxy.model.calculateData()
                }
                if (qmlProxy.fitting.isFitFinished) {
                    qmlProxy.fitting.fit()
                }
            }

            onDescriptionChanged: qmlProxy.project.setNeedSaveToTrue()
            onXDataChanged: qmlProxy.project.setNeedSaveToTrue()
            onYDataChanged: qmlProxy.project.setNeedSaveToTrue()
            onParametersChanged: {
                if (isCreated) {
                    qmlProxy.parameters.setFittables()
                    qmlProxy.project.setNeedSaveToTrue()
                }
            }
            onIsCreatedChanged: {
                if (isCreated) {
                    qmlProxy.parameters.setFittables()
                    qmlProxy.project.setNeedSaveToTrue()
                }
            }

            function loadData() {
                const length = dataSize
                const slope = -3.0
                const yIntercept = 1.5
                xData = Array.from({ length: length }, (_, i) => i / (length - 1))
                yData = Logic.LineCalculator.pseudoMeasured(xData, slope, yIntercept)
                isCreated = true
            }            

            function emptyData() {
                xData = []
                yData = []
                isCreated = false
            }

            function editParameter(label, item, value) {
                if (item === 'value') {
                    value = parseFloat(value)
                } else if (item === 'fit') {
                    if (!value) {
                        parameters[label].error = 0
                    }
                }
                if (parameters[label][item] === value) {
                    return
                }
                parameters[label][item] = value
                parametersChanged()
            }
        }

        // Model

        readonly property var model: QtObject {
            readonly property var description: {
                    'label': 'Line'
            }
            property var parameters: {
                'slope': {
                    'value': 1.0,
                    'error': 0,
                    'min': -5,
                    'max': 5,
                    'unit': '',
                    'fittable': true,
                    'fit': true
                },
                'yIntercept': {
                    'value': 0.0,
                    'error': 0,
                    'min': -5,
                    'max': 5,
                    'unit': '',
                    'fittable': true,
                    'fit': true
                }
            }

            property var yData: []
            property bool isCreated: false

            onParametersChanged: {
                if (isCreated) {
                    calculateData()
                    qmlProxy.parameters.setFittables()
                    qmlProxy.project.setNeedSaveToTrue()
                }
            }
            onIsCreatedChanged: {
                if (isCreated) {
                    qmlProxy.parameters.setFittables()
                    qmlProxy.project.setNeedSaveToTrue()
                }
            }

            function calculateData() {
                const slope = parameters.slope.value
                const yIntercept = parameters.yIntercept.value
                const xData = qmlProxy.experiment.xData
                yData = Logic.LineCalculator.calculated(xData, slope, yIntercept)
                isCreated = true
            }

            function emptyData() {
                yData = []
                isCreated = false
            }

            function editParameter(label, item, value) {
                if (item === 'value') {
                    value = parseFloat(value)
                } else if (item === 'fit') {
                    if (!value) {
                        parameters[label].error = 0
                    }
                }
                if (parameters[label][item] === value) {
                    return
                }
                parameters[label][item] = value
                parametersChanged()
            }
        }

        // Fitting

        readonly property var fitting: QtObject {
            property bool isFitFinished: false

            onIsFitFinishedChanged: {
                qmlProxy.model.parametersChanged()
                qmlProxy.project.setNeedSaveToTrue()
            }

            function fit() {
                isFitFinished = false
                if (qmlProxy.model.parameters.slope.fit) {
                    qmlProxy.model.parameters.slope.value = -3.0015
                    qmlProxy.model.parameters.slope.error = 0.0023
                }
                if (qmlProxy.model.parameters.yIntercept.fit) {
                    qmlProxy.model.parameters.yIntercept.value = 1.4950
                    qmlProxy.model.parameters.yIntercept.error = 0.0045
                }
                isFitFinished = true
            }
        }

        // Parameters

        readonly property var parameters: QtObject {
            property var fittables: []

            function edit(group, label, item, value) {
                if (group === 'experiment') {
                    qmlProxy.experiment.editParameter(label, item, value)
                } else if (group === 'model') {
                    qmlProxy.model.editParameter(label, item, value)
                }
            }

            function setFittables() {
                let _fittables = []
                for (let label in qmlProxy.experiment.parameters) {
                    let param = qmlProxy.experiment.parameters[label]
                    if (param.fittable) {
                        param.group = 'experiment'
                        param.parent = qmlProxy.experiment.description.label
                        param.label = label
                        _fittables.push(param)
                    }
                }
                for (let label in qmlProxy.model.parameters) {
                    let param = qmlProxy.model.parameters[label]
                    if (param.fittable) {
                        param.group = 'model'
                        param.parent = qmlProxy.model.description.label
                        param.label = label
                        _fittables.push(param)
                    }
                }
                if (_fittables.length !== 0) {
                    fittables = _fittables
                }
            }

        }

        // Summary

        readonly property var summary: QtObject {
            property bool isCreated: false

            onIsCreatedChanged: qmlProxy.project.setNeedSaveToTrue()

            // https://stackoverflow.com/questions/17882518/reading-and-writing-files-in-qml-qt
            // https://stackoverflow.com/questions/57351643/how-to-save-dynamically-generated-web-page-in-qwebengineview
            function saveHtmlReport(fileUrl) {
                const webEngine = Globals.Refs.summaryReportWebEngine
                webEngine.runJavaScript("document.documentElement.outerHTML",
                                        function(htmlContent) {
                                            const status = EaLogic.Utils.writeFile(fileUrl, htmlContent)
                                        })
            }
        }

        // Status

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

        // Plotting

        readonly property var plotting: QtObject {
            readonly property bool useWebGL1d: false
            readonly property var libs1d: ['Plotly']
            property string currentLib1d: 'Plotly'
        }

    }

}
