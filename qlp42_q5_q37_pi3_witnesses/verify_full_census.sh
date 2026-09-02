#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
frontier="$script_dir/../qlp42_q5_q37_binary_frontier/frontier_orbits.tsv"
build="$script_dir/build"
cxx=${CXX:-/opt/homebrew/bin/g++-16}

mkdir -p "$build"
test "$(shasum -a 256 "$frontier" | awk '{print $1}')" = \
  f1dff75420fb37a2454767a7177367045e100ab07a07a11addd5e5551407d89e
test "$(shasum -a 256 "$script_dir/full_witnesses.tsv" | awk '{print $1}')" = \
  283779dc06d031bf2a5f333dbb32c9cfa540313db8e4a82886caf7134fe8e8eb

python3 "$script_dir/verify_pi3_full_census.py" > "$build/full_python.txt"
diff -u "$script_dir/full_expected_summary.txt" "$build/full_python.txt"

"$cxx" -std=c++20 -O2 -Wall -Wextra -Wpedantic \
  "$script_dir/verify_pi3_full_census.cpp" -o "$build/verify_full_release"
"$build/verify_full_release" "$frontier" "$script_dir/full_witnesses.tsv" \
  > "$build/full_cpp.txt"
diff -u "$script_dir/full_expected_summary.txt" "$build/full_cpp.txt"

"$cxx" -std=c++20 -O1 -g -Wall -Wextra -Wpedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  "$script_dir/verify_pi3_full_census.cpp" -o "$build/verify_full_sanitized"
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 \
  "$build/verify_full_sanitized" "$frontier" "$script_dir/full_witnesses.tsv" \
  > "$build/full_cpp_sanitized.txt"
diff -u "$build/full_cpp.txt" "$build/full_cpp_sanitized.txt"

echo 'full_census_checks=passed'
