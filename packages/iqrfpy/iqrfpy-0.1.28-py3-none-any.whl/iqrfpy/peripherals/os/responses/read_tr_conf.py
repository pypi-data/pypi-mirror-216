from __future__ import annotations
from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import OSResponseCommands
from iqrfpy.enums.message_types import OSMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.os.os_tr_conf_data import OsTrConfData
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers, ResponseCodes
from iqrfpy.utils.common import Common
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = [
    'ReadTrConfResponse',
    'OsTrConfData'
]


class ReadTrConfResponse(IResponseGetterMixin):

    __slots__ = '_checksum', '_configuration', '_rfpgm', '_init_phy'

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.OS,
            pcmd=OSResponseCommands.READ_CFG,
            m_type=OSMessages.READ_CFG,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        if rcode == ResponseCodes.OK:
            self._checksum = result['checksum']
            self._configuration = OsTrConfData.from_pdata(result['configuration'])
            self._rfpgm = result['rfpgm']
            self._init_phy = result['initphy']

    @property
    def checksum(self) -> int:
        return self._checksum

    @property
    def configuration(self) -> OsTrConfData:
        return self._configuration

    @property
    def rfpgm(self) -> int:
        return self._rfpgm

    @property
    def init_phy(self) -> int:
        return self._init_phy

    @staticmethod
    def from_dpa(dpa: bytes) -> ReadTrConfResponse:
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        pdata = None
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=42)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'checksum': pdata[0],
                'configuration': list(pdata[1:32]),
                'rfpgm': pdata[32],
                'initphy': pdata[33],
            }
        return ReadTrConfResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @staticmethod
    def from_json(json: dict) -> ReadTrConfResponse:
        JsonValidator.response_received(json=json)
        nadr = Common.nadr_from_json(json=json)
        msgid = Common.msgid_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        return ReadTrConfResponse(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata,
                                  result=result)
