#!/usr/bin/env python3
"""Exact replay and typed certificate/input rejection controls."""
from copy import deepcopy
import json
from verify import ROOT, compute, edges_doc, require, source_edges, verify


def main():
    certificate = json.loads((ROOT / 'CERTIFICATE.json').read_text())
    source = json.loads((ROOT / 'SOURCE.json').read_text())
    h = json.loads((ROOT / 'H20.json').read_text())
    verify(certificate, source, h)
    changes = [
        lambda d: d['base_fourteen_domains'].pop(),
        lambda d: d['base_fourteen_domains'][0].update(maximum_triangle_free_size=9),
        lambda d: d['base_fourteen_domains'][0]['capacity_witness'].pop(),
        lambda d: d['base_fourteen_domains'][3].update(complement_red_K4=None),
        lambda d: d['base_fourteen_domains'][3].update(complement_red_K4=[0, 1, 2, 3]),
        lambda d: d['candidate_family'].pop(),
        lambda d: d['candidate_family'][0].update(marked_density_upper_bound=92),
        lambda d: d.update(universal_marked_density_upper_bound=True),
    ]
    for change in changes:
        damaged = deepcopy(certificate)
        change(damaged)
        try:
            verify(damaged, source, h)
        except ValueError:
            continue
        raise ValueError('accepted damaged certificate')
    input_cases = [
        (source_edges, source, lambda d: d.update(n=True)),
        (source_edges, source, lambda d: d['red_deletions'].__setitem__(1, d['red_deletions'][0])),
        (lambda d: edges_doc(d, 20), h, lambda d: d['red_edges'].append(d['red_edges'][0])),
        (lambda d: compute(source, d), h, lambda d: d['red_edges'].remove([0, 1])),
    ]
    for checker, original, change in input_cases:
        damaged = deepcopy(original)
        change(damaged)
        try:
            checker(damaged)
        except ValueError:
            continue
        raise ValueError('accepted damaged input')
    print('Positive complete replay: PASS')
    print('Damaged certificates rejected: 8/8')
    print('Damaged inputs rejected: 4/4')


if __name__ == '__main__':
    main()
