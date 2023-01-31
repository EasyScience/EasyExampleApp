// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Column {
    spacing: EaStyle.Sizes.fontPixelSize

    EaComponents.TableView {

        defaultInfoText: qsTr("No Experiments Loaded")

        // Table model

        model: XmlListModel {
            xml: ExGlobals.Proxies.mainProxy.project.experimentsLoaded ?
                     ExGlobals.Proxies.mainProxy.experiment.experimentDataAsXml :
                     ""
            query: "/root/item"

            XmlRole { name: "label"; query: "name/string()" }
        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                headerText: "No."
                text: model.index + 1
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignLeft
                width: EaStyle.Sizes.fontPixelSize * 27.9
                headerText: "Label"
                text: model.label
            }

            EaComponents.TableViewLabel {
                headerText: "Color"
                //backgroundColor: model.color ? model.color : "transparent"
                backgroundColor: EaStyle.Colors.chartForegrounds[1]
            }

            EaComponents.TableViewButton {
                id: deleteRowColumn
                headerText: "Del."
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this dataset")
            }

        }

    }

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            fontIcon: "upload"
            text: qsTr("Import data from local drive")
            onClicked: ExGlobals.Proxies.mainProxy.project.experimentsLoaded = true
        }

        EaElements.SideBarButton {
            enabled: false
            fontIcon: "download"
            text: qsTr("Download data from SciCat")
        }
    }

}
