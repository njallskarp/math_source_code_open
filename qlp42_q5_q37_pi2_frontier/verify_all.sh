#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
frontier="$script_dir/../qlp42_q5_q37_binary_frontier/frontier_orbits.tsv"
build="$script_dir/build"
cxx=${CXX:-/opt/homebrew/bin/g++-16}

mkdir -p "$build"
test "$(shasum -a 256 "$frontier" | awk '{print $1}')" = \
  f1dff75420fb37a2454767a7177367045e100ab07a07a11addd5e5551407d89e

python3 "$script_dir/analyze_pi2_frontier.py" > "$build/python.txt"
grep '^q=.*;orbits=.*;rank=' "$build/python.txt" > "$build/python_summary.txt"
diff -u "$script_dir/expected_summary.txt" "$build/python_summary.txt"

"$cxx" -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  "$script_dir/verify_pi2_frontier.cpp" -o "$build/verify_release"
"$build/verify_release" "$frontier" > "$build/cpp.txt"
head -n 2 "$build/cpp.txt" > "$build/cpp_summary.txt"
diff -u "$script_dir/expected_summary.txt" "$build/cpp_summary.txt"
grep -qx 'independent_certificate=verified' "$build/cpp.txt"

"$cxx" -std=c++20 -O1 -g -Wall -Wextra -Wpedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  "$script_dir/verify_pi2_frontier.cpp" -o "$build/verify_sanitized"
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 \
  "$build/verify_sanitized" "$frontier" > "$build/cpp_sanitized.txt"
diff -u "$build/cpp.txt" "$build/cpp_sanitized.txt"

echo 'all_checks=passed'
