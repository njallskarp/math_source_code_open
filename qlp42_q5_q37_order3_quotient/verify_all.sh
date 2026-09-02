#!/usr/bin/env bash
set -euo pipefail

directory=$(cd "$(dirname "$0")" && pwd)
cd "$directory"

cxx=${CXX:-c++}
support=../qlp42_q5_q37_binary_frontier/frontier_orbits.tsv

"$cxx" -std=c++20 -O3 -Wall -Wextra -Wpedantic \
  generate_order3_lifts.cpp -o generate_order3_lifts

{
  ./generate_order3_lifts "$support" order3_lifts.regenerated.tsv
  cmp order3_lifts.tsv order3_lifts.regenerated.tsv
  python3 verify_order3_lifts.py
} | tee verification_output.txt

cmp expected_output.txt verification_output.txt
shasum -a 256 -c SHA256SUMS
