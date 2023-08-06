from __future__ import annotations
from typing import Optional, Union
from iqrfpy.enums.commands import OSRequestCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest
from iqrfpy.peripherals.os.os_tr_conf_data import OsTrConfData

__all__ = [
    'WriteTrConfRequest',
    'OsTrConfData'
]


class WriteTrConfRequest(IRequest):
    __slots__ = '_configuration', '_rfpgm'

    def __init__(self, nadr: int, configuration: OsTrConfData, rfpgm: int, hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(rfpgm=rfpgm)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSRequestCommands.WRITE_CFG,
            m_type=OSMessages.WRITE_CFG,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._configuration = configuration
        self._rfpgm = rfpgm

    def _validate(self, rfpgm: int) -> None:
        self._validate_rfpgm(rfpgm)

    @staticmethod
    def _validate_rfpgm(rfpgm: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rfpgm <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RFPGM should be a value between 0 and 255.')

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, value: OsTrConfData) -> None:
        self._configuration = value

    @property
    def rfpgm(self):
        return self._rfpgm

    @rfpgm.setter
    def rfpgm(self, value: int) -> None:
        self._validate_rfpgm(value)
        self._rfpgm = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [0] + self._configuration.to_pdata() + [self._rfpgm]
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {
            'checksum': 0,
            'configuration': self._configuration.to_pdata(),
            'rfpgm': self._rfpgm,
        }
        return super().to_json()
