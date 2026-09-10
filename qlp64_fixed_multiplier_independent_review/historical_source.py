"""Export eight hash-pinned historical files for forensic queue replay only."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

COMMIT = '005c8e773d178e0fb050261885ecfd445bfe8de3'
ROOT = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    raise SystemExit('usage: python3 historical_source.py TEMPORARY_OUTPUT_DIRECTORY')
out = Path(sys.argv[1]).resolve()
repo = ROOT.parent
if out == repo or repo in out.parents:
    raise SystemExit('historical replay files must be outside the repository')
out.mkdir(parents=True, exist_ok=True)
hashes = json.loads((ROOT/'source_hashes.json').read_text())
for name, digest in hashes.items():
    if Path(name).name != name:
        raise RuntimeError('unexpected source path')
    data = subprocess.check_output(['git', 'show', f'{COMMIT}:qlp64_fixed_multiplier_exclusion/{name}'], cwd=repo)
    if hashlib.sha256(data).hexdigest() != digest:
        raise RuntimeError(f'historical source hash mismatch: {name}')
    (out/name).write_bytes(data)
print(json.dumps({'historical_commit': COMMIT, 'files_verified': len(hashes),
                  'scope': 'withdrawn source; queue replay only'}, sort_keys=True))
