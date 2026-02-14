"""Home Assistant integration for Vimar shades via Android View app."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_ADB_HOST,
    CONF_ADB_PORT,
    CONF_PASSWORD,
    CONF_PIN,
    CONF_POLL_INTERVAL,
    CONF_SERIAL,
    CONF_USERNAME,
    DATA_CLIENT,
    DATA_COORDINATOR,
    PLATFORMS,
)
from .coordinator import VimarDataUpdateCoordinator
from .vimar_android_client import VimarAndroidClient


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Vimar integration from config entry."""
    client = VimarAndroidClient(
        adb_host=entry.data[CONF_ADB_HOST],
        adb_port=entry.data[CONF_ADB_PORT],
        serial=entry.data.get(CONF_SERIAL),
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        pin=entry.data.get(CONF_PIN),
    )
    await client.async_connect()

    coordinator = VimarDataUpdateCoordinator(
        hass,
        client,
        poll_interval=entry.options.get(CONF_POLL_INTERVAL, entry.data[CONF_POLL_INTERVAL]),
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(entry.domain, {})[entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_COORDINATOR: coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[entry.domain].pop(entry.entry_id)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
