from __future__ import annotations
from typing import Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['BondNodeRequest']


class BondNodeRequest(IRequest):
    __slots__ = '_req_addr', '_bonding_test_retries'

    def __init__(self, req_addr: int, bonding_test_retries: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(req_addr, bonding_test_retries)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.BOND_NODE,
            m_type=CoordinatorMessages.BOND_NODE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._req_addr = req_addr
        self._bonding_test_retries = bonding_test_retries

    def _validate(self, req_addr: int, bonding_test_retries: int) -> None:
        self._validate_req_addr(req_addr)
        self._validate_bonding_test_retries(bonding_test_retries)

    @staticmethod
    def _validate_req_addr(req_addr: int):
        if req_addr < dpa_constants.BYTE_MIN or req_addr > dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Address value should be between 0 and 255.')

    @property
    def req_addr(self):
        return self._req_addr

    @req_addr.setter
    def req_addr(self, value: int):
        self._validate_req_addr(value)
        self._req_addr = value

    @staticmethod
    def _validate_bonding_test_retries(bonding_test_retries: int):
        if bonding_test_retries < dpa_constants.BYTE_MIN or bonding_test_retries > dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Bonding test retries value should be between 0 and 255.')

    @property
    def bonding_test_retries(self):
        return self._bonding_test_retries

    @bonding_test_retries.setter
    def bonding_test_retries(self, value: int):
        self._validate_bonding_test_retries(value)
        self._bonding_test_retries = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._req_addr, self._bonding_test_retries]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'reqAddr': self._req_addr, 'bondingMask': self._bonding_test_retries}
        return super().to_json()
