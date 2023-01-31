// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick 2.15


QtObject {

    readonly property var mainProxy: QtObject {

        readonly property var project: QtObject {
            property bool projectCreated: false
            property bool modelsAdded: false
            property bool experimentsLoaded: false
            property bool summaryGenerated: false
            property string currentProjectPath: '_path_'
            property var projectInfoAsJson: QtObject {
                property string name: '_name_'
                property string short_description: '_short_description_'
                property string modified: '_modified_'
            }
            property string projectExamplesAsXml:
`<root>
  <item>
    <name>PbSO4</name>
    <description>neutrons, powder, constant wavelength, D1A@ILL</description>
    <path>../Resources/Examples/PbSO4/project.json</path>
  </item>
  <item>
    <name>Co2SiO4</name>
    <description>neutrons, powder, constant wavelength, D20@ILL</description>
    <path>../Resources/Examples/Co2SiO4/project.json</path>
  </item>
  <item>
    <name>Dy3Al5O12</name>
    <description>neutrons, powder, constant wavelength, G41@LLB</description>
    <path>../Resources/Examples/Dy3Al5O12/project.json</path>
  </item>
</root>`
            function createProject() { projectCreated = true }
            function loadExampleProject(fileUrl) {}
        }

        readonly property var phase: QtObject {
            property string phasesAsXml:
`<root>
  <item>
    <name>Si3N4_alpha</name>
  </item>
  <item>
    <name>Si3N4_beta</name>
  </item>
</root>`
        }

        readonly property var experiment: QtObject {
            property string experimentDataAsXml:
`<root>
  <item>
    <name>D1A@ILL</name>
  </item>
</root>`
        }

        readonly property var statusBar: QtObject {
            property string modelAsXml:
`<root>
  <item>
    <label>Calculations</label>
    <value>CrysPy</value>
  </item>
  <item>
    <label>Minimization</label>
    <value>lmfit</value>
  </item>
</root>`
        }

        readonly property var plotting1d: QtObject {
            property var libs: ['Plotly']
            property string currentLib: 'Plotly'
        }
    }

}
