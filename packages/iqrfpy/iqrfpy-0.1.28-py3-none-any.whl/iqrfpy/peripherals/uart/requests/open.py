from __future__ import annotations
from typing import Optional, Union
from iqrfpy.enums.commands import UartRequestCommands
from iqrfpy.enums.message_types import UartMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.dpa import BaudRates, BYTE_MIN, BYTE_MAX, HWPID_MAX
from iqrfpy.irequest import IRequest

__all__ = [
    'OpenRequest',
]


class OpenRequest(IRequest):

    __slots__ = '_baud_rate'

    def __init__(self, nadr: int, baud_rate: Union[BaudRates, int], hwpid: int = HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(baud_rate=baud_rate)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.UART,
            pcmd=UartRequestCommands.OPEN,
            m_type=UartMessages.OPEN,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._baud_rate = baud_rate

    def _validate(self, baud_rate: Union[BaudRates, int]):
        self._validate_baud_rate(baud_rate=baud_rate)

    @staticmethod
    def _validate_baud_rate(baud_rate: Union[BaudRates, int]):
        if not (BYTE_MIN <= baud_rate <= BYTE_MAX):
            raise RequestParameterInvalidValueError('Baud rate value should be between 0 and 255.')

    @property
    def baud_rate(self):
        return self._baud_rate

    @baud_rate.setter
    def baud_rate(self, value: Union[BaudRates, int]):
        self._validate_baud_rate(value)
        self._baud_rate = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._baud_rate]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'baudRate': self._baud_rate}
        return super().to_json()
