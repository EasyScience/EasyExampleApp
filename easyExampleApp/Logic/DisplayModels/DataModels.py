__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from random import random

from PySide2.QtCore import QPointF
from PySide2.QtCharts import QtCharts


class MeasuredDataModel:
    def __init__(self, data_obj=None):
        self.data_obj = data_obj
        self._lowerSeriesRefs = []
        self._upperSeriesRefs = []

    def updateSeries(self):
        """
        Generates new data and updates the GUI ChartView LineSeries.
        """
        if not self._lowerSeriesRefs or not self._upperSeriesRefs:
            return

        lowerSeries = self.data_obj.get_lowerXY()
        upperSeries = self.data_obj.get_upperXY()

        for seriesRef in self._lowerSeriesRefs:
            seriesRef.replace(lowerSeries)
        for seriesRef in self._upperSeriesRefs:
            seriesRef.replace(upperSeries)

    def addLowerSeriesRef(self, seriesRef):
        """
        Sets series to be a reference to the GUI ChartView LineSeries.
        """
        self._lowerSeriesRefs.append(seriesRef)

    def addUpperSeriesRef(self, seriesRef):
        """
        Sets series to be a reference to the GUI ChartView LineSeries.
        """
        self._upperSeriesRefs.append(seriesRef)


class CalculatedDataModel:
    def __init__(self, data_obj=None):
        self._seriesRef = None
        self.data_obj = data_obj

    def updateSeries(self):
        """
        Generates new data and updates the GUI ChartView LineSeries.
        """
        if self._seriesRef is None:
            return

        series = self.data_obj.get_fit_XY()
        self._seriesRef.replace(series)

    def setSeriesRef(self, seriesRef):
        """
        Sets series to be a reference to the GUI ChartView LineSeries.
        """
        self._seriesRef = seriesRef
