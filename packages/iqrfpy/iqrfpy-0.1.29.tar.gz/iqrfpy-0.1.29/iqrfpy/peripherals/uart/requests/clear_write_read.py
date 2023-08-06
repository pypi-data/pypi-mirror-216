from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import UartRequestCommands
from iqrfpy.enums.message_types import UartMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.irequest import IRequest

__all__ = ['ClearWriteReadRequest']


class ClearWriteReadRequest(IRequest):

    __slots__ = '_read_timeout', '_data'

    def __init__(self, nadr: int, read_timeout: int, data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(read_timeout=read_timeout, data=data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.UART,
            pcmd=UartRequestCommands.CLEAR_WRITE_READ,
            m_type=UartMessages.CLEAR_WRITE_READ,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._read_timeout = read_timeout
        self._data = data

    def _validate(self, read_timeout: int, data: List[int]):
        self._validate_read_timeout(read_timeout=read_timeout)
        self._validate_data(data=data)

    @staticmethod
    def _validate_read_timeout(read_timeout: int):
        if not (dpa_constants.BYTE_MIN <= read_timeout <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Read timeout value should be between 0 and 255.')

    @property
    def read_timeout(self):
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, value: int):
        self._validate_read_timeout(value)
        self._read_timeout = value

    @staticmethod
    def _validate_data(data: List[int]):
        if len(data) > 57:
            raise RequestParameterInvalidValueError('Maximum data length is 57 bytes.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Write data values should be between 0 and 255.')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: List[int]):
        self._validate_data(value)
        self._data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._read_timeout] + self._data
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {
            'readTimeout': self._read_timeout,
            'writtenData': self._data,
        }
        return super().to_json()
