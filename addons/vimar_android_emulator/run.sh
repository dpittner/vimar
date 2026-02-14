#!/usr/bin/env bash
set -euo pipefail

OPTIONS_FILE="/data/options.json"
DEVICE_DEFAULT="Samsung Galaxy S10"
EMULATOR_ARGS_DEFAULT="-no-audio -no-boot-anim -gpu swiftshader_indirect"

if [ -f "$OPTIONS_FILE" ]; then
  DEVICE="$(python - <<'PY'
import json
from pathlib import Path
p=Path('/data/options.json')
obj=json.loads(p.read_text()) if p.exists() else {}
print(obj.get('device', 'Samsung Galaxy S10'))
PY
)"
  EMULATOR_ARGS="$(python - <<'PY'
import json
from pathlib import Path
p=Path('/data/options.json')
obj=json.loads(p.read_text()) if p.exists() else {}
print(obj.get('emulator_args', '-no-audio -no-boot-anim -gpu swiftshader_indirect'))
PY
)"
else
  DEVICE="$DEVICE_DEFAULT"
  EMULATOR_ARGS="$EMULATOR_ARGS_DEFAULT"
fi

# Persist Android emulator/user data under Home Assistant add-on /data.
# /data is retained across add-on and Home Assistant restarts.
export DEVICE
export EMULATOR_ARGS
export WEB_VNC=true
export HOME="/data/android-home"
export ANDROID_EMULATOR_HOME="/data/.android"
export ANDROID_SDK_HOME="/data/.android"
export ANDROID_AVD_HOME="/data/.android/avd"

mkdir -p "$HOME" "$ANDROID_EMULATOR_HOME" "$ANDROID_AVD_HOME"

# Ensure common home paths used by base image point to persistent storage.
if [ -d /home/androidusr ]; then
  mkdir -p /home/androidusr
  rm -rf /home/androidusr/.android
  ln -s "$ANDROID_EMULATOR_HOME" /home/androidusr/.android
fi

echo "Starting Android emulator with DEVICE=${DEVICE}"
echo "Persistent storage: AVD and app data in ${ANDROID_AVD_HOME}"

action_failed=true
for candidate in /entrypoint.sh /docker-android.sh /home/androidusr/docker-android/docker_run.sh; do
  if [ -x "$candidate" ]; then
    action_failed=false
    exec "$candidate"
  fi
done

if [ "$action_failed" = true ]; then
  echo "No known docker-android entrypoint found in image." >&2
  echo "Inspect container and update addons/vimar_android_emulator/run.sh accordingly." >&2
  sleep infinity
fi
