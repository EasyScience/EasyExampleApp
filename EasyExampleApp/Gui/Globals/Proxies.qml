// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals
import Gui.Logic as Logic


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    property var main: typeof pyProxy !== 'undefined' && pyProxy !== null ?
                                         pyProxy:
                                         qmlProxy

    readonly property var qmlProxy: QtObject {

        //////////
        // Logger
        //////////

        readonly property var logger: QtObject {
            property string level: 'debug'
        }

        //////////////
        // Connections
        //////////////

        readonly property var connections: QtObject {

            Component.onCompleted: {
                // Project

//                qmlProxy.project.nameChanged.connect(qmlProxy.project.setNeedSaveToTrue)
//                qmlProxy.project.descriptionChanged.connect(qmlProxy.project.setNeedSaveToTrue)
 //               qmlProxy.project.createdChanged.connect(qmlProxy.project.save)

                // Experiment

                qmlProxy.experiment.dataChanged.connect(qmlProxy.project.setNeedSaveToTrue)

                qmlProxy.experiment.dataChanged.connect(qmlProxy.fittables.set)


                qmlProxy.experiment.definedChanged.connect(function() {
                    print(`Experiment created: ${qmlProxy.experiment.defined}`)
                    qmlProxy.fittables.set()
                    qmlProxy.project.setNeedSaveToTrue()
                })

//                qmlProxy.experiment.parameterEdited.connect(function(needSetFittables) {
  //                  qmlProxy.experiment.parametersEdited(needSetFittables)
    //            })
/*
                qmlProxy.experiment.parametersEdited.connect(function(needSetFittables) {
                    print(`Experiment parameters changed. Need set fittables: ${needSetFittables}`)
                    qmlProxy.experiment.parametersChanged()
                    qmlProxy.experiment.loadData()
                    if (needSetFittables) {
                        qmlProxy.fittables.set()
                    }
                    qmlProxy.project.setNeedSaveToTrue()
                })

                qmlProxy.experiment.dataSizeChanged.connect(function() {
                    print(`Experiment data size: ${qmlProxy.experiment.dataSize}`)
                    qmlProxy.experiment.loadData()
                    if (qmlProxy.model.isCreated) {
                        qmlProxy.model.calculateData()
                    }
                })
*/
                // Model


//                qmlProxy.model.dataChanged.connect(qmlProxy.fittables.set)

                //qmlProxy.model.descriptionChanged.connect(qmlProxy.project.setNeedSaveToTrue)
/*
                qmlProxy.model.modelAdded.connect(function() {
                    print(`Model added. Models count: ${qmlProxy.model.models.length}`)
                    qmlProxy.model.calculateData()
                    qmlProxy.fittables.set()
                    qmlProxy.project.setNeedSaveToTrue()
                    qmlProxy.model.modelsChanged()
                })
*/
                qmlProxy.model.parameterEdited.connect(function(needSetFittables) {
                    //qmlProxy.model.parametersEdited(needSetFittables)
                    //qmlProxy.model.dataChanged()
                    qmlProxy.model.calculate()
                    if (needSetFittables) {
                        //print('!!!!!!!!!!', needSetFittables)
                        qmlProxy.fittables.set()
                    }
                    qmlProxy.project.setNeedSaveToTrue()
                })

                /*
                qmlProxy.model.parametersEdited.connect(function(needSetFittables) {
                    //qmlProxy.model.modelsChanged()
                    //qmlProxy.model.calculateData()
                    qmlProxy.model.dataChanged()
                    if (needSetFittables) {
                        qmlProxy.fittables.set()
                    }
                    qmlProxy.project.setNeedSaveToTrue()
                })
                */

                // Fitting

                /*
                qmlProxy.fitting.fitFinishedChanged.connect(function() {
                    print(`Fit finished: ${qmlProxy.fitting.fitFinished}`)
                    const needSetFittables = true
                    qmlProxy.model.parametersEdited(needSetFittables)
                })
                */

            }

        }

        //////////
        // Project
        //////////

        readonly property var project: QtObject {

            readonly property var _EMPTY_DATA: {
                'name': '',
                'description': '',
                'location': '',
                'creationDate': ''
            }

            readonly property var _DEFAULT_DATA: {
                'name': 'Default project',
                'description': 'Default project description',
                'location': '',
                'creationDate': ''
            }

            readonly property var _EXAMPLES: [
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

            property var data: _DEFAULT_DATA
            property var examples: _EXAMPLES
            property bool created: false
            property bool needSave: false

            function setNeedSaveToTrue() {
                needSave = true
            }

            function create() {
                data = _DEFAULT_DATA
                data.creationDate = `${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}`
                dataChanged()  // Emit signal, as it is not emited automatically
                created = true
            }

            function editData(key, value) {
                if (data[key] === value) {
                    return
                }
                data[key] = value
                dataChanged()  // Emit signal, as it is not emited automatically
            }

            function save() {
                let out = {}
                if (created) {
                    out['project'] = data
                }
                if (qmlProxy.experiment.defined) {
                    out['experiment'] = qmlProxy.experiment.dataBlocks
                }
                if (qmlProxy.model.defined) {
                    out['model'] = qmlProxy.model.dataBlocks
                }
                const filePath = `${out.project.location}/project.json`
                EaLogic.Utils.writeFile(filePath, JSON.stringify(project))
                needSave = false
            }
        }

        /////////////
        // Experiment
        /////////////

        readonly property var experiment: QtObject {

            readonly property var _EMPTY_DATA: [
                {
                    'name': '',
                    'params': {},
                    'xArray': [],
                    'yArray': []
                }
            ]

            readonly property var _DEFAULT_DATA: [
                {
                    'name': 'PicoScope',
                    'params': {
                        'xMin': {
                            'value': 0.0,
                            'fittable': false
                        },
                        'xMax': {
                            'value': 1.0,
                            'fittable': false
                        },
                        'xStep': {
                            'value': 0.01,
                            'fittable': false
                        }
                    },
                    'xArray': [],
                    'yArray': []
                }
            ]

            property var data: _EMPTY_DATA
            property bool defined: false

            function load() {
                data = _DEFAULT_DATA  // dataChanged() signal emited automatically
                const xMax = data[0].params.xMax.value
                const xMin = data[0].params.xMin.value
                const xStep = data[0].params.xStep.value
                const length = (xMax - xMin) / xStep + 1
                const xArray = Array.from({ length: length }, (_, i) => i / (length - 1))
                const slope = -3.0
                const yIntercept = 1.5
                const yArray = Logic.LineCalculator.pseudoMeasured(xArray, slope, yIntercept)
                data[0].xArray = xArray
                data[0].yArray = yArray
                dataChanged()  // Emit signal, as it is not emited automatically
                created = true
            }            

            function reset() {
                data = _EMPTY_DATA  // dataChanged() signal emited automatically
                created = false
            }

        }

        ////////
        // Model
        ////////

        readonly property var model: QtObject {
            signal parameterEdited(bool needSetFittables)
            //signal parametersEdited(bool needSetFittables)
            //signal modelAdded()
            //signal modelRemoved()

            readonly property var _EMPTY_DATA: [
                {
                    'name': '',
                    'params': {},
                    'yArray': []
                }
            ]

            readonly property var _DEFAULT_DATA: [
                {
                    'name': 'LineA',
                    'params': {
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
                    },
                    'yArray': []
                },
                {
                    'name': 'LineB',
                    'params': {
                        'slope': {
                            'value': -1.5,
                            'error': 0,
                            'min': -5,
                            'max': 5,
                            'unit': '',
                            'fittable': true,
                            'fit': true
                        },
                        'yIntercept': {
                            'value': 0.5,
                            'error': 0,
                            'min': -5,
                            'max': 5,
                            'unit': '',
                            'fittable': true,
                            'fit': true
                        }
                    },
                    'yArray': []
                }
            ]

            property var data: _EMPTY_DATA
            property var totalYArray: []
            property bool created: false
            property int currentIndex: 0

            function load() {
                data = _DEFAULT_DATA  // dataChanged() signal emited automatically
                calculate()
                qmlProxy.fittables.set() //////////////////////////
                created = true
            }

            function reset() {
                data = _EMPTY_DATA  // dataChanged() signal emited automatically
                created = false
            }

            function calculate() {
                for (let i in data) {
                    calculateYArray(i)
                }
                dataChanged()  // Emit signal, as it is not emited automatically
                calculateTotalYArray()
            }

            function calculateYArray(i) {
                const xArray = qmlProxy.experiment.data[0].xArray
                const slope = data[i].params.slope.value
                const yIntercept = data[i].params.yIntercept.value
                const yArray = Logic.LineCalculator.calculated(xArray, slope, yIntercept)
                data[i].yArray = yArray
            }

            function calculateTotalYArray() {
                const length = data[0].yArray.length
                let out = Array(length).fill(0)
                for (const block of data) {
                    out = out.map((val, idx) => val + block.yArray[idx])
                }
                totalYArray = out  // totalYArrayChanged() signal emited automatically
            }

            function editParameter(currentModelIndex, name, item, value, needSetFittables) {
                if (item === 'value') {
                    value = parseFloat(value)
                } else if (item === 'fit') {
                    if (!value) {
                        data[currentModelIndex].params[name].error = 0
                    }
                }
                if (data[currentModelIndex].params[name][item] === value) {
                    return
                }
                data[currentModelIndex].params[name][item] = value
                parameterEdited(needSetFittables)
            }

        }

        //////////
        // Fitting
        //////////

        readonly property var fitting: QtObject {
            property bool isFittingNow: false

            function fit() {
                isFittingNow = true
                /*
                if (qmlProxy.model.fittables.slope.fit) {
                    qmlProxy.model.fittables.slope.value = -3.0015
                    qmlProxy.model.fittables.slope.error = 0.0023
                }
                if (qmlProxy.model.fittables.yIntercept.fit) {
                    qmlProxy.model.fittables.yIntercept.value = 1.4950
                    qmlProxy.model.fittables.yIntercept.error = 0.0045
                }
                */
                isFittingNow = false
            }
        }

        /////////////
        // Parameters
        /////////////

        readonly property var fittables: QtObject {
            property var data: []

            function edit(group, parentIndex, name, item, value) {
                const needSetFittables = false
                if (group === 'experiment') {
                    qmlProxy.experiment.editParameter(parentIndex, name, item, value, needSetFittables)
                } else if (group === 'model') {
                    qmlProxy.model.editParameter(parentIndex, name, item, value, needSetFittables)
                }
            }

            function set() {
                let _data = []
                for (let i in qmlProxy.experiment.data) {
                    const block = qmlProxy.experiment.data[i]
                    for (const name in block.params) {
                        const param = block.params[name]
                        if (param.fittable) {
                            let fittable = {}
                            fittable.group = 'experiment'
                            fittable.name = name
                            fittable.parentIndex = i
                            fittable.parentName = block.name
                            fittable.value = param.value
                            fittable.error = param.error
                            fittable.min = param.min
                            fittable.max = param.max
                            fittable.unit = param.unit
                            fittable.fit = param.fit
                            _data.push(fittable)
                        }
                    }
                }
                for (let i in qmlProxy.model.data) {
                    const block = qmlProxy.model.data[i]
                    for (const name in block.params) {
                        const param = block.params[name]
                        if (param.fittable) {
                            let fittable = {}
                            fittable.group = 'model'
                            fittable.name = name
                            fittable.parentIndex = i
                            fittable.parentName = block.name
                            fittable.value = param.value
                            fittable.error = param.error
                            fittable.min = param.min
                            fittable.max = param.max
                            fittable.unit = param.unit
                            fittable.fit = param.fit
                            _data.push(fittable)
                        }
                    }
                }
                if (_data.length !== 0) {
                    /*
                    for (let i = 0; i < 10000; ++i) {
                        _fittables.push(_fittables[0])
                    }
                    */
                    data = _data  // dataChanged() signal emited automatically
                }
            }

        }

        //////////
        // Summary
        //////////

        readonly property var summary: QtObject {
            property bool isCreated: false

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

        /////////
        // Status
        /////////

        readonly property var status: QtObject {
            property string asXml:
                `<root>
                  <item>
                    <name>Calculations</name>
                    <value>CrysPy</value>
                  </item>
                  <item>
                    <name>Minimization</name>
                    <value>lmfit</value>
                  </item>
                </root>`
            property var asJson: [
                {
                    name: 'Calculations',
                    value: 'CrysPy'
                },
                {
                    name: 'Minimization',
                    value: 'lmfit'
                }
              ]
        }

        ///////////
        // Plotting
        ///////////

        readonly property var plotting: QtObject {
            readonly property bool useWebGL1d: false
            readonly property var libs1d: ['Plotly']
            property string currentLib1d: 'Plotly'
        }

    }

    // Charts

    property string currentLib1d: EaGlobals.Vars.currentLib1d
    onCurrentLib1dChanged: main.plotting.currentLib1d = currentLib1d

    // Logging

    property string loggingLevel: EaGlobals.Vars.loggingLevel
    onLoggingLevelChanged: main.logger.level = loggingLevel


    // Common functions

    function modelMainParameterValue(name) {
        if (!main.model.defined) {
            return ''
        }
        const currentModelIndex = main.model.currentIndex
        const value = main.model.dataBlocks[currentModelIndex].params[name]['value']
        const formattedValue = typeof value === "number" ? value.toFixed(4) : value
        return formattedValue
    }

    function setModelMainParameterValue(name, value) {
        main.model.editParameter(name, 'value', value)
    }

    function modelLoopParameterValue(loopName, parameterName, parameterIndex) {
        if (!main.model.defined) {
            return ''
        }
        const currentModelIndex = main.model.currentIndex
        const value = main.model.dataBlocks[currentModelIndex].loops[loopName][parameterIndex][parameterName]['value']
        const formattedValue = typeof value === "number" ? value.toFixed(4) : value
        return formattedValue
    }

    function setModelLoopParameterValue(loopName, parameterName, parameterIndex, value) {
        main.model.editLoopParameterValue(loopName, parameterName, parameterIndex, value)
    }

    function experimentMainParameterValue(name) {
        if (!main.experiment.defined) {
            return ''
        }
        const currentExperimentIndex = main.experiment.currentIndex
        const value = main.experiment.dataBlocks[currentExperimentIndex].params[name]['value']
        const formattedValue = typeof value === "number" ? value.toFixed(4) : value
        return formattedValue
    }

    function experimentLoopParameterValue(loopName, parameterName, parameterIndex) {
        if (!main.experiment.defined) {
            return ''
        }
        const currentExperimentIndex = main.experiment.currentIndex
        const value = main.experiment.dataBlocks[currentExperimentIndex].loops[loopName][parameterIndex][parameterName]['value']
        const formattedValue = typeof value === "number" ? value.toFixed(4) : value
        return formattedValue
    }

    function atomColor(symbol) {
        const jmolColors = {
            'H'  : '#FFFFFF',
            'He' : '#D9FFFF',
            'Li' : '#CC80FF',
            'Be' : '#C2FF00',
            'B'  : '#FFB5B5',
            'C'  : '#909090',
            'N'  : '#3050F8',
            'O'  : '#FF0D0D',
            'F'  : '#90E050',
            'Ne' : '#B3E3F5',
            'Na' : '#AB5CF2',
            'Mg' : '#8AFF00',
            'Al' : '#BFA6A6',
            'Si' : '#F0C8A0',
            'P'  : '#FF8000',
            'S'  : '#FFFF30',
            'Cl' : '#1FF01F',
            'Ar' : '#80D1E3',
            'K'  : '#8F40D4',
            'Ca' : '#3DFF00',
            'Sc' : '#E6E6E6',
            'Ti' : '#BFC2C7',
            'V'  : '#A6A6AB',
            'Cr' : '#8A99C7',
            'Mn' : '#9C7AC7',
            'Fe' : '#E06633',
            'Co' : '#F090A0',
            'Ni' : '#50D050',
            'Cu' : '#C88033',
            'Zn' : '#7D80B0',
            'Ga' : '#C28F8F',
            'Ge' : '#668F8F',
            'As' : '#BD80E3',
            'Se' : '#FFA100',
            'Br' : '#A62929',
            'Kr' : '#5CB8D1',
            'Rb' : '#702EB0',
            'Sr' : '#00FF00',
            'Y'  : '#94FFFF',
            'Zr' : '#94E0E0',
            'Nb' : '#73C2C9',
            'Mo' : '#54B5B5',
            'Tc' : '#3B9E9E',
            'Ru' : '#248F8F',
            'Rh' : '#0A7D8C',
            'Pd' : '#006985',
            'Ag' : '#C0C0C0',
            'Cd' : '#FFD98F',
            'In' : '#A67573',
            'Sn' : '#668080',
            'Sb' : '#9E63B5',
            'Te' : '#D47A00',
            'I'  : '#940094',
            'Xe' : '#429EB0',
            'Cs' : '#57178F',
            'Ba' : '#00C900',
            'La' : '#70D4FF',
            'Ce' : '#FFFFC7',
            'Pr' : '#D9FFC7',
            'Nd' : '#C7FFC7',
            'Pm' : '#A3FFC7',
            'Sm' : '#8FFFC7',
            'Eu' : '#61FFC7',
            'Gd' : '#45FFC7',
            'Tb' : '#30FFC7',
            'Dy' : '#1FFFC7',
            'Ho' : '#00FF9C',
            'Er' : '#00E675',
            'Tm' : '#00D452',
            'Yb' : '#00BF38',
            'Lu' : '#00AB24',
            'Hf' : '#4DC2FF',
            'Ta' : '#4DA6FF',
            'W'  : '#2194D6',
            'Re' : '#267DAB',
            'Os' : '#266696',
            'Ir' : '#175487',
            'Pt' : '#D0D0E0',
            'Au' : '#FFD123',
            'Hg' : '#B8B8D0',
            'Tl' : '#A6544D',
            'Pb' : '#575961',
            'Bi' : '#9E4FB5',
            'Po' : '#AB5C00',
            'At' : '#754F45',
            'Rn' : '#428296',
            'Fr' : '#420066',
            'Ra' : '#007D00',
            'Ac' : '#70ABFA',
            'Th' : '#00BAFF',
            'Pa' : '#00A1FF',
            'U'  : '#008FFF',
            'Np' : '#0080FF',
            'Pu' : '#006BFF',
            'Am' : '#545CF2',
            'Cm' : '#785CE3',
            'Bk' : '#8A4FE3',
            'Cf' : '#A136D4',
            'Es' : '#B31FD4',
            'Fm' : '#B31FBA',
            'Md' : '#B30DA6',
            'No' : '#BD0D87',
            'Lr' : '#C70066',
            'Rf' : '#CC0059',
            'Db' : '#D1004F',
            'Sg' : '#D90045',
            'Bh' : '#E00038',
            'Hs' : '#E6002E',
            'Mt' : '#EB0026',
            'Ds' : '#000000',
            'Rg' : '#000000',
            'Cn' : '#000000',
            'Nh' : '#000000',
            'Fl' : '#000000',
            'Mc' : '#000000',
            'Lv' : '#000000',
            'Ts' : '#000000',
            'Og' : '#000000'
        }
        const colors = jmolColors
        // Simple case, e.g. Co
        if (colors.hasOwnProperty(symbol)) {
            return colors[symbol]
        }
        // First 2 symbols, if valency is given for 2 characters element, e.g. Mn3+
        if (colors.hasOwnProperty(symbol.substring(0, 2))) {
            return colors[symbol.substring(0, 2)]
        }
        // First symbol, if valency is given for 1 characters element, e.g. O2-
        if (colors.hasOwnProperty(symbol.substring(0, 1))) {
            return colors[symbol.substring(0, 1)]
        }
        // Transparent color if no elements found
        return 'transparent'
    }

}
