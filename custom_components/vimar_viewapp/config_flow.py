"""Config flow for Vimar View App integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_ADB_HOST,
    CONF_ADB_PORT,
    CONF_PASSWORD,
    CONF_PIN,
    CONF_POLL_INTERVAL,
    CONF_SERIAL,
    CONF_USERNAME,
    DEFAULT_ADB_HOST,
    DEFAULT_ADB_PORT,
    DEFAULT_POLL_INTERVAL,
    DOMAIN,
)


class VimarViewAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Vimar View App config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input.get(CONF_SERIAL) or f"{user_input[CONF_ADB_HOST]}:{user_input[CONF_ADB_PORT]}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Vimar View App", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_ADB_HOST, default=DEFAULT_ADB_HOST): str,
                vol.Required(CONF_ADB_PORT, default=DEFAULT_ADB_PORT): int,
                vol.Optional(CONF_SERIAL): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Optional(CONF_PIN): str,
                vol.Required(CONF_POLL_INTERVAL, default=DEFAULT_POLL_INTERVAL): int,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return VimarViewAppOptionsFlow(config_entry)


class VimarViewAppOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow updates."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_POLL_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_POLL_INTERVAL,
                        self.config_entry.data.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL),
                    ),
                ): int,
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
