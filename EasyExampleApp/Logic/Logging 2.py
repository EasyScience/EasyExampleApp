# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

# https://docs.python.org/3/library/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
# https://stackoverflow.com/questions/42936810/python-logging-module-set-formatter-dynamically
# https://doc.qt.io/qt-6/qtquick-debugging.html
# https://raymii.org/s/articles/Disable_logging_in_QT_and_QML.html

from PySide6.QtCore import QObject, Signal, Property, qDebug, QtMsgType, QLoggingCategory, QTime
import logging

#logging.basicConfig()

import inspect


LOGGER_LEVELS = {
    'error': 30,  # logging.CRITICAL, logging.ERROR, QtMsgType.QtSystemMsg, QtMsgType.QtCriticalMsg, QtMsgType.QtFatalMsg
    'info': 20,  # logging.INFO, logging.WARNING, QtMsgType.QtInfoMsg, QtMsgType.QtWarningMsg
    'debug': 10  # logging.NOTSET, logging.DEBUG, QtMsgType.QtDebugMsg
}


class Logger(QObject):
    levelChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._level = 'info'
        self.caller = None
        self.params = {}
        #self.levelChanged.connect(self.onLevelChanged)


    # QML accessible properties

    @Property(str, notify=levelChanged)
    def level(self):
        print('+++++ get', self._level)
        return self._level

    @level.setter
    def level(self, newValue):
        print('+++++ set 1', self._level, self.level, newValue)
        if self._level == newValue:
            return
        self._level = newValue
        self.levelChanged.emit()
        print('+++++ set 2', self._level, self.level, newValue)

    # ....

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

    def consoleMessage(self):
        timestamp = self.params['timestamp']
        category = self.params['category']
        level = self.params['level']
        message = self.params['message']
        funcname = self.params['funcname']
        fileurl = self.params['fileurl']
        lineno = self.params['lineno']
        return f"{timestamp} {category:>4} {level:<8}   {message:<80.80}   {funcname:<34.34} {fileurl}:{lineno} {self}"

    def printConsoleMessage(self):
        #return
        print('--------', self.level, self._level)
        #if LOGGER_LEVELS[self.level.lower()] <= LOGGER_LEVELS[self.level.lower()]:
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


class CustomLogger:

    def __init__(self):
        self.format = logging.Formatter('{asctime}.{msecs:03.0f}   PY {levelname:<8}   {message:<80.80}   {funcName:34.34} file://{pathname}:{lineno:d}',
                                    datefmt='%H:%M:%S',
                                    style='{')

        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setFormatter(self.format)

        self.console = logging.getLogger()  ## logging.getLogger('main')
        self.console.setLevel(logging.DEBUG)
        self.console.addHandler(self.consoleHandler)

    def new_logger_method(self, caller=None):
        self.info("new_logger_method() called from: {}.".format(caller))

    #
    def info(self, msg):
        #print('AAAA', msg, *args, **kwargs)
        caller = self.console.findCaller(stack_info=True, stacklevel=7)
        print('info --->', caller)
        self.console.info(msg)

    #
    def debug(self, msg):
        #print('self.getEffectiveLevel()', self.getEffectiveLevel())
        #print('self.findCaller()', self.findCaller())
        #caller = self.findCaller(stack_info=True, stacklevel=7)
        #print('debug --->', caller)
        #self.
        #numeric_level = getattr(logging, loglevel.upper(), None)
        #print('BBBB', msg, numeric_level)
        #
        #return super(CustomLogger, self).debug(msg, *args, **kwargs)
        self.console.debug(msg)



# Use this mapping. Not implemented yet.
LOGGER_LEVELS_X = {
    'Error': 3,  # logging.CRITICAL, logging.ERROR, QtMsgType.QtSystemMsg, QtMsgType.QtCriticalMsg, QtMsgType.QtFatalMsg
    'Info': 2,  # logging.INFO, logging.WARNING, QtMsgType.QtInfoMsg, QtMsgType.QtWarningMsg
    'Debug': 1  # logging.NOTSET, logging.DEBUG, QtMsgType.QtDebugMsg
}

# Python logger (*.py)

