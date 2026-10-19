#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
mkdir -p dist/presentation-monitor-diagnostics
# GTK3 enumerates RandR outputs, not Xinerama heads. The CI-only dummy
# Xorg server is launched by the container; this script is unprivileged.
wm=''
trap 'if [[ -n "$wm" ]]; then kill "$wm" 2>/dev/null || true; fi' EXIT
export DISPLAY=:93
ready=0
for attempt in {1..100}; do
  if xdpyinfo >dist/presentation-monitor-diagnostics/display.txt 2>&1; then ready=1; break; fi
  sleep .1
done
[[ "$ready" == 1 ]]
xrandr --query >dist/presentation-monitor-diagnostics/randr-before.txt
xrandr --addmode DUMMY1 1024x768
xrandr --output DUMMY0 --mode 1280x800 --pos 0x0 --primary \
  --output DUMMY1 --mode 1024x768 --pos 1280x0
xrandr --listmonitors >dist/presentation-monitor-diagnostics/randr-after.txt
openbox --sm-disable >dist/presentation-monitor-diagnostics/openbox.log 2>&1 &
wm=$!
export LINUXIT_CI_DUMMY_HOTPLUG=1
/usr/bin/python3 scripts/check_presentation_monitors.py dist/presentation-monitors
