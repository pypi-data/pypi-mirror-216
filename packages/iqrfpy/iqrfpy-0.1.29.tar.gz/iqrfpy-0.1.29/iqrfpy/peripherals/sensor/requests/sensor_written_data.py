from typing import List
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants


class SensorWrittenData:

    __slots__ = '_index', '_data'

    def __init__(self, index: int, data: List[int]):
        self._validate(index=index, data=data)
        self._index = index
        self._data = data

    def _validate(self, index: int, data: List[int]):
        self._validate_index(index)
        self._validate_data(data)

    @staticmethod
    def _validate_index(index: int):
        if not (dpa_constants.SENSOR_INDEX_MIN <= index <= dpa_constants.SENSOR_INDEX_MAX):
            raise RequestParameterInvalidValueError('Index value should be between 0 and 31.')

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value: int):
        self._validate_index(value)
        self._index = value

    @staticmethod
    def _validate_data(data: List[int]):
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Data values should be between 0 and 255.')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: List[int]):
        self._validate_data(value)
        self._data = value

    def to_pdata(self):
        return [self.index] + self.data
