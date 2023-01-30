// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick 2.15


QtObject {

    property var proxy: QtObject {
        property var project: QtObject {
            property bool projectCreated: false
            property string currentProjectPath: '_path_'
            property var projectInfoAsJson: QtObject {
                property string name: '_name_'
                property string short_description: '_short_description_'
                property string modified: '_modified_'
            }
            property string statusModelAsXml:
`<root>
   <item>
     <label>Minimization</label>
     <value>lmfit</value>
   </item>
</root>`
            function createProject() { projectCreated = true }
        }
        property var plotting1d: QtObject {
            property var libs: ['Plotly']
            property string currentLib: 'Plotly'
        }
    }

    property var projectConfig: QtObject {
        property var release: QtObject {
            property string app_name: 'EasyExample'
            property string app_issues_url: 'https://github.com/EasyScience/EasyExampleApp/issues'
        }
        property var tool: QtObject {
            property var poetry: QtObject {
                property string homepage: 'https://github.com/EasyScience/EasyExampleApp'
                property string version: '0.0.1-alpha.1'
            }
        }
        property var ci: QtObject {
            property var app: QtObject {}
        }
    }

    readonly property bool remote: typeof projectConfig.ci.app.info !== 'undefined'

    readonly property string appName: projectConfig.release.app_name
    readonly property string appPrefixName: "Easy"
    readonly property string appSuffixName: appName.replace(appPrefixName, "")
    readonly property string appPrefixNameLogo: appPrefixName.toLowerCase()
    readonly property string appSuffixNameLogo: appSuffixName.toLowerCase()
    readonly property string appLogo: logo('App.svg')
    readonly property string appUrl: projectConfig.tool.poetry.homepage
    readonly property string appIssuesUrl: projectConfig.release.app_issues_url
    readonly property string appVersion: projectConfig.tool.poetry.version
    readonly property string appDate: remote ?
                                          projectConfig.ci.app.info.build_date :
                                          new Date().toISOString().slice(0,10)

    readonly property string commit: remote ?
                                         projectConfig.ci.app.info.commit_sha_short :
                                         ''
    readonly property string commitUrl: remote ?
                                           projectConfig.ci.app.info.commit_url :
                                           ''
    readonly property string branch: remote ?
                                         projectConfig.ci.app.info.branch_name :
                                         ''
    readonly property string branchUrl: remote ?
                                            projectConfig.ci.app.info.branch_url :
                                            ''

    readonly property string eulaUrl: githubRawContent(branch, 'LICENSE.md')
    readonly property string oslUrl: githubRawContent(branch, 'DEPENDENCIES.md')

    readonly property string description: // diffraction texture data sets
`${appName} is a software for reduction of powder
diffraction data from textured materials.

${appName} is a collaborative project between
the Geoscience Center of the University of Göttingen, Germany, and
the European Spallation Source ERIC, Sweden.`

    readonly property string essLogo: logo('ESSlogo.png')

    // Logic

    function logo(file) {
        return Qt.resolvedUrl(`../Resources/Logo/${file}`)
    }

    function githubRawContent(branch, file) {
        return `https://raw.githubusercontent.com/easyScience/EasyExampleApp/${branch}/${file}`
    }
}
