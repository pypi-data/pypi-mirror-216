from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import NodeRequestCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['RestoreRequest']


class RestoreRequest(IRequest):

    __slots__ = '_backup_data'

    def __init__(self, nadr: int, backup_data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(backup_data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeRequestCommands.RESTORE,
            m_type=NodeMessages.RESTORE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._backup_data = backup_data

    @staticmethod
    def _validate(backup_data: List[int]):
        if len(backup_data) > dpa_constants.REQUEST_PDATA_MAX_LEN:
            raise RequestParameterInvalidValueError('Backup data should be at most 58 bytes long.')
        if not Common.values_in_byte_range(backup_data):
            raise RequestParameterInvalidValueError('Backup data block values should be between 0 and 255.')

    @property
    def backup_data(self):
        return self._backup_data

    @backup_data.setter
    def backup_data(self, value: List[int]) -> None:
        self._validate(value)
        self._backup_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = self._backup_data
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'backupData': self._backup_data}
        return super().to_json()
