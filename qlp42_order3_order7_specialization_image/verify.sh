#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
result_file="$(mktemp)"
trap 'rm -f "$result_file"' EXIT

{
  echo "verify_specialization_image.py"
  python3 verify_specialization_image.py
  echo
  echo "derive_with_sympy.py"
  python3 derive_with_sympy.py
} >"$result_file"

diff -u expected_output.txt "$result_file"
python3 -m json.tool graph_receipt.json >/dev/null
shasum -a 256 -c SHA256SUMS
echo "package=verified"
