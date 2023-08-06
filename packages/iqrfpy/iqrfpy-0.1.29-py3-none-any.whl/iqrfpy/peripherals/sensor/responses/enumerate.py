from __future__ import annotations
from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import SensorResponseCommands
from iqrfpy.enums.message_types import SensorMessages
from iqrfpy.enums.peripherals import Standards
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponseCodes, ResponsePacketMembers
from iqrfpy.utils.validators import DpaValidator, JsonValidator
from iqrfpy.utils.sensor_parser import SensorParser, SensorData

__all__ = ['EnumerateResponse']


class EnumerateResponse(IResponseGetterMixin):

    __slots__ = '_sensor_data'

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=Standards.SENSOR,
            pcmd=SensorResponseCommands.ENUMERATE,
            m_type=SensorMessages.ENUMERATE,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        if rcode == ResponseCodes.OK:
            self._sensor_data: List[SensorData] = result['sensors']

    @property
    def sensor_data(self):
        return self._sensor_data

    @staticmethod
    def from_dpa(dpa: bytes) -> EnumerateResponse:
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        pdata = None
        result = None
        if rcode == ResponseCodes.OK:
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {'sensors': SensorParser.enumerate_from_dpa(pdata)}
        return EnumerateResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @staticmethod
    def from_json(json: dict) -> EnumerateResponse:
        JsonValidator.response_received(json=json)
        msgid = Common.msgid_from_json(json=json)
        nadr = Common.nadr_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        if rcode == ResponseCodes.OK:
            result = {'sensors': SensorParser.enumerate_from_json(result['sensors'])}
        return EnumerateResponse(msgid=msgid, nadr=nadr, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, pdata=pdata,
                                 result=result)
