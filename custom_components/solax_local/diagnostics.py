"""Diagnostics support for SolaX Local."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from .const import CONF_PASSWORD, CONF_USERNAME
from .coordinator import SolaxLocalConfigEntry

TO_REDACT = {CONF_PASSWORD, CONF_USERNAME}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: SolaxLocalConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    runtime_data = entry.runtime_data
    coordinator = runtime_data.coordinator

    sensor_data: dict[str, Any] = {}
    if coordinator.data is not None:
        sensor_data = asdict(coordinator.data)

    info_data: dict[str, Any] = asdict(runtime_data.info)

    return {
        "config_entry": async_redact_data(dict(entry.data), TO_REDACT),
        "inverter_info": info_data,
        "sensor_data": sensor_data,
    }
