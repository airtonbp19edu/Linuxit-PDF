#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
mkdir -p dist/presentation-monitor-diagnostics
# Xvfb's heads share an origin; GTK can collapse them into one monitor.
# Xephyr supplies two non-overlapping Xinerama heads on the virtual host.
Xephyr -help >dist/presentation-monitor-diagnostics/xephyr-help.txt 2>&1 || true
Xephyr :93 -noreset -nolisten tcp -ac +xinerama -extension RANDR \
  -origin 0,0 -screen 1280x800 -origin 1280,0 -screen 1024x768 \
  >dist/presentation-monitor-diagnostics/xephyr.log 2>&1 &
nested=$!
wm=''
trap 'if [[ -n "$wm" ]]; then kill "$wm" 2>/dev/null || true; fi; kill "$nested" 2>/dev/null || true' EXIT
export DISPLAY=:93
ready=0
for attempt in {1..100}; do
  if xdpyinfo >dist/presentation-monitor-diagnostics/display.txt 2>&1; then ready=1; break; fi
  kill -0 "$nested"
  sleep .1
done
[[ "$ready" == 1 ]]
xdpyinfo -ext XINERAMA >dist/presentation-monitor-diagnostics/xinerama.txt
openbox --sm-disable >dist/presentation-monitor-diagnostics/openbox.log 2>&1 &
wm=$!
/usr/bin/python3 scripts/check_presentation_monitors.py dist/presentation-monitors
