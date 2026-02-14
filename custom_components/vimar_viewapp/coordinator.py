"""Data coordinator for Vimar View App integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_POLL_INTERVAL, DOMAIN
from .vimar_android_client import VimarAndroidClient

_LOGGER = logging.getLogger(__name__)


class VimarDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Poll app state from Android emulator and fan it out to entities."""

    def __init__(self, hass: HomeAssistant, client: VimarAndroidClient, poll_interval: int) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=poll_interval),
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.client.async_get_snapshot()
        except Exception as err:
            raise UpdateFailed(f"Unable to refresh Vimar app state: {err}") from err
