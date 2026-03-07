"""Base entity for SolaX Local."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SolaxLocalCoordinator


class SolaxLocalEntity(CoordinatorEntity[SolaxLocalCoordinator]):
    """Base entity for SolaX Local."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SolaxLocalCoordinator,
        description: EntityDescription,
        serial_number: str,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{description.key}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, serial_number)},
            name=f"SolaX Inverter ({serial_number})",
            manufacturer="SolaX Power",
            model="X1-Hybrid Gen4",
        )
