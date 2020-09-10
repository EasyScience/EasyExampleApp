from typing import List

import numpy as np
from PySide2.QtCore import QPointF

from easyTemplateLib.interface import Interface, calculators_list


class QtInterface(Interface):
    def __init__(self, model, generator):
        super().__init__(model)
        self.generator = generator
        self.x = np.linspace(0, 10, 100)
        self.y = self.generator(self.x)
        self.sy = np.random.normal(1.5, 0.0, self.x.shape) * 0.3
        self.calculator = 'scipy'
        self.calculatorList = [calc.name for calc in calculators_list]

    def get_XY(self) -> List[QPointF]:
        return [QPointF(x, y) for x, y in zip(self.x, self.y)]

    def get_lowerXY(self) -> List[QPointF]:
        return [QPointF(x, y - sy) for x, y, sy in zip(self.x, self.y, self.sy)]

    def get_upperXY(self) -> List[QPointF]:
        return [QPointF(x, y + sy) for x, y, sy in zip(self.x, self.y, self.sy)]

    def get_fit_XY(self):
        return [QPointF(x, y) for x, y in zip(self.x, self.y_opt)]

    def new_model(self):
        self.y = self.generator(self.x)

    def update_model(self):
        self.y_opt = self.model.func(self.x)

    def set_parameter(self, parm, value):
        super().set_parameter(parm, value)
        self.update_model()



