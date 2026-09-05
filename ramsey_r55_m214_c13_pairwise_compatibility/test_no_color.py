#!/usr/bin/env python3
"""Deterministic rejection tests for check_no_color.py."""
from __future__ import annotations
import json,subprocess,sys,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/"no_color_certificate.json").read_text(encoding="ascii"))
CASES=[]
for name,mutate in (
    ("multiplicity",lambda d:d.__setitem__("multiplicity",1)),
    ("cell",lambda d:d.__setitem__("cell","O")),
    ("red_edge",lambda d:d.__setitem__("red_core_edge",[1,8])),
    ("blue_triple",lambda d:d.__setitem__("blue_core_triple",[0,2,5])),
    ("source_hash",lambda d:d.__setitem__("source_certificate_sha256","0"*64)),
):
    copy=json.loads(json.dumps(BASE));mutate(copy);CASES.append((name,copy))
with tempfile.TemporaryDirectory() as temporary:
    for name,data in CASES:
        path=Path(temporary)/(name+".json");path.write_text(json.dumps(data),encoding="ascii")
        run=subprocess.run([sys.executable,str(ROOT/"check_no_color.py"),str(path)],capture_output=True,text=True)
        if run.returncode==0:raise AssertionError((name,"accepted"))
print("PASS rejected_corruptions=5")
