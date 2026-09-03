#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 derive_collision_rigidity.py > derived_output.txt
python3 derive_fiber_trade_counterexample.py > fiber_trade_derived_output.txt
{
    python3 verify_collision_rigidity.py
    python3 verify_fiber_trade_counterexample.py
} | tee actual_output.txt
diff -u expected_output.txt actual_output.txt
python3 - <<'PY'
from pathlib import Path
import hashlib

names = [
    "README.md",
    "FIBER_TRADE_COUNTEREXAMPLE.md",
    "derive_collision_rigidity.py",
    "derive_fiber_trade_counterexample.py",
    "verify_collision_rigidity.py",
    "verify_fiber_trade_counterexample.py",
    "collision_rigidity_certificate.json",
    "fiber_trade_counterexample.json",
    "expected_output.txt",
    "verify.sh",
]
lines = [f"{hashlib.sha256(Path(name).read_bytes()).hexdigest()}  {name}" for name in names]
Path("SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
rm -f actual_output.txt derived_output.txt fiber_trade_derived_output.txt
echo "reproduction=verified"
