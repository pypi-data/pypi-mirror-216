from __future__ import annotations
from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['SetMidRequest']


class SetMidRequest(IRequest):

    __slots__ = '_bond_addr', '_mid'

    def __init__(self, bond_addr: int, mid: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(bond_addr, mid)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SET_MID,
            m_type=CoordinatorMessages.SET_MID,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._bond_addr = bond_addr
        self._mid = mid

    def _validate(self, bond_addr: int, mid: int) -> None:
        self._validate_bond_addr(bond_addr)
        self._validate_mid(mid)

    @staticmethod
    def _validate_bond_addr(bond_addr: int):
        if bond_addr < dpa_constants.BYTE_MIN or bond_addr > dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Bond address value should be between 0 and 255.')

    @property
    def bond_addr(self):
        return self._bond_addr

    @bond_addr.setter
    def bond_addr(self, value: int) -> None:
        self._validate_bond_addr(value)
        self._bond_addr = value

    @staticmethod
    def _validate_mid(mid: int):
        if mid < dpa_constants.MID_MIN or mid > dpa_constants.MID_MAX:
            raise RequestParameterInvalidValueError('MID value should be between 0 and 4294967295.')

    @property
    def mid(self):
        return self._mid

    @mid.setter
    def mid(self, value: int) -> None:
        self._validate_mid(value)
        self._mid = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [
            self._mid & 0xFF,
            (self._mid >> 8) & 0xFF,
            (self._mid >> 16) & 0xFF,
            (self._mid >> 24) & 0xFF,
            self._bond_addr
        ]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'bondAddr': self._bond_addr, 'mid': self._mid}
        return super().to_json()
