#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
results="$PWD/dist/stage21-results"
mkdir -p "$results"
export PYTHONUTF8=1
/usr/bin/python3 scripts/run_tests.py --pattern test_delivery_audit.py \
  --output "$results/auditor-controls.json" >"$results/auditor-controls.log" 2>&1
bundle="$(/usr/bin/python3 scripts/fetch_delivery_bundle.py --all)"
/usr/bin/python3 scripts/audit_delivery.py --output "$results/repository-audit.json"
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user --noninteractive -y --no-related flathub org.freedesktop.Platform//25.08 \
  >"$results/runtime-install.log" 2>&1
flatpak install --user --noninteractive -y --no-related "$bundle" >"$results/app-install.log" 2>&1
app=io.github.airtonbp19edu.LinuxitPDF//devel
deployment="$(flatpak info --user --show-location "$app")"
/usr/bin/python3 scripts/audit_delivery.py --installed-root "$deployment/files" \
  --output "$results/installed-delivery-audit.json"
openbox --sm-disable >"$results/openbox.log" 2>&1 &
window_manager=$!
trap 'kill "$window_manager" 2>/dev/null || true' EXIT
flatpak run --user --filesystem="$PWD/scripts:ro" --env=PRINT_VIEW_TEST_APP=/app/share/linuxit-pdf \
  --command=linuxit-python "$app" "$PWD/scripts/smoke_linuxit.py" \
  >"$results/published-bundle-smoke.json" 2>"$results/published-bundle-smoke.log"
/usr/bin/python3 -c 'import json,sys; r=json.load(open(sys.argv[1])); assert r["passed"] is True and r["inside_flatpak"] is True and len(r["checks"])==5 and all(r["checks"].values()) and not r["errors"]' \
  "$results/published-bundle-smoke.json"
# Exercise the corrected session-readiness wait against the same published
# bundle. This is a focused additional check, never a replacement full suite.
flatpak run --user --filesystem="$PWD:ro" --filesystem="$results:rw" \
  --env=PRINT_VIEW_TEST_APP=/app/share/linuxit-pdf --command=linuxit-python "$app" \
  "$PWD/scripts/run_tests.py" --app /app/share/linuxit-pdf --pattern test_sidebar_layout_gtk.py \
  --output "$results/sidebar-gtk-regression.json" >"$results/sidebar-gtk-regression.log" 2>&1
/usr/bin/python3 -c 'import json,sys; r=json.load(open(sys.argv[1])); assert r["run"]==r["passed"]==3 and all(r[k]==0 for k in ("failures","errors","skipped"))' \
  "$results/sidebar-gtk-regression.json"
