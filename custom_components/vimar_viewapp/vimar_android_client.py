"""Android View App bridge for Vimar shades.

This module automates the official Vimar Android app running on an emulator/device
and exposes high-level operations used by Home Assistant entities.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import logging
import re
from typing import Any

import uiautomator2 as u2

from .const import VIMAR_PACKAGE

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class ShadeState:
    """Represents a single shade status extracted from app UI."""

    id: str
    name: str
    position: int | None
    is_moving: bool
    battery: int | None = None
    signal: int | None = None


@dataclass(slots=True)
class Scenario:
    """Represents a scenario/action button in the app."""

    id: str
    name: str


class VimarAndroidClient:
    """Client that controls Vimar View app by UI automation.

    This class intentionally uses only app credentials (username/password/pin) and
    an ADB endpoint for the emulator/device.
    """

    def __init__(
        self,
        adb_host: str,
        adb_port: int,
        serial: str | None,
        username: str,
        password: str,
        pin: str | None,
    ) -> None:
        self._adb_host = adb_host
        self._adb_port = adb_port
        self._serial = serial or f"{adb_host}:{adb_port}"
        self._username = username
        self._password = password
        self._pin = pin
        self._device: u2.Device | None = None

    async def async_connect(self) -> None:
        """Open ADB/uiautomator session."""
        _LOGGER.debug("Connecting to Android emulator/device %s", self._serial)
        self._device = u2.connect(self._serial)
        await self.async_prepare_session()

    async def async_prepare_session(self) -> None:
        """Bring app in foreground and authenticate if needed."""
        if self._device is None:
            raise RuntimeError("Device is not connected")

        self._device.app_start(VIMAR_PACKAGE, stop=False)
        await self.async_login_if_needed()

    async def async_login_if_needed(self) -> None:
        """Attempt login flow when login widgets are visible."""
        if self._device is None:
            raise RuntimeError("Device is not connected")

        d = self._device

        email_field = d(className="android.widget.EditText", instance=0)
        pass_field = d(className="android.widget.EditText", instance=1)
        login_button = d(textMatches="(?i)(login|accedi|sign in)")

        if email_field.exists(timeout=0.5) and pass_field.exists(timeout=0.5):
            _LOGGER.info("Vimar app login required, filling credentials")
            email_field.set_text(self._username)
            pass_field.set_text(self._password)
            if login_button.exists(timeout=0.5):
                login_button.click()

        pin_field = d(className="android.widget.EditText")
        confirm_pin = d(textMatches="(?i)(conferma|confirm|ok)")
        if self._pin and pin_field.exists(timeout=0.5):
            _LOGGER.info("Submitting Vimar app PIN")
            pin_field.set_text(self._pin)
            if confirm_pin.exists(timeout=0.5):
                confirm_pin.click()

    async def async_get_snapshot(self) -> dict[str, Any]:
        """Collect shades and scenarios from currently displayed pages.

        The parser is intentionally permissive and relies on visible strings,
        enabling compatibility with localized app versions.
        """
        if self._device is None:
            raise RuntimeError("Device is not connected")

        await self.async_prepare_session()
        d = self._device

        shades = self._extract_shades(d.dump_hierarchy())
        scenarios = self._extract_scenarios(d.dump_hierarchy())

        return {
            "shades": [asdict(shade) for shade in shades],
            "scenarios": [asdict(scenario) for scenario in scenarios],
        }

    def _extract_shades(self, hierarchy_xml: str) -> list[ShadeState]:
        shades: list[ShadeState] = []
        candidates = re.findall(r'text="([^"]+)"', hierarchy_xml)

        for idx, text in enumerate(candidates):
            if "%" not in text:
                continue
            percent_match = re.search(r"(\d{1,3})\s*%", text)
            if not percent_match:
                continue

            position = max(0, min(100, int(percent_match.group(1))))
            name = candidates[idx - 1] if idx > 0 else f"Shade {idx + 1}"
            clean_name = name.strip() or f"Shade {idx + 1}"
            shade_id = re.sub(r"[^a-z0-9]+", "_", clean_name.lower()).strip("_")

            shades.append(
                ShadeState(
                    id=shade_id,
                    name=clean_name,
                    position=position,
                    is_moving=False,
                )
            )

        return shades

    def _extract_scenarios(self, hierarchy_xml: str) -> list[Scenario]:
        scenarios: list[Scenario] = []
        for text in re.findall(r'text="([^"]+)"', hierarchy_xml):
            if len(text) < 3:
                continue
            if re.search(r"(?i)(scenario|scena)", text):
                scenario_id = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
                scenarios.append(Scenario(id=scenario_id, name=text.strip()))

        unique: dict[str, Scenario] = {}
        for scenario in scenarios:
            unique[scenario.id] = scenario

        return list(unique.values())

    async def async_open_shade(self, name: str) -> None:
        await self._tap_text_and_action(name, action_regex=r"(?i)(open|up|apri|su)")

    async def async_close_shade(self, name: str) -> None:
        await self._tap_text_and_action(name, action_regex=r"(?i)(close|down|chiudi|giu)")

    async def async_stop_shade(self, name: str) -> None:
        await self._tap_text_and_action(name, action_regex=r"(?i)(stop|ferma)")

    async def async_set_shade_position(self, name: str, position: int) -> None:
        if self._device is None:
            raise RuntimeError("Device is not connected")

        await self.async_prepare_session()
        d = self._device

        if not d(text=name).exists(timeout=2):
            raise RuntimeError(f"Shade '{name}' not found in app UI")

        d(text=name).click()
        slider = d(className="android.widget.SeekBar")
        if not slider.exists(timeout=2):
            raise RuntimeError("Shade slider not available")

        slider.set_progress(max(0, min(100, position)))

    async def async_run_scenario(self, name: str) -> None:
        if self._device is None:
            raise RuntimeError("Device is not connected")

        await self.async_prepare_session()
        d = self._device

        if not d(text=name).exists(timeout=3):
            raise RuntimeError(f"Scenario '{name}' not found")

        d(text=name).click()

    async def _tap_text_and_action(self, name: str, action_regex: str) -> None:
        if self._device is None:
            raise RuntimeError("Device is not connected")

        await self.async_prepare_session()
        d = self._device

        if not d(text=name).exists(timeout=2):
            raise RuntimeError(f"Shade '{name}' not found")

        d(text=name).click()
        action = d(textMatches=action_regex)
        if not action.exists(timeout=2):
            raise RuntimeError(f"No action matching '{action_regex}' found")
        action.click()
