"""Regenerate every scalar-cell allocation and check definitions independently."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys

import construct
import verify

ROOT=Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def rejection(fn):
    try:fn()
    except ValueError:return 1
    raise ValueError('Deliberate corruption was accepted')


def run():
    params=json.loads((ROOT/'parameters.json').read_text())
    words=[verify.degree_word(g) for g in params['interfaces']]
    verify.require(len(words)==13,'Incomplete imported interfaces')
    for g,word in zip(params['interfaces'],words):
        verify.require(construct.degree_word(g)==word,'Independent graph6 decode mismatch')
    keys=list(construct.cells())
    verify.require(keys==verify.cell_domain() and len(keys)==189,'Full scalar cover mismatch')
    counts={q:c for q,c in zip(range(9,14),[290,313,105,12,1])}
    verify.require(params['r35_counts']==list(counts.values()),'Imported core-count mismatch')
    coarse=sum(counts[q] for d,p,q in keys)
    verify.require(coarse==18767,'Coarse label count')
    stream=hashlib.sha256();bounds=[];triangles=[];budgets={};paid=[]
    for key in keys:
        allocation=construct.construct(*key)
        checked=verify.verify(allocation,words)
        permutation=[0,1]+list(reversed(range(2,43)))
        moved=copy.deepcopy(allocation)
        for old,new in enumerate(permutation):
            moved['degrees'][new]=allocation['degrees'][old]
            moved['neighbor_selections'][new]=sorted(permutation[w] for w in allocation['neighbor_selections'][old])
            for color in ('red','blue'):
                moved['deficiencies'][color][new]=allocation['deficiencies'][color][old]
                moved['local_degrees'][color][new]=allocation['local_degrees'][color][old][:]
        for color in ('red','blue'):
            moved['anchors'][color]=[dict(m,vertex=permutation[m['vertex']],hub=permutation[m['hub']]) for m in allocation['anchors'][color]]
        verify.require(verify.verify(moved,words)==checked,'Nonroot relabeling changed the verdict')
        verify.require((checked['red_anchors'],checked['blue_anchors'],checked['red_charge'],checked['blue_charge'])==(20,0,180,0),'Positive demand was lost')
        stream.update(json.dumps([allocation,checked],sort_keys=True,separators=(',',':')).encode()+b'\n')
        R=sum(allocation['deficiencies']['red']);B=sum(allocation['deficiencies']['blue'])
        d,p,q=key
        summary=[d,p,allocation['degrees'][2],allocation['deficiencies']['red'][2],checked['delta'],R,B]
        verify.require((d,p) not in budgets or budgets[(d,p)]==summary,'Budget should not depend on q')
        budgets[(d,p)]=summary;bounds.append(checked['delta']);triangles.append([checked['red_triangles'],checked['blue_triangles']]);paid.append(B)
    # Havel-Hakimi and Erdos-Gallai independently agree on every sorted
    # candidate degree word through order seven, including nongraphical ones.
    graphical_controls=0
    for n in range(1,8):
        for seq in itertools.combinations_with_replacement(range(n),n):
            eg=verify.graphical(list(seq))
            try:construct.realize(list(seq));hh=True
            except ValueError:hh=False
            verify.require(hh==eg,'Graphicality algorithms disagree')
            graphical_controls+=1
    sample=construct.construct(18,18,9)
    bad=[]
    x=copy.deepcopy(sample);x['extra']=0;bad.append(x)
    x=copy.deepcopy(sample);x['cell']=[18,18,8];bad.append(x)
    x=copy.deepcopy(sample);x['degrees'][0]=True;bad.append(x)
    x=copy.deepcopy(sample);x['degrees'][2]=26;bad.append(x)
    x=copy.deepcopy(sample);x['degrees'][2]+=1;bad.append(x)
    x=copy.deepcopy(sample);x['cell_sizes'][3]+=1;bad.append(x)
    x=copy.deepcopy(sample);x['deficiencies']['red'][2]+=1;x['deficiencies']['blue'][2]-=1;bad.append(x)
    x=copy.deepcopy(sample);x['deficiencies']['blue'][5]+=3;bad.append(x)
    x=copy.deepcopy(sample);x['local_degrees']['red'][0]=[9]+[13]*11+[6]+[0]*5;bad.append(x)
    x=copy.deepcopy(sample);x['anchors']['red'].pop();bad.append(x)
    x=copy.deepcopy(sample);x['anchors']['red'][0]['hub']=24;bad.append(x)
    x=copy.deepcopy(sample);x['anchors']['red'][0]['interface']=5;bad.append(x)
    x=copy.deepcopy(sample);x['anchors']['red'][0]['interface']=True;bad.append(x)
    x=copy.deepcopy(sample);x['local_degrees']['red'][23]=construct.balanced(23,226);bad.append(x)
    # Preserve total deficiency and both triangle sums, but move one unit
    # between hubs. Aggregate payment stays180; one individual gap becomes8.
    x=copy.deepcopy(sample)
    for v,delta in [(23,8),(24,10)]:
        x['deficiencies']['red'][v]=delta
        x['local_degrees']['red'][v]=construct.balanced(23,2*(122-delta),5)
    bad.append(x)
    x=copy.deepcopy(sample);x['neighbor_selections'][0][0]=0;bad.append(x)
    x=copy.deepcopy(sample);x['neighbor_selections'][0][-1]=x['neighbor_selections'][0][0];bad.append(x)
    # Keep cardinality and required partner; change the sum by one.
    x=copy.deepcopy(sample)
    row=x['neighbor_selections'][0]
    removed=next(w for w in row if w!=1 and x['degrees'][w]==23)
    added=next(w for w in range(3,23) if w not in row)
    row.remove(removed);row.append(added);bad.append(x)
    x=construct.construct(22,22,10)
    row=x['neighbor_selections'][0]
    row.remove(1);row.append(next(w for w in range(3,23) if w not in row));bad.append(x)
    rejected=sum(rejection(lambda x=x:verify.verify(x,words)) for x in bad)
    # Missing scalar key and malformed local record are separate coverage/input controls.
    rejected+=rejection(lambda:verify.require(keys[:-1]==verify.cell_domain(),'Missing cell'))
    rejected+=rejection(lambda:verify.degree_word(params['interfaces'][8][:-1]))
    rows=sample['neighbor_selections']
    asym=sum((j in rows[i])!=(i in rows[j]) for i in range(43) for j in range(i+1,43))
    intersection=len(set(rows[0]) & set(rows[1]))
    verify.require(asym==400 and intersection==17,'Explicit missing-compatibility witness changed')
    output={'fixture_asymmetric_pairs':asym,'fixture_root_row_intersection':intersection,'status':'VERIFIED_ALL_189_LOW_CELL_CHARGE_SURVIVORS','scalar_cells':len(keys),
            'degree_budget_cases':len(budgets),'coarse_labels_retained_only':coarse,
            'anchors_per_allocation':20,'distinct_degree23_hubs':20,'type62_charge_per_hub':9,
            'red_charge_per_allocation':180,'global_degree_realizations':189,
            'pointwise_neighbor_rows':189*43,'local_degree_realizations':189*86,'nonroot_relabel_controls':189,'graphicality_differential_controls':graphical_controls,
            'rejected_corruptions':rejected,'delta_range':[min(bounds),max(bounds)],
            'blue_budget_range':[min(paid),max(paid)],'budget_rows':list(budgets.values()),
            'allocation_stream_sha256':stream.hexdigest(),'fixture_sha256':sha(sample),
            'ramsey_graph_found':False,'scalar_cells_excluded':0,'bound_improved':False}
    return output,sample


if __name__=='__main__':
    result,sample=run()
    if sys.argv[1:]==['--write-expected']:
        (ROOT/'expected.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        (ROOT/'allocation.json').write_text(json.dumps(sample,separators=(',',':'),sort_keys=True)+'\n')
    elif sys.argv[1:]:raise SystemExit('usage: python3 -B reproduce.py')
    else:
        verify.require(json.loads((ROOT/'expected.json').read_text())==result,'Expected evidence mismatch')
        verify.require(json.loads((ROOT/'allocation.json').read_text())==sample,'Fixture mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
