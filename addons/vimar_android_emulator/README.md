# Vimar Android Emulator (ADB) Home Assistant Add-on

This add-on runs an Android emulator inside Home Assistant add-on infrastructure and exposes:

- `5555/tcp` for ADB (used by `custom_components/vimar_viewapp`)
- `6080/tcp` for web VNC access to interact with emulator UI

## What this add-on is for

Use it as the Android runtime for the Vimar View App integration, so you only need Vimar app credentials.

## Installation

1. In Home Assistant, go to **Settings → Add-ons → Add-on Store → ⋮ → Repositories**.
2. Add this repository URL.
3. Install **Vimar Android Emulator (ADB)**.
4. Enable **Start on boot** and start the add-on.
5. Open `http://<home-assistant-host>:6080`.
6. Install/login to the Vimar View App inside emulator.
7. Configure the `vimar_viewapp` integration with:
   - ADB host: `homeassistant` (if same HA host networking allows) or your HA host IP
   - ADB port: `5555`

## Configuration options

- `device`: Android profile name (default: `Samsung Galaxy S10`)
- `emulator_args`: extra emulator flags

## Notes

- Requires CPU virtualization support (`/dev/kvm`) for acceptable performance.
- This add-on is currently targeted at `amd64`.
- Keep ADB port accessible only on trusted networks.
