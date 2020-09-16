import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Calculator")
        collapsible: false

        EaElements.ComboBox {
            width: 200
            currentIndex: ExGlobals.Constants.proxy.calculatorIndex
            model: ExGlobals.Constants.proxy.calculatorList
            onActivated: ExGlobals.Constants.proxy.calculatorIndex = currentIndex
        }
    }

    EaElements.GroupBox {
        title: qsTr("Minimizer")
        collapsible: false

        EaElements.ComboBox {
            width: 200
            currentIndex: ExGlobals.Constants.proxy.minimizerIndex
            model: ExGlobals.Constants.proxy.minimizerList
            onActivated: ExGlobals.Constants.proxy.minimizerIndex = currentIndex
        }
    }

}
