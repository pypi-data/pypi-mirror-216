from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import NodeResponseCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils import dpa as dpa_constants
from iqrfpy.utils.common import Common
from iqrfpy.utils.dpa import ResponsePacketMembers, ResponseCodes
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['ReadResponse', 'NodeReadData']


@dataclass
class NodeReadData:

    def __init__(self, data: dict):
        self.ntw_addr = data['ntwADDR']
        self.ntw_vrn = data['ntwVRN']
        self.ntw_zin = data['ntwZIN']
        self.ntw_did = data['ntwDID']
        self.ntw_pvrn = data['ntwPVRN']
        self.ntw_useraddr = data['ntwUSERADDRESS']
        self.ntw_id = data['ntwID']
        self.ntw_vrnfnz = data['ntwVRNFNZ']
        self.ntw_cfg = data['ntwCFG']
        self.flags = data['flags']


class ReadResponse(IResponseGetterMixin):

    __slots__ = '_node_data'

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeResponseCommands.READ,
            m_type=NodeMessages.READ,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )
        if rcode == 0:
            self._node_data = NodeReadData(result)

    @property
    def node_data(self) -> NodeReadData:
        return self._node_data

    @staticmethod
    def from_dpa(dpa: bytes) -> ReadResponse:
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        pdata = None
        result = None
        if rcode == 0:
            DpaValidator.response_length(dpa=dpa, expected_len=20)
            pdata = Common.pdata_from_dpa(dpa=dpa)
            result = {
                'ntwADDR': pdata[0],
                'ntwVRN': pdata[1],
                'ntwZIN': pdata[2],
                'ntwDID': pdata[3],
                'ntwPVRN': pdata[4],
                'ntwUSERADDRESS': (pdata[6] << 8) + pdata[5],
                'ntwID': (pdata[8] << 8) + pdata[7],
                'ntwVRNFNZ': pdata[9],
                'ntwCFG': pdata[10],
                'flags': pdata[11]
            }
        return ReadResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata, result=result)

    @staticmethod
    def from_json(json: dict) -> ReadResponse:
        JsonValidator.response_received(json=json)
        nadr = Common.nadr_from_json(json=json)
        msgid = Common.msgid_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        pdata = Common.pdata_from_json(json=json)
        result = Common.result_from_json(json=json) if rcode == ResponseCodes.OK else None
        return ReadResponse(nadr=nadr, msgid=msgid, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, pdata=pdata,
                            result=result)
