// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick

import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Experiment data explorer")
        collapsible: false
        last: !Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/ExperimentDataExplorer.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Diffrn radiation")
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/DiffrnRadiation.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Pd meas 2θ range")
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/PdMeas2ThetaRange.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Pd instr resolution")
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/PdInstrResolution.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Pd instr reflex asymmetry")
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/PdInstrReflexAsymmetry.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Pd background")
        visible: Globals.Proxies.main.experiment.defined

        Loader { source: 'SideBarBasic/PdBackgroundGroup.qml' }
    }

    EaElements.GroupBox {
        title: qsTr("Phase")
        visible: Globals.Proxies.main.experiment.defined
        last: true

        Loader { source: 'SideBarBasic/Phase.qml' }
    }

}
