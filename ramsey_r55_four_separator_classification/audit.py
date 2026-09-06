"""Different finite decomposition; no producer imports, no solver."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def contains(adj, candidates, size):
    if size == 0:
        return True
    while candidates.bit_count() >= size:
        bit = candidates & -candidates
        candidates ^= bit
        if contains(adj, candidates & adj[bit.bit_length()-1], size-1):
            return True
    return False


def unpack(raw):
    require(raw and all(63 <= x <= 126 for x in raw), 'graph6 alphabet')
    n = raw[0]-63
    require(n < 63 and len(raw) == 1+(n*(n-1)//2+5)//6, 'short graph6 length')
    packed = 0
    for char in raw[1:]:
        packed = 64*packed+char-63
    padding = 6*(len(raw)-1)-n*(n-1)//2
    require(packed % (1 << padding) == 0, 'zero padding')
    packed >>= padding
    adj = [0]*n
    for j in range(n-1, 0, -1):
        for i in range(j-1, -1, -1):
            if packed & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            packed >>= 1
    require(packed == 0, 'packed residue')
    return adj


def complement(adj):
    full = (1 << len(adj))-1
    return [full ^ (1 << i) ^ neighbors for i, neighbors in enumerate(adj)]


def code(value):
    return sha256((json.dumps(value, separators=(',', ':'))+'\n').encode()).hexdigest()


def run(directory):
    # This report supplies identities and a proposed permutation, not Ramsey truth.
    expected = json.loads((ROOT/'EXPECTED.json').read_text())
    primary_counts = {}
    for size in (15, 16, 17):
        name = f'r44_{size}.g6'
        if directory is None:
            with urlopen('https://users.cecs.anu.edu.au/~bdm/data/'+name, timeout=30) as stream:
                raw = stream.read()
        else:
            raw = (directory/name).read_bytes()
        target = expected['catalogues'][str(size)]
        require(sha256(raw).hexdigest() == target['sha256'], 'primary identity')
        graphs = [unpack(line) for line in raw.splitlines()]
        histogram = Counter()
        for adj in graphs:
            require(len(adj) == size, 'primary order')
            require(not contains(adj, (1 << size)-1, 4) and
                    not contains(complement(adj), (1 << size)-1, 4), 'primary Ramsey check')
            histogram[sum(v.bit_count() for v in adj)//2] += 1
        require(len(graphs) == target['count'], 'primary count')
        require({str(k): v for k, v in histogram.items()} == target['edge_histogram'], 'primary edges')
        primary_counts[str(size)] = len(graphs)
        if size == 17:
            catalog_graph = graphs[0]

    residue = {1, 2, 4, 8, 9, 13, 15, 16}
    red = [sum(1 << j for j in range(17) if (j-i) % 17 in residue) for i in range(17)]
    blue = complement(red)
    perm = expected['catalogues']['17']['catalogue_to_paley']
    require(sorted(perm) == list(range(17)), 'Paley bijection')
    require(all(bool(catalog_graph[i] & (1 << j)) == bool(red[perm[i]] & (1 << perm[j]))
                for i, j in combinations(range(17), 2)), 'Paley edge correspondence')
    # Independently enumerate ALL 2^17 masks, and assign C4 vertices in cyclic order.
    masks = [m for m in range(1 << 17) if m.bit_count() == 8 and not contains(red, m, 3)]
    full = (1 << 17)-1
    def compatible(i, j, adjacent):
        return not (contains(red, i & j, 2) if adjacent else contains(blue, full ^ (i | j), 3))
    accepted = set()
    def visit(prefix):
        if len(prefix) == 4:
            accepted.add(tuple(tuple(i for i in range(17) if m & (1 << i)) for m in prefix))
            return
        index = len(prefix)
        for m in masks:
            if all(compatible(m, old, (index-j) % 4 in (1, 3)) for j, old in enumerate(prefix)):
                visit(prefix+[m])
    visit([])

    seed = json.loads((ROOT/'certificate.json').read_text())
    sig = seed['signatures']
    require(len(sig) == 4 and all(len(s) == 8 and s == sorted(set(s))
                                and all(type(x) is int and 0 <= x < 17 for x in s) for s in sig), 'seed schema')
    edges = {(i, j) for i, j in combinations(range(17), 2) if red[i] & (1 << j)}
    edges |= {(x, 17+j) for j, s in enumerate(sig) for x in s}
    edges |= {(17, 18), (18, 19), (19, 20), (17, 20)} | {(v, 21) for v in range(17, 21)}
    adjacency = [sum(1 << j for j in range(22) if tuple(sorted((i, j))) in edges) for i in range(22)]
    require(not contains(adjacency, (1 << 22)-1, 4) and
            not contains(complement(adjacency), (1 << 22)-1, 5), 'literal seed Ramsey graph')
    require(code(sorted(edges)) == seed['edge_sha256'], 'literal seed identity')
    orbit = set()
    # Apply physical 22-vertex permutations, then extract the four columns again.
    for scale in sorted(residue):
        for offset in range(17):
            for start in range(4):
                for step in (1, -1):
                    p = [(scale*i+offset) % 17 for i in range(17)]
                    p += [17+(start+step*i) % 4 for i in range(4)]+[21]
                    require(sorted(p) == list(range(22)), 'physical bijection')
                    image = {tuple(sorted((p[i], p[j]))) for i, j in edges}
                    orbit.add(tuple(tuple(i for i in range(17) if (i, j) in image) for j in range(17, 21)))
    require(accepted == orbit, 'orbit equality')
    require(code(sorted(accepted)) == expected['classification']['tuple_sha256'], 'independent tuple identity')
    require(len(masks) == 51 and len(accepted) == 1088, 'independent sizes')
    result = {'primary_counts': primary_counts, 'all_masks_visited': 1 << 17,
              'signatures': len(masks), 'ordered_tuples': len(accepted), 'physical_orbit': len(orbit),
              'tuple_sha256': code(sorted(accepted)), 'seed_edge_sha256': code(sorted(edges))}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog-dir', type=Path)
    run(parser.parse_args().catalog_dir)
