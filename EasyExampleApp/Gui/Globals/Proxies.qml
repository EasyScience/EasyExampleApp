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

    // Model

    function modelMainParam(name) {
        if (!main.model.defined) {
            return {}
        }
        const currentModelIndex = main.model.currentIndex
        return main.model.dataBlocks[currentModelIndex].params[name]
    }

    function modelLoopParam(loopName, paramName, rowIndex) {
        if (!main.model.defined) {
            return {}
        }
        const currentModelIndex = main.model.currentIndex
        return main.model.dataBlocks[currentModelIndex].loops[loopName][rowIndex][paramName]
    }

    function setModelMainParam(parameter, field, value) {
        console.debug(`---------- Editing model main param ${parameter.name} '${field}' to ${value} ----------`)
        main.model.setMainParam(parameter.name, field, value)
    }

    function setModelLoopParam(param, field, value) {
        console.debug(`---------- Editing model loop param ${param.loopName}${param.name}[${param.idx}] '${field}' to ${value} ----------`)
        main.model.setLoopParam(param.loopName, param.name, param.idx, field, value)
    }

    // Experiment

    function experimentMainParam(name) {
        if (!main.experiment.defined) {
            return {}
        }
        const currentModelIndex = main.experiment.currentIndex
        return main.experiment.dataBlocks[currentModelIndex].params[name]
    }

    function experimentLoopParam(loopName, paramName, rowIndex) {
        if (!main.experiment.defined) {
            return {}
        }
        const currentModelIndex = main.experiment.currentIndex
        return main.experiment.dataBlocks[currentModelIndex].loops[loopName][rowIndex][paramName]
    }

    function setExperimentMainParam(parameter, field, value) {
        console.debug(`---------- Editing experiment main param ${parameter.name} '${field}' to ${value} ----------`)
        main.experiment.setMainParam(parameter.name, field, value)
    }

    function setExperimentLoopParam(param, field, value) {
        console.debug(`---------- Editing experiment loop param ${param.loopName}${param.name}[${param.idx}] '${field}' to ${value} ----------`)
        main.experiment.setLoopParam(param.loopName, param.name, param.idx, field, value)
    }

    // Misc

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
        // If symbol is not defined
        if (typeof symbol === 'undefined') {
            return 'black'
        }
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
        return 'black'
    }


   function atomData(typeSymbol, item) {
      const data = {
           "H": {
             "symbol": "H",
             "name": "Hydrogen",
             "atomicNumber": 1,
             "addH": false,
             "color": "#FFFFFF",
             "covalentRadius": 0.31,
             "vdWRadius": 1.1,
             "valency": 1,
             "mass": 1
           },
           "He": {
             "symbol": "He",
             "name": "Helium",
             "atomicNumber": 2,
             "addH": false,
             "color": "#D9FFFF",
             "covalentRadius": 0.28,
             "vdWRadius": 1.4,
             "valency": 0,
             "mass": 4
           },
           "Li": {
             "symbol": "Li",
             "name": "Lithium",
             "atomicNumber": 3,
             "addH": false,
             "color": "#CC80FF",
             "covalentRadius": 1.28,
             "vdWRadius": 1.82,
             "valency": 1,
             "mass": 7
           },
           "Be": {
             "symbol": "Be",
             "name": "Beryllium",
             "atomicNumber": 4,
             "addH": false,
             "color": "#C2FF00",
             "covalentRadius": 0.96,
             "vdWRadius": 1.53,
             "valency": 2,
             "mass": 9
           },
           "B": {
             "symbol": "B",
             "name": "Boron",
             "atomicNumber": 5,
             "addH": false,
             "color": "#FFB5B5",
             "covalentRadius": 0.84,
             "vdWRadius": 1.92,
             "valency": 3,
             "mass": 11
           },
           "C": {
             "symbol": "C",
             "name": "Carbon",
             "atomicNumber": 6,
             "addH": false,
             "color": "#909090",
             "covalentRadius": 0.76,
             "vdWRadius": 1.7,
             "valency": 4,
             "mass": 12
           },
           "N": {
             "symbol": "N",
             "name": "Nitrogen",
             "atomicNumber": 7,
             "addH": false,
             "color": "#3050F8",
             "covalentRadius": 0.71,
             "vdWRadius": 1.55,
             "valency": 3,
             "mass": 14
           },
           "O": {
             "symbol": "O",
             "name": "Oxygen",
             "atomicNumber": 8,
             "addH": false,
             "color": "#FF0D0D",
             "covalentRadius": 0.66,
             "vdWRadius": 1.52,
             "valency": 2,
             "mass": 16
           },
           "F": {
             "symbol": "F",
             "name": "Fluorine",
             "atomicNumber": 9,
             "addH": false,
             "color": "#90E050",
             "covalentRadius": 0.57,
             "vdWRadius": 1.47,
             "valency": 1,
             "mass": 19
           },
           "Ne": {
             "symbol": "Ne",
             "name": "Neon",
             "atomicNumber": 10,
             "addH": false,
             "color": "#B3E3F5",
             "covalentRadius": 0.58,
             "vdWRadius": 1.54,
             "valency": 0,
             "mass": 20
           },
           "Na": {
             "symbol": "Na",
             "name": "Sodium",
             "atomicNumber": 11,
             "addH": true,
             "color": "#AB5CF2",
             "covalentRadius": 1.66,
             "vdWRadius": 2.27,
             "valency": 1,
             "mass": 23
           },
           "Mg": {
             "symbol": "Mg",
             "name": "Magnesium",
             "atomicNumber": 12,
             "addH": true,
             "color": "#8AFF00",
             "covalentRadius": 1.41,
             "vdWRadius": 1.73,
             "valency": 2,
             "mass": 24
           },
           "Al": {
             "symbol": "Al",
             "name": "Aluminum",
             "atomicNumber": 13,
             "addH": true,
             "color": "#BFA6A6",
             "covalentRadius": 1.21,
             "vdWRadius": 2.11,
             "valency": 3,
             "mass": 27
           },
           "Si": {
             "symbol": "Si",
             "name": "Silicon",
             "atomicNumber": 14,
             "addH": true,
             "color": "#F0C8A0",
             "covalentRadius": 1.11,
             "vdWRadius": 2.03,
             "valency": 4,
             "mass": 28
           },
           "P": {
             "symbol": "P",
             "name": "Phosphorus",
             "atomicNumber": 15,
             "addH": true,
             "color": "#FF8000",
             "covalentRadius": 1.07,
             "vdWRadius": 1.8,
             "valency": 3,
             "mass": 31
           },
           "S": {
             "symbol": "S",
             "name": "Sulfur",
             "atomicNumber": 16,
             "addH": true,
             "color": "#FFFF30",
             "covalentRadius": 1.05,
             "vdWRadius": 1.8,
             "valency": 2,
             "mass": 32
           },
           "Cl": {
             "symbol": "Cl",
             "name": "Chlorine",
             "atomicNumber": 17,
             "addH": false,
             "color": "#1FF01F",
             "covalentRadius": 1.02,
             "vdWRadius": 1.75,
             "valency": 1,
             "mass": 35
           },
           "Ar": {
             "symbol": "Ar",
             "name": "Argon",
             "atomicNumber": 18,
             "addH": false,
             "color": "#80D1E3",
             "covalentRadius": 1.06,
             "vdWRadius": 1.88,
             "valency": 0,
             "mass": 40
           },
           "K": {
             "symbol": "K",
             "name": "Potassium",
             "atomicNumber": 19,
             "addH": true,
             "color": "#8F40D4",
             "covalentRadius": 2.03,
             "vdWRadius": 2.75,
             "valency": 1,
             "mass": 39
           },
           "Ca": {
             "symbol": "Ca",
             "name": "Calcium",
             "atomicNumber": 20,
             "addH": true,
             "color": "#3DFF00",
             "covalentRadius": 1.76,
             "vdWRadius": 2.31,
             "valency": 2,
             "mass": 40
           },
           "Sc": {
             "symbol": "Sc",
             "name": "Scandium",
             "atomicNumber": 21,
             "addH": true,
             "color": "#E6E6E6",
             "covalentRadius": 1.7,
             "vdWRadius": 2.11,
             "valency": 3,
             "mass": 45
           },
           "Ti": {
             "symbol": "Ti",
             "name": "Titanium",
             "atomicNumber": 22,
             "addH": true,
             "color": "#BFC2C7",
             "covalentRadius": 1.6,
             "vdWRadius": 2.0,
             "valency": 4,
             "mass": 48
           },
           "V": {
             "symbol": "V",
             "name": "Vanadium",
             "atomicNumber": 23,
             "addH": true,
             "color": "#A6A6AB",
             "covalentRadius": 1.53,
             "vdWRadius": 1.92,
             "valency": 5,
             "mass": 51
           },
           "Cr": {
             "symbol": "Cr",
             "name": "Chromium",
             "atomicNumber": 24,
             "addH": true,
             "color": "#8A99C7",
             "covalentRadius": 1.39,
             "vdWRadius": 1.85,
             "valency": 3,
             "mass": 52
           },
           "Mn": {
             "symbol": "Mn",
             "name": "Manganese",
             "atomicNumber": 25,
             "addH": true,
             "color": "#9C7AC7",
             "covalentRadius": 1.39,
             "vdWRadius": 1.79,
             "valency": 2,
             "mass": 55
           },
           "Fe": {
             "symbol": "Fe",
             "name": "Iron",
             "atomicNumber": 26,
             "addH": true,
             "color": "#E06633",
             "covalentRadius": 1.32,
             "vdWRadius": 1.72,
             "valency": 2,
             "mass": 56
           },
           "Co": {
             "symbol": "Co",
             "name": "Cobalt",
             "atomicNumber": 27,
             "addH": true,
             "color": "#F090A0",
             "covalentRadius": 1.26,
             "vdWRadius": 1.67,
             "valency": 2,
             "mass": 59
           },
           "Ni": {
             "symbol": "Ni",
             "name": "Nickel",
             "atomicNumber": 28,
             "addH": true,
             "color": "#50D050",
             "covalentRadius": 1.24,
             "vdWRadius": 1.62,
             "valency": 2,
             "mass": 59
           },
           "Cu": {
             "symbol": "Cu",
             "name": "Copper",
             "atomicNumber": 29,
             "addH": true,
             "color": "#C88033",
             "covalentRadius": 1.32,
             "vdWRadius": 1.57,
             "valency": 2,
             "mass": 64
           },
           "Zn": {
             "symbol": "Zn",
             "name": "Zinc",
             "atomicNumber": 30,
             "addH": true,
             "color": "#7D80B0",
             "covalentRadius": 1.22,
             "vdWRadius": 1.53,
             "valency": 2,
             "mass": 65
           },
           "Ga": {
             "symbol": "Ga",
             "name": "Gallium",
             "atomicNumber": 31,
             "addH": true,
             "color": "#C28F8F",
             "covalentRadius": 1.22,
             "vdWRadius": 1.87,
             "valency": 3,
             "mass": 70
           },
           "Ge": {
             "symbol": "Ge",
             "name": "Germanium",
             "atomicNumber": 32,
             "addH": true,
             "color": "#668F8F",
             "covalentRadius": 1.2,
             "vdWRadius": 2.11,
             "valency": 4,
             "mass": 73
           },
           "As": {
             "symbol": "As",
             "name": "Arsenic",
             "atomicNumber": 33,
             "addH": true,
             "color": "#BD80E3",
             "covalentRadius": 1.19,
             "vdWRadius": 1.85,
             "valency": 3,
             "mass": 75
           },
           "Se": {
             "symbol": "Se",
             "name": "Selenium",
             "atomicNumber": 34,
             "addH": true,
             "color": "#FFA100",
             "covalentRadius": 1.2,
             "vdWRadius": 1.9,
             "valency": 2,
             "mass": 79
           },
           "Br": {
             "symbol": "Br",
             "name": "Bromine",
             "atomicNumber": 35,
             "addH": true,
             "color": "#A62929",
             "covalentRadius": 1.2,
             "vdWRadius": 1.85,
             "valency": 1,
             "mass": 80
           },
           "Kr": {
             "symbol": "Kr",
             "name": "Krypton",
             "atomicNumber": 36,
             "addH": false,
             "color": "#5CB8D1",
             "covalentRadius": 1.16,
             "vdWRadius": 2.02,
             "valency": 0,
             "mass": 84
           },
           "Rb": {
             "symbol": "Rb",
             "name": "Rubidium",
             "atomicNumber": 37,
             "addH": true,
             "color": "#702EB0",
             "covalentRadius": 2.2,
             "vdWRadius": 3.03,
             "valency": 1,
             "mass": 85
           },
           "Sr": {
             "symbol": "Sr",
             "name": "Strontium",
             "atomicNumber": 38,
             "addH": true,
             "color": "#00FF00",
             "covalentRadius": 1.95,
             "vdWRadius": 2.49,
             "valency": 2,
             "mass": 88
           },
           "Y": {
             "symbol": "Y",
             "name": "Yttrium",
             "atomicNumber": 39,
             "addH": true,
             "color": "#94FFFF",
             "covalentRadius": 1.9,
             "vdWRadius": 2.27,
             "valency": 3,
             "mass": 89
           },
           "Zr": {
             "symbol": "Zr",
             "name": "Zirconium",
             "atomicNumber": 40,
             "addH": true,
             "color": "#94E0E0",
             "covalentRadius": 1.75,
             "vdWRadius": 2.16,
             "valency": 4,
             "mass": 91
           },
           "Nb": {
             "symbol": "Nb",
             "name": "Niobium",
             "atomicNumber": 41,
             "addH": true,
             "color": "#73C2C9",
             "covalentRadius": 1.64,
             "vdWRadius": 2.08,
             "valency": 5,
             "mass": 93
           },
           "Mo": {
             "symbol": "Mo",
             "name": "Molybdenum",
             "atomicNumber": 42,
             "addH": true,
             "color": "#54B5B5",
             "covalentRadius": 1.54,
             "vdWRadius": 2.01,
             "valency": 6,
             "mass": 96
           },
           "Tc": {
             "symbol": "Tc",
             "name": "Technetium",
             "atomicNumber": 43,
             "addH": true,
             "color": "#3B9E9E",
             "covalentRadius": 1.47,
             "vdWRadius": 1.95,
             "valency": 7,
             "mass": 98
           },
           "Ru": {
             "symbol": "Ru",
             "name": "Ruthenium",
             "atomicNumber": 44,
             "addH": true,
             "color": "#248F8F",
             "covalentRadius": 1.46,
             "vdWRadius": 1.89,
             "valency": 8,
             "mass": 101
           },
           "Rh": {
             "symbol": "Rh",
             "name": "Rhodium",
             "atomicNumber": 45,
             "addH": true,
             "color": "#0A7D8C",
             "covalentRadius": 1.42,
             "vdWRadius": 1.83,
             "valency": 9,
             "mass": 103
           },
           "Pd": {
             "symbol": "Pd",
             "name": "Palladium",
             "atomicNumber": 46,
             "addH": true,
             "color": "#006985",
             "covalentRadius": 1.39,
             "vdWRadius": 1.79,
             "valency": 10,
             "mass": 106
           },
           "Ag": {
             "symbol": "Ag",
             "name": "Silver",
             "atomicNumber": 47,
             "addH": true,
             "color": "#C0C0C0",
             "covalentRadius": 1.45,
             "vdWRadius": 1.75,
             "valency": 11,
             "mass": 108
           },
           "Cd": {
             "symbol": "Cd",
             "name": "Cadmium",
             "atomicNumber": 48,
             "addH": true,
             "color": "#FFD98F",
             "covalentRadius": 1.44,
             "vdWRadius": 1.71,
             "valency": 12,
             "mass": 112
           },
           "In": {
             "symbol": "In",
             "name": "Indium",
             "atomicNumber": 49,
             "addH": true,
             "color": "#A67573",
             "covalentRadius": 1.42,
             "vdWRadius": 1.66,
             "valency": 13,
             "mass": 115
           },
           "Sn": {
             "symbol": "Sn",
             "name": "Tin",
             "atomicNumber": 50,
             "addH": true,
             "color": "#668080",
             "covalentRadius": 1.39,
             "vdWRadius": 1.62,
             "valency": 14,
             "mass": 119
           },
           "Sb": {
             "symbol": "Sb",
             "name": "Antimony",
             "atomicNumber": 51,
             "addH": true,
             "color": "#9E63B5",
             "covalentRadius": 1.39,
             "vdWRadius": 1.59,
             "valency": 15,
             "mass": 122
           },
           "Te": {
             "symbol": "Te",
             "name": "Tellurium",
             "atomicNumber": 52,
             "addH": true,
             "color": "#D47A00",
             "covalentRadius": 1.38,
             "vdWRadius": 1.57,
             "valency": 16,
             "mass": 128
           },
           "I": {
             "symbol": "I",
             "name": "Iodine",
             "atomicNumber": 53,
             "addH": true,
             "color": "#940094",
             "covalentRadius": 1.39,
             "vdWRadius": 1.56,
             "valency": 17,
             "mass": 127
           },
           "Xe": {
             "symbol": "Xe",
             "name": "Xenon",
             "atomicNumber": 54,
             "addH": false,
             "color": "#429EB0",
             "covalentRadius": 1.4,
             "vdWRadius": 2.16,
             "valency": 18,
             "mass": 131
           },
           "Cs": {
             "symbol": "Cs",
             "name": "Cesium",
             "atomicNumber": 55,
             "addH": true,
             "color": "#57178F",
             "covalentRadius": 2.44,
             "vdWRadius": 3.43,
             "valency": 1,
             "mass": 133
           },
           "Ba": {
             "symbol": "Ba",
             "name": "Barium",
             "atomicNumber": 56,
             "addH": true,
             "color": "#00C900",
             "covalentRadius": 2.15,
             "vdWRadius": 2.68,
             "valency": 2,
             "mass": 137
           },
           "La": {
             "symbol": "La",
             "name": "Lanthanum",
             "atomicNumber": 57,
             "addH": true,
             "color": "#70D4FF",
             "covalentRadius": 2.07,
             "vdWRadius": 2.57,
             "valency": 3,
             "mass": 139
           },
           "Ce": {
             "symbol": "Ce",
             "name": "Cerium",
             "atomicNumber": 58,
             "addH": true,
             "color": "#FFFFC7",
             "covalentRadius": 2.04,
             "vdWRadius": 2.58,
             "valency": 4,
             "mass": 140
           },
           "Pr": {
             "symbol": "Pr",
             "name": "Praseodymium",
             "atomicNumber": 59,
             "addH": true,
             "color": "#D9FFC7",
             "covalentRadius": 2.03,
             "vdWRadius": 2.47,
             "valency": 3,
             "mass": 141
           },
           "Nd": {
             "symbol": "Nd",
             "name": "Neodymium",
             "atomicNumber": 60,
             "addH": true,
             "color": "#C7FFC7",
             "covalentRadius": 2.01,
             "vdWRadius": 2.49,
             "valency": 3,
             "mass": 144
           },
           "Pm": {
             "symbol": "Pm",
             "name": "Promethium",
             "atomicNumber": 61,
             "addH": true,
             "color": "#A3FFC7",
             "covalentRadius": 1.99,
             "vdWRadius": 2.43,
             "valency": 3,
             "mass": 145
           },
           "Sm": {
             "symbol": "Sm",
             "name": "Samarium",
             "atomicNumber": 62,
             "addH": true,
             "color": "#8FFFC7",
             "covalentRadius": 1.98,
             "vdWRadius": 2.46,
             "valency": 3,
             "mass": 150
           },
           "Eu": {
             "symbol": "Eu",
             "name": "Europium",
             "atomicNumber": 63,
             "addH": true,
             "color": "#61FFC7",
             "covalentRadius": 1.98,
             "vdWRadius": 2.4,
             "valency": 3,
             "mass": 152
           },
           "Gd": {
             "symbol": "Gd",
             "name": "Gadolinium",
             "atomicNumber": 64,
             "addH": true,
             "color": "#45FFC7",
             "covalentRadius": 1.96,
             "vdWRadius": 2.38,
             "valency": 3,
             "mass": 157
           },
           "Tb": {
             "symbol": "Tb",
             "name": "Terbium",
             "atomicNumber": 65,
             "addH": true,
             "color": "#30FFC7",
             "covalentRadius": 1.94,
             "vdWRadius": 2.33,
             "valency": 3,
             "mass": 159
           },
           "Dy": {
             "symbol": "Dy",
             "name": "Dysprosium",
             "atomicNumber": 66,
             "addH": true,
             "color": "#1FFFC7",
             "covalentRadius": 1.92,
             "vdWRadius": 2.31,
             "valency": 3,
             "mass": 163
           },
           "Ho": {
             "symbol": "Ho",
             "name": "Holmium",
             "atomicNumber": 67,
             "addH": true,
             "color": "#00FF9C",
             "covalentRadius": 1.92,
             "vdWRadius": 2.33,
             "valency": 3,
             "mass": 165
           },
           "Er": {
             "symbol": "Er",
             "name": "Erbium",
             "atomicNumber": 68,
             "addH": true,
             "color": "#00E675",
             "covalentRadius": 1.89,
             "vdWRadius": 2.31,
             "valency": 3,
             "mass": 167
           },
           "Tm": {
             "symbol": "Tm",
             "name": "Thulium",
             "atomicNumber": 69,
             "addH": true,
             "color": "#00D452",
             "covalentRadius": 1.9,
             "vdWRadius": 2.33,
             "valency": 3,
             "mass": 169
           },
           "Yb": {
             "symbol": "Yb",
             "name": "Ytterbium",
             "atomicNumber": 70,
             "addH": true,
             "color": "#00BF38",
             "covalentRadius": 1.87,
             "vdWRadius": 2.32,
             "valency": 3,
             "mass": 173
           },
           "Lu": {
             "symbol": "Lu",
             "name": "Lutetium",
             "atomicNumber": 71,
             "addH": true,
             "color": "#00AB24",
             "covalentRadius": 1.87,
             "vdWRadius": 2.25,
             "valency": 3,
             "mass": 175
           },
           "Hf": {
             "symbol": "Hf",
             "name": "Hafnium",
             "atomicNumber": 72,
             "addH": true,
             "color": "#4DC2FF",
             "covalentRadius": 1.75,
             "vdWRadius": 2.16,
             "valency": 4,
             "mass": 178
           },
           "Ta": {
             "symbol": "Ta",
             "name": "Tantalum",
             "atomicNumber": 73,
             "addH": true,
             "color": "#4DA6FF",
             "covalentRadius": 1.7,
             "vdWRadius": 2.09,
             "valency": 5,
             "mass": 181
           },
           "W": {
             "symbol": "W",
             "name": "Tungsten",
             "atomicNumber": 74,
             "addH": true,
             "color": "#2194D6",
             "covalentRadius": 1.62,
             "vdWRadius": 2.02,
             "valency": 6,
             "mass": 184
           },
           "Re": {
             "symbol": "Re",
             "name": "Rhenium",
             "atomicNumber": 75,
             "addH": true,
             "color": "#267DAB",
             "covalentRadius": 1.51,
             "vdWRadius": 1.96,
             "valency": 7,
             "mass": 186
           },
           "Os": {
             "symbol": "Os",
             "name": "Osmium",
             "atomicNumber": 76,
             "addH": true,
             "color": "#266696",
             "covalentRadius": 1.44,
             "vdWRadius": 1.9,
             "valency": 8,
             "mass": 190
           },
           "Ir": {
             "symbol": "Ir",
             "name": "Iridium",
             "atomicNumber": 77,
             "addH": true,
             "color": "#175487",
             "covalentRadius": 1.41,
             "vdWRadius": 1.83,
             "valency": 9,
             "mass": 192
           },
           "Pt": {
             "symbol": "Pt",
             "name": "Platinum",
             "atomicNumber": 78,
             "addH": true,
             "color": "#D0D0E0",
             "covalentRadius": 1.36,
             "vdWRadius": 1.79,
             "valency": 10,
             "mass": 195
           },
           "Au": {
             "symbol": "Au",
             "name": "Gold",
             "atomicNumber": 79,
             "addH": true,
             "color": "#FFD123",
             "covalentRadius": 1.36,
             "vdWRadius": 1.75,
             "valency": 11,
             "mass": 197
           },
           "Hg": {
             "symbol": "Hg",
             "name": "Mercury",
             "atomicNumber": 80,
             "addH": true,
             "color": "#B8B8D0",
             "covalentRadius": 1.32,
             "vdWRadius": 1.71,
             "valency": 12,
             "mass": 201
           },
           "Tl": {
             "symbol": "Tl",
             "name": "Thallium",
             "atomicNumber": 81,
             "addH": true,
             "color": "#A6544D",
             "covalentRadius": 1.45,
             "vdWRadius": 1.56,
             "valency": 13,
             "mass": 204
           },
           "Pb": {
             "symbol": "Pb",
             "name": "Lead",
             "atomicNumber": 82,
             "addH": true,
             "color": "#575961",
             "covalentRadius": 1.46,
             "vdWRadius": 1.54,
             "valency": 14,
             "mass": 207
           },
           "Bi": {
             "symbol": "Bi",
             "name": "Bismuth",
             "atomicNumber": 83,
             "addH": true,
             "color": "#9E4FB5",
             "covalentRadius": 1.48,
             "vdWRadius": 1.51,
             "valency": 15,
             "mass": 208
           },
           "Po": {
             "symbol": "Po",
             "name": "Polonium",
             "atomicNumber": 84,
             "addH": true,
             "color": "#AB5C00",
             "covalentRadius": 1.4,
             "vdWRadius": 1.5,
             "valency": 16,
             "mass": 209
           },
           "At": {
             "symbol": "At",
             "name": "Astatine",
             "atomicNumber": 85,
             "addH": true,
             "color": "#754F45",
             "covalentRadius": 1.5,
             "vdWRadius": 1.62,
             "valency": 17,
             "mass": 210
           },
           "Rn": {
             "symbol": "Rn",
             "name": "Radon",
             "atomicNumber": 86,
             "addH": false,
             "color": "#428296",
             "covalentRadius": 1.5,
             "vdWRadius": 2.2,
             "valency": 18,
             "mass": 222
           },
           "Fr": {
             "symbol": "Fr",
             "name": "Francium",
             "atomicNumber": 87,
             "addH": true,
             "color": "#420066",
             "covalentRadius": 2.6,
             "vdWRadius": 3.48,
             "valency": 1,
             "mass": 223
           },
           "Ra": {
             "symbol": "Ra",
             "name": "Radium",
             "atomicNumber": 88,
             "addH": true,
             "color": "#007D00",
             "covalentRadius": 2.21,
             "vdWRadius": 2.83,
             "valency": 2,
             "mass": 226
           },
           "Ac": {
             "symbol": "Ac",
             "name": "Actinium",
             "atomicNumber": 89,
             "addH": true,
             "color": "#70ABFA",
             "covalentRadius": 2.15,
             "vdWRadius": 2.835,
             "valency": 3,
             "mass": 227
           },
           "Th": {
             "symbol": "Th",
             "name": "Thorium",
             "atomicNumber": 90,
             "addH": true,
             "color": "#00BAFF",
             "covalentRadius": 2.06,
             "vdWRadius": 2.81,
             "valency": 4,
             "mass": 232
           },
           "Pa": {
             "symbol": "Pa",
             "name": "Protactinium",
             "atomicNumber": 91,
             "addH": true,
             "color": "#00A1FF",
             "covalentRadius": 2,
             "vdWRadius": 2.82,
             "valency": 5,
             "mass": 231
           },
           "U": {
             "symbol": "U",
             "name": "Uranium",
             "atomicNumber": 92,
             "addH": true,
             "color": "#008FFF",
             "covalentRadius": 1.96,
             "vdWRadius": 2.82,
             "valency": 6,
             "mass": 238
           },
           "Np": {
             "symbol": "Np",
             "name": "Neptunium",
             "atomicNumber": 93,
             "addH": true,
             "color": "#0080FF",
             "covalentRadius": 1.9,
             "vdWRadius": 2.81,
             "valency": 7,
             "mass": 237
           },
           "Pu": {
             "symbol": "Pu",
             "name": "Plutonium",
             "atomicNumber": 94,
             "addH": true,
             "color": "#006BFF",
             "covalentRadius": 1.87,
             "vdWRadius": 2.84,
             "valency": 8,
             "mass": 244
           },
           "Am": {
             "symbol": "Am",
             "name": "Americium",
             "atomicNumber": 95,
             "addH": true,
             "color": "#545CF2",
             "covalentRadius": 1.8,
             "vdWRadius": 2.83,
             "valency": 3,
             "mass": 243
           },
           "Cm": {
             "symbol": "Cm",
             "name": "Curium",
             "atomicNumber": 96,
             "addH": true,
             "color": "#785CE3",
             "covalentRadius": 1.69,
             "vdWRadius": 2.8,
             "valency": 3,
             "mass": 247
           },
           "Bk": {
             "symbol": "Bk",
             "name": "Berkelium",
             "atomicNumber": 97,
             "addH": true,
             "color": "#8A4FE3",
             "covalentRadius": 1.69,
             "vdWRadius": 2.8,
             "valency": 3,
             "mass": 247
           },
           "Cf": {
             "symbol": "Cf",
             "name": "Californium",
             "atomicNumber": 98,
             "addH": true,
             "color": "#A136D4",
             "covalentRadius": 1.68,
             "vdWRadius": 2.8,
             "valency": 3,
             "mass": 251
           },
           "Es": {
             "symbol": "Es",
             "name": "Einsteinium",
             "atomicNumber": 99,
             "addH": true,
             "color": "#B31FD4",
             "covalentRadius": 1.65,
             "vdWRadius": 2.8,
             "valency": 3,
             "mass": 252
           },
           "Fm": {
             "symbol": "Fm",
             "name": "Fermium",
             "atomicNumber": 100,
             "addH": true,
             "color": "#B31FBA",
             "covalentRadius": 1.67,
             "vdWRadius": 2.8,
             "valency": 3,
             "mass": 257
           },
           "Md": {
             "symbol": "Md",
             "name": "Mendelevium",
             "atomicNumber": 101,
             "addH": true,
             "color": "#B30DA6",
             "covalentRadius": 1.73,
             "vdWRadius": 2.8,
             "valency": 3,
             "mass": 258
           },
           "No": {
             "symbol": "No",
             "name": "Nobelium",
             "atomicNumber": 102,
             "addH": true,
             "color": "#BD0D87",
             "covalentRadius": 1.76,
             "vdWRadius": 2.8,
             "valency": 3,
             "mass": 259
           },
           "Lr": {
             "symbol": "Lr",
             "name": "Lawrencium",
             "atomicNumber": 103,
             "addH": true,
             "color": "#C70066",
             "covalentRadius": 1.61,
             "vdWRadius": 2.7,
             "valency": 3,
             "mass": 262
           },
           "Rf": {
             "symbol": "Rf",
             "name": "Rutherfordium",
             "atomicNumber": 104,
             "addH": true,
             "color": "#CC0059",
             "covalentRadius": 1.57,
             "vdWRadius": 2.5,
             "valency": 4,
             "mass": 267
           },
           "Db": {
             "symbol": "Db",
             "name": "Dubnium",
             "atomicNumber": 105,
             "addH": true,
             "color": "#D1004F",
             "covalentRadius": 1.49,
             "vdWRadius": 2.4,
             "valency": 5,
             "mass": 270
           },
           "Sg": {
             "symbol": "Sg",
             "name": "Seaborgium",
             "atomicNumber": 106,
             "addH": true,
             "color": "#D90045",
             "covalentRadius": 1.43,
             "vdWRadius": 2.3,
             "valency": 6,
             "mass": 271
           },
           "Bh": {
             "symbol": "Bh",
             "name": "Bohrium",
             "atomicNumber": 107,
             "addH": true,
             "color": "#E00038",
             "covalentRadius": 1.41,
             "vdWRadius": 2.25,
             "valency": 7,
             "mass": 270
           },
           "Hs": {
             "symbol": "Hs",
             "name": "Hassium",
             "atomicNumber": 108,
             "addH": true,
             "color": "#E6002E",
             "covalentRadius": 1.34,
             "vdWRadius": 2.2,
             "valency": 8,
             "mass": 277
           },
           "Mt": {
             "symbol": "Mt",
             "name": "Meitnerium",
             "atomicNumber": 109,
             "addH": true,
             "color": "#EB0026",
             "covalentRadius": 1.29,
             "vdWRadius": 2.1,
             "valency": 9,
             "mass": 278
           },
           "Ds": {
             "symbol": "Ds",
             "name": "Darmstadtium",
             "atomicNumber": 110,
             "addH": true,
             "color": "#EE0026",
             "covalentRadius": 1.28,
             "vdWRadius": 2.1,
             "valency": 10,
             "mass": 281
           },
           "Rg": {
             "symbol": "Rg",
             "name": "Roentgenium",
             "atomicNumber": 111,
             "addH": true,
             "color": "#F10014",
             "covalentRadius": 1.21,
             "vdWRadius": 2.05,
             "valency": 11,
             "mass": 282
           },
           "Cn": {
             "symbol": "Cn",
             "name": "Copernicium",
             "atomicNumber": 112,
             "addH": true,
             "color": "#F60002",
             "covalentRadius": 1.22,
             "vdWRadius": 2,
             "valency": 12,
             "mass": 285
           },
           "Nh": {
             "symbol": "Nh",
             "name": "Nihonium",
             "atomicNumber": 113,
             "addH": true,
             "color": "#FF4F00",
             "covalentRadius": 1.36,
             "vdWRadius": 2,
             "valency": 13,
             "mass": 286
           },
           "Fl": {
             "symbol": "Fl",
             "name": "Flerovium",
             "atomicNumber": 114,
             "addH": true,
             "color": "#FF7000",
             "covalentRadius": 1.42,
             "vdWRadius": 2,
             "valency": 14,
             "mass": 289
           },
           "Mc": {
             "symbol": "Mc",
             "name": "Moscovium",
             "atomicNumber": 115,
             "addH": true,
             "color": "#FF8C00",
             "covalentRadius": 1.47,
             "vdWRadius": 2,
             "valency": 15,
             "mass": 290
           },
           "Lv": {
             "symbol": "Lv",
             "name": "Livermorium",
             "atomicNumber": 116,
             "addH": true,
             "color": "#FFA100",
             "covalentRadius": 1.6,
             "vdWRadius": 2,
             "valency": 16,
             "mass": 293
           },
           "Ts": {
             "symbol": "Ts",
             "name": "Tennessine",
             "atomicNumber": 117,
             "addH": true,
             "color": "#FFBA00",
             "covalentRadius": 1.6,
             "vdWRadius": 2,
             "valency": 17,
             "mass": 294
           },
           "Og": {
             "symbol": "Og",
             "name": "Oganesson",
             "atomicNumber": 118,
             "addH": true,
             "color": "#FFD100",
             "covalentRadius": 1.6,
             "vdWRadius": 2,
             "valency": 18,
             "mass": 294
           }
       }
       if (typeSymbol === '') {
           return ''
       }
       return data[typeSymbol][item]
   }



}