#format = logging.Formatter('{asctime}.{msecs:03.0f}   PY {levelname:<8}   {message:<80.80}   {funcName:34.34} file://{pathname}:{lineno:d}',
#                             datefmt='%H:%M:%S',
#                             style='{')

#consoleHandler = logging.StreamHandler()
#consoleHandler.setFormatter(format)

#console = logging.getLogger('main')
#console.setLevel(logging.DEBUG)
#console.addHandler(consoleHandler)
#def console():
#    pass

PY_LOGGER_LEVELS = {
    'Critical': logging.CRITICAL,   # 50
    'Error': logging.ERROR,         # 40
    'Warning': logging.WARNING,     # 30
    'Info': logging.INFO,           # 20
    'Debug': logging.DEBUG,         # 10
    'Notset': logging.NOTSET        # 0
}

# Qt logger (*.qml)

# https://doc.qt.io/qt-6/qml-qtqml-loggingcategory.html
# https://community.kde.org/Guidelines_and_HOWTOs/Debugging/Using_Error_Messages

QT_MSG_TYPES = {
    'Fatal': QtMsgType.QtFatalMsg,          # 3
    'Critical': QtMsgType.QtCriticalMsg,    # 2
    'Warning': QtMsgType.QtWarningMsg,      # 1
    'Info': QtMsgType.QtInfoMsg,            # 4
    'Debug': QtMsgType.QtDebugMsg,          # 0
    'System': QtMsgType.QtSystemMsg         # 2
}

QT_LOGGER_LEVELS = {
    'Fatal': 50,
    'System': 40,
    'Critical': 40,
    'Warning': 30,
    'Info': 20,
    'Debug': 10
}

def messageType(type):

    if type == QtMsgType.QtDebugMsg:
        return 'debug'
    elif type == QtMsgType.QtInfoMsg:
        return 'info'
    elif type == QtMsgType.QtWarningMsg:
        return 'warning'
    elif type == QtMsgType.QtCriticalMsg or type == QtMsgType.QtSystemMsg:
        return 'critical'
    elif type == QtMsgType.QtFatalMsg:
        return 'fatal'
    else:
        return ''

def contextCategory(context):
    if context.category == 'qml':
        return 'QML'
    elif context.category == 'default':
        return 'PY'
    else:
        return ''

def sourceFile(context):
    if context.file is not None:
        return context.file
    else:
        return ''

def sourceLine(context):
    if context.file is not None:
        return context.line
    else:
        return ''

def callerFunction(context):
    if context.function is not None:
        return context.function
    else:
        return ''

def timeStamp():
    return QTime.currentTime().toString("hh:mm:ss.zzz")

def messageHandler(level, context, message):
    level = LoggerX.qtMsgTypeToCustomLevel(level) #messageType(level).upper()
    fileurl = sourceFile(context)
    lineno = sourceLine(context)
    funcname = callerFunction(context)
    console.printQmlCategory(message, level, funcname, fileurl, lineno)


    #qDebug(f"{time} {category:>4} {level:<8}   {message:<80.80}   {func:<34.34} {file}:{line}")

# JS supported:
    #console.debug => QtMsgType.QtDebugMsg
    #console.info => QtMsgType.QtInfoMsg
    #console.warn => QtMsgType.QtWarningMsg
    #console.error => QtMsgType.QtCriticalMsg

# Proxy

class LoggerY(QObject):
    levelChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        ###self._level = logging.DEBUG
        self.levelChanged.connect(self.onLevelChanged)

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

    # Private methods

    def onLevelChanged(self):
        return
        # Set py logger
        console.setLevel(PY_LOGGER_LEVELS[self.level])
        # Set qt logger
        level = QT_LOGGER_LEVELS[self.level]
        rules = ''
        for key, value in QT_LOGGER_LEVELS.items():
            key = key.lower()
            if level > value:
                rules += f"*.{key}=false\n"
        print('======rules I\n', rules)
        rules = "*.debug=false\n*.info=false\n"
        rules = "*.debug=false\n"
        print('======rules II\n', rules)
        #print('isDebugEnabled()', QLoggingCategory.isDebugEnabled(1))
        #print('isInfoEnabled()', QLoggingCategory.isInfoEnabled(2))
        #print('isWarningEnabled()', QLoggingCategory.isWarningEnabled(3))
        QLoggingCategory.setFilterRules(rules)
