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
print(obj.get('device','Samsung Galaxy S10'))
PY
)"
  EMULATOR_ARGS="$(python - <<'PY'
import json
from pathlib import Path
p=Path('/data/options.json')
obj=json.loads(p.read_text()) if p.exists() else {}
print(obj.get('emulator_args','-no-audio -no-boot-anim -gpu swiftshader_indirect'))
PY
)"
else
  DEVICE="$DEVICE_DEFAULT"
  EMULATOR_ARGS="$EMULATOR_ARGS_DEFAULT"
fi

export DEVICE
export EMULATOR_ARGS
export WEB_VNC=true

echo "Starting Android emulator with DEVICE=${DEVICE}"

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
