#!/usr/bin/env bash
set -euo pipefail
openbox --sm-disable >dist/desktop-results/openbox.log 2>&1 &
exec /usr/bin/python3 scripts/check_desktop_integrations.py "$@"
