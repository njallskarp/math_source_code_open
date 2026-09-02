#!/usr/bin/env bash
set -euo pipefail

artifact_dir="$(cd "$(dirname "$0")" && pwd)"
research_tmp="$(mktemp -d)"
trap 'rm -rf "$research_tmp"' EXIT
research_cxx="${CXX:-g++}"

cd "$artifact_dir"
shasum -a 256 -c SHA256SUMS

python3 verify_binary_frontier.py >"$research_tmp/python.txt"
diff -u verification_python.txt "$research_tmp/python.txt"

"$research_cxx" -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  -Wconversion -Wsign-conversion verify_binary_frontier.cpp \
  -o "$research_tmp/verify_binary_frontier"
"$research_tmp/verify_binary_frontier" >"$research_tmp/cpp.txt"
diff -u verification_cpp.txt "$research_tmp/cpp.txt"

"$research_cxx" -std=c++20 -O1 -g -Wall -Wextra -Wpedantic \
  -Wconversion -Wsign-conversion -fsanitize=address,undefined \
  -fno-omit-frame-pointer verify_binary_frontier.cpp \
  -o "$research_tmp/verify_binary_frontier_san"
ASAN_OPTIONS=detect_leaks=1 \
  "$research_tmp/verify_binary_frontier_san" >"$research_tmp/cpp_san.txt"
diff -u verification_cpp.txt "$research_tmp/cpp_san.txt"

echo "verification=passed"
