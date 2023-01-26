import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Item {

    ScrollView {
        anchors.fill: parent

        EaElements.TextArea {
            text: EaLogic.Utils.prettyJson(ExGlobals.Constants.proxy.phasesDict)
            onEditingFinished: ExGlobals.Constants.proxy.phasesDict = text
        }
    }

}
