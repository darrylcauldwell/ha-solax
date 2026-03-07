"""Sensor platform for SolaX Local."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from aiosolax import InverterData

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .coordinator import SolaxLocalConfigEntry, SolaxLocalCoordinator
from .entity import SolaxLocalEntity

PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class SolaxSensorDescription(SensorEntityDescription):
    """Describes a SolaX sensor entity."""

    value_fn: Callable[[InverterData], StateType]


SENSOR_DESCRIPTIONS: tuple[SolaxSensorDescription, ...] = (
    # Grid sensors
    SolaxSensorDescription(
        key="grid_voltage",
        translation_key="grid_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.grid_voltage,
    ),
    SolaxSensorDescription(
        key="grid_current",
        translation_key="grid_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.grid_current,
    ),
    SolaxSensorDescription(
        key="grid_power",
        translation_key="grid_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.grid_power,
    ),
    SolaxSensorDescription(
        key="grid_frequency",
        translation_key="grid_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=lambda d: d.grid_frequency,
    ),
    # PV1 sensors
    SolaxSensorDescription(
        key="pv1_voltage",
        translation_key="pv1_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.pv1_voltage,
    ),
    SolaxSensorDescription(
        key="pv1_current",
        translation_key="pv1_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.pv1_current,
    ),
    SolaxSensorDescription(
        key="pv1_power",
        translation_key="pv1_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.pv1_power,
    ),
    # PV2 sensors
    SolaxSensorDescription(
        key="pv2_voltage",
        translation_key="pv2_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.pv2_voltage,
    ),
    SolaxSensorDescription(
        key="pv2_current",
        translation_key="pv2_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.pv2_current,
    ),
    SolaxSensorDescription(
        key="pv2_power",
        translation_key="pv2_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.pv2_power,
    ),
    # Battery sensors
    SolaxSensorDescription(
        key="battery_voltage",
        translation_key="battery_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=lambda d: d.battery_voltage,
    ),
    SolaxSensorDescription(
        key="battery_current",
        translation_key="battery_current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=lambda d: d.battery_current,
    ),
    SolaxSensorDescription(
        key="battery_power",
        translation_key="battery_power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.battery_power,
    ),
    SolaxSensorDescription(
        key="battery_temperature",
        translation_key="battery_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.battery_temperature,
    ),
    SolaxSensorDescription(
        key="battery_soc",
        translation_key="battery_soc",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.battery_soc,
    ),
    # Inverter sensors
    SolaxSensorDescription(
        key="inverter_temperature",
        translation_key="inverter_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.inverter_temperature,
    ),
    # Power flow
    SolaxSensorDescription(
        key="grid_power_io",
        translation_key="grid_power_io",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.grid_power_io,
    ),
    # Energy totals (lifetime)
    SolaxSensorDescription(
        key="total_pv_energy",
        translation_key="total_pv_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=1,
        value_fn=lambda d: d.total_pv_energy,
    ),
    SolaxSensorDescription(
        key="total_feed_in_energy",
        translation_key="total_feed_in_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: d.total_feed_in_energy,
    ),
    SolaxSensorDescription(
        key="total_consumption",
        translation_key="total_consumption",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: d.total_consumption,
    ),
    # Today's energy
    SolaxSensorDescription(
        key="today_pv_energy",
        translation_key="today_pv_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=1,
        value_fn=lambda d: d.today_pv_energy,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolaxLocalConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up SolaX Local sensor entities."""
    runtime_data = entry.runtime_data
    coordinator = runtime_data.coordinator
    serial_number = runtime_data.info.serial_number

    entities = [
        SolaxLocalSensor(coordinator, description, serial_number)
        for description in SENSOR_DESCRIPTIONS
    ]
    async_add_entities(entities)


class SolaxLocalSensor(SolaxLocalEntity, SensorEntity):
    """Sensor entity for SolaX Local."""

    entity_description: SolaxSensorDescription

    def __init__(
        self,
        coordinator: SolaxLocalCoordinator,
        description: SolaxSensorDescription,
        serial_number: str,
    ) -> None:
        super().__init__(coordinator, description, serial_number)
        self.entity_description = description

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
