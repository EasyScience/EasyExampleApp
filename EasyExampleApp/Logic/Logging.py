# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

# https://docs.python.org/3/library/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
# https://stackoverflow.com/questions/42936810/python-logging-module-set-formatter-dynamically
# https://doc.qt.io/qt-6/qtquick-debugging.html
# https://raymii.org/s/articles/Disable_logging_in_QT_and_QML.html

import inspect

from PySide6.QtCore import QObject, Signal, Property, qDebug, QtMsgType, QTime


LOGGER_LEVELS = {
    'disabled': 40,
    'error': 30,  # logging.CRITICAL, logging.ERROR, QtMsgType.QtSystemMsg, QtMsgType.QtCriticalMsg, QtMsgType.QtFatalMsg
    'info': 20,  # logging.INFO, logging.WARNING, QtMsgType.QtInfoMsg, QtMsgType.QtWarningMsg
    'debug': 10  # logging.NOTSET, logging.DEBUG, QtMsgType.QtDebugMsg
}


class Logger(QObject):
    levelChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._level = 'disabled'
        self.caller = None
        self.params = {}


    # QML accessible properties

    @Property(str, notify=levelChanged)
    def level(self):
        return self._level

    @level.setter
    def level(self, newValue):
        if self._level == newValue:
            return
        self._level = newValue
        self.levelChanged.emit()

    ###

    def setCaller(self):
        self.caller = inspect.getframeinfo(inspect.stack()[1][0])

    def setParamsQmlCategory(self, message, level, funcname, fileurl, lineno):
        self.params['category'] = 'qml'
        self.params['message'] = message
        self.params['level'] = level
        self.params['funcname'] = funcname
        self.params['fileurl'] = fileurl
        self.params['lineno'] = lineno

    def setParamsPyCategory(self, message, level, caller):
        self.params['category'] = 'py'
        self.params['message'] = message
        self.params['level'] = level
        self.params['funcname'] = caller.function
        self.params['fileurl'] = f'file://{caller.filename}'
        self.params['lineno'] = caller.lineno

    def setTimeStamp(self):
        self.params['timestamp'] = QTime.currentTime().toString("hh:mm:ss.zzz")

    def colorizeMessage(self, message):
        return message
        colors = {
            'debug': '\033[92m',
            'info': '\033[97m',
            'error': '\033[91m'
        }
        colorStart = colors[self.params['level']]
        colorEnd = '\033[0m'
        return f'{colorStart}{message}{colorEnd}'

    def consoleMessage(self):
        timestamp = self.params['timestamp']
        category = self.params['category']
        level = self.params['level']
        message = self.params['message']
        funcname = self.params['funcname']
        fileurl = self.params['fileurl']
        lineno = self.params['lineno']
        return self.colorizeMessage(f"{timestamp} {category:>4} {level:<8}   {message:<80.80}   {funcname:<34.34} {fileurl}:{lineno}")

    def printConsoleMessage(self):
        #if LOGGER_LEVELS[self.params['level'].lower()] > LOGGER_LEVELS[self.level.lower()]:
        print(self.consoleMessage())

    def printPyCategory(self, message, level, caller):
        self.setParamsPyCategory(message, level, caller)
        self.setTimeStamp()
        self.printConsoleMessage()

    def printQmlCategory(self, message, level, funcname, fileurl, lineno):
        self.setParamsQmlCategory(message, level, funcname, fileurl, lineno)
        self.setTimeStamp()
        self.printConsoleMessage()

    def info(self, message):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        self.printPyCategory(message, 'info', caller)
    #
    def debug(self, message):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        self.printPyCategory(message, 'debug', caller)

    def error(self, message):
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        self.printPyCategory(message, 'error', caller)



console = Logger()


def qtMsgTypeToCustomLevel(msgType):
    return {
        QtMsgType.QtDebugMsg: 'debug',
        QtMsgType.QtInfoMsg: 'info',
        QtMsgType.QtWarningMsg: 'info',
        QtMsgType.QtCriticalMsg: 'error',
        QtMsgType.QtSystemMsg: 'error',
        QtMsgType.QtFatalMsg: 'error'
    }[msgType]

def qtMessageHandler(msgType, context, message):
    level = qtMsgTypeToCustomLevel(msgType)
    funcname = context.function
    fileurl = context.file
    lineno = context.line
    console.printQmlCategory(message, level, funcname, fileurl, lineno)
