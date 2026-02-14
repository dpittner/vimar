"""Sensor entities for Vimar shade diagnostics."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_COORDINATOR, DOMAIN
from .coordinator import VimarDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: VimarDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    entities: list[VimarShadeSensor] = []

    for shade in coordinator.data.get("shades", []):
        shade_id = shade["id"]
        entities.append(VimarShadeSensor(coordinator, shade_id, "position", PERCENTAGE))
        entities.append(VimarShadeSensor(coordinator, shade_id, "battery", PERCENTAGE))
        entities.append(VimarShadeSensor(coordinator, shade_id, "signal", SIGNAL_STRENGTH_DECIBELS_MILLIWATT))

    async_add_entities(entities)


class VimarShadeSensor(CoordinatorEntity[VimarDataUpdateCoordinator], SensorEntity):
    """Simple coordinator-backed sensor for shade attributes."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: VimarDataUpdateCoordinator,
        shade_id: str,
        metric: str,
        unit: str,
    ) -> None:
        super().__init__(coordinator)
        self._shade_id = shade_id
        self._metric = metric
        self._attr_native_unit_of_measurement = unit

    @property
    def _shade(self):
        for shade in self.coordinator.data.get("shades", []):
            if shade["id"] == self._shade_id:
                return shade
        return None

    @property
    def unique_id(self) -> str:
        return f"vimar_{self._shade_id}_{self._metric}"

    @property
    def name(self) -> str | None:
        shade = self._shade
        shade_name = shade["name"] if shade else self._shade_id
        return f"{shade_name} {self._metric}"

    @property
    def native_value(self):
        shade = self._shade
        if not shade:
            return None
        return shade.get(self._metric)
