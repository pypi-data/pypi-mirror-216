from __future__ import annotations
from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['DiscoveryRequest']


class DiscoveryRequest(IRequest):
    __slots__ = '_tx_power', '_max_addr'

    def __init__(self, tx_power: int, max_addr: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(tx_power, max_addr)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.DISCOVERY,
            m_type=CoordinatorMessages.DISCOVERY,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._tx_power = tx_power
        self._max_addr = max_addr

    def _validate(self, tx_power: int, max_addr: int) -> None:
        self._validate_tx_power(tx_power)
        self._validate_max_addr(max_addr)

    @staticmethod
    def _validate_tx_power(tx_power: int):
        if not (dpa_constants.BYTE_MIN <= tx_power <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('TX power value should be between 0 and 255.')

    @property
    def tx_power(self):
        return self._tx_power

    @tx_power.setter
    def tx_power(self, value: int):
        self._validate_tx_power(value)
        self._tx_power = value

    @staticmethod
    def _validate_max_addr(max_addr: int):
        print(max_addr)
        if not (dpa_constants.BYTE_MIN <= max_addr <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Max address value should be between 0 and 255.')

    @property
    def max_addr(self):
        return self._max_addr

    @max_addr.setter
    def max_addr(self, value: int) -> None:
        self._validate_max_addr(value)
        self._max_addr = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._tx_power, self._max_addr]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'txPower': self._tx_power, 'maxAddr': self._max_addr}
        return super().to_json()
