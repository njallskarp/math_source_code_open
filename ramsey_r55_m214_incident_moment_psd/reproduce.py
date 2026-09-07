#!/usr/bin/env python3
"""Regenerate the complete incident PSD survivor and its mixed-edge separating square."""
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
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('work',type=Path);parser.add_argument('--soplex',default='soplex');args=parser.parse_args();work=args.work.resolve()
    require(work!=REPO and REPO not in work.parents,'generated state must be outside source checkout')
    for name,digest in PINS.items():require(hashlib.sha256((REPO/name).read_bytes()).hexdigest()==digest,'changed generator '+name)
    work.mkdir(parents=True,exist_ok=False)
    def run(script,*arguments):return subprocess.check_output([sys.executable,'-B',str(script),*map(str,arguments)],text=True)
    link_source=REPO/'ramsey_r55_m214_postcut_selector_fiber/emit_links.py'
    require(hashlib.sha256(link_source.read_bytes()).hexdigest()=='ccb5be69e24b19b1ec01ca648f9397f9e905f3b0091f85ba181b8acbf19f5659','changed anchor-link generator')
    run(link_source,'--output',work/'anchor-links.opbpart')
    run(HERE/'emit_forbidden.py','--output',work/'forbidden.opbpart')
    run(HERE/'emit_degree.py','--output',work/'degree-separator.opbpart','--witness-only')
    paths={h:work/f'm214-{h}.opb' for h in (3160,3228,3254,3274,3323)}
    log=[]
    log.append(run(REPO/'ramsey_r55_m214_integrated_pair_roots/generate_opb.py','--output',paths[3160]))
    log.append(run(REPO/'ramsey_r55_m214_all_c_footprint_bound/build.py','--prior-opb',paths[3160],'--output-opb',paths[3228]));paths[3160].unlink()
    log.append(run(REPO/'ramsey_r55_m214_blue_pair_footprints/build.py','--prior-opb',paths[3228],'--output-opb',paths[3254]));paths[3228].unlink()
    log.append(run(REPO/'ramsey_r55_m214_pair_cell_c5_lift/build.py','--certificate',work/'pair-roots.tsv','--suffix',work/'pair.opbpart','--prior-opb',paths[3254],'--output-opb',paths[3274]));paths[3254].unlink()
    log.append(run(REPO/'ramsey_r55_m214_pair_column_hull/build.py','--certificate',work/'column-roots.tsv','--suffix',work/'column.opbpart','--prior-opb',paths[3274],'--output-opb',paths[3323]));paths[3274].unlink()
    (work/'generation.log').write_text(''.join(log));print('complete parent regenerated',file=sys.stderr,flush=True)
    run(HERE/'emit_deficiency.py','--output',work/'deficiency-separator.opbpart')
    run(HERE/'emit_square.py','--output',work/'square.opbpart')
    run(HERE/'emit_mixed.py','--output',work/'mixed-square.opbpart')
    run(HERE/'discover.py','--base',paths[3323],'--work',work,'--soplex',args.soplex)
    print('exact candidate regenerated',file=sys.stderr,flush=True)
    controls=run(HERE/'controls.py','--certificate',work/'certificate.json','--links',work/'anchor-links.opbpart','--forbidden',work/'forbidden.opbpart','--degree-separator',work/'degree-separator.opbpart','--deficiency-separator',work/'deficiency-separator.opbpart','--square',work/'square.opbpart','--mixed-square',work/'mixed-square.opbpart')
    require(controls==(HERE/'EXPECTED_CONTROLS.json').read_text(),'controls changed');(work/'controls.json').write_text(controls)
    result=run(HERE/'check.py','--certificate',work/'certificate.json','--opb',paths[3323],'--links',work/'anchor-links.opbpart','--forbidden',work/'forbidden.opbpart','--degree-separator',work/'degree-separator.opbpart','--deficiency-separator',work/'deficiency-separator.opbpart','--square',work/'square.opbpart','--mixed-square',work/'mixed-square.opbpart')
    require(result==(HERE/'EXPECTED_RESULT.json').read_text(),'complete result changed: '+result)
    (work/'result.json').write_text(result)
    independent=run(HERE/'independent_matrix.py',work/'certificate.json')
    require(independent==(HERE/'EXPECTED_INDEPENDENT.json').read_text(),'independent scalar changed');(work/'independent.json').write_text(independent)
    (work/'nine-cuts.opbpart').write_text(''.join(f'-1 x{13245+r} >= 0 ;\n' for r in (48,128,129,201,202,299,300,375,376)))
    print(result,end='')

if __name__=='__main__':main()
