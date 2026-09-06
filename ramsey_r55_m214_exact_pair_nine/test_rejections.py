#!/usr/bin/env python3
import copy
import json
from pathlib import Path
from verify import check, require


def main():
    good = json.loads(Path(__file__).with_name('certificate.json').read_text())
    check(good)
    mutations = []
    for key, value in [('catalog_upper_U14', 61), ('D_lower', 1568), ('upper_g', 122),
                       ('J_edges', 197), ('lower_a_b_e', [9, 56, 6]), ('partner_min', 8)]:
        bad = copy.deepcopy(good)
        bad[key] = value
        mutations.append(bad)
    bad = copy.deepcopy(good)
    bad['triangle_types']['XXT'][2] = 2
    mutations.append(bad)
    bad = copy.deepcopy(good)
    bad['catalog_witness_graph6'] = 'M' + '?' * 16
    mutations.append(bad)
    for index, bad in enumerate(mutations):
        rejected = False
        try:
            check(bad)
        except ValueError:
            rejected = True
        require(rejected, f'mutation {index} accepted')
    print(f'PASS negative controls={len(mutations)}')


if __name__ == '__main__':
    main()
