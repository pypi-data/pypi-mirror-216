from __future__ import annotations
from enum import IntEnum
from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['SetDpaParamsRequest', 'DpaParam']


class DpaParam(IntEnum):
    LAST_RSSI = 0
    VOLTAGE = 1
    SYSTEM = 2
    USER_SPECIFIED = 3


class SetDpaParamsRequest(IRequest):

    __slots__ = '_dpa_param'

    def __init__(self, dpa_param: Union[DpaParam, int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(dpa_param)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SET_DPA_PARAMS,
            m_type=CoordinatorMessages.SET_DPA_PARAMS,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._dpa_param = dpa_param

    @staticmethod
    def _validate(dpa_param: Union[DpaParam, int]):
        if not (dpa_constants.BYTE_MIN <= dpa_param <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('DPA param value should be between 0 and 255.')

    @property
    def dpa_param(self):
        return self._dpa_param

    @dpa_param.setter
    def dpa_param(self, value: Union[DpaParam, int]) -> None:
        self._validate(value)
        self._dpa_param = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._dpa_param]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'dpaParam': self._dpa_param}
        return super().to_json()
