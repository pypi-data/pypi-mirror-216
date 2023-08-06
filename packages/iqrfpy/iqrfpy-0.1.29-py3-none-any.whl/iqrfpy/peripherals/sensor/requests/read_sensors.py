from typing import List, Optional, Union
from iqrfpy.enums.commands import SensorRequestCommands
from iqrfpy.enums.peripherals import Standards
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest
from iqrfpy.peripherals.sensor.requests.sensor_written_data import SensorWrittenData

__all__ = [
    'ReadSensorsRequest',
]


class ReadSensorsRequest(IRequest):

    __slots__ = '_sensors', '_written_data'

    def __init__(self, nadr: int, sensors: Optional[List[int]] = None,
                 written_data: Optional[List[SensorWrittenData]] = None, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(sensors)
        super().__init__(
            nadr=nadr,
            pnum=Standards.SENSOR,
            pcmd=SensorRequestCommands.READ_SENSORS,
            m_type=None,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._sensors = sensors
        self._written_data = written_data

    @staticmethod
    def _validate(sensors: Optional[List[int]] = None):
        if sensors is not None:
            if len(sensors) > 32:
                raise RequestParameterInvalidValueError('Sensors length should be at most 32 bytes.')
            if len(sensors) == 0:
                return
            if min(sensors) < 0 or max(sensors) > 31:
                raise RequestParameterInvalidValueError('Sensors values should be between 0 and 31.')

    @property
    def sensors(self):
        return self._sensors

    @sensors.setter
    def sensors(self, value: Optional[List[int]]):
        self._validate(value)
        self._sensors = value

    @property
    def written_data(self):
        return self._written_data

    @written_data.setter
    def written_data(self, value: List[SensorWrittenData]):
        self._written_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        if self._sensors is not None:
            written_data = []
            if self._written_data is not None:
                for data in self._written_data:
                    written_data += data.to_pdata()
            self._pdata = Common.sensors_indexes_to_bitmap(self._sensors) + written_data
        else:
            self._pdata = None
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        raise NotImplementedError('JSON API request not implemented.')
