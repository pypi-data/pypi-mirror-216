from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Union
from iqrfpy.enums.commands import Command
from iqrfpy.enums.message_types import MessageType
from iqrfpy.enums.peripherals import Peripheral
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.validators import *

__all__ = ['IResponse', 'IResponseGetterMixin']


class IResponse(ABC):

    ASYNC_MSGID = 'async'

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], pcmd: Union[Command, int],
                 hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 pdata: Optional[List[int]] = None, m_type: Optional[MessageType] = None, msgid: Optional[str] = None,
                 result: Optional[dict] = None):
        self._nadr = nadr
        self._pnum = pnum
        self._pcmd = pcmd
        self._mtype = m_type
        self._hwpid = hwpid
        self._rcode = rcode
        self._dpa_value = dpa_value
        self._pdata = pdata
        self._msgid = msgid
        self._result = result

    @property
    @abstractmethod
    def nadr(self) -> int:
        return self._nadr

    @property
    @abstractmethod
    def pnum(self) -> Union[Peripheral, int]:
        return self._pnum

    @property
    @abstractmethod
    def pcmd(self) -> Union[Command, int]:
        return self._pcmd

    @property
    @abstractmethod
    def mtype(self) -> MessageType:
        return self._mtype

    @property
    @abstractmethod
    def hwpid(self) -> int:
        return self._hwpid

    @property
    @abstractmethod
    def rcode(self) -> int:
        return self._rcode

    @abstractmethod
    def get_rcode_as_string(self) -> str:
        return dpa_constants.ResponseCodes.to_string(self._rcode)

    @property
    @abstractmethod
    def dpa_value(self) -> int:
        return self._dpa_value

    @property
    @abstractmethod
    def pdata(self) -> Union[List[int], None]:
        return self._pdata

    @property
    @abstractmethod
    def result(self) -> Union[dict, None]:
        return self._result

    @property
    @abstractmethod
    def msgid(self) -> str:
        return self._msgid

    @staticmethod
    def validate_dpa_response(data: bytes) -> None:
        DpaValidator.base_response_length(data)

    @staticmethod
    @abstractmethod
    def from_dpa(dpa: bytes) -> IResponse:
        pass

    @staticmethod
    @abstractmethod
    def from_json(json: dict) -> IResponse:
        pass


class IResponseGetterMixin(IResponse):

    @property
    def nadr(self) -> int:
        return super().nadr

    @property
    def pnum(self) -> Union[Peripheral, int]:
        return super().pnum

    @property
    def pcmd(self) -> Union[Command, int]:
        return super().pcmd

    @property
    def mtype(self) -> MessageType:
        return super().mtype

    @property
    def hwpid(self) -> int:
        return super().hwpid

    @property
    def rcode(self) -> int:
        return super().rcode

    def get_rcode_as_string(self) -> str:
        return super().get_rcode_as_string()

    @property
    def dpa_value(self) -> int:
        return super().dpa_value

    @property
    def pdata(self) -> Optional[List[int]]:
        return super().pdata

    @property
    def result(self) -> Optional[dict]:
        return super().result

    @property
    def msgid(self) -> str:
        return super().msgid

    @staticmethod
    def from_dpa(dpa: bytes) -> IResponse:
        raise NotImplementedError('from_dpa() method not implemented.')

    @staticmethod
    def from_json(json: dict) -> IResponse:
        raise NotImplementedError('from_json() method not implemented.')
