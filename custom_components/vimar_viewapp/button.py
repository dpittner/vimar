"""Button entities to execute Vimar scenarios."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_CLIENT, DATA_COORDINATOR, DOMAIN
from .coordinator import VimarDataUpdateCoordinator
from .vimar_android_client import VimarAndroidClient


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: VimarDataUpdateCoordinator = data[DATA_COORDINATOR]
    client: VimarAndroidClient = data[DATA_CLIENT]

    entities = [
        VimarScenarioButton(client, coordinator, scenario["id"])
        for scenario in coordinator.data.get("scenarios", [])
    ]
    async_add_entities(entities)


class VimarScenarioButton(CoordinatorEntity[VimarDataUpdateCoordinator], ButtonEntity):
    """Button entity that triggers a Vimar scenario."""

    def __init__(
        self,
        client: VimarAndroidClient,
        coordinator: VimarDataUpdateCoordinator,
        scenario_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._client = client
        self._scenario_id = scenario_id

    @property
    def _scenario(self):
        for scenario in self.coordinator.data.get("scenarios", []):
            if scenario["id"] == self._scenario_id:
                return scenario
        return None

    @property
    def unique_id(self) -> str:
        return f"vimar_scenario_{self._scenario_id}"

    @property
    def name(self) -> str | None:
        scenario = self._scenario
        return scenario["name"] if scenario else self._scenario_id

    async def async_press(self) -> None:
        scenario = self._scenario
        if scenario:
            await self._client.async_run_scenario(scenario["name"])
