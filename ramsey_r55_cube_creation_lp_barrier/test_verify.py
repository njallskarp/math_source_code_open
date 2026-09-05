#!/usr/bin/env python3
"""Malformed-input and damaged-certificate controls, active under python -O."""
from copy import deepcopy
import json
from verify import ROOT, require, verify


def main():
    seed = (ROOT/'SEED.json').read_bytes()
    point = json.loads((ROOT/'primal.json').read_text())
    expected = json.loads((ROOT/'EXPECTED_OUTPUT.json').read_text())
    require(verify(seed,point) == expected, 'positive exact replay')
    mutations = [
        ('missing field',lambda p:p.pop('format')),
        ('wrong format',lambda p:p.update(format='unrelated')),
        ('wrong edge order',lambda p:p.update(edge_order='reverse')),
        ('wrong seed identity',lambda p:p.update(seed_sha256='0'*64)),
        ('zero denominator',lambda p:p.update(denominator=0)),
        ('floating denominator',lambda p:p.update(denominator=float(p['denominator']))),
        ('short vector',lambda p:p['numerators'].pop()),
        ('Boolean numerator',lambda p:p['numerators'].__setitem__(0,False)),
        ('negative numerator',lambda p:p['numerators'].__setitem__(0,-1)),
        ('outside box',lambda p:p['numerators'].__setitem__(0,p['denominator']+1)),
        ('one-unit damage',lambda p:p['numerators'].__setitem__(0,p['numerators'][0]+1)),
        ('wrong hole',lambda p:p['missing_local_clause'].update(hole=[3,10])),
        ('wrong anchor',lambda p:p['missing_local_clause'].update(blue_anchor=0)),
    ]
    for name,mutation in mutations:
        damaged = deepcopy(point)
        mutation(damaged)
        try:
            verify(seed,damaged)
        except ValueError:
            continue
        raise ValueError('accepted '+name)
    try:
        verify(seed+b' ',point)
    except ValueError:
        pass
    else:
        raise ValueError('accepted seed-byte damage')
    print('Positive replay: PASS')
    print('Malformed/damaged inputs rejected: 14/14')


if __name__ == '__main__':
    main()
