from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import FrcRequestCommands
from iqrfpy.enums.message_types import SensorMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['FrcRequest']


class FrcRequest(IRequest):

    __slots__ = '_sensor_type', '_sensor_index', '_frc_command', '_selected_nodes'

    def __init__(self, sensor_type: int, sensor_index: int, frc_command: int, selected_nodes: Optional[List[int]] = None,
                 hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        self._validate(sensor_type, sensor_index, frc_command, selected_nodes)
        super().__init__(
            nadr=dpa_constants.COORDINATOR_NADR,
            pnum=EmbedPeripherals.FRC,
            pcmd=FrcRequestCommands.SEND,
            m_type=SensorMessages.FRC,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._sensor_type = sensor_type
        self._sensor_index = sensor_index
        self._frc_command = frc_command
        self._selected_nodes = selected_nodes

    def _validate(self, sensor_type: int, sensor_index: int, frc_command: int,
                  selected_nodes: Optional[List[int]] = None):
        self._validate_sensor_type(sensor_type)
        self._validate_sensor_index(sensor_index)
        self._validate_frc_command(frc_command)
        self._validate_selected_nodes(selected_nodes)

    @staticmethod
    def _validate_sensor_type(sensor_type: int):
        if not (dpa_constants.BYTE_MIN <= sensor_type <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Sensor type value should be between 0 and 255.')

    @property
    def sensor_type(self):
        return self._sensor_type

    @sensor_type.setter
    def sensor_type(self, value: int):
        self._validate_sensor_type(value)
        self._sensor_type = value

    @staticmethod
    def _validate_sensor_index(sensor_index: int):
        if not (dpa_constants.SENSOR_INDEX_MIN <= sensor_index <= dpa_constants.SENSOR_INDEX_MAX):
            raise RequestParameterInvalidValueError('Sensor index value should be between 0 and 31.')

    @property
    def sensor_index(self):
        return self._sensor_index

    @sensor_index.setter
    def sensor_index(self, value: int):
        self._validate_sensor_index(value)
        self._sensor_index = value

    @staticmethod
    def _validate_frc_command(frc_command: int):
        if not (dpa_constants.BYTE_MIN <= frc_command <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('FRC command value should be between 0 and 255.')

    @property
    def frc_command(self):
        return self._frc_command

    @frc_command.setter
    def frc_command(self, value: int):
        self._validate_frc_command(value)
        self._frc_command = value

    @staticmethod
    def _validate_selected_nodes(selected_nodes: Optional[List[int]] = None):
        if selected_nodes is None:
            return
        if len(selected_nodes) > 240:
            raise RequestParameterInvalidValueError('Selected nodes should contain at most 240 values.')
        if min(selected_nodes) < 0 or max(selected_nodes) > 239:
            raise RequestParameterInvalidValueError('Selected nodes values should be between 1 and 239.')

    @property
    def selected_nodes(self):
        return self._selected_nodes

    @selected_nodes.setter
    def selected_nodes(self, value: Optional[List[int]] = None):
        self._validate_selected_nodes(value)
        self._selected_nodes = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        raise NotImplementedError('Sensor FRC dpa serialization not implemented.')

    def to_json(self) -> dict:
        self._params = {
            'sensorType': self._sensor_type,
            'sensorIndex': self._sensor_index,
            'frcCommand': self._frc_command,
            'getExtraResult': True,
        }
        if self._selected_nodes is not None:
            self._pcmd = FrcRequestCommands.SEND_SELECTIVE
            self._params['selectedNodes'] = self._selected_nodes
        return super().to_json()
