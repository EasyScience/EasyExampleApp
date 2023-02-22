// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick


QtObject { // If "Unknown component. (M300) in QtCreator", try: "Tools > QML/JS > Reset Code Model"

    readonly property var projectConfig: QtObject {
        readonly property var release: QtObject {
            readonly property string app_name: 'EasyExample'
            readonly property string app_issues_url: 'https://github.com/EasyScience/EasyExampleApp/issues'
        }
        readonly property var tool: QtObject {
            property var poetry: QtObject {
                readonly property string homepage: 'https://github.com/EasyScience/EasyExampleApp'
                readonly property string version: '0.0.1-alpha.1'
            }
        }
        readonly property var ci: QtObject {
            property var app: QtObject {}
        }
    }

    readonly property var appConfig: QtObject {
        readonly property string name: projectConfig.release.app_name
        readonly property string namePrefix: "Easy"
        readonly property string nameSuffix: name.replace(namePrefix, "")
        readonly property string namePrefixForLogo: namePrefix.toLowerCase()
        readonly property string nameSuffixForLogo: nameSuffix.toLowerCase()

        readonly property string icon: iconPath('App.svg')

        readonly property string version: projectConfig.tool.poetry.version

        readonly property string homePageUrl: projectConfig.tool.poetry.homepage
        readonly property string issuesUrl: projectConfig.release.app_issues_url

        readonly property bool remote: typeof projectConfig.ci.app.info !== 'undefined'

        readonly property string date: remote ?
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

        readonly property string licenseUrl: githubRawContentUrl(branch, 'LICENSE.md')
        readonly property string dependenciesUrl: githubRawContentUrl(branch, 'DEPENDENCIES.md')

        readonly property string description:
`${name} is a software for reduction of powder
diffraction data from textured materials.

${name} is a collaborative project between
the Geoscience Center of the University of Göttingen, Germany, and
the European Spallation Source ERIC, Sweden.`
        readonly property var developerIcons: [
            { url: "http://www.uni-goettingen.de/de/dr-jens-m-walter/503416.html", icon: iconPath('GAU.png'), heightScale: 2.3 },
            { url: "https://ess.eu", icon: iconPath('ESS.png'), heightScale: 3.0 }
        ]
        readonly property string developerYearsFrom: "2019"
        readonly property string developerYearsTo: "2023"
    }

    // Logic

    function iconPath(file) {
        return Qt.resolvedUrl(`../Resources/Logo/${file}`)
    }

    function githubRawContentUrl(branch, file) {
        return `https://raw.githubusercontent.com/easyScience/EasyExampleApp/${branch}/${file}`
    }
}
