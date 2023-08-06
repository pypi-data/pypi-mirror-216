from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
from iqrfpy.utils import dpa as dpa_constants

__all__ = ['OsTrConfData']


class OsTrConfData:

    __slots__ = '_embedded_peripherals', '_custom_dpa_handler', '_dpa_peer_to_peer', '_routing_off', '_io_setup', \
        '_user_peer_to_peer', '_stay_awake_when_not_bonded', '_std_and_lp_network', '_rf_output_power', \
        '_rf_signal_filter', '_lp_rf_timeout', '_uart_baud_rate', '_alternative_dsm_channel', '_local_frc', \
        '_rf_channel_a', '_rf_channel_b', '_undocumented'

    def __init__(self, embedded_peripherals: Optional[List[int]] = None, custom_dpa_handler: bool = False,
                 dpa_peer_to_peer: bool = False, routing_off: bool = False, io_setup: bool = False,
                 user_peer_to_peer: bool = False, stay_awake_when_not_bonded: bool = False,
                 std_and_lp_network: bool = False, rf_output_power: int = 7, rf_signal_filter: int = 5,
                 lp_rf_timeout: int = 6,
                 uart_baud_rate: Union[dpa_constants.BaudRates, int] = dpa_constants.BaudRates.B9600,
                 alternative_dsm_channel: int = 0, local_frc: bool = False, rf_channel_a: int = 52,
                 rf_channel_b: int = 2, undocumented: Optional[List[int]] = None):
        if embedded_peripherals is None:
            embedded_peripherals = []
        if undocumented is None:
            undocumented = [0] * 13
        self._validate(embedded_peripherals=embedded_peripherals, rf_output_power=rf_output_power,
                       rf_signal_filter=rf_signal_filter, lp_rf_timeout=lp_rf_timeout, baud_rate=uart_baud_rate,
                       alternative_dsm=alternative_dsm_channel, rf_channel_a=rf_channel_a, rf_channel_b=rf_channel_b,
                       undocumented=undocumented)
        self._embedded_peripherals = embedded_peripherals
        self._custom_dpa_handler = custom_dpa_handler
        self._dpa_peer_to_peer = dpa_peer_to_peer
        self._routing_off = routing_off
        self._io_setup = io_setup
        self._user_peer_to_peer = user_peer_to_peer
        self._stay_awake_when_not_bonded = stay_awake_when_not_bonded
        self._std_and_lp_network = std_and_lp_network
        self._rf_output_power = rf_output_power
        self._rf_signal_filter = rf_signal_filter
        self._lp_rf_timeout = lp_rf_timeout
        self._uart_baud_rate = uart_baud_rate
        self._alternative_dsm_channel = alternative_dsm_channel
        self._local_frc = local_frc
        self._rf_channel_a = rf_channel_a
        self._rf_channel_b = rf_channel_b
        self._undocumented = undocumented

    def __eq__(self, other: OsTrConfData):
        return self._embedded_peripherals == other._embedded_peripherals and \
                self._custom_dpa_handler == other._custom_dpa_handler and \
                self._dpa_peer_to_peer == other._dpa_peer_to_peer and \
                self._routing_off == other.routing_off and \
                self._io_setup == other._io_setup and \
                self._user_peer_to_peer == other._user_peer_to_peer and \
                self._stay_awake_when_not_bonded == other._stay_awake_when_not_bonded and \
                self._std_and_lp_network == other._std_and_lp_network and \
                self._rf_output_power == other._rf_output_power and \
                self._rf_signal_filter == other._rf_signal_filter and \
                self._lp_rf_timeout == other._lp_rf_timeout and \
                self._uart_baud_rate == other._uart_baud_rate and \
                self._alternative_dsm_channel == other._alternative_dsm_channel and \
                self._local_frc == other._local_frc and \
                self._rf_channel_a == other._rf_channel_a and \
                self._rf_channel_b == other._rf_channel_b and \
                self._undocumented == other._undocumented

    def _validate(self, embedded_peripherals: List[int], rf_output_power: int, rf_signal_filter: int,
                  lp_rf_timeout: int, baud_rate: Union[dpa_constants.BaudRates, int], alternative_dsm: int,
                  rf_channel_a: int, rf_channel_b: int, undocumented: Optional[List[int]] = None):
        self._validate_embedded_peripherals(embedded_peripherals)
        self._validate_rf_output_power(rf_output_power)
        self._validate_rf_signal_filter(rf_signal_filter)
        self._validate_lp_rf_timeout(lp_rf_timeout)
        self._validate_uart_baud_rate(baud_rate)
        self._validate_alternative_dsm_channel(alternative_dsm)
        self._validate_rf_channel_a(rf_channel_a)
        self._validate_rf_channel_b(rf_channel_b)
        self._validate_undocumented(undocumented)

    @staticmethod
    def _validate_embedded_peripherals(embedded_peripherals: List[Union[EmbedPeripherals, int]]) -> None:
        if len(embedded_peripherals) > 32:
            raise RequestParameterInvalidValueError('Embedded peripherals should be at most 32 values.')
        if min(embedded_peripherals, default=0) < 0 or max(embedded_peripherals, default=0) > 31:
            raise RequestParameterInvalidValueError('Embedded peripherals values should be between 0 and 31.')

    @property
    def embedded_peripherals(self):
        return self._embedded_peripherals

    @embedded_peripherals.setter
    def embedded_peripherals(self, value: List[Union[EmbedPeripherals, int]]):
        self._validate_embedded_peripherals(embedded_peripherals=value)
        self._embedded_peripherals = value

    @property
    def custom_dpa_handler(self):
        return self._custom_dpa_handler

    @custom_dpa_handler.setter
    def custom_dpa_handler(self, value: bool):
        self._custom_dpa_handler = value

    @property
    def dpa_peer_to_peer(self):
        return self._dpa_peer_to_peer

    @dpa_peer_to_peer.setter
    def dpa_peer_to_peer(self, value: bool):
        self._dpa_peer_to_peer = value

    @property
    def routing_off(self):
        return self._routing_off

    @routing_off.setter
    def routing_off(self, value: bool):
        self._routing_off = value

    @property
    def io_setup(self):
        return self._io_setup

    @io_setup.setter
    def io_setup(self, value: bool):
        self._io_setup = value

    @property
    def user_peer_to_peer(self):
        return self._user_peer_to_peer

    @user_peer_to_peer.setter
    def user_peer_to_peer(self, value: bool):
        self._user_peer_to_peer = value

    @property
    def stay_awake_when_not_bonded(self):
        return self._stay_awake_when_not_bonded

    @stay_awake_when_not_bonded.setter
    def stay_awake_when_not_bonded(self, value: bool):
        self._stay_awake_when_not_bonded = value

    @property
    def std_and_lp_network(self):
        return self._std_and_lp_network

    @std_and_lp_network.setter
    def std_and_lp_network(self, value: bool):
        self._std_and_lp_network = value

    @staticmethod
    def _validate_rf_output_power(rf_output_power: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rf_output_power <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RF output power value should be between 0 and 255.')

    @property
    def rf_output_power(self):
        return self._rf_output_power

    @rf_output_power.setter
    def rf_output_power(self, value: int):
        self._validate_rf_output_power(rf_output_power=value)
        self._rf_output_power = value

    @staticmethod
    def _validate_rf_signal_filter(rf_signal_filter: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rf_signal_filter <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RF signal filter value should be between 0 and 255.')

    @property
    def rf_signal_filter(self):
        return self._rf_signal_filter

    @rf_signal_filter.setter
    def rf_signal_filter(self, value: int):
        self._validate_rf_signal_filter(rf_signal_filter=value)
        self._rf_signal_filter = value

    @staticmethod
    def _validate_lp_rf_timeout(lp_rf_timeout: int) -> None:
        if not (dpa_constants.BYTE_MIN <= lp_rf_timeout <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('LP RF timeout value should be between 0 and 255.')

    @property
    def lp_rf_timeout(self):
        return self._lp_rf_timeout

    @lp_rf_timeout.setter
    def lp_rf_timeout(self, value: int):
        self._validate_lp_rf_timeout(lp_rf_timeout=value)
        self._lp_rf_timeout = value

    @staticmethod
    def _validate_uart_baud_rate(uart_baud_rate: Union[dpa_constants.BaudRates, int]) -> None:
        if not (dpa_constants.BYTE_MIN <= uart_baud_rate <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('UART baud rate value should be between 0 and 255.')

    @property
    def uart_baud_rate(self):
        return self._uart_baud_rate

    @uart_baud_rate.setter
    def uart_baud_rate(self, value: Union[dpa_constants.BaudRates, int]):
        self._validate_uart_baud_rate(uart_baud_rate=value)
        self._uart_baud_rate = value

    @staticmethod
    def _validate_alternative_dsm_channel(alternative_dsm_channels: int) -> None:
        if not (dpa_constants.BYTE_MIN <= alternative_dsm_channels <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('Alternative DMS channel value should be between 0 and 255.')

    @property
    def alternative_dsm_channel(self):
        return self._alternative_dsm_channel

    @alternative_dsm_channel.setter
    def alternative_dsm_channel(self, value: int):
        self._validate_alternative_dsm_channel(alternative_dsm_channels=value)
        self._alternative_dsm_channel = value

    @property
    def local_frc(self):
        return self._local_frc

    @local_frc.setter
    def local_frc(self, value: bool):
        self._local_frc = value

    @staticmethod
    def _validate_rf_channel_a(rf_channel_a: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rf_channel_a <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RF channel A value should be between 0 and 255.')

    @property
    def rf_channel_a(self):
        return self._rf_channel_a

    @rf_channel_a.setter
    def rf_channel_a(self, value: int):
        self._validate_rf_channel_a(rf_channel_a=value)
        self._rf_channel_a = value

    @staticmethod
    def _validate_rf_channel_b(rf_channel_b: int) -> None:
        if not (dpa_constants.BYTE_MIN <= rf_channel_b <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('RF channel B value should be between 0 and 255.')

    @property
    def rf_channel_b(self):
        return self._rf_channel_b

    @rf_channel_b.setter
    def rf_channel_b(self, value: int):
        self._validate_rf_channel_b(rf_channel_b=value)
        self._rf_channel_b = value

    @staticmethod
    def _validate_undocumented(undocumented: List[int]) -> None:
        if len(undocumented) != 13:
            raise RequestParameterInvalidValueError('Undocumented block should be 13B long.')
        if not Common.values_in_byte_range(undocumented):
            raise RequestParameterInvalidValueError('Undocumented block values should be between 0 and 255.')

    @property
    def undocumented(self):
        return self._undocumented

    @undocumented.setter
    def undocumented(self, value: List[int]):
        self._validate_undocumented(undocumented=value)
        self._undocumented = value

    @staticmethod
    def from_pdata(data: Union[List[int], bytearray]) -> OsTrConfData:
        if type(data) == bytearray:
            data = list(data)
        embed_pers_data = data[0:4]
        embedded_pers = []
        for i in range(0, len(embed_pers_data * 8)):
            if embed_pers_data[int(i / 8)] & (1 << (i % 8)) and EmbedPeripherals.has_value(i):
                embedded_pers.append(EmbedPeripherals(i))
        embedded_peripherals = embedded_pers
        custom_dpa_handler = bool(data[4] & 1)
        dpa_peer_to_peer = bool(data[4] & 2)
        routing_off = bool(data[4] & 8)
        io_setup = bool(data[4] & 16)
        user_peer_to_peer = bool(data[4] & 32)
        stay_awake_when_not_bonded = bool(data[4] & 64)
        std_and_lp_network = bool(data[4] & 128)
        rf_output_power = data[7]
        rf_signal_filter = data[8]
        lp_rf_timeout = data[9]
        uart_baud_rate = data[10]
        alternative_dsm_channel = data[11]
        local_frc = bool(data[12] & 1)
        rf_channel_a = data[16]
        rf_channel_b = data[17]
        undocumented = data[18:]
        return OsTrConfData(embedded_peripherals=embedded_peripherals, custom_dpa_handler=custom_dpa_handler,
                            dpa_peer_to_peer=dpa_peer_to_peer, routing_off=routing_off, io_setup=io_setup,
                            user_peer_to_peer=user_peer_to_peer, stay_awake_when_not_bonded=stay_awake_when_not_bonded,
                            std_and_lp_network=std_and_lp_network, rf_output_power=rf_output_power,
                            rf_signal_filter=rf_signal_filter, lp_rf_timeout=lp_rf_timeout,
                            uart_baud_rate=uart_baud_rate, alternative_dsm_channel=alternative_dsm_channel,
                            local_frc=local_frc, rf_channel_a=rf_channel_a, rf_channel_b=rf_channel_b,
                            undocumented=undocumented)

    def to_pdata(self, to_bytes: bool = False) -> Union[List[int], bytearray]:
        embed_pers = Common.peripheral_list_to_bitmap(self.embedded_peripherals)
        conf_bits_0 = int(self.custom_dpa_handler) | int(self.dpa_peer_to_peer) << 1 | int(self.routing_off) << 3 | \
            int(self.io_setup) << 4 | int(self.user_peer_to_peer) << 5 | \
            int(self.stay_awake_when_not_bonded) << 6 | int(self.std_and_lp_network) << 7
        pdata = embed_pers + [conf_bits_0] + [0] * 2 + \
            [self.rf_output_power, self.rf_signal_filter, self.lp_rf_timeout, self.uart_baud_rate,
             self.alternative_dsm_channel, int(self.local_frc)] + [0] * 3 + [self.rf_channel_a, self.rf_channel_b] + \
            self.undocumented
        if to_bytes:
            return bytearray(pdata)
        return pdata
