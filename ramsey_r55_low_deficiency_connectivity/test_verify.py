"""Small rejection controls; author regression tests, not peer review."""
from copy import deepcopy
import json
from pathlib import Path
from audit import component_masks, decode
from verify import check, components, construct, monochromatic, need


if __name__ == '__main__':
    data = json.loads((Path(__file__).parent / 'WITNESS.json').read_text())
    rejected = 0
    for field in ('short_signature', 'wrong_signature', 'wrong_cut', 'wrong_hash'):
        bad = deepcopy(data)
        if field == 'short_signature':
            bad['red_signatures'][0].pop()
        elif field == 'wrong_signature':
            bad['red_signatures'][0][-1] = 16
        elif field == 'wrong_cut':
            bad['separator'][-1] = 21
        else:
            bad['edge_sha256'] = '0' * 64
        try:
            check(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('damaged witness accepted')
    try:
        decode(data['graph6_base64'][:-4])
    except ValueError:
        rejected += 1
    else:
        raise ValueError('truncated graph6 accepted')
    edges = construct(data)
    damaged_edges = edges | {(0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (0, 1)}
    need(monochromatic(22, damaged_edges, 4, True), 'inserted K4 missed')
    # Both connectivity routines must handle a graph with diameter beyond four.
    path = {(i, i + 1) for i in range(17)}
    need(components(18, path, []) == [list(range(18))], 'long path connectivity')
    need(list(map(len, components(18, path, [8]))) == [8, 9], 'path cut')
    rows = [sum(1 << v for v in range(18) if tuple(sorted((u, v))) in path) for u in range(18)]
    need(component_masks(rows, 0) == [(1 << 18) - 1], 'long path bitset connectivity')
    need(sorted(c.bit_count() for c in component_masks(rows, 1 << 8)) == [8, 9], 'bitset path cut')
    print(json.dumps({'rejected_corruptions': rejected, 'inserted_k4_detected': True,
                      'long_path_controls': 4}, sort_keys=True))
