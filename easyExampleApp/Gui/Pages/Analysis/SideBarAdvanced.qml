import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Minimizer")
        collapsible: false

        EaElements.ComboBox {
            width: 200
            currentIndex: ExGlobals.Variables.proxy.minimizerIndex
            model: ExGlobals.Variables.proxy.minimizerList
            onActivated: ExGlobals.Variables.proxy.minimizerIndex = currentIndex
        }
    }

    EaElements.GroupBox {
        title: qsTr("Calculator")
        collapsible: false

        EaElements.ComboBox {
            width: 200
            currentIndex: ExGlobals.Variables.proxy.calculatorIndex
            model: ExGlobals.Variables.proxy.calculatorList
            onActivated: ExGlobals.Variables.proxy.calculatorIndex = currentIndex
            //Component.onCompleted: ExGlobals.Variables.proxy.calculatorInt = currentIndex
        }
    }

}
