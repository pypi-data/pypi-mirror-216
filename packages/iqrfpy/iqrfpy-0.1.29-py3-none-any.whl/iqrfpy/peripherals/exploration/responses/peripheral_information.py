from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import ExplorationResponseCommands
from iqrfpy.enums.message_types import ExplorationMessages
from iqrfpy.enums.peripherals import Peripheral
from iqrfpy.utils.common import Common
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers, ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator
from iqrfpy.peripherals.exploration.responses.peripheral_information_data import PeripheralInformationData

__all__ = [
    'PeripheralInformationResponse',
]


class PeripheralInformationResponse(IResponseGetterMixin):

    __slots__ = '_peripheral_data'

    def __init__(self, nadr: int, pnum: Union[Peripheral, int], hwpid: int = dpa_constants.HWPID_MAX,
                 rcode: int = 0, dpa_value: int = 0, msgid: Optional[str] = None, pdata: Optional[List[int]] = None,
                 result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=pnum,
            pcmd=ExplorationResponseCommands.PERIPHERALS_ENUMERATION_INFORMATION,
            m_type=ExplorationMessages.PERIPHERAL_INFORMATION,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        if rcode == ResponseCodes.OK:
            self._peripheral_data = PeripheralInformationData(data=result)

    @property
    def peripheral_data(self):
        return self._peripheral_data

    @staticmethod
    def from_dpa(dpa: bytes) -> PeripheralInformationResponse:
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        pnum = dpa[ResponsePacketMembers.PNUM]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        pdata = None
        result = None
        if rcode == ResponseCodes.OK:
            DpaValidator.response_length(dpa=dpa, expected_len=12)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'perTe': dpa[8],
                'perT': dpa[9],
                'par1': dpa[10],
                'par2': dpa[11],
            }
        return PeripheralInformationResponse(nadr=nadr, pnum=pnum, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value,
                                             pdata=pdata, result=result)

    @staticmethod
    def from_json(json: dict) -> PeripheralInformationResponse:
        JsonValidator.response_received(json=json)
        nadr = Common.nadr_from_json(json=json)
        pnum = Common.pnum_from_json(json=json)
        msgid = Common.msgid_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        if rcode < 0:
            pnum += 0x80
        return PeripheralInformationResponse(nadr=nadr, pnum=pnum, msgid=msgid, hwpid=hwpid, rcode=rcode,
                                             dpa_value=dpa_value, pdata=pdata, result=result)
