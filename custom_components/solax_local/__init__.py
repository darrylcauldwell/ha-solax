"""The SolaX Local integration."""

from __future__ import annotations

import logging

from aiosolax import SolaxClient, SolaxError

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME, DEFAULT_PORT
from .coordinator import (
    SolaxLocalConfigEntry,
    SolaxLocalCoordinator,
    SolaxLocalRuntimeData,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(
    hass: HomeAssistant, entry: SolaxLocalConfigEntry
) -> bool:
    """Set up SolaX Local from a config entry."""
    session = async_get_clientsession(hass)
    client = SolaxClient(
        host=entry.data[CONF_HOST],
        password=entry.data[CONF_PASSWORD],
        port=entry.data.get(CONF_PORT, DEFAULT_PORT),
        username=entry.data.get(CONF_USERNAME),
        session=session,
    )

    coordinator = SolaxLocalCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()

    if coordinator.info is None:
        raise ConfigEntryNotReady("Inverter info not available after first refresh")

    entry.runtime_data = SolaxLocalRuntimeData(
        coordinator=coordinator,
        info=coordinator.info,
    )

    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def _async_options_updated(
    hass: HomeAssistant, entry: SolaxLocalConfigEntry
) -> None:
    """Reload integration when options are updated."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(
    hass: HomeAssistant, entry: SolaxLocalConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
