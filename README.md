# easyExampleApp

Advanced example of easyScience applications

[![CI Build][20]][21]

[![Release][30]][31]

[![Downloads][70]][71] [![Lines of code][81]](<>) [![Total lines][80]](<>) [![Files][82]](<>)

[![License][50]][51]

[![w3c][90]][91]

## Download easyExample

-   Open **Terminal**
-   Change the current working directory to the location where you want the **easyExampleApp** directory
-   Clone **easyExampleApp** repo from GitHub using **git**
        git clone <https://github.com/easyScience/easyExampleApp>

## Install easyExample dependencies

-   Open **Terminal**
-   Install [**Poetry**](https://python-poetry.org/docs/) (Python dependency manager)
    -   osx / linux / bashonwindows
            curl -sSL <https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py> | python
    -   windows powershell
            (Invoke-WebRequest -Uri <https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py> -UseBasicParsing).Content | python
-   Go to **easyExampleApp** directory
-   Create virtual environment for **easyExample** and install its dependences using **poetry** (configuration file: **pyproject.toml**)
        poetry install --no-dev

## Launch easyExample application

-   Open **Terminal**
-   Go to **easyExampleApp** directory
-   Launch **easyExample** application using **poetry**
        poetry run easyExample

## Update easyExample dependencies

-   Open **Terminal**
-   Go to **easyExampleApp** directory
-   Update **easyExample** using **poetry** (configuration file: **pyproject.toml**)
        poetry update --no-dev

## Delete easyExample

-   ...
-   Uninstall **Poetry**
    -   osx / linux / bashonwindows
            curl -sSL <https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py> | POETRY_UNINSTALL=1 python

## Test easyExample

-   Unit tests
    -   ...
-   GUI
    -   Test video: <https://easyscience.github.io/easyExampleApp>

<!---URLs--->

<!---https://naereen.github.io/badges/--->

<!---CI Build Status--->

[20]: https://github.com/easyScience/easyExampleApp/workflows/macOS,%20Linux,%20Windows/badge.svg

[21]: https://github.com/easyScience/easyExampleApp/actions

<!---Release--->

[30]: https://img.shields.io/github/release/easyScience/easyExampleApp.svg

[31]: https://github.com/easyScience/easyExampleApp/releases

<!---License--->

[50]: https://img.shields.io/github/license/easyScience/easyExampleApp.svg

[51]: https://github.com/easyScience/easyExampleApp/blob/master/LICENSE.md

<!---LicenseScan--->

[60]: https://app.fossa.com/api/projects/git%2Bgithub.com%2FeasyScience%2FeasyExampleApp.svg?type=shield

[61]: https://app.fossa.com/projects/git%2Bgithub.com%2FeasyScience%2FeasyExampleApp?ref=badge_shield

<!---Downloads--->

[70]: https://img.shields.io/github/downloads/easyScience/easyExampleApp/total.svg

[71]: https://github.com/easyScience/easyExampleApp/releases

<!---Code statistics--->

[80]: https://tokei.rs/b1/github/easyScience/easyExampleApp

[81]: https://tokei.rs/b1/github/easyScience/easyExampleApp?category=code

[82]: https://tokei.rs/b1/github/easyScience/easyExampleApp?category=files

<!---W3C validation--->

[90]: https://img.shields.io/w3c-validation/default?targetUrl=https://easyscience.github.io/easyExampleApp

[91]: https://easyscience.github.io/easyExampleApp
