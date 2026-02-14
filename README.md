# Vimar View App Home Assistant custom integration

This repository contains a Home Assistant custom component that controls Vimar shades by automating the official **Android Vimar View App**.

## What this integration does

- Exposes Vimar shades as `cover` entities.
- Exposes shade diagnostics (`position`, `battery`, `signal`) as `sensor` entities when available in-app UI.
- Exposes Vimar scenarios as `button` entities.
- Uses only Vimar app credentials (`username`, `password`, optional app PIN) + emulator/device ADB endpoint.

## How it works

1. Home Assistant connects to an Android emulator/device over ADB (`uiautomator2`).
2. The integration starts `it.vimar.View` app and logs in if login fields are detected.
3. It parses visible UI labels/percent values to build shade and scenario entities.
4. Commands are executed by navigating/tapping in the app UI.

## Requirements

- Home Assistant installation with `custom_components` support.
- Android emulator/device reachable over ADB.
- Vimar View app installed and working in the emulator.

## Installation

1. Copy `custom_components/vimar_viewapp` into your Home Assistant `config/custom_components`.
2. Restart Home Assistant.
3. Add integration: **Settings → Devices & Services → Add Integration → "Vimar View App (Android Bridge)"**.
4. Enter:
   - ADB host/port or serial
   - Vimar app username/password
   - Optional app PIN
   - Poll interval

## Important notes

- UI automation depends on app layout and localization. If your app labels differ, some actions may need selector tuning in `vimar_android_client.py`.
- Keep emulator screen unlocked and app accessible for reliable control.
- This approach avoids requiring Vimar API tokens or gateway credentials not already used by the Android app.
