#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
results="$PWD/dist/ci-results"
mkdir -p "$results"
export PYTHONUTF8=1
export LINUXIT_SEARCH_CAPTURE_DIR="$results/search-ui"
export XDG_CONFIG_HOME="$PWD/analysis-local/ci-config"
export XDG_CACHE_HOME="$PWD/analysis-local/ci-cache"
openbox --sm-disable >"$results/openbox.log" 2>&1 &
window_manager=$!
trap 'kill "$window_manager" 2>/dev/null || true' EXIT

# Reproduce the previous own source under the same corrected geometry oracle.
mkdir -p analysis-local/sidebar-baseline
git archive 76d901e8007c4ced339492be7fb1f5e0081bff05 app | tar -x -C analysis-local/sidebar-baseline
PRINT_VIEW_TEST_APP="$PWD/analysis-local/sidebar-baseline/app" /usr/bin/python3 scripts/check_sidebar_layout.py \
  --observe-only --output "$results/sidebar-before.json" --screenshots "$results/sidebar-before"
/usr/bin/python3 scripts/check_sidebar_layout.py \
  --output "$results/sidebar-after.json" --screenshots "$results/sidebar-after"

/usr/bin/python3 scripts/check_intermediate.py --profile linux \
  --work-dir analysis-local/ci-source --output "$results/source-intermediate.json" \
  >"$results/source.log" 2>&1

overlay="$PWD/analysis-local/ci-runtime-overlay"
mkdir -p "$overlay/gi-cairo/usr/share/doc/python3-gi-cairo"
cp /usr/share/doc/python3-gi-cairo/copyright \
  "$overlay/gi-cairo/usr/share/doc/python3-gi-cairo/copyright"
stage="$PWD/analysis-local/ci-flatpak-stage"
/usr/bin/python3 scripts/build_flatpak.py --stage "$stage" \
  --repo "$PWD/analysis-local/ci-flatpak-repo" --extra-runtime "$overlay" \
  >"$results/build.log" 2>&1
/usr/bin/python3 scripts/record_linux_candidate.py integrity --payload "$stage/files/share/linuxit-pdf" \
  --output "$results/source-payload-integrity.json"
"$stage/files/bin/linuxit-python" scripts/run_tests.py --app "$stage/files/share/linuxit-pdf" \
  --output "$results/payload-tests.json" >"$results/payload-tests.log" 2>&1

flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user --noninteractive -y --no-related flathub org.freedesktop.Platform//25.08 \
  >"$results/runtime-install.log" 2>&1
version="$(/usr/bin/python3 -c 'import sys; sys.path.insert(0,"app"); from version import VERSION; print(VERSION)')"
bundle="$PWD/dist/LinuxitPDF-$version-x86_64.flatpak"
flatpak install --user --noninteractive -y --no-related "$bundle" >"$results/app-install.log" 2>&1
app=io.github.airtonbp19edu.LinuxitPDF//devel
flatpak run --user --filesystem="$PWD:ro" --filesystem="$results:rw" \
  --env=PRINT_VIEW_TEST_APP=/app/share/linuxit-pdf --command=linuxit-python "$app" \
  "$PWD/scripts/run_tests.py" --app /app/share/linuxit-pdf --output "$results/sandbox-tests.json" \
  >"$results/sandbox-tests.log" 2>&1
flatpak run --user --filesystem="$PWD:ro" --env=PRINT_VIEW_TEST_APP=/app/share/linuxit-pdf \
  --command=linuxit-python "$app" "$PWD/scripts/smoke_linuxit.py" \
  >"$results/sandbox-smoke.json" 2>"$results/sandbox-smoke.log"
LINUXIT_LAUNCH_RESULTS="$results" /usr/bin/python3 scripts/check_flatpak_launch.py \
  >"$results/launcher-check.log" 2>&1
/usr/bin/python3 scripts/record_linux_candidate.py finalize --reports "$results" --stage "$stage" \
  --artifact "$bundle" --output "$results/candidate.json"
