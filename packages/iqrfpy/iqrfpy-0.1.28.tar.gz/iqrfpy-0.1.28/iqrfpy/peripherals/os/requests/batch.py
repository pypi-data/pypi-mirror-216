from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import Command, OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import Peripheral, EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['BatchRequest']


class BatchData:

    __slots__ = '_pnum', '_pcmd', '_hwpid', '_pdata'

    def __init__(self, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int, pdata: List[int]):
        self._validate(pnum=pnum, pcmd=pcmd, hwpid=hwpid, pdata=pdata)
        self._pnum = pnum
        self._pcmd = pcmd
        self._hwpid = hwpid
        self._pdata = pdata

    def _validate(self, pnum: Union[Peripheral, int], pcmd: Union[Command, int], hwpid: int, pdata: List[int]):
        self._validate_pnum(pnum)
        self._validate_pcmd(pcmd)
        self._validate_hwpid(hwpid)
        self._validate_pdata(pdata)

    @staticmethod
    def _validate_pnum(pnum: Union[Peripheral, int]):
        if not (dpa_constants.BYTE_MIN <= pnum <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('PNUM value should be between 0 and 255.')

    @property
    def pnum(self):
        return self._pnum

    @pnum.setter
    def pnum(self, value: Union[Peripheral, int]):
        self._validate_pnum(value)
        self._pnum = value

    @staticmethod
    def _validate_pcmd(pcmd: Union[Command, int]):
        if not (dpa_constants.BYTE_MIN <= pcmd <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('PCMD value should be between 0 and 255.')

    @property
    def pcmd(self):
        return self._pcmd

    @pcmd.setter
    def pcmd(self, value: Union[Command, int]):
        self._validate_pcmd(value)
        self._pcmd = value

    @staticmethod
    def _validate_hwpid(hwpid: int):
        if not (dpa_constants.HWPID_MIN <= hwpid <= dpa_constants.HWPID_MAX):
            raise RequestParameterInvalidValueError('HWPID value should be between 0 and 65535.')

    @property
    def hwpid(self):
        return self._hwpid

    @hwpid.setter
    def hwpid(self, value: int):
        self._validate_hwpid(value)
        self._hwpid = value

    @staticmethod
    def _validate_pdata(pdata: List[int]):
        if not Common.values_in_byte_range(pdata):
            raise RequestParameterInvalidValueError('PDATA values should be between 0 and 255.')

    @property
    def pdata(self):
        return self._pdata

    @pdata.setter
    def pdata(self, value: List[int]):
        self._validate_pdata(value)
        self._pdata = value

    def to_pdata(self):
        data = [self._pnum, self._pcmd, self._hwpid & 0xFF, (self._hwpid >> 8) & 0xFF] + self._pdata
        return [len(data)] + data

    def to_json(self):
        return {
            'pnum': f'{self._pnum:02x}',
            'pcmd': f'{self._pcmd:02x}',
            'hwpid': f'{self._hwpid:04x}',
            'rdata': '.'.join([f'{x:02x}' for x in self._pdata])
        }


class BatchRequest(IRequest):

    __slots__ = '_requests'

    def __init__(self, nadr: int, requests: List[BatchData], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(requests)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.SET_SECURITY,
            m_type=OSMessages.SET_SECURITY,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._requests = requests

    @staticmethod
    def _validate(requests: List[BatchData]):
        data = []
        for request in requests:
            data += request.to_pdata()
        if len(data) + 1 > 58:
            raise RequestParameterInvalidValueError('Batch requests data should be no larger than 58B.')

    @property
    def requests(self):
        return self._requests

    @requests.setter
    def requests(self, value: List[BatchData]):
        self._validate(value)
        self._requests = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = []
        for request in self._requests:
            self._pdata += request.to_pdata()
        self._pdata.append(0)
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'requests': [request.to_json() for request in self._requests]}
        return super().to_json()
