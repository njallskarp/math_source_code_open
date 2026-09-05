#!/usr/bin/env python3
"""Positive replay and certificate corruption controls, including python -O."""
from copy import deepcopy
import json
from verify import ROOT, require, verify


def main():
    doc=json.loads((ROOT/'fixture.json').read_text())
    require(verify(doc)==json.loads((ROOT/'EXPECTED_OUTPUT.json').read_text()),'positive replay')
    def cell(d,u,v,c):
        row=list(d['partial'][u]);row[v]=c;d['partial'][u]=''.join(row)
    mutations=[
        ('field missing',lambda d:d.pop('format')),
        ('wrong format',lambda d:d.update(format='other')),
        ('wrong order',lambda d:d.update(n=16)),
        ('wrong anchors',lambda d:d.update(anchors=[0,1,3])),
        ('wrong block',lambda d:d['blocks'][0][0].__setitem__(0,7)),
        ('short matrix',lambda d:d['partial'].pop()),
        ('self loop',lambda d:cell(d,3,3,'1')),
        ('asymmetry',lambda d:cell(d,3,4,'0')),
        ('wrong margin',lambda d:d['red_degrees'].__setitem__(3,6)),
        ('duplicate selected row',lambda d:d['selected_clauses'].__setitem__(1,deepcopy(d['selected_clauses'][0]))),
        ('wrong equal state',lambda d:d['selected_clauses'][0].update(equal_state=1)),
        ('wrong colored witness',lambda d:d['selected_clauses'][0].update(color=1)),
        ('wrong five-set',lambda d:d['selected_clauses'][0].update(five=[0,1,2,3,4])),
    ]
    for name,mutate in mutations:
        damaged=deepcopy(doc);mutate(damaged)
        try: verify(damaged)
        except ValueError: continue
        raise ValueError('accepted '+name)
    print('Positive exact replay: PASS')
    print('Damaged certificates rejected: 13/13')


if __name__=='__main__': main()
