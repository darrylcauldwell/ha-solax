"""Tests for sensor descriptions and value functions."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)

from custom_components.solax_local.sensor import SENSOR_DESCRIPTIONS

from .conftest import MOCK_DATA


def test_sensor_count():
    """Test that there are exactly 21 sensor descriptions."""
    assert len(SENSOR_DESCRIPTIONS) == 21


def test_all_keys_unique():
    """Test that all sensor keys are unique."""
    keys = [d.key for d in SENSOR_DESCRIPTIONS]
    assert len(keys) == len(set(keys))


def test_all_translation_keys_present():
    """Test that all sensors have translation keys."""
    for desc in SENSOR_DESCRIPTIONS:
        assert desc.translation_key is not None, f"Missing translation_key for {desc.key}"


def test_value_functions_return_values():
    """Test that all value functions return non-None values from mock data."""
    for desc in SENSOR_DESCRIPTIONS:
        value = desc.value_fn(MOCK_DATA)
        assert value is not None, f"value_fn returned None for {desc.key}"


def test_grid_sensors():
    """Test grid sensor values and metadata."""
    grid_descs = {d.key: d for d in SENSOR_DESCRIPTIONS if d.key.startswith("grid_") and d.key != "grid_power_io"}

    assert grid_descs["grid_voltage"].value_fn(MOCK_DATA) == 241.4
    assert grid_descs["grid_voltage"].device_class == SensorDeviceClass.VOLTAGE
    assert grid_descs["grid_voltage"].native_unit_of_measurement == UnitOfElectricPotential.VOLT

    assert grid_descs["grid_current"].value_fn(MOCK_DATA) == 3.2
    assert grid_descs["grid_current"].device_class == SensorDeviceClass.CURRENT

    assert grid_descs["grid_power"].value_fn(MOCK_DATA) == 780
    assert grid_descs["grid_power"].device_class == SensorDeviceClass.POWER

    assert grid_descs["grid_frequency"].value_fn(MOCK_DATA) == 49.93
    assert grid_descs["grid_frequency"].device_class == SensorDeviceClass.FREQUENCY


def test_battery_sensors():
    """Test battery sensor values."""
    batt_descs = {d.key: d for d in SENSOR_DESCRIPTIONS if d.key.startswith("battery_")}

    assert batt_descs["battery_voltage"].value_fn(MOCK_DATA) == 235.10
    assert batt_descs["battery_current"].value_fn(MOCK_DATA) == -0.65
    assert batt_descs["battery_power"].value_fn(MOCK_DATA) == -350
    assert batt_descs["battery_temperature"].value_fn(MOCK_DATA) == 22
    assert batt_descs["battery_soc"].value_fn(MOCK_DATA) == 45
    assert batt_descs["battery_soc"].device_class == SensorDeviceClass.BATTERY
    assert batt_descs["battery_soc"].native_unit_of_measurement == PERCENTAGE


def test_energy_totals_state_class():
    """Test that lifetime energy totals use TOTAL_INCREASING."""
    total_keys = {"total_pv_energy", "total_feed_in_energy", "total_consumption"}
    for desc in SENSOR_DESCRIPTIONS:
        if desc.key in total_keys:
            assert desc.state_class == SensorStateClass.TOTAL_INCREASING, (
                f"{desc.key} should be TOTAL_INCREASING"
            )
            assert desc.device_class == SensorDeviceClass.ENERGY
            assert desc.native_unit_of_measurement == UnitOfEnergy.KILO_WATT_HOUR


def test_today_energy_state_class():
    """Test that today's energy uses TOTAL (resets daily)."""
    today_desc = next(d for d in SENSOR_DESCRIPTIONS if d.key == "today_pv_energy")
    assert today_desc.state_class == SensorStateClass.TOTAL
    assert today_desc.device_class == SensorDeviceClass.ENERGY


def test_grid_power_io():
    """Test grid import/export sensor."""
    desc = next(d for d in SENSOR_DESCRIPTIONS if d.key == "grid_power_io")
    assert desc.value_fn(MOCK_DATA) == -120
    assert desc.device_class == SensorDeviceClass.POWER
    assert desc.native_unit_of_measurement == UnitOfPower.WATT
