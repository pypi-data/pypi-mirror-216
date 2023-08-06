from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.utils.enums import IntEnumMember
from iqrfpy.irequest import IRequest

__all__ = [
    'SetSecurityRequest',
    'OsSecurityType'
]


class OsSecurityType(IntEnumMember):
    ACCESS_PASSWORD = 0
    USER_KEY = 1


class SetSecurityRequest(IRequest):

    __slots__ = '_security_type', '_data'

    def __init__(self, nadr: int, security_type: Union[OsSecurityType, int], data: List[int],
                 hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        self._validate(security_type, data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.SET_SECURITY,
            m_type=OSMessages.SET_SECURITY,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._security_type = security_type
        self._data = data

    def _validate(self, security_type: Union[OsSecurityType, int], data: List[int]):
        self._validate_security_type(security_type)
        self._validate_data(data)

    @staticmethod
    def _validate_security_type(security_type: Union[OsSecurityType, int]):
        if not (dpa_constants.BYTE_MIN <= security_type <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Security type value should be between 0 and 255.')

    @property
    def security_type(self):
        return self._security_type

    @security_type.setter
    def security_type(self, value: Union[OsSecurityType, int]):
        self._validate_security_type(value)
        self._security_type = value

    @staticmethod
    def _validate_data(data: List[int]):
        if len(data) != 16:
            raise RequestParameterInvalidValueError('Data should be a list of 16 values.')
        if not Common.values_in_byte_range(data):
            raise RequestParameterInvalidValueError('Data values should be between 0 and 255.')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: List[int]):
        self._validate_data(value)
        self._data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._security_type] + self._data
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'type': self._security_type, 'data': self._data}
        return super().to_json()
