from __future__ import annotations
from typing import Optional, Union
from iqrfpy.enums.commands import FrcRequestCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = [
    'SetFrcParamsRequest',
    'FrcParams'
]


class FrcParams:

    __slots__ = 'offline_frc', 'frc_response_time'

    def __init__(self, offline_frc: bool = False,
                 frc_response_time: dpa_constants.FrcResponseTimes = dpa_constants.FrcResponseTimes.MS40):
        self.offline_frc = offline_frc
        self.frc_response_time = frc_response_time

    @staticmethod
    def from_int(frc_params: int) -> FrcParams:
        return FrcParams(
            offline_frc=bool(frc_params & 0x08),
            frc_response_time=dpa_constants.FrcResponseTimes(frc_params & 0x70)
        )

    def to_data(self):
        return self.frc_response_time | int(self.offline_frc) << 3


class SetFrcParamsRequest(IRequest):
    __slots__ = '_frc_params'

    def __init__(self, nadr: int, frc_params: Union[FrcParams, int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(frc_params)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.FRC,
            pcmd=FrcRequestCommands.SET_PARAMS,
            m_type=FrcMessages.SET_PARAMS,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._frc_params = frc_params

    @staticmethod
    def _validate(frc_params: Union[FrcParams, int]):
        if type(frc_params) == int and not (dpa_constants.BYTE_MIN <= frc_params <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('FRC params value should be between 0 and 255.')

    @property
    def frc_params(self):
        return self._frc_params

    @frc_params.setter
    def frc_params(self, value: Union[FrcParams, int]):
        self._validate(value)
        self._frc_params = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._frc_params if type(self._frc_params) == int else self._frc_params.to_data()]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {
            'frcResponseTime': self._frc_params if type(self._frc_params) == int else self._frc_params.to_data()
        }
        return super().to_json()
