# Android emulator setup for Home Assistant + Vimar View App

This integration controls Vimar through the official Android app, so you must provide an Android runtime reachable over ADB.

## Option A (recommended): Sidecar emulator with Docker Compose

Use `deployment/docker-compose.emulator.yml` on the same host where Home Assistant runs.

```bash
docker compose -f deployment/docker-compose.emulator.yml up -d
```

Then:
1. Open emulator UI at `http://<host>:6080`.
2. Install the Vimar View app (Play Store/APK).
3. Complete first login manually in the emulator.
4. In Home Assistant integration config:
   - **ADB host**: hostname/IP where emulator container is reachable from HA.
   - **ADB port**: `5555`.
   - **Serial**: optional (`<host>:5555`).

## Option B: Android Studio emulator on another machine

1. Create and start an Android Virtual Device.
2. Enable ADB TCP:
   ```bash
   adb tcpip 5555
   adb connect <emulator-host>:5555
   ```
3. Use `<emulator-host>` and `5555` in Home Assistant integration config.

## Option C: Physical Android device

1. Enable Developer Options + USB debugging.
2. Pair/connect ADB over network.
3. Use the device ADB endpoint in integration config.

## Home Assistant deployment notes

- **Home Assistant Container / Supervised**: sidecar emulator is feasible on the host.
- **Home Assistant OS on low-power hardware**: emulator may be too heavy. Use Option B (remote emulator/desktop) and point HA to remote ADB.
- Keep emulator/device unlocked and app session active for best reliability.

## Security

- ADB endpoint grants high control of the Android runtime; isolate it on trusted network segments.
- Do not expose ADB port 5555 publicly.
