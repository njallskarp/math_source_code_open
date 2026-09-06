#!/usr/bin/env python3
"""Exact publication bridge for Albertson r=27,28; CPython 3.12, stdlib.

Uses three hash-pinned, previously reviewed source modules from this repository.
This is composition and source delivery, not an independent review of them.
Only the order dispatch and minimum-degree marked-join calculation are new.
"""
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path
import json
import sys
import argparse

ROOT = Path(__file__).resolve().parent.parent
PINS = {
    "r27": ("albertson_r27_terminal_gallai_review_20260905/verify_review.py",
            "2f655ee26b87f48af36afa193089c3b81763b1a4c2a635a5c1357275f4acc555"),
    "r28": ("albertson_r28_full_chain_review/verify_review.py",
            "9154c4b6d27c02b510fd976b569233af8e0882b349b71bc5fdf2e0def5e08398"),
    "separator": ("albertson_r28_separator_certificate_review/verify.py",
                  "98bd731e71473e959ba0556d13bb32445fa163e608ccfd562ce2d15d9d58a115"),
}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def load(name):
    relative, expected = PINS[name]
    path = ROOT / relative
    require(sha256(path.read_bytes()).hexdigest() == expected,
            "Imported source hash mismatch: " + relative)
    spec = spec_from_file_location("albertson_paper_" + name, path)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ceil_div(a, b):
    return -((-a) // b)


def ceiling(value):
    return ceil_div(value.numerator, value.denominator)


def hill(r):
    return (r // 2) * ((r-1) // 2) * ((r-2) // 2) * ((r-3) // 2) // 4


def edge_floor(r, n):
    """Barat--Toth Corollaries 5 and 7; no Kostochka--Yancey input."""
    values = [(r-1)*n + 2*r-6]
    if r+2 <= n <= 2*r-1:
        p = n-r
        values.append((r-1)*n + p*(r-p)-1)
    return ceil_div(max(values), 2)


def affine_sample(n, m, k):
    """Average cr >= 5m - (203/9)(n-2) over all k-subsets."""
    return (Fraction(5*m*(n-2)*(n-3), (k-2)*(k-3))
            - Fraction(203*n*(n-1)*(n-2)*(n-3),
                       9*k*(k-1)*(k-3)))


def order_dispatch():
    records = []
    expected = {27: [52,53,54], 28: [54,55,56]}
    for r in (27,28):
        survivors = []
        # Published large-order cutoff: n >= 3.57*r, with r>=17.
        for n in range(r+5, ceil_div(357*r,100)):
            m = edge_floor(r,n)
            bound,k = max((affine_sample(n,m,k),k) for k in range(4,n+1))
            status = "closed" if ceiling(bound) >= hill(r) else "recursive_or_join"
            if status != "closed":
                survivors.append(n)
            records.append([r,n,m,k,str(bound),ceiling(bound),status])
        require(survivors == expected[r], "Unexpected coarse order survivor")
    return records


def join_minimum(r, n):
    """Relax every disconnected-complement decomposition, marking ONE part.

    Part types: (1,1) or k>=3, v>=2k-1. Every part gets only the degree
    floor ceil((k-1)v/2); exactly one part with k>=4 gets Corollary 7.
    Edges across distinct parts contribute (n^2-sum v_i^2)/2.
    Ordered part sequences cover every multiset; duplicates are harmless.
    """
    types = [(1,1)]
    types += [(k,v) for k in range(3,r+1) for v in range(2*k-1,n+1)]
    # key=(sum chromatic, sum vertices, marked, count capped at 2)
    states = {(0,0,False,0): (0,())}
    for ksum in range(r+1):
        for vsum in range(n+1):
            for marked in (False,True):
                for count in range(3):
                    key=(ksum,vsum,marked,count)
                    if key not in states:
                        continue
                    cost,witness=states[key]
                    for k,v in types:
                        if ksum+k>r or vsum+v>n:
                            continue
                        base=ceil_div((k-1)*v,2)
                        options=[(marked,base,False)]
                        if not marked and k>=4:
                            options.append((True,ceil_div((k-1)*v+2*k-6,2),True))
                        for new_marked,edges,is_marked in options:
                            target=(ksum+k,vsum+v,new_marked,min(2,count+1))
                            candidate=(cost+2*edges-v*v,witness+((k,v,is_marked),))
                            if target not in states or candidate<states[target]:
                                states[target]=candidate
    cost,witness=states[(r,n,True,2)]
    require((n*n+cost)%2==0,"Nonintegral join edge count")
    return [(n*n+cost)//2,witness]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificates', action='store_true',
                        help='regenerate the two compact, deterministic TSV certificates')
    args = parser.parse_args()
    a,b,c=(load(name) for name in ("r27","r28","separator"))
    dispatch=order_dispatch()
    table,sweeps=a.recursive_bounds(56)
    wanted={(53,713):6071,(53,714):6100,(54,725):6106,(54,726):6134}
    for (n,m),value in wanted.items():
        require(table[n][m]==value,"Historical recursive row mismatch")
    # The row thresholds prove all higher edge counts impossible by monotonicity.
    thresholds=[]
    for r,orders in ((27,(52,53,54)),(28,(54,55,56))):
        for n in orders:
            row=table[n]
            require(all(x<=y for x,y in zip(row,row[1:])),"Nonmonotone row")
            maximum=max(m for m,v in enumerate(row) if v<hill(r))
            thresholds.append([r,n,edge_floor(r,n),maximum,row[maximum+1]])
    expected_thresholds={(27,52):702,(27,53):713,(27,54):724,
                         (28,54):757,(28,55):769}
    for r,n,floor,maximum,value in thresholds:
        if (r,n) in expected_thresholds:
            require(maximum==expected_thresholds[r,n],"Unexpected edge ceiling")
        if n==2*r:
            require(floor>maximum,"Even order not excluded")
    joins=[]
    for r,n,maximum in ((27,52,702),(27,53,713),(28,54,757),(28,55,769)):
        minimum,witness=join_minimum(r,n)
        require(minimum>maximum,"Disconnected complement survives")
        joins.append([r,n,maximum,minimum,witness])
    require([j[3] for j in joins]==[712,725,766,780],"Join floor changed")

    # Consume the reviewed complete component enumerations with K12-only seeds.
    r27_barriers=a.barrier_survivors(table,a.complete_lower_through_12)
    require(r27_barriers=={3:[(49,1),(48,1,1)],4:[(47,1,1)]},"r27 barrier changed")
    r27_triangle=a.triangle_free_totals(table,a.complete_lower_through_12)
    require(r27_triangle==[(0,7088)],"r27 triangle-free bound changed")
    entry_records=[]
    r28_survivors={}
    for m in (768,769):
        live={}
        for barrier in range(3,29):
            parts=c.multiplicity_partitions(55-barrier,barrier-1,barrier,2*m-55*27)
            for sizes in parts:
                record=c.classify(m,barrier,sizes)
                entry_records.append(record.line())
                if record.status=="survives":
                    live.setdefault(barrier,[]).append(sizes)
        require(live=={3:[(51,1),(50,1,1)],4:[(49,1,1)]},"r28 barrier changed")
        r28_survivors[m]=live
    entries_digest=sha256(("\n".join(entry_records)+"\n").encode()).hexdigest()
    require(entries_digest=="bd5ce6a29e7fb90259e5fe4ec3b341cbb5fcceb8de25ad0416a8bbe21af5cf5e",
            "Reviewed entry-level certificate changed")

    # The same reviewed component checker, specialized to r=27, closes its
    # 34-entry table even with the weaker single-level sampling bound.
    # These globals are the module's explicit fixed-parameter interface;
    # cached crossing functions depend only on n,m,k, not on R or N.
    c.R,c.N=27,53
    records27=[]
    live27={}
    for barrier in range(3,28):
        for sizes in c.multiplicity_partitions(53-barrier,barrier-1,barrier,48):
            record=c.classify(713,barrier,sizes)
            records27.append(record.line())
            if record.status=='survives':
                live27.setdefault(barrier,[]).append(sizes)
    require(live27==r27_barriers and len(records27)==34,
            'Common component checker does not reproduce r27')
    c.R,c.N=28,55

    order_text='r\tn\tedge_floor\tsample_order\trational_bound\tceil_bound\tstatus\n'
    order_text+=''.join('\t'.join(map(str,row))+'\n' for row in dispatch)
    component_text=('r\tm\tb\tparts\tdeficiency\tbipartite\tcross_lower\t'
                    'cross_upper\ttk_obstruction\tsplit\tstatus\n')
    for r,records in ((27,records27),(28,entry_records)):
        for line in records:
            component_text+=str(r)+'\t'+line.replace('topological_K28','topological_Kr')+'\n'
    certificate_texts={'ORDER_CERTIFICATE.tsv':order_text,
                       'COMPONENT_CERTIFICATE.tsv':component_text}
    for filename,content in certificate_texts.items():
        path=Path(__file__).resolve().parent/filename
        if args.write_certificates:
            path.write_text(content)
        else:
            require(path.read_text()==content,'Certificate mismatch: '+filename)

    # Shared terminal mechanism: disjoint large Gallai clique blocks.
    complete=b.complete_crossing_bounds(b.K12_BASE,53)
    states=b.forward_block_states(53,complete)
    terminal=[]
    cases=[(27,713,2,614),(27,713,3,588),
           (28,768,2,664),(28,768,3,637),(28,768,4,612),
           (28,769,2,663),(28,769,3,636),(28,769,4,609),
           (28,769,5,582),(28,769,6,560)]
    for r,m,high,edges in cases:
        minimum,actual_edges,used,witness=b.split_minimum(2*r-1-high,edges,states)
        require(minimum>hill(r),"Terminal split does not close")
        terminal.append([r,m,high,edges,minimum,minimum-hill(r),witness])
    require([row[4] for row in terminal]==
            [8424,7722,9920,9126,8424,9920,9126,8424,7589,7104],
            "Reviewed split minima changed")

    result={
        "scope":"r27_r28_only; mathematical and source-composition audit, not independent review",
        "order_dispatch_records":len(dispatch),
        "certificate_files":{name:sha256(value.encode()).hexdigest()
                             for name,value in certificate_texts.items()},
        "recursive_sweeps":sweeps,
        "recursive_thresholds":thresholds,
        "disconnected_complement":joins,
        "r27_barriers":r27_barriers,
        "r27_triangle_free":r27_triangle,
        "r27_component_records":len(records27),
        "r28_barriers":r28_survivors,
        "r28_triangle_free":[[m,*c.triangle_free_total(m)] for m in (768,769)],
        "r28_component_records":len(entry_records),
        "r28_component_digest":entries_digest,
        "terminal_splits":terminal,
        "imported_sources":PINS,
    }
    canonical=json.dumps(result,sort_keys=True,separators=(",",":"))
    print(json.dumps(result,indent=2,sort_keys=True))
    print("result_sha256="+sha256(canonical.encode()).hexdigest())
    print("VERIFIED")


if __name__=="__main__":
    main()
