"""
Sensor constants module.

This module provides constants related to Sensor standards.
"""

from iqrfpy.utils.enums import IntEnumMember


class SensorTypes(IntEnumMember):
    """Sensor type constants enum."""

    TEMPERATURE = 1
    CARBON_DIOXIDE = 2
    VOLATILE_ORGANIC_COMPOUND = 3
    EXTRA_LOW_VOLTAGE = 4
    EARTHS_MAGNETIC_FIELD = 5
    LOW_VOLTAGE = 6
    CURRENT = 7
    POWER = 8
    MAINS_FREQUENCY = 9
    TIME_SPAN = 10
    ILLUMINANCE = 11
    NITROGEN_DIOXIDE = 12
    SULFUR_DIOXIDE = 13
    CARBON_MONOXIDE = 14
    OZONE = 15
    ATMOSPHERIC_PRESSURE = 16
    COLOR_TEMPERATURE = 17
    PARTICULATES_PM2_5 = 18
    SOUND_PRESSURE_LEVEL = 19
    ALTITUDE = 20
    ACCELERATION = 21
    AMMONIA = 22
    METHANE = 23
    SHORT_LENGTH = 24
    PARTICULATES_PM1 = 25
    PARTICULATES_PM4 = 26
    PARTICULATES_PM10 = 27
    TOTAL_VOLATILE_ORGANIC_COMPOUND = 28
    NITROGEN_OXIDES = 29
    RELATIVE_HUMIDITY = 128
    BINARY_DATA7 = 129
    POWER_FACTOR = 130
    UV_INDEX = 131
    PH = 132
    RSSI = 133
    BINARY_DATA30 = 160
    CONSUMPTION = 161
    DATETIME = 162
    TIME_SPAN_LONG = 163
    LATITUDE = 164
    LONGITUDE = 165
    TEMPERATURE_FLOAT = 166
    LENGTH = 167
    DATA_BLOCK = 192


class SensorFrcCommands(IntEnumMember):
    """Sensor FRC commands enum."""

    FRC_2BITS = 0x10
    FRC_1BYTE = 0x90
    FRC_2BYTES = 0xE0
    FRC_4BYTES = 0xF9


class SensorDataSize(IntEnumMember):
    """Sensor data size by FRC command enum."""

    DATA_2BYTES_MIN = 1
    DATA_2BYTES_MAX = 127
    DATA_1BYTE_MIN = 128
    DATA_1BYTE_MAX = 159
    DATA_4BYTES_MIN = 160
    DATA_4BYTES_MAX = 191


class SensorFrcErrors(IntEnumMember):
    """Sensor FRC error codes enum."""

    NO_FRC_RESPONSE = 0
    FRC_NOT_IMPLEMENTED = 1
    SENSOR_ERROR_OR_OUT_OF_RANGE = 2
    RESERVED = 3
