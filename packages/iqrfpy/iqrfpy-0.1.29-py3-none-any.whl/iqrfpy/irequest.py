from __future__ import annotations
import math
from abc import ABC, abstractmethod
from typing import List, Optional, Union
from uuid import uuid4
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.enums.commands import Command
from iqrfpy.enums.message_types import MessageType
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.exceptions import RequestNadrInvalidError, RequestPnumInvalidError, RequestPcmdInvalidError,\
    RequestHwpidInvalidError, RequestParameterInvalidValueError

__all__ = ['IRequest']


class IRequest(ABC):

    __slots__ = '_nadr', '_pnum', '_pcmd', '_mtype', '_hwpid', '_pdata', '_msgid', '_params', '_dpa_rsp_time', \
        '_dev_process_time'

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int],
                 hwpid: int = dpa_constants.HWPID_MAX, pdata: Union[List[int], None] = None,
                 m_type: Union[MessageType, None] = None, params: Union[dict, None] = None,
                 dpa_rsp_time: Union[float, None] = None, dev_process_time: Union[float, None] = None,
                 msgid: Union[str, None] = None):
        self._nadr = nadr
        self._pnum = pnum
        self._pcmd = pcmd
        self._hwpid = hwpid
        self._pdata = pdata
        self._mtype = m_type
        self._msgid = msgid if msgid is not None else str(uuid4())
        self._params = params if params is not None else {}
        self._dpa_rsp_time = dpa_rsp_time
        self._dev_process_time = dev_process_time
        self._validate_base(nadr, pnum, pcmd, hwpid, dpa_rsp_time, dev_process_time)

    def _validate_base(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int,
                       dpa_rsp_time: Union[float, None], dev_process_time: Union[float, None]) -> None:
        self._validate_nadr(nadr)
        self._validate_pnum(pnum)
        self._validate_pcmd(pcmd)
        self._validate_hwpid(hwpid)
        self._validate_dpa_rsp_time(dpa_rsp_time)
        self._validate_dev_process_time(dev_process_time)

    @staticmethod
    def _validate_nadr(nadr: int):
        if not (dpa_constants.BYTE_MIN <= nadr <= dpa_constants.BYTE_MAX):
            raise RequestNadrInvalidError('NADR should be between 0 and 255.')

    @staticmethod
    def _validate_pnum(pnum: Union[Peripheral, int]):
        if not (dpa_constants.BYTE_MIN <= pnum <= dpa_constants.BYTE_MAX):
            raise RequestPnumInvalidError('PNUM should be between 0 and 255.')

    @staticmethod
    def _validate_pcmd(pcmd: Union[Command, int]):
        if not (dpa_constants.BYTE_MIN <= pcmd <= dpa_constants.BYTE_MAX):
            raise RequestPcmdInvalidError('PCMD should be between 0 and 255.')

    @staticmethod
    def _validate_hwpid(hwpid: int):
        if not (dpa_constants.HWPID_MIN <= hwpid <= dpa_constants.HWPID_MAX):
            raise RequestHwpidInvalidError('HWPID should be between 0 and 65535.')

    @staticmethod
    def _validate_dpa_rsp_time(dpa_rsp_time: Union[float, None]):
        if dpa_rsp_time is None:
            return
        if dpa_rsp_time < 0:
            raise RequestParameterInvalidValueError('DPA response time should a positive integer.')

    @staticmethod
    def _validate_dev_process_time(dev_process_time: Union[float, None]):
        if dev_process_time is None:
            return
        if dev_process_time < 0:
            raise RequestParameterInvalidValueError('Device processing time should be a positive integer.')

    @property
    def nadr(self):
        return self._nadr

    @nadr.setter
    def nadr(self, value: int):
        self._validate_nadr(value)
        self._nadr = value

    @property
    def msgid(self) -> str:
        return self._msgid

    @property
    def mtype(self) -> MessageType:
        return self._mtype

    @property
    def dpa_rsp_time(self) -> Optional[float]:
        return self._dpa_rsp_time

    @dpa_rsp_time.setter
    def dpa_rsp_time(self, value: Union[float, None] = None):
        self._validate_dpa_rsp_time(value)
        self._dpa_rsp_time = value

    @property
    def dev_process_time(self) -> Optional[float]:
        return self._dev_process_time

    @dev_process_time.setter
    def dev_process_time(self, value: Union[float, None] = None):
        self._validate_dev_process_time(value)
        self._dev_process_time = value

    @abstractmethod
    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        dpa: List[int] = [self._nadr, 0, self._pnum, self._pcmd, self._hwpid & 0xFF, (self._hwpid >> 8) & 0xFF]
        if self._pdata is not None:
            dpa.extend(self._pdata)
        if mutable:
            return bytearray(dpa)
        return bytes(dpa)

    @abstractmethod
    def to_json(self) -> dict:
        json: dict = {
            'mType': self._mtype.value,
            'data': {
                'msgId': self._msgid,
                'req': {
                    'nAdr': self._nadr,
                    'hwpId': self._hwpid,
                    'param': self._params,
                },
                'returnVerbose': True,
            },
        }
        if self._dpa_rsp_time is not None:
            json['data']['timeout'] = math.ceil(self._dpa_rsp_time * 1000)
        return json
