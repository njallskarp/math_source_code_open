#!/usr/bin/env python3
"""Regenerate the full parent stream and replay the exact root376 certificate."""
import argparse
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
PARENT_SHA='e6b26db8a05ee7c246b431b185bee2543697c2a7a720154bea70dfa2e10c8a08'
ROOT_SOURCE_SHA='8fdccc44cab88d462cc122c055a9c54cffbefc957a73b6eeff84aa57a9e2256e'


def require(ok,message):
    if not ok:raise ValueError(message)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('work',type=Path);args=parser.parse_args();work=args.work.resolve()
    require(work!=REPO and REPO not in work.parents,'generated state must be outside the source checkout')
    parent=REPO/'ramsey_r55_m214_integrated_pair_roots/generate_opb.py'
    root_source=REPO/'ramsey_r55_m214_pair_normalization/pair_roots.py'
    require(hashlib.sha256(parent.read_bytes()).hexdigest()==PARENT_SHA,'parent source changed')
    require(hashlib.sha256(root_source.read_bytes()).hexdigest()==ROOT_SOURCE_SHA,'root source changed')
    spec=importlib.util.spec_from_file_location('parent_roots',root_source);roots=importlib.util.module_from_spec(spec);spec.loader.exec_module(roots)
    key=('C77partition',13,0,'AB');require(list(roots.definitions()).index(key)==376,'root index')
    require(roots.canonical_bytes(roots.root(*key))==(HERE/'root.json').read_bytes(),'complete descriptor regeneration')
    work.mkdir(parents=True,exist_ok=False)
    def run(script,*arguments):
        return subprocess.check_output([sys.executable,'-B',str(script),*map(str,arguments)],text=True)
    (work/'parent-generation.json').write_text(run(parent,'--output',work/'parent.opb'))
    controls=run(HERE/'controls.py','--opb',work/'parent.opb');require(controls==(HERE/'EXPECTED_CONTROLS.json').read_text(),'control result changed')
    result=run(HERE/'audit.py','--opb',work/'parent.opb');require(result==(HERE/'EXPECTED_RESULT.json').read_text(),'proof result changed: '+result)
    (work/'cut.opbpart').write_text('-1 x13621 >= 0 ;\n')
    (work/'result.json').write_text(result);print(result,end='')

if __name__=='__main__':main()
