#!/usr/bin/env bash
set -euo pipefail

directory=$(cd "$(dirname "$0")" && pwd)
repository=$(cd "$directory/.." && pwd)
manifest="$directory/pi4_witnesses.tsv"
frontier="$repository/qlp42_q5_q37_binary_frontier/frontier_orbits.tsv"
build=$(mktemp -d "${TMPDIR:-/tmp}/qlp42-pi4-verify.XXXXXX")
trap 'rm -rf "$build"' EXIT

python3 "$directory/verify_pi4_witnesses.py" "$manifest"
python3 "$directory/verify_pi4_manifest_stats.py"

if command -v g++-16 >/dev/null 2>&1; then
  compiler=$(command -v g++-16)
else
  compiler=${CXX:-c++}
fi

"$compiler" -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  "$directory/verify_pi4_witnesses.cpp" -o "$build/verify-release"
"$build/verify-release" "$frontier" "$manifest"

"$compiler" -std=c++20 -O1 -g -Wall -Wextra -Wpedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  "$directory/verify_pi4_witnesses.cpp" -o "$build/verify-sanitized"
ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 \
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 \
  "$build/verify-sanitized" "$frontier" "$manifest"

echo "pi4_certificate_checks=passed"
