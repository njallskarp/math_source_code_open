#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
result_file="$(mktemp)"
trap 'rm -f "$result_file"' EXIT

python3 verify_shifted_gram_completion.py >"$result_file"
diff -u expected_output.txt "$result_file"
python3 -m json.tool completion_certificate.json >/dev/null
python3 -m json.tool graph_receipt.json >/dev/null
shasum -a 256 -c SHA256SUMS
echo "package=verified"
