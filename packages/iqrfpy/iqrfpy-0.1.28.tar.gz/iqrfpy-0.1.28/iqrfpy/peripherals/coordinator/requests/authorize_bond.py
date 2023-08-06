from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['AuthorizeBondRequest', 'AuthorizeBondParams']


class AuthorizeBondParams:

    __slots__ = '_req_addr', '_mid'

    def __init__(self, req_addr: int, mid: int):
        self._validate(req_addr=req_addr, mid=mid)
        self._req_addr = req_addr
        self._mid = mid

    def _validate(self, req_addr: int, mid: int):
        self._validate_req_addr(req_addr=req_addr)
        self._validate_mid(mid=mid)

    @staticmethod
    def _validate_req_addr(req_addr: int):
        if not (dpa_constants.BYTE_MIN <= req_addr <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Requested address value should be between 1 and 239.')

    @property
    def req_addr(self):
        return self._req_addr

    @req_addr.setter
    def req_addr(self, value: int):
        self._validate_req_addr(req_addr=value)
        self._req_addr = value

    @staticmethod
    def _validate_mid(mid: int):
        if not (dpa_constants.MID_MIN <= mid <= dpa_constants.MID_MAX):
            raise RequestParameterInvalidValueError('MID value should be an unsigned 32bit integer.')

    @property
    def mid(self):
        return self._mid

    @mid.setter
    def mid(self, value: int):
        self._validate_mid(mid=value)
        self._mid = value


class AuthorizeBondRequest(IRequest):

    __slots__ = '_nodes'

    def __init__(self, nodes: List[AuthorizeBondParams], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(nodes)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.AUTHORIZE_BOND,
            m_type=CoordinatorMessages.AUTHORIZE_BOND,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        ),
        self._nodes: List[AuthorizeBondParams] = nodes

    @staticmethod
    def _validate(nodes: List[AuthorizeBondParams]) -> None:
        if len(nodes) == 0:
            raise RequestParameterInvalidValueError('At least one pair of requested address and MID is required.')
        if len(nodes) > 11:
            raise RequestParameterInvalidValueError('Request can carry at most 11 pairs of address and MID.')

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value: List[AuthorizeBondParams]):
        self._validate(value)
        self._nodes = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        pdata = []
        for node in self._nodes:
            pdata.append(node.req_addr)
            pdata.append(node.mid & 0xFF)
            pdata.append((node.mid >> 8) & 0xFF)
            pdata.append((node.mid >> 16) & 0xFF)
            pdata.append((node.mid >> 24) & 0xFF)
        self._pdata = pdata
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'nodes': [{'reqAddr': node.req_addr, 'mid': node.mid} for node in self._nodes]}
        return super().to_json()
