from __future__ import annotations
from typing import Optional, Union
from iqrfpy.enums.commands import NodeRequestCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['BackupRequest']


class BackupRequest(IRequest):

    __slots__ = '_index'

    def __init__(self, nadr: int, index: int = 0, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(index)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.BACKUP,
            m_type=NodeMessages.BACKUP,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._index = index

    @staticmethod
    def _validate(index: int) -> None:
        if index < dpa_constants.BYTE_MIN or index > dpa_constants.BYTE_MAX:
            raise RequestParameterInvalidValueError('Index value should be between 0 and 255.')

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._validate(value)
        self._index = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._index]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'index': self._index}
        return super().to_json()
