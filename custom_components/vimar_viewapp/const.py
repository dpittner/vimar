"""Constants for the Vimar View App integration."""

from __future__ import annotations

DOMAIN = "vimar_viewapp"
PLATFORMS = ["cover", "sensor", "button"]

CONF_ADB_HOST = "adb_host"
CONF_ADB_PORT = "adb_port"
CONF_SERIAL = "serial"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_PIN = "pin"
CONF_POLL_INTERVAL = "poll_interval"

DEFAULT_ADB_HOST = "127.0.0.1"
DEFAULT_ADB_PORT = 5555
DEFAULT_POLL_INTERVAL = 20

DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"

ATTR_SHADE_POSITION = "position"
ATTR_SHADE_MOVING = "is_moving"
ATTR_SHADE_BATTERY = "battery"
ATTR_SHADE_SIGNAL = "signal"

VIMAR_PACKAGE = "it.vimar.View"
