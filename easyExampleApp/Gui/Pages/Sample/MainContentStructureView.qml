import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Globals 1.0 as EaGlobals
import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

Rectangle {
    visible: ExGlobals.Variables.experimentPageEnabled

    color: EaStyle.Colors.mainContentBackground

    Rectangle {
        anchors.centerIn: parent

        height: ExGlobals.Constants.proxy.amplitude * 80
        width: ExGlobals.Constants.proxy.period * 80

        opacity: 0.8
        color: "coral"
        border.width: 1
        border.color: Qt.darker("coral", 1.5)

        Behavior on height {
            NumberAnimation { duration: 500; easing.type: Easing.InOutQuad }
        }
        Behavior on width {
            NumberAnimation { duration: 500; easing.type: Easing.InOutQuad }
        }

        EaElements.Label {
            x: -height
            y: (parent.height + width) / 2
            transform: Rotation { origin.x: 0; origin.y: 0; angle: -90}
            text: "Amplitude = " + (parent.height / 80).toFixed(2)
        }
        EaElements.Label {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.bottom
            text: "Period = " + (parent.width / 80).toFixed(2)
        }
    }

}
