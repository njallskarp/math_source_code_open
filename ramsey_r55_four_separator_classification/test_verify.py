"""Small exhaustive controls and rejection tests, without network access."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import audit
import verify


def main():
    graphs = comparisons = 0
    for n in range(6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = {e for i, e in enumerate(pairs) if mask & (1 << i)}
            adj = [sum(1 << j for j in range(n) if tuple(sorted((i, j))) in edges) for i in range(n)]
            bits = ''.join('1' if (i, j) in edges else '0' for j in range(1, n) for i in range(j))
            bits += '0'*(-len(bits) % 6)
            g6 = bytes([63+n]+[63+int(bits[i:i+6], 2) for i in range(0, len(bits), 6)])
            verify.need(verify.decode(g6) == (n, edges), 'graph6 set round trip')
            verify.need(audit.unpack(g6) == adj, 'graph6 bit round trip')
            for red in (False, True):
                for size in range(n+2):
                    literal = any(all((e in edges) == red for e in combinations(S, 2))
                                  for S in combinations(range(n), size))
                    verify.need(bool(verify.cliques(range(n), edges, size, red)) == literal, 'literal control')
                    verify.need(audit.contains(adj if red else audit.complement(adj), (1 << n)-1, size)
                                == literal, 'recursive control')
                    comparisons += 1
            graphs += 1
    rejected = 0
    for bad in (b'', b'!???', b'~', b'A', b'A@', b'A??'):
        for reader in (verify.decode, audit.unpack):
            try:
                reader(bad)
            except ValueError:
                rejected += 1
            else:
                raise ValueError('invalid graph6 accepted')
    seed = json.loads((Path(__file__).parent/'certificate.json').read_text())
    bad_seeds = []
    x = deepcopy(seed); x.pop('edge_sha256'); bad_seeds.append(x)
    x = deepcopy(seed); x['signatures'][0][0] = False; bad_seeds.append(x)
    x = deepcopy(seed); x['signatures'][0][0] = 17; bad_seeds.append(x)
    x = deepcopy(seed); x['signatures'][0][0] = 1; bad_seeds.append(x)
    x = deepcopy(seed); x['signatures'][0][2] = 2; bad_seeds.append(x)
    x = deepcopy(seed); x['edge_sha256'] = '0'*64; bad_seeds.append(x)
    for bad in bad_seeds:
        try:
            verify.validate_seed(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('invalid seed accepted')
    verify.validate_seed(seed)
    verify.need(verify.separator_rows() == [[1, 17, 108], [2, 16, 104], [3, 15, 103]], 'arithmetic')
    print(json.dumps({'small_graphs': graphs, 'clique_comparisons': comparisons,
                      'rejected_inputs': rejected, 'valid_seed': True}, sort_keys=True))


if __name__ == '__main__':
    main()
