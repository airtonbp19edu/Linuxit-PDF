#!/usr/bin/env bash
# Optional direct-backend cross-check; output is not REA MCP Evidence.
set -euo pipefail
if test "$#" -ne 3; then
    echo 'Usage: analyze_foxit_headless.sh FoxitPDFReader.exe seeds.tsv new-output-directory' >&2
    exit 2
fi
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
foxit_file="$(realpath -- "$1")"
seed_file="$(realpath -- "$2")"
session_dir="$(realpath -m -- "$3")"
printf '%s  %s\n' 90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6 "$foxit_file" | sha256sum --check
test ! -e "$session_dir"
mkdir -p "$session_dir/project"
source /workspace/ghidra-tools/env.sh
python3 - "$foxit_file" "$seed_file" "$session_dir" <<'PY'
import hashlib, json, sys
from pathlib import Path
target, seeds, output = map(Path, sys.argv[1:])
(output / 'source.json').write_text(json.dumps({
    'target': str(target), 'source_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    'seeds_sha256': hashlib.sha256(seeds.read_bytes()).hexdigest(),
    'mode': 'Direct Ghidra headless -noanalysis, using the REA seed script; not MCP Evidence',
    'limitations': 'Decompiler success does not prove recovered types, complete boundaries, behavior or Linux equivalence.',
}, indent=2) + '\n')
PY
"$GHIDRA_INSTALL_DIR/support/analyzeHeadless" "$session_dir/project" foxit-selected \
    -import "$foxit_file" -noanalysis \
    -scriptPath "$script_dir/ghidra;/workspace/rea/bridge/ghidra" \
    -preScript ReaGhidraApplySeeds.java "$seed_file" \
    -postScript FoxitSelectedFunctions.java "$seed_file" "$session_dir/functions" \
    -log "$session_dir/ghidra.log" -scriptlog "$session_dir/script.log"
printf '%s  %s\n' 90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6 "$foxit_file" | sha256sum --check
