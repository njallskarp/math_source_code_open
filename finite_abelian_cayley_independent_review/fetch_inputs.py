#!/usr/bin/env python3
"""Fetch three hash-pinned public data files; never import or execute them."""
import hashlib
import json
from pathlib import Path
import sys
from urllib.request import urlopen

manifest = json.loads(Path(__file__).with_name('inputs.json').read_text())
if len(sys.argv) != 2:
    raise SystemExit('usage: python3 fetch_inputs.py /tmp/abelian-review-inputs')
destination = Path(sys.argv[1])
destination.mkdir(parents=True, exist_ok=True)
base = 'https://raw.githubusercontent.com/{repository}/{commit}/{directory}/'.format(**manifest)
for name, expected in manifest['sha256'].items():
    data = urlopen(base + name, timeout=60).read()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('input hash mismatch: ' + name)
    (destination / name).write_bytes(data)
print('Fetched and hash-verified three public data files.')
