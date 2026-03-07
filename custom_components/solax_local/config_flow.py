"""Config flow for SolaX Local."""

from __future__ import annotations

import logging
from typing import Any

from aiosolax import (
    SolaxAllZeroError,
    SolaxAuthenticationError,
    SolaxClient,
    SolaxConnectionError,
    SolaxResponseError,
    SolaxTimeoutError,
)
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_UPDATE_INTERVAL,
    CONF_USERNAME,
    DEFAULT_PORT,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default="192.168.1.106"): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_USERNAME): str,
    }
)


class SolaxLocalConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SolaX Local."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry,
    ) -> SolaxLocalOptionsFlow:
        return SolaxLocalOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            password = user_input[CONF_PASSWORD].strip()
            port = user_input.get(CONF_PORT, DEFAULT_PORT)
            username = user_input.get(CONF_USERNAME, "").strip() or None

            session = async_get_clientsession(self.hass)
            client = SolaxClient(
                host, password, port=port, username=username, session=session
            )

            try:
                info, _data = await client.get_data()
            except SolaxAuthenticationError:
                errors["base"] = "invalid_auth"
            except SolaxConnectionError:
                errors["base"] = "cannot_connect"
            except SolaxTimeoutError:
                errors["base"] = "timeout"
            except SolaxAllZeroError:
                errors["base"] = "inverter_offline"
            except SolaxResponseError as err:
                if "Unsupported inverter type" in str(err):
                    errors["base"] = "unsupported_model"
                else:
                    errors["base"] = "unknown"
            except Exception:
                _LOGGER.exception("Unexpected exception during validation")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info.serial_number)
                self._abort_if_unique_id_configured()

                data: dict[str, Any] = {
                    CONF_HOST: host,
                    CONF_PASSWORD: password,
                    CONF_PORT: port,
                }
                if username:
                    data[CONF_USERNAME] = username

                return self.async_create_entry(
                    title=f"SolaX ({info.serial_number})",
                    data=data,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class SolaxLocalOptionsFlow(OptionsFlow):
    """Handle options flow for SolaX Local."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(
                data={
                    CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL],
                }
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_UPDATE_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                    ),
                ): vol.All(int, vol.Range(min=10, max=300)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
