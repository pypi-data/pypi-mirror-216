from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['SmartConnectRequest']


class SmartConnectRequest(IRequest):

    __slots__ = '_req_addr', '_bonding_test_retries', '_ibk', '_mid', '_virtual_device_address'

    def __init__(self, req_addr: int, bonding_test_retries: int, ibk: Union[List[int]], mid: int,
                 virtual_device_address: int = 0xFF, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(req_addr, bonding_test_retries, ibk, mid, virtual_device_address)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.SMART_CONNECT,
            m_type=CoordinatorMessages.SMART_CONNECT,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._req_addr = req_addr
        self._bonding_test_retries = bonding_test_retries
        self._ibk = ibk
        self._mid = mid
        self._virtual_device_address = virtual_device_address

    def _validate(self, req_addr: int, bonding_test_retries: int, ibk: List[int], mid: int,
                  virtual_device_address: int) -> None:
        self._validate_req_addr(req_addr)
        self._validate_bonding_test_retries(bonding_test_retries)
        self._validate_ibk(ibk)
        self._validate_mid(mid)
        self._validate_virtual_device_address(virtual_device_address)

    @staticmethod
    def _validate_req_addr(req_addr: int):
        if not (dpa_constants.BYTE_MIN <= req_addr <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Requested address should be between 0 and 255.')

    @property
    def req_addr(self):
        return self._req_addr

    @req_addr.setter
    def req_addr(self, value: int) -> None:
        self._validate_req_addr(value)
        self._req_addr = value

    @staticmethod
    def _validate_bonding_test_retries(bonding_test_retries: int):
        if not (dpa_constants.BYTE_MIN <= bonding_test_retries <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Bonding test retries should be between 0 and 255.')

    @property
    def bonding_test_retries(self):
        return self._bonding_test_retries

    @bonding_test_retries.setter
    def bonding_test_retries(self, value: int) -> None:
        self._validate_bonding_test_retries(value)
        self._bonding_test_retries = value

    @staticmethod
    def _validate_ibk(ibk: List[int]):
        if len(ibk) != dpa_constants.IBK_LEN:
            raise RequestParameterInvalidValueError('IBK should be list of 16 8bit unsigned integers.')
        if not Common.values_in_byte_range(ibk):
            raise RequestParameterInvalidValueError('IBK list should only contain values between 0 and 255.')

    @property
    def ibk(self):
        return self._ibk

    @ibk.setter
    def ibk(self, value: List[int]) -> None:
        self._validate_ibk(value)
        self._ibk = value

    @staticmethod
    def _validate_mid(mid: int):
        if not (dpa_constants.MID_MIN <= mid <= dpa_constants.MID_MAX):
            raise RequestParameterInvalidValueError('MID value should be between 0 and 4294967295.')

    @property
    def mid(self):
        return self._mid

    @mid.setter
    def mid(self, value: int) -> None:
        self._validate_mid(value)
        self._mid = value

    @staticmethod
    def _validate_virtual_device_address(virtual_device_address: int):
        if not (dpa_constants.BYTE_MIN <= virtual_device_address <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Virtual device address should be between 0 and 255.')

    @property
    def virtual_device_address(self):
        return self._virtual_device_address

    @virtual_device_address.setter
    def virtual_device_address(self, value: int) -> None:
        self._validate_virtual_device_address(value)
        self._virtual_device_address = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        params = [self._req_addr, self._bonding_test_retries]
        params.extend(self._ibk)
        params.extend([
            self._mid & 0xFF,
            (self._mid >> 8) & 0xFF,
            (self._mid >> 16) & 0xFF,
            (self._mid >> 24) & 0xFF,
            0,
            self._virtual_device_address,
        ])
        params.extend([0] * 14)
        self._pdata = params
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {
            'reqAddr': self._req_addr,
            'bondingTestRetries': self._bonding_test_retries,
            'ibk': self._ibk,
            'mid': self._mid,
            'virtualDeviceAddress': self._virtual_device_address,
            'userData': [0, 0, 0, 0]
        }
        return super().to_json()
