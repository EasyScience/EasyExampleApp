__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from typing import List

from PySide2.QtCore import QPointF
from Example1.interface import InterfaceFactory
from Example1.model import Sin, DummySin


class QtInterface():
    def __init__(self):
        self.interface = InterfaceFactory()
        self.model = Sin(interface_factory=self.interface)
        self.generator = DummySin()
        self.x = self.generator.x_data
        self.y = self.generator.y_data
        self.sy = self.generator.sy_data

    def get_XY(self) -> List[QPointF]:
        return [QPointF(x, y) for x, y in zip(self.x, self.y)]

    def get_lowerXY(self) -> List[QPointF]:
        return [QPointF(x, y - sy) for x, y, sy in zip(self.x, self.y, self.sy)]

    def get_upperXY(self) -> List[QPointF]:
        return [QPointF(x, y + sy) for x, y, sy in zip(self.x, self.y, self.sy)]

    def get_fit_XY(self):
        return [QPointF(x, y) for x, y in zip(self.x, self.y_opt)]

    def new_model(self):
        self.generator = DummySin()
        self.x = self.generator.x_data
        self.y = self.generator.y_data
        self.sy = self.generator.sy_data
