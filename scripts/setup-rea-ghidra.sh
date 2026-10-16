#!/usr/bin/env bash
# Local analysis tools only; no system install and no change to REA client settings.
# Ghidra digest: official NSA release asset; OpenJDK digests: signed Debian index.
set -euo pipefail
tools_dir=/workspace/ghidra-tools
mkdir -p "$tools_dir/downloads" "$tools_dir/cache" "$tools_dir/config" "$tools_dir/data" "$tools_dir/state"

fetch_checked() {
    local filename="$1" digest="$2" url="$3"
    local destination="$tools_dir/downloads/$filename"
    if ! test -f "$destination"; then
        curl --fail --location --retry 3 --output "$destination.part" "$url"
        printf '%s  %s\n' "$digest" "$destination.part" | sha256sum --check --status
        mv "$destination.part" "$destination"
    fi
    printf '%s  %s\n' "$digest" "$destination" | sha256sum --check
}

fetch_checked ghidra_12.1.4_PUBLIC_20260921.zip \
    ddac49f903da9d5bac833e5cc79395098b9c33cfd3279be5f31bd00387d2d4db \
    https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.1.4_build/ghidra_12.1.4_PUBLIC_20260921.zip

if ! test -x "$tools_dir/ghidra_12.1.4_PUBLIC/support/analyzeHeadless"; then
    python3 - "$tools_dir" <<'PY'
import stat, sys, zipfile
from pathlib import Path
root = Path(sys.argv[1]).resolve()
with zipfile.ZipFile(root / 'downloads/ghidra_12.1.4_PUBLIC_20260921.zip') as archive:
    if archive.testzip() is not None:
        raise SystemExit('Ghidra ZIP CRC failure')
    for item in archive.infolist():
        destination = (root / item.filename).resolve()
        if not destination.is_relative_to(root):
            raise SystemExit('Unsafe Ghidra ZIP path')
        mode = item.external_attr >> 16
        if stat.S_ISLNK(mode):
            raise SystemExit('Unexpected Ghidra ZIP symlink')
        archive.extract(item, root)
        if mode & 0o111 and destination.is_file():
            destination.chmod(destination.stat().st_mode | 0o111)
PY
fi

# The matching JRE and JDK are extracted together; javac is required by REA.
if ! test -x "$tools_dir/java/usr/lib/jvm/java-21-openjdk-amd64/bin/javac"; then
    fetch_checked 'openjdk-21-jre-headless_21.0.12.1+1-1~deb13u1_amd64.deb' \
        e95f36193e45464ac758e5436f940bf3eaecc77de67188275a42104f58aa7674 \
        'https://deb.debian.org/debian/pool/main/o/openjdk-21/openjdk-21-jre-headless_21.0.12.1+1-1~deb13u1_amd64.deb'
    fetch_checked 'openjdk-21-jdk-headless_21.0.12.1+1-1~deb13u1_amd64.deb' \
        f3abafb6c644b03df042824e707cd211ea33254761d7f7b75be3f8dc0df97c7a \
        'https://deb.debian.org/debian/pool/main/o/openjdk-21/openjdk-21-jdk-headless_21.0.12.1+1-1~deb13u1_amd64.deb'
    dpkg-deb --extract "$tools_dir/downloads/openjdk-21-jre-headless_21.0.12.1+1-1~deb13u1_amd64.deb" "$tools_dir/java"
    dpkg-deb --extract "$tools_dir/downloads/openjdk-21-jdk-headless_21.0.12.1+1-1~deb13u1_amd64.deb" "$tools_dir/java"
    # Debian's JRE configuration uses absolute links to /etc/java-21-openjdk.
    # Keep the extracted runtime independent of those host configuration files.
    python3 - "$tools_dir/java" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1])
for link in root.rglob('*'):
    if link.is_symlink():
        target = link.readlink()
        if str(target).startswith('/etc/java-21-openjdk/'):
            local = root / str(target).lstrip('/')
            if local.exists():
                link.unlink()
                link.symlink_to(local)
PY
fi

cat > "$tools_dir/env.sh" <<'EOF'
export GHIDRA_INSTALL_DIR=/workspace/ghidra-tools/ghidra_12.1.4_PUBLIC
export JAVA_HOME=/workspace/ghidra-tools/java/usr/lib/jvm/java-21-openjdk-amd64
export GHIDRA_HEADLESS_MAXMEM=8G
export REA_GHIDRA_STARTUP_TIMEOUT_MS=1800000
export REA_ANALYSIS_PROVIDER=ghidra
export XDG_CACHE_HOME=/workspace/ghidra-tools/cache
export XDG_CONFIG_HOME=/workspace/ghidra-tools/config
export XDG_DATA_HOME=/workspace/ghidra-tools/data
export XDG_STATE_HOME=/workspace/ghidra-tools/state
EOF
source "$tools_dir/env.sh"
"$JAVA_HOME/bin/java" -version
"$JAVA_HOME/bin/javac" -version
/workspace/.rea-cli/bin/rea doctor --provider ghidra --format json > "$tools_dir/doctor-ready.json"
python3 - "$tools_dir/doctor-ready.json" <<'PY_CHECK'
import json, sys
report=json.load(open(sys.argv[1]))
assert report['healthy'] and all(check['ok'] for check in report['scope_checks']), 'REA Ghidra readiness failed; inspect the saved doctor report'
PY_CHECK
printf 'REA doctor saved: %s/doctor-ready.json\n' "$tools_dir"
