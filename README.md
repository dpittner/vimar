# Vimar View App for Home Assistant

This repository now includes:

1. A custom integration (`custom_components/vimar_viewapp`) that controls Vimar shades/scenarios through the official Android app UI.
2. A Home Assistant add-on (`addons/vimar_android_emulator`) that runs an Android emulator with ADB, so the integration has a built-in Android target.

## Repository layout

- `custom_components/vimar_viewapp`: Home Assistant integration code.
- `addons/vimar_android_emulator`: Home Assistant add-on (Dockerfile included).
- `docs/android_emulator_setup.md`: detailed emulator setup alternatives.
- `deployment/docker-compose.emulator.yml`: standalone sidecar deployment option.

---

## Install the add-on + integration (recommended)

### 1) Add this repository as an Add-on repository

In Home Assistant:
- **Settings → Add-ons → Add-on Store → ⋮ → Repositories**
- Add this git repository URL.

### 2) Install and start add-on: `Vimar Android Emulator (ADB)`

- Open add-on page and install.
- Enable **Start on boot**.
- Start add-on.
- Open emulator UI: `http://<HA_HOST>:6080`.
- Install/open Vimar View app in emulator and complete first login.

### 3) Install integration files

Copy folder:

- `custom_components/vimar_viewapp` → `<HA_CONFIG>/custom_components/vimar_viewapp`

Restart Home Assistant.

### 4) Configure integration

- **Settings → Devices & Services → Add Integration → Vimar View App (Android Bridge)**
- Provide:
  - ADB host (`<HA_HOST>` or add-on container hostname reachable by HA)
  - ADB port `5555`
  - Vimar username/password
  - optional app PIN
  - polling interval

---

## Add-on implementation details

The add-on is defined by:

- `addons/vimar_android_emulator/config.yaml`
- `addons/vimar_android_emulator/Dockerfile`
- `addons/vimar_android_emulator/run.sh`
- `addons/vimar_android_emulator/build.yaml`

It uses Android emulator image `budtmo/docker-android:emulator_13.0` and exposes ADB on `5555`.

## Features exposed by integration

- `cover` entities for shades.
- `sensor` entities for `position`, `battery`, `signal` (if visible in app UI).
- `button` entities for Vimar scenarios.

## Limitations

- UI automation depends on Vimar app layout/localization; selector updates may be needed when app UI changes.
- Emulator performance requires virtualization support (`/dev/kvm`).


## Emulator persistence on restart

Yes — in the add-on, emulator and app data are configured to persist in Home Assistant add-on `/data`:

- `/data/android-home`
- `/data/.android`
- `/data/.android/avd`

So installed apps (including Vimar View) and emulator state survive Home Assistant/add-on restarts.
