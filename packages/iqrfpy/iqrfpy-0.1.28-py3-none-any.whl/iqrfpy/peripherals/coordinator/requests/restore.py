from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import CoordinatorRequestCommands
from iqrfpy.enums.message_types import CoordinatorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['RestoreRequest']


class RestoreRequest(IRequest):

    __slots__ = '_network_data'

    def __init__(self, network_data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(network_data)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.COORDINATOR,
            pcmd=CoordinatorRequestCommands.RESTORE,
            m_type=CoordinatorMessages.RESTORE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._network_data = network_data

    @staticmethod
    def _validate(network_data: List[int]):
        if len(network_data) > dpa_constants.REQUEST_PDATA_MAX_LEN:
            raise RequestParameterInvalidValueError('Network data should be at most 58 bytes long.')
        if not Common.values_in_byte_range(network_data):
            raise RequestParameterInvalidValueError('Network data block values should be between 0 and 255.')

    @property
    def network_data(self):
        return self._network_data

    @network_data.setter
    def network_data(self, value: List[int]) -> None:
        self._validate(value)
        self._network_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = self._network_data
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'networkData': self._network_data}
        return super().to_json()
