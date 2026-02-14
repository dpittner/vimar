# Vimar View App Home Assistant custom integration

Home Assistant custom component to control Vimar shades by automating the official **Android Vimar View App** over ADB/UI automation.

## Features

- `cover` entities for shades (open/close/stop/set-position).
- `sensor` entities for shade diagnostics (`position`, `battery`, `signal`) when available from app UI.
- `button` entities for Vimar scenarios.
- Uses only Vimar app credentials (username/password + optional PIN) and an Android ADB endpoint.

## Architecture

1. Integration connects to Android emulator/device over ADB (`uiautomator2`).
2. Launches `it.vimar.View` and performs login when required.
3. Reads current shades/scenarios from UI hierarchy.
4. Executes shade/scenario actions by UI interactions.

---

## Android emulator options

You can either run an emulator “embedded” next to Home Assistant (same host) or use a remote emulator.

### Embedded sidecar emulator (recommended)

A ready compose file is provided:

- `deployment/docker-compose.emulator.yml`

Start it:

```bash
docker compose -f deployment/docker-compose.emulator.yml up -d
```

Then open `http://<host>:6080`, install/login Vimar View app, and configure integration with:

- ADB host: `<host>`
- ADB port: `5555`
- Serial: optional (`<host>:5555`)

### Detailed installation guide

See `docs/android_emulator_setup.md` for:
- sidecar setup,
- Android Studio emulator setup,
- physical device fallback,
- HA OS/container caveats.

---

## Requirements

- Home Assistant with custom components support.
- Android emulator/device reachable by ADB.
- Official Vimar View app installed and usable in that Android runtime.

## Installation

1. Copy `custom_components/vimar_viewapp` into `<ha_config>/custom_components/`.
2. Restart Home Assistant.
3. Add integration: **Settings → Devices & Services → Add Integration → “Vimar View App (Android Bridge)”**.
4. Enter:
   - ADB host/port (or serial),
   - Vimar username/password,
   - optional app PIN,
   - polling interval.

## Known limitations

- UI automation is sensitive to app layout/localization changes.
- Some selectors may need tuning in `vimar_android_client.py`.
- If the app changes screens/flows, entity discovery or actions may fail until selectors are updated.
