// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    readonly property var expected: {
        "project": {
          "name": "Default project",
          "description": "Default project description",
          "location": "",
          "creationDate": ""
        },
        "experiment": [{
          "name": "PicoScopeB",
          "params": {
            "xMin": {
              "value": -10.0,
              "fittable": false
            },
            "xMax": {
              "value": 10.0,
              "fittable": false
            },
            "xStep": {
              "value": 0.5,
              "fittable": false
            },
            "background_min": {
              "value": 0.5,
              "error": 0,
              "min": -5,
              "max": 5,
              "unit": "",
              "fittable": true,
              "fit": true
            },
            "background_max": {
              "value": 0.75,
              "error": 0,
              "min": -5,
              "max": 5,
              "unit": "",
              "fittable": true,
              "fit": true
            }
          },
          "xArray": [-10.0, -9.5, -9.0, -8.5, -8.0, -7.5, -7.0, -6.5, -6.0, -5.5, -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0],
          "yMeasArray": [0.4837129254507315, 0.5511305798229396, 0.41456284455114933, 0.48404264986693724, 0.46515177684865777, 0.47258258654982926, 0.5205411394973696, 0.5996038595240007, 0.6847948049014249, 0.8275114082053687, 0.9688721914027683, 1.2467332925979964, 1.4355891091424966, 1.9052553513350756, 2.0959901946165154, 2.5758106867823063, 2.829717071953717, 3.1021987707609533, 3.2245171083047683, 3.379281882143549, 3.422247205771032, 3.061304664358094, 2.387075527292456, 1.9832936069129854, 1.6541342528321805, 1.3770759514849138, 1.0021038356911642, 0.8400614106099333, 0.7644074502357919, 0.843620215603888, 0.6529584639953895, 0.7008363925971165, 0.8023785047153356, 0.7177091923351727, 0.752915392377775, 0.6826688073357206, 0.7626087100465334, 0.7982855248168439, 0.6411950188151504, 0.7937908257824738, 0.8477758409785168]
        }],
        "model": [{
          "name": "GaussianA",
          "params": {
            "shift": {
              "value": 0.5,
              "error": 0,
              "min": -5,
              "max": 5,
              "unit": "",
              "fittable": true,
              "fit": true
            },
            "width": {
              "value": 0.5,
              "error": 0,
              "min": 0,
              "max": 5,
              "unit": "",
              "fittable": true,
              "fit": true
            },
            "scale": {
              "value": 1.1,
              "error": 0,
              "min": 0.1,
              "max": 5,
              "unit": "",
              "fittable": true,
              "fit": true
            }
          },
          "yCalcArray": [1.446858484343211e-48, 4.09208357362292e-44, 7.01965379286687e-40, 7.303644919538809e-36, 4.6091025139438374e-32, 1.764191979603502e-28, 4.095699433925562e-25, 5.76717422969981e-22, 4.925505685890132e-19, 2.5514751132679267e-16, 8.016496505401662e-14, 1.5276738251460423e-11, 1.765750860704173e-09, 1.2378869219118504e-07, 5.26362913134191e-06, 0.00013575078449534753, 0.0021234995498504803, 0.0201472027776076, 0.11593914701805078, 0.4046673852885866, 0.8566808613785455, 1.1, 0.8566808613785455, 0.4046673852885866, 0.11593914701805078, 0.0201472027776076, 0.0021234995498504803, 0.00013575078449534753, 5.26362913134191e-06, 1.2378869219118504e-07, 1.765750860704173e-09, 1.5276738251460423e-11, 8.016496505401662e-14, 2.5514751132679267e-16, 4.925505685890132e-19, 5.76717422969981e-22, 4.095699433925562e-25, 1.764191979603502e-28, 4.6091025139438374e-32, 7.303644919538809e-36, 7.01965379286687e-40]
        }, {
          "name": "GaussianB",
          "params": {
            "shift": {
              "value": 3.0,
              "error": 0,
              "min": -5,
              "max": 5,
              "unit": "",
              "fittable": true,
              "fit": true
            },
            "width": {
              "value": 2.0,
              "error": 0,
              "min": 0,
              "max": 5,
              "unit": "",
              "fittable": true,
              "fit": true
            },
            "scale": {
              "value": 1.5,
              "error": 0,
              "min": 0.1,
              "max": 5,
              "unit": "",
              "fittable": true,
              "fit": true
            }
          },
          "yCalcArray": [3.8802150333981184e-05, 8.608633310920312e-05, 0.00018511470613001934, 0.00038581217820099755, 0.0007793620232322577, 0.001525916765422051, 0.002895681204341564, 0.005325972835863809, 0.00949457314122862, 0.01640515126590745, 0.027473458333101268, 0.04459382457923813, 0.07015593357593847, 0.10697502404663706, 0.1580988368427965, 0.22646612768387192, 0.3144170807266467, 0.4230944275407232, 0.5518191617571635, 0.6975647822010844, 0.8546742370963845, 1.0149507692425934, 1.1682011746071073, 1.3032225843942649, 1.4091195942202137, 1.4767446555081127, 1.5, 1.4767446555081127, 1.4091195942202137, 1.3032225843942649, 1.1682011746071073, 1.0149507692425934, 0.8546742370963845, 0.6975647822010844, 0.5518191617571635, 0.4230944275407232, 0.3144170807266467, 0.22646612768387192, 0.1580988368427965, 0.10697502404663706, 0.07015593357593847]
        }]
      }

}
