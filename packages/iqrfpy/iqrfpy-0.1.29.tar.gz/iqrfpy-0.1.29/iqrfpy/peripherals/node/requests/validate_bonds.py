from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import NodeRequestCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = [
    'ValidateBondsRequest',
    'NodeValidateBondsParams'
]


class NodeValidateBondsParams:

    __slots__ = '_bond_addr', '_mid'

    def __init__(self, bond_addr: int, mid: int):
        self._validate(bond_addr=bond_addr, mid=mid)
        self._bond_addr = bond_addr
        self._mid = mid

    def _validate(self, bond_addr: int, mid: int):
        self._validate_bond_addr(bond_addr)
        self._validate_mid(mid)

    @staticmethod
    def _validate_bond_addr(bond_addr: int):
        if not (dpa_constants.BYTE_MIN <= bond_addr <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Bond address value should be between 1 and 255.')

    @property
    def bond_addr(self):
        return self._bond_addr

    @bond_addr.setter
    def bond_addr(self, value: int):
        self._validate_bond_addr(value)
        self._bond_addr = value

    @staticmethod
    def _validate_mid(mid: int):
        if not (dpa_constants.MID_MIN <= mid <= dpa_constants.MID_MAX):
            raise RequestParameterInvalidValueError('MID value should be an unsigned 32bit integer.')

    @property
    def mid(self):
        return self._mid

    @mid.setter
    def mid(self, value):
        self._validate_mid(value)
        self._mid = value


class ValidateBondsRequest(IRequest):

    __slots__ = '_nodes'

    def __init__(self, nadr: int, nodes: List[NodeValidateBondsParams], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(nodes)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.VALIDATE_BONDS,
            m_type=NodeMessages.VALIDATE_BONDS,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        ),
        self._nodes: List[NodeValidateBondsParams] = nodes

    @staticmethod
    def _validate(nodes: List[NodeValidateBondsParams]) -> None:
        if len(nodes) > 11:
            raise RequestParameterInvalidValueError('Request can carry at most 11 pairs of address and MID.')

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, value: List[NodeValidateBondsParams]) -> None:
        self._validate(value)
        self._nodes = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        pdata = []
        for node in self._nodes:
            pdata.append(node.bond_addr)
            pdata.append(node.mid & 0xFF)
            pdata.append((node.mid >> 8) & 0xFF)
            pdata.append((node.mid >> 16) & 0xFF)
            pdata.append((node.mid >> 24) & 0xFF)
        self._pdata = pdata
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'nodes': [{'bondAddr': node.bond_addr, 'mid': node.mid} for node in self._nodes]}
        return super().to_json()
