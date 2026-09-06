#!/usr/bin/env python3
"""Regenerate and independently replay all eight native UNSAT proofs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('work',type=Path)
    for name in ('cadical','drat-trim','lrat-check'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();work=args.work.resolve()
    require(work!=REPO and REPO not in work.parents,'generated state must be outside source checkout')
    binaries={name:getattr(args,name.replace('-','_')).resolve() for name in ('cadical','drat-trim','lrat-check')}
    require(all(path.is_file() for path in binaries.values()),'native executable missing')
    parent=REPO/'ramsey_r55_m214_integrated_pair_roots/generate_opb.py'
    root=REPO/'ramsey_r55_m214_pair_normalization/pair_roots.py'
    require(sha(parent)=='e6b26db8a05ee7c246b431b185bee2543697c2a7a720154bea70dfa2e10c8a08','pinned parent generator')
    require(sha(root)=='8fdccc44cab88d462cc122c055a9c54cffbefc957a73b6eeff84aa57a9e2256e','pinned root source')
    work.mkdir(parents=True,exist_ok=False)
    def run(script,*arguments):return subprocess.check_output([sys.executable,'-B',str(script),*map(str,arguments)],text=True)
    (work/'parent-generation.json').write_text(run(parent,'--output',work/'parent.opb'))
    encoded=run(HERE/'encode.py',work)
    require(encoded==(HERE/'EXPECTED_CASES.json').read_text(),'encoded cases changed')
    audit=run(HERE/'audit.py','--opb',work/'parent.opb','--cnfs',work)
    require(audit==(HERE/'EXPECTED_AUDIT.json').read_text(),'semantic audit changed')
    (work/'audit.json').write_text(audit)
    controls=run(HERE/'controls.py','--cnfs',work,'--drat-trim',binaries['drat-trim'])
    require(controls==(HERE/'EXPECTED_CONTROLS.json').read_text(),'controls changed')
    (work/'controls.json').write_text(controls)
    proof_index=[]
    for i in range(8):
        cnf=work/f'case-{i}.cnf';drat=work/f'case-{i}.drat';lrat=work/f'case-{i}.lrat'
        start=time.monotonic()
        log=work/f'case-{i}-solver.log'
        with log.open('w') as handle:
            result=subprocess.run([str(binaries['cadical']),'--no-binary',str(cnf),str(drat)],stdout=handle,stderr=subprocess.STDOUT)
        require(result.returncode==20 and 's UNSATISFIABLE' in log.read_text(),'native run did not produce UNSAT trace')
        drat_log=work/f'case-{i}-drat-check.log'
        with drat_log.open('w') as handle:
            result=subprocess.run([str(binaries['drat-trim']),str(cnf),str(drat),'-L',str(lrat)],stdout=handle,stderr=subprocess.STDOUT)
        require(result.returncode==0 and '\ns VERIFIED\n' in drat_log.read_text(),'DRAT proof rejected')
        lrat_log=work/f'case-{i}-lrat-check.log'
        with lrat_log.open('w') as handle:
            result=subprocess.run([str(binaries['lrat-check']),str(cnf),str(lrat)],stdout=handle,stderr=subprocess.STDOUT)
        require(result.returncode==0 and '\nc VERIFIED\n' in lrat_log.read_text(),'LRAT proof rejected')
        proof_index.append({'case':i,'cnf_sha256':sha(cnf),'drat_sha256':sha(drat),'lrat_sha256':sha(lrat),
                            'drat_bytes':drat.stat().st_size,'lrat_bytes':lrat.stat().st_size,
                            'seconds':round(time.monotonic()-start,3),'drat_verified':True,'lrat_verified':True})
        print('checked case '+str(i),file=sys.stderr,flush=True)
    (work/'proof-index.json').write_text(json.dumps(proof_index,indent=2)+'\n')
    (work/'native-tools.json').write_text(json.dumps({name:{'path':str(path),'sha256':sha(path)} for name,path in binaries.items()},indent=2)+'\n')
    cuts=''.join(f'-1 x{13245+r} >= 0 ;\n' for r in (48,128,129,201,202,299,300,376))
    (work/'new-cuts.opbpart').write_text(cuts)
    result={'status':'VERIFIED_COMPLETE_M214_C13_K0_WEIGHTED_CELL_EXCLUSION_WITH_CATALOG_IMPORT',
            'native_drat_proofs':8,'native_lrat_proofs':8,'physical_source_rows':59409,
            'current_excluded_roots':[48,128,129,201,202,299,300,376],
            'new_excluded_roots':[48,128,129,201,202,299,300],
            'cumulative_excluded_roots':[48,128,129,201,202,299,300,375,376],
            'residual_descriptors':380,'residual_counts':[59,83,68,102,68],
            'weighted_cell_upper_bound':24,'farkas_rhs':-1,'accepted_P4_cell_slacks':['-1','-1'],
            'catalog_completeness':'IMPORTED_PRIMARY_SOURCE','prior_root375':'IMPORTED_REVIEWED_EXCLUSION',
            'certificate_sha256':sha(HERE/'certificate.json')}
    output=json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    require(output==(HERE/'EXPECTED_RESULT.json').read_text(),'final result changed')
    (work/'result.json').write_text(output);print(output,end='')

if __name__=='__main__':main()
