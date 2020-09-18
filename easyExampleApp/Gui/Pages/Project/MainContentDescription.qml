import QtQuick 2.13
import QtQuick.Controls 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

Item {
    readonly property int commonSpacing: EaStyle.Sizes.fontPixelSize * 1.5

    Column {

        anchors.left: parent.left
        anchors.leftMargin: commonSpacing
        anchors.top: parent.top
        anchors.topMargin: commonSpacing * 0.5
        spacing: commonSpacing

        EaElements.Label {
            font.family: EaStyle.Fonts.secondFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
            font.weight: Font.ExtraLight
            text: "Project"
        }

        Grid {
            columns: 2
            rowSpacing: 0
            columnSpacing: commonSpacing

            EaElements.Label {
                font.bold: true
                text: "Keywords:"
            }
            EaElements.Label {
                text: "sine, cosine, lmfit, bumps"
            }

            EaElements.Label {
                font.bold: true
                text: "Samples:"
            }
            EaElements.Label {
                text: "samples.cif"
            }

            EaElements.Label {
                font.bold: true
                text: "Experiments:"
            }
            EaElements.Label {
                text: "experiments.cif"
            }

            EaElements.Label {
                font.bold: true
                text: "Calculations:"
            }
            EaElements.Label {
                text: "calculations.cif"
            }

            EaElements.Label {
                font.bold: true
                text: "Modified:"
            }
            EaElements.Label {
                text: "18.09.2020, 09:24"
            }
        }

    }

}
