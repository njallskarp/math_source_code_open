"""Discovery-only SAT search; any model requires a definition-level audit."""
import argparse
import base64
import itertools as it
import json
from pathlib import Path
import time

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


def decode(s):
    data = base64.b64decode(s)
    n = data[0] - 63
    bits = [(v - 63) >> k & 1 for v in data[1:] for k in range(5, -1, -1)]
    return n, {e for e, b in zip(((i, j) for j in range(1, n) for i in range(j)), bits) if b}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=int, default=60)
    args = ap.parse_args()
    start = time.monotonic()
    original = json.loads((Path(__file__).resolve().parent / 'WITNESS.json').read_text())
    _, H = decode(original['red_core_parent_graph6_base64'])
    H -= set(map(tuple, original['red_core_delete_edges']))
    _, J = decode(original['blue_core_graph6_base64'])
    v = 3
    if sum(v-1 in e for e in H) < 10:
        raise ValueError('ineligible partner')
    pool = IDPool()
    fixed, variables = {}, {}
    for a, b in it.combinations(range(43), 2):
        e = (a,b)
        if a == 0:
            fixed[e] = b <= 22
        elif b <= 22:
            fixed[e] = (a-1,b-1) in H
        elif a <= 22:
            variables[e] = pool.id(e)
        else:
            fixed[e] = (a-23,b-23) not in J
    clauses = []
    def prohibit(conditions):
        lits = set()
        for a,b,col in conditions:
            e = (min(a,b),max(a,b))
            if e in fixed:
                if fixed[e] != col:
                    return
            else:
                lit = -variables[e] if col else variables[e]
                if -lit in lits:
                    return
                lits.add(lit)
        clauses.append(sorted(lits))
    for root in (0,v):
        for color in (True,False):
            possible = [x for x in range(43) if x != root and fixed.get(tuple(sorted((root,x))),color)==color]
            for k, target_color in ((4,color),(5,not color)):
                for subset in it.combinations(possible,k):
                    prohibit([(a,b,target_color) for a,b in it.combinations(subset,2)] + [(root,x,color) for x in subset])
    print('GENERATED',len(variables),len(clauses),'seconds',time.monotonic()-start,flush=True)
    for vertex in range(43):
        fixed_red = sum(col for e,col in fixed.items() if vertex in e)
        lits = [var for e,var in variables.items() if vertex in e]
        lo,hi=(22,22) if vertex==0 else ((21,22) if vertex<=22 else (20,21))
        for bound, negate in ((hi-fixed_red,False),(len(lits)-(lo-fixed_red),True)):
            if 0 <= bound < len(lits):
                clauses.extend(CardEnc.atmost([-x for x in lits] if negate else lits, bound=bound,vpool=pool,encoding=EncType.seqcounter).clauses)
            elif bound < 0:
                clauses.append([])
    cross=[var for (a,b),var in variables.items() if a<=22<b]
    clauses.extend(CardEnc.equals(cross,bound=232,vpool=pool,encoding=EncType.totalizer).clauses)
    import threading
    with Solver(name='glucose42', bootstrap_with=clauses) as solver:
        timer=threading.Timer(args.seconds,solver.interrupt)
        timer.start()
        answer=solver.solve_limited(expect_interrupt=True)
        timer.cancel()
        print('SOLVE',answer,solver.accum_stats(),'elapsed',time.monotonic()-start,flush=True)
        if answer:
            model=set(solver.get_model())
            red = sorted([e for e,c in fixed.items() if c]+[e for e,x in variables.items() if x in model])
            red_set=set(red)
            cross_rows=[''.join('1' if (1+i,23+j) in red_set else '0' for j in range(20)) for i in range(22)]
            print(json.dumps({'cross_rows':cross_rows,'partner':v},indent=2),flush=True)
            print('MATCHES_CERTIFICATE',cross_rows==original['cross_rows'],flush=True)


if __name__=='__main__':
    main()
