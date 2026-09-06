#!/usr/bin/env python3
"""Regenerate the complete retained base and check the exact selector fiber."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
PINS={
    'ramsey_r55_m214_integrated_pair_roots/generate_opb.py':'e6b26db8a05ee7c246b431b185bee2543697c2a7a720154bea70dfa2e10c8a08',
    'ramsey_r55_m214_all_c_footprint_bound/build.py':'bbdf1bb731478546bdb6a2fb9a03cbf50f51f9da5780d530b2e615685cecb6e2',
    'ramsey_r55_m214_blue_pair_footprints/build.py':'e988b27f1ec5f025828eb93a44c099b1a464a0ff2b2ccafffa912d6cfa745886',
    'ramsey_r55_m214_pair_cell_c5_lift/build.py':'e8e769e58c5ce34419a9f8bdb252e275aabd9b1ae2a69865efcd916d6e4b90e4',
    'ramsey_r55_m214_pair_column_hull/build.py':'b26267a40f252269ca235181533a8f31a0716b3d4195dde0c979961e45cd909d',
}


def require(ok,message):
    if not ok:raise ValueError(message)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('work',type=Path);args=parser.parse_args();work=args.work.resolve()
    require(work!=REPO and REPO not in work.parents,'generated state must be outside source checkout')
    for name,digest in PINS.items():require(hashlib.sha256((REPO/name).read_bytes()).hexdigest()==digest,'changed generator '+name)
    work.mkdir(parents=True,exist_ok=False)
    def run(script,*arguments):return subprocess.check_output([sys.executable,'-B',str(script),*map(str,arguments)],text=True)
    run(HERE/'construct.py','--output',work/'certificate.json')
    require((work/'certificate.json').read_bytes()==(HERE/'certificate.json').read_bytes(),'constructed certificate changed')
    run(HERE/'emit_links.py','--output',work/'anchor-links.opbpart')
    controls=run(HERE/'controls.py','--links',work/'anchor-links.opbpart')
    require(controls==(HERE/'EXPECTED_CONTROLS.json').read_text(),'controls changed');(work/'controls.json').write_text(controls)
    paths={h:work/f'm214-{h}.opb' for h in (3160,3228,3254,3274,3323)}
    log=[]
    log.append(run(REPO/'ramsey_r55_m214_integrated_pair_roots/generate_opb.py','--output',paths[3160]))
    log.append(run(REPO/'ramsey_r55_m214_all_c_footprint_bound/build.py','--prior-opb',paths[3160],'--output-opb',paths[3228]));paths[3160].unlink()
    log.append(run(REPO/'ramsey_r55_m214_blue_pair_footprints/build.py','--prior-opb',paths[3228],'--output-opb',paths[3254]));paths[3228].unlink()
    log.append(run(REPO/'ramsey_r55_m214_pair_cell_c5_lift/build.py','--certificate',work/'pair-roots.tsv','--suffix',work/'pair.opbpart','--prior-opb',paths[3254],'--output-opb',paths[3274]));paths[3254].unlink()
    log.append(run(REPO/'ramsey_r55_m214_pair_column_hull/build.py','--certificate',work/'column-roots.tsv','--suffix',work/'column.opbpart','--prior-opb',paths[3274],'--output-opb',paths[3323]));paths[3274].unlink()
    (work/'generation.log').write_text(''.join(log));print('complete parent regenerated',file=sys.stderr,flush=True)
    result=run(HERE/'check.py','--certificate',work/'certificate.json','--opb',paths[3323],'--links',work/'anchor-links.opbpart')
    require(result==(HERE/'EXPECTED_RESULT.json').read_text(),'complete result changed: '+result)
    (work/'result.json').write_text(result)
    (work/'nine-cuts.opbpart').write_text(''.join(f'-1 x{13245+r} >= 0 ;\n' for r in (48,128,129,201,202,299,300,375,376)))
    print(result,end='')

if __name__=='__main__':main()
