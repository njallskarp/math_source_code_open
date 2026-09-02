#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
result_file="$(mktemp)"
trap 'rm -f "$result_file"' EXIT

python3 verify_per_family_gram.py >"$result_file"
diff -u expected_output.txt "$result_file"
shasum -a 256 -c SHA256SUMS
echo "package=verified"
