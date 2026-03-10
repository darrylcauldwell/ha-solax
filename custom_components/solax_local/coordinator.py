"""Data update coordinator for SolaX Local."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import timedelta
import logging

from aiosolax import (
    InverterData,
    InverterInfo,
    SolaxAllZeroError,
    SolaxClient,
    SolaxConnectionError,
    SolaxError,
    SolaxTimeoutError,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

type SolaxLocalConfigEntry = ConfigEntry["SolaxLocalRuntimeData"]


@dataclass
class SolaxLocalRuntimeData:
    """Runtime data for the SolaX Local config entry."""

    coordinator: SolaxLocalCoordinator
    info: InverterInfo


class SolaxLocalCoordinator(DataUpdateCoordinator[InverterData]):
    """Coordinator for fetching SolaX inverter data."""

    config_entry: SolaxLocalConfigEntry
    info: InverterInfo | None = None

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: SolaxLocalConfigEntry,
        client: SolaxClient,
    ) -> None:
        interval = config_entry.options.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
        )
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval),
        )
        self.client = client
        self._update_lock = asyncio.Lock()

    async def _async_update_data(self) -> InverterData:
        """Fetch data from the SolaX dongle."""
        async with self._update_lock:
            return await self._do_update()

    async def _do_update(self) -> InverterData:
        """Perform the actual data fetch (must be called under lock)."""
        try:
            info, data = await self.client.get_data()
            self.info = info
            return data
        except SolaxAllZeroError:
            if self.data is not None:
                _LOGGER.debug("All-zero response, returning previous data")
                return self.data
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="inverter_offline",
            )
        except SolaxTimeoutError as err:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="timeout_error",
            ) from err
        except SolaxConnectionError as err:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="connection_error",
            ) from err
        except SolaxError as err:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_error",
                translation_placeholders={"error": str(err)},
            ) from err
