"""Test fixtures for ha-solax."""

from __future__ import annotations

from aiosolax import InverterData, InverterInfo

MOCK_SERIAL = "H4372AI4633110"

MOCK_INFO = InverterInfo(
    serial_number=MOCK_SERIAL,
    inverter_type=15,
    rated_power=3.7,
    firmware_main="V3.0-H3.0",
    firmware_sub="3.006.04",
)

MOCK_DATA = InverterData(
    grid_voltage=241.4,
    grid_current=3.2,
    grid_power=780,
    grid_frequency=49.93,
    pv1_voltage=321.5,
    pv2_voltage=187.0,
    pv1_current=8.9,
    pv2_current=4.2,
    pv1_power=2861,
    pv2_power=786,
    total_pv_energy=13259.5,
    today_pv_energy=4.5,
    battery_voltage=235.10,
    battery_current=-0.65,
    battery_power=-350,
    battery_temperature=22,
    battery_soc=45,
    inverter_temperature=34,
    grid_power_io=-120,
    total_feed_in_energy=152.34,
    total_consumption=1531.86,
)
