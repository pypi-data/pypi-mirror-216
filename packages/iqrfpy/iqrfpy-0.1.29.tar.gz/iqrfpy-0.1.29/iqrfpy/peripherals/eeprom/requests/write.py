from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import EEPROMRequestCommands
from iqrfpy.enums.message_types import EEPROMMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['WriteRequest']


class WriteRequest(IRequest):
    __slots__ = '_address', '_data'

    def __init__(self, nadr: int, address: int, data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(address, data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.EEPROM,
            pcmd=EEPROMRequestCommands.WRITE,
            m_type=EEPROMMessages.WRITE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._address = address
        self._data = data

    def _validate(self, address: int, data: List[int]) -> None:
        self._validate_address(address)
        self._validate_data(data)

    @staticmethod
    def _validate_address(address: int):
        if not (dpa_constants.BYTE_MIN <= address <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Address should be between 0 and 255.')

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value: int) -> None:
        self._validate_address(address=value)
        self._address = value

    @staticmethod
    def _validate_data(data: List[int]):
        if len(data) > dpa_constants.REQUEST_PDATA_MAX_LEN:
            raise RequestParameterInvalidValueError('Data should be at most 58 bytes long.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Data values should be between 0 and 255.')

    @property
    def data(self) -> List[int]:
        return self._data

    @data.setter
    def data(self, value: List[int]) -> None:
        self._validate_data(value)
        self._data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        pdata = [self._address]
        pdata.extend(self._data)
        self._pdata = pdata
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'address': self._address, 'pData': self._data}
        return super().to_json()
