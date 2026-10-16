#!/usr/bin/env bash
# Build the unmodified REA checkout with its pinned Node/npm toolchain.
set -euo pipefail
node_dir=/workspace/rea-tools/node-v24.18.0-linux-x64
archive=/workspace/rea-tools/downloads/node-v24.18.0-linux-x64.tar.xz
digest=55aa7153f9d88f28d765fcdad5ae6945b5c0f98a36881703817e4c450fa76742
mkdir -p /workspace/rea-tools/downloads
if ! test -f "$archive"; then
    curl --fail --location --retry 3 --output "$archive.part" \
        https://nodejs.org/dist/v24.18.0/node-v24.18.0-linux-x64.tar.xz
    printf '%s  %s\n' "$digest" "$archive.part" | sha256sum --check --status
    mv "$archive.part" "$archive"
fi
printf '%s  %s\n' "$digest" "$archive" | sha256sum --check
if ! test -x "$node_dir/bin/node"; then
    tar -xJf "$archive" -C /workspace/rea-tools
fi
export PATH="$node_dir/bin:$PATH"
test "$(node --version)" = v24.18.0
cd /workspace/rea
test "$(git rev-parse --verify HEAD^{commit})" = b9b3a9098b072313119eccb3ae574faa57c3e517
test "$(cat .nvmrc)" = 24.18.0
test "$(node -p 'JSON.parse(require("fs").readFileSync("package.json")).packageManager')" = npm@11.16.0
HUSKY=0 npx --yes --cache /workspace/.npm-cache npm@11.16.0 ci --cache /workspace/.npm-cache --no-audit --no-fund
HUSKY=0 npx --yes --cache /workspace/.npm-cache npm@11.16.0 run build
source /workspace/ghidra-tools/env.sh
node scripts/rea.mjs doctor --provider ghidra --format json > /workspace/ghidra-tools/doctor-source-pinned.json
python3 - /workspace/ghidra-tools/doctor-source-pinned.json <<'PY_CHECK'
import json, sys
report=json.load(open(sys.argv[1]))
assert report['healthy'] and all(check['ok'] for check in report['scope_checks']), 'REA Ghidra readiness failed; inspect the saved doctor report'
PY_CHECK
