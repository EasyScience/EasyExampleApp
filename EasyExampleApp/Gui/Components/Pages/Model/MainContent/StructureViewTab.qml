// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls
import QtQuick3D
import QtQuick3D.Helpers

import EasyApp.Gui.Animations as EaAnimations
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


View3D {
    id: view

    property real mult: 35.0
    property real mult2: 100.0 / mult
    property real mult3: mult * mult2
    property real cellCilinderThickness: 0.01
    property real axesCilinderThickness: 0.05
    property real axisConeScale: 0.2

    anchors.fill: parent

    environment: SceneEnvironment {
        backgroundMode: SceneEnvironment.Color
        clearColor: EaStyle.Colors.chartBackground
        Behavior on clearColor { EaAnimations.ThemeChange {} }
    }

    camera: perspectiveCamera

    // Node (Root scene?) (predefined cameras?)
    Node {
        id: originNode
        position: Qt.vector3d(Globals.Proxies.modelMainParameterValue('_cell_length_a', false) * mult / 2,
                              Globals.Proxies.modelMainParameterValue('_cell_length_b', false) * mult / 2,
                              Globals.Proxies.modelMainParameterValue('_cell_length_c', false) * mult / 2)  // NEED FIX: Not updated

        PerspectiveCamera {
            id: perspectiveCamera
            position: Qt.vector3d(0, 0, 600) // position translation in local coordinate
            //scale: Qt.vector3d(0.333, 0.333, 0.333)
        //    //eulerRotation.x: 90
        }
        OrthographicCamera {
            id: orthographicCamera
            //rotation: Qt.quaternion(0.7, 0, 0.7, 0)
           // position: Qt.vector3d(0, 0, 600) // position translation in local coordinate
           // scale: Qt.vector3d(0.333, 0.333, 0.333)
            //eulerRotation: Qt.vector3d(90, 0, 0)
        }

        /*
        // Stationary orthographic camera viewing from the top
        OrthographicCamera {
            id: cameraOrthographicTop
            y: 600
            eulerRotation.x: -90
        }

        // Stationary orthographic camera viewing from the front
        OrthographicCamera {
            id: cameraOrthographicFront
            z: 600
        }

        // Stationary orthographic camera viewing from left
        OrthographicCamera {
            id: cameraOrthographicLeft
            x: -600
            eulerRotation.y: -90
        }

        // Stationary perspective camera viewing from the top
        PerspectiveCamera {
            id: cameraPerspectiveTop
            y: 600
            eulerRotation.x: -90
        }

        // Stationary perspective camera viewing from the front
        PerspectiveCamera {
            id: cameraPerspectiveFront
            z: 600
        }

        // Stationary perspective camera viewing from left
        PerspectiveCamera {
            id: cameraPerspectiveLeft
            x: -600
            eulerRotation.y: -90
        }
        */

    }
    // Node

    // Rotation controller
    /*
    OrbitCameraController {
        id: cameraController

        anchors.fill: parent
        origin: originNode
        camera: orthographicCamera
    }
    */
    OrbitCameraController {

        id: cameraController

        anchors.fill: parent
        origin: originNode
        camera: view.camera

    }

    // Rotation controller

    // Light
    DirectionalLight {
        eulerRotation.x: -30
        eulerRotation.y: 30
        //ambientColor: Qt.rgba(1.0, 1.0, 1.0, 1.0)
    }
    // Light

    // Unit cell
    Repeater3D {
        id: cell
        model: Globals.Proxies.main.model.structViewCellModel
        Model {
            source: "#Cylinder"
            position: Qt.vector3d(cell.model[index].x * mult,
                                  cell.model[index].y * mult,
                                  cell.model[index].z * mult)
            eulerRotation: Qt.vector3d(cell.model[index].rotx,
                                       cell.model[index].roty,
                                       cell.model[index].rotz)
            scale: Qt.vector3d(cellCilinderThickness,
                               cell.model[index].len / mult2,
                               cellCilinderThickness)
            materials: [ DefaultMaterial { diffuseColor: "grey" } ]
        }
    }
    // Unit cell

    // Axes
    Repeater3D {
        id: axes
        model: Globals.Proxies.main.model.structViewAxesModel
        Node {
            // Main line
            Model {
                source: "#Cylinder"
                position: Qt.vector3d(axes.model[index].x * axes.model[index].len * mult,
                                      axes.model[index].y * axes.model[index].len * mult,
                                      axes.model[index].z * axes.model[index].len * mult)
                eulerRotation: Qt.vector3d(axes.model[index].rotx,
                                           axes.model[index].roty,
                                           axes.model[index].rotz)
                scale: Qt.vector3d(axesCilinderThickness,
                                   axes.model[index].len / mult2,
                                   axesCilinderThickness)
                materials: [ DefaultMaterial { diffuseColor: [EaStyle.Colors.red, EaStyle.Colors.green, EaStyle.Colors.blue][index] } ]
            }
            // Extra piece after cell end
            Model {
                source: "#Cylinder"
                position: Qt.vector3d(axes.model[index].x * 2 * (axes.model[index].len * mult + axisConeScale * mult3),
                                      axes.model[index].y * 2 * (axes.model[index].len * mult + axisConeScale * mult3),
                                      axes.model[index].z * 2 * (axes.model[index].len * mult + axisConeScale * mult3))
                eulerRotation: Qt.vector3d(axes.model[index].rotx,
                                           axes.model[index].roty,
                                           axes.model[index].rotz)
                scale: Qt.vector3d(axesCilinderThickness,
                                   axisConeScale * 2,
                                   axesCilinderThickness)
                materials: [ DefaultMaterial { diffuseColor: [EaStyle.Colors.red, EaStyle.Colors.green, EaStyle.Colors.blue][index] } ]
            }
            // Cone to get arrow
            Model {
                source: "#Cone"
                position: Qt.vector3d(axes.model[index].x * 2 * (axes.model[index].len * mult + axisConeScale * mult3 * 2),
                                      axes.model[index].y * 2 * (axes.model[index].len * mult + axisConeScale * mult3 * 2),
                                      axes.model[index].z * 2 * (axes.model[index].len * mult + axisConeScale * mult3 * 2))
                eulerRotation: Qt.vector3d(axes.model[index].rotx,
                                           axes.model[index].roty,
                                           axes.model[index].rotz)
                scale: Qt.vector3d(axisConeScale, axisConeScale, axisConeScale)
                materials: [ DefaultMaterial { diffuseColor: [EaStyle.Colors.red, EaStyle.Colors.green, EaStyle.Colors.blue][index] } ]
            }
        }
    }
    // Axes

    // Atoms
    Repeater3D {
        id: atoms

        model: Globals.Proxies.main.model.structViewAtomsModel

        Model {
            source: "#Sphere"
            position: Qt.vector3d(atoms.model[index].x * mult,
                                  atoms.model[index].y * mult,
                                  atoms.model[index].z * mult)
            scale: Qt.vector3d(atoms.model[index].diameter,
                               atoms.model[index].diameter,
                               atoms.model[index].diameter)
            materials: [ DefaultMaterial { diffuseColor: atoms.model[index].color } ]
        }
    }
    // Atoms

    // Mouse area
    MouseArea {
        anchors.fill: view
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onClicked: (mouse) => {
            if (mouse.button === Qt.LeftButton) {
                console.debug('Left mouse button clicked')
            }
            else {
                console.debug('Right mouse button clicked')
            }
            //console.error(cameraController.camera.position)
            //console.info(cameraController.camera.eulerRotation)
        }
    }
    // Mouse area

    // Tool buttons
    Row {
        anchors.top: parent.top
        anchors.right: parent.right

        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.rightMargin: EaStyle.Sizes.fontPixelSize

        spacing: 0.25 * EaStyle.Sizes.fontPixelSize

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "cube"
            ToolTip.text: qsTr("Set perspective/orthographic view")
            onClicked: {
                //console.error(view.camera)
                //console.info(perspectiveCamera)
                if (view.camera === perspectiveCamera) {
                    //console.debug(true)
                    view.camera = orthographicCamera
                } else {
                    //console.debug(false)
                    view.camera = perspectiveCamera
                }
            }
        }

        Item {
            height: 1
            width: parent.spacing
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "x"
            ToolTip.text: qsTr("View along the x axis")
//            onClicked: view.camera = cameraOrthographicTop //view.camera.rotation = Qt.quaternion(1, 0, 0, 0)
//            onClicked: view.camera.rotation = Qt.quaternion(1, 0, 0, 0)
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "y"
            ToolTip.text: qsTr("View along the y axis")
//            onClicked: view.camera = cameraOrthographicFront //view.camera.rotation = Qt.quaternion(-0.5, 0.5, 0.5, 0.5)
//            onClicked: view.camera.rotation = Qt.quaternion(0.5, -0.5, -0.5, -0.5)
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "z"
            ToolTip.text: qsTr("View along the z axis")
//            onClicked: view.camera = cameraOrthographicLeft //view.camera.rotation = Qt.quaternion(1, 0, 0, 0)
//            onClicked: view.camera.rotation = Qt.quaternion(1, 0, 0, 0)
        }

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "backspace"
            ToolTip.text: qsTr("Reset to default view")
//            onClicked: view.camera.rotation = Qt.quaternion(0.9, -0.1, -0.4, 0.0)
        }
    }
    // Tool buttons

    // Legend
    Rectangle {
        width: childrenRect.width
        height: childrenRect.height

        anchors.bottom: view.bottom
        anchors.left: view.left
        anchors.margins: EaStyle.Sizes.fontPixelSize

        color: EaStyle.Colors.mainContentBackgroundHalfTransparent
        Behavior on color { EaAnimations.ThemeChange {} }

        border {
            color: EaStyle.Colors.chartGridLine
            Behavior on color { EaAnimations.ThemeChange {} }
        }

        Column {
            leftPadding: EaStyle.Sizes.fontPixelSize
            rightPadding: EaStyle.Sizes.fontPixelSize
            topPadding: EaStyle.Sizes.fontPixelSize * 0.5
            bottomPadding: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.Label {
                text: 'x-axis'
                color: EaStyle.Colors.red
            }
            EaElements.Label {
                text: 'y-axis'
                color: EaStyle.Colors.green
            }
            EaElements.Label {
                text: 'z-axis'
                color: EaStyle.Colors.blue
            }
            /*
            EaElements.Label { text: `eulerRotation ${cameraController.camera.eulerRotation}` }
            //EaElements.Label { text: `forward ${cameraController.camera.forward}` }
            EaElements.Label { text: `pivot ${cameraController.camera.pivot}` }
            EaElements.Label { text: `position ${cameraController.camera.position}` }
            EaElements.Label { text: `rotation ${cameraController.camera.rotation}` }
            EaElements.Label { text: `scale ${cameraController.camera.scale}` }
            EaElements.Label { text: `scenePosition ${cameraController.camera.scenePosition}` }
            EaElements.Label { text: `sceneRotation ${cameraController.camera.sceneRotation}` }
            EaElements.Label { text: `sceneScale ${cameraController.camera.sceneScale}` }
            //EaElements.Label { text: `sceneTransform ${cameraController.camera.sceneTransform}` }
            */
        }
    }
    // Legend

}
// View3D
