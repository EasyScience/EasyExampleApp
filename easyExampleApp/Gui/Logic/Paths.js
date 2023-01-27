// SPDX-FileCopyrightText: 2022 EasyTexture contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyTexture project <https://github.com/EasyScience/EasyTextureApp>

function component(fileName)
{
    const dirPath = Qt.resolvedUrl("../Components")
    const filePath = dirPath + "/" + fileName
    return filePath
}
