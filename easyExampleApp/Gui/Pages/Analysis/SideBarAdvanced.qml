import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyAppGui.Style 1.0 as EaStyle
import easyAppGui.Elements 1.0 as EaElements
import easyAppGui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Calculator")
        collapsed: false

        EaElements.ComboBox {
            width: 200
            currentIndex: ExGlobals.Constants.proxy.calculatorIndex
            model: ExGlobals.Constants.proxy.calculatorList
            onActivated: ExGlobals.Constants.proxy.calculatorIndex = currentIndex
        }
    }

    EaElements.GroupBox {
        title: qsTr("Minimizer")
        collapsed: false

        EaElements.ComboBox {
            width: 200
            currentIndex: ExGlobals.Constants.proxy.minimizerIndex
            model: ExGlobals.Constants.proxy.minimizerList
            onActivated: ExGlobals.Constants.proxy.minimizerIndex = currentIndex
        }
    }

    EaElements.GroupBox {
        title: qsTr("Constraints")
        visible: ExGlobals.Variables.analysisPageEnabled
        collapsed: false

        EaComponents.ConstraintsView {}

        Grid {
            columns: 5
            columnSpacing: 10
            rowSpacing: 10
            verticalItemAlignment: Grid.AlignVCenter

            EaElements.ComboBox {
                id: dependentPar
                width: 137
                currentIndex: -1
                displayText: currentIndex === -1 ? "Select parameter" : currentText
                model: XmlListModel {
                    xml: ExGlobals.Constants.proxy.fitablesListAsXml
                    query: "/root/item"
                    XmlRole { name: "label"; query: "label/string()" }
                }
            }

            EaElements.ComboBox {
                id: relationalOperator
                width: 50
                currentIndex: 0
                //model: ["=", ">", "<"]
                //font.pixelSize: EaStyle.Sizes.fontPixelSize * 1.25
                font.family: EaStyle.Fonts.iconsFamily
                model: XmlListModel {
                    xml: "<root><item><operator>=</operator><icon>\uf52c</icon></item><item><operator>&gt;</operator><icon>\uf531</icon></item><item><operator>&lt;</operator><icon>\uf536</icon></item></root>"
                    query: "/root/item"
                    XmlRole { name: "icon"; query: "icon/string()" }
                }
            }

            EaElements.TextField {
                id: value
                width: 61
                horizontalAlignment: Text.AlignRight
                text: "1.0000"
            }

            EaElements.ComboBox {
                id: arithmeticOperator
                width: 50
                currentIndex: 0
                //model: ["", "*", "/", "+", "-"]
                //font.pixelSize: EaStyle.Sizes.fontPixelSize * 1.25
                font.family: EaStyle.Fonts.iconsFamily
                //model: ["\uf00d", "\uf529", "\uf067", "\uf068"]
                model: XmlListModel {
                    xml: "<root><item><operator></operator><icon></icon></item><item><operator>*</operator><icon>\uf00d</icon></item><item><operator>/</operator><icon>\uf529</icon></item><item><operator>+</operator><icon>\uf067</icon></item><item><operator>-</operator><icon>\uf068</icon></item></root>"
                    query: "/root/item"
                    XmlRole { name: "icon"; query: "icon/string()" }
                }
            }

            EaElements.ComboBox {
                id: independentPar
                width: dependentPar.width
                currentIndex: 0
                model: XmlListModel {
                    xml: ExGlobals.Constants.proxy.fitablesListAsXml.replace("<root>", "<root><item><label></label></item>")
                    query: "/root/item"
                    XmlRole { name: "label"; query: "label/string()" }
                    onXmlChanged: {
                        //print("1 onXmlChanged", independentPar.currentIndex)
                        independentPar.currentIndex = 0
                        //print("2 onXmlChanged", independentPar.currentIndex)
                    }
                }
                onCurrentIndexChanged: {
                    if (independentPar.currentIndex === -1 && model.count > 0)
                        independentPar.currentIndex = 0
                }
            }
        }

        EaElements.SideBarButton {
            id: addConstraint
            fontIcon: "plus-circle"
            text: qsTr("Add constraint")
            onClicked: {
                ExGlobals.Constants.proxy.addConstraint(
                           dependentPar.currentIndex,
                           relationalOperator.currentText.replace("\uf52c", "=").replace("\uf531", ">").replace("\uf536", "<"),
                           value.text,
                           arithmeticOperator.currentText.replace("\uf00d", "*").replace("\uf529", "/").replace("\uf067", "+").replace("\uf068", "-"),
                           independentPar.currentIndex - 1
                           )
            }
        }
    }

}
