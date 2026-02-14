"""Cover entities exposed by Vimar View App integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.cover import (
    ATTR_POSITION,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_CLIENT, DATA_COORDINATOR, DOMAIN
from .coordinator import VimarDataUpdateCoordinator
from .vimar_android_client import ShadeState, VimarAndroidClient


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: VimarDataUpdateCoordinator = data[DATA_COORDINATOR]
    entities: list[VimarShadeCover] = []

    for shade in coordinator.data.get("shades", []):
        entities.append(VimarShadeCover(data[DATA_CLIENT], coordinator, shade["id"]))

    async_add_entities(entities)


class VimarShadeCover(CoordinatorEntity[VimarDataUpdateCoordinator], CoverEntity):
    """Representation of one Vimar shade."""

    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
        | CoverEntityFeature.STOP
        | CoverEntityFeature.SET_POSITION
    )

    def __init__(
        self,
        client: VimarAndroidClient,
        coordinator: VimarDataUpdateCoordinator,
        shade_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._client = client
        self._shade_id = shade_id

    @property
    def _shade(self) -> dict[str, Any] | None:
        for shade in self.coordinator.data.get("shades", []):
            if shade["id"] == self._shade_id:
                return shade
        return None

    @property
    def unique_id(self) -> str:
        return f"vimar_shade_{self._shade_id}"

    @property
    def name(self) -> str | None:
        shade = self._shade
        return shade["name"] if shade else self._shade_id

    @property
    def current_cover_position(self) -> int | None:
        shade = self._shade
        if not shade:
            return None
        return shade.get("position")

    @property
    def is_opening(self) -> bool | None:
        return False

    @property
    def is_closing(self) -> bool | None:
        return False

    async def async_open_cover(self, **kwargs: Any) -> None:
        shade = self._shade
        if shade:
            await self._client.async_open_shade(shade["name"])
            await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs: Any) -> None:
        shade = self._shade
        if shade:
            await self._client.async_close_shade(shade["name"])
            await self.coordinator.async_request_refresh()

    async def async_stop_cover(self, **kwargs: Any) -> None:
        shade = self._shade
        if shade:
            await self._client.async_stop_shade(shade["name"])
            await self.coordinator.async_request_refresh()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        shade = self._shade
        if shade:
            await self._client.async_set_shade_position(shade["name"], kwargs[ATTR_POSITION])
            await self.coordinator.async_request_refresh()
