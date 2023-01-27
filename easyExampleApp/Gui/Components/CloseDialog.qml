import QtQuick 2.15
import QtQuick.Controls 2.15

import easyApp.Gui.Elements 1.0 as EaElements

// SPDX-FileCopyrightText: 2022 EasyTexture contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyTexture project <https://github.com/EasyScience/EasyTextureApp>

import Gui.Globals 1.0 as ExGlobals

EaElements.Dialog {
    visible: false

    title: qsTr("Save Changes")

    EaElements.Label {
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("The project has not been saved. Do you want to exit?")
    }

    footer: EaElements.DialogButtonBox {
        EaElements.Button {
            text: qsTr("Save and exit")
            onClicked: {
                ExGlobals.Constants.proxy.project.saveProject()
                window.quit()
            }
        }

        EaElements.Button {
            text: qsTr("Exit without saving")
            onClicked: window.quit()
        }
    }
}

