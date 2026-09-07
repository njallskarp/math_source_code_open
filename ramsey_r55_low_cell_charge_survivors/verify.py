"""Definition-level allocation checker. Imports no constructor or parameter file."""
import itertools
import json
import math
import sys

U = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
GAPS = [7, 7, 7, 7, 7, None, 9, 9, 9, 7, 7, 7, 7]
FIELDS = {'cell', 'cell_sizes', 'degrees', 'deficiencies', 'local_degrees', 'anchors', 'neighbor_selections'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def integer(x, lo, hi):
    return type(x) is int and lo <= x <= hi


def graphical(seq):
    """Every Erdos-Gallai inequality, independent of construction by removal."""
    n = len(seq)
    if any(not integer(x, 0, n - 1) for x in seq) or sum(seq) % 2:
        return False
    ds = sorted(seq, reverse=True)
    for k in range(1, n + 1):
        if sum(ds[:k]) > k * (k - 1) + sum(min(k, x) for x in ds[k:]):
            return False
    return True


def degree_word(word):
    require(isinstance(word, str) and len(word) > 1, 'Bad graph6')
    n = ord(word[0]) - 63
    require(n == 22 and len(word) == 1 + (n*(n-1)//2 + 5)//6, 'Bad graph6 length')
    values = [ord(c)-63 for c in word[1:]]
    require(all(0 <= x < 64 for x in values), 'Bad graph6 character')
    matrix = [[0] * n for _ in range(n)]
    for j in range(1, n):
        for i in range(j):
            bit = j*(j-1)//2 + i
            matrix[i][j] = matrix[j][i] = (values[bit//6] >> (5-bit%6)) & 1
    used = n*(n-1)//2
    if used % 6:
        require(values[-1] % (1 << (6-used%6)) == 0, 'Nonzero graph6 padding')
    ds = sorted(sum(r) for r in matrix)
    require(sum(ds) == 218 and ds.count(5) == 1, 'Wrong dense-anchor record')
    for size, color in ((4, 1), (5, 0)):
        for vs in itertools.combinations(range(n), size):
            require(not all(matrix[i][j] == color for i, j in itertools.combinations(vs, 2)), 'Bad local Ramsey record')
    return ds


def cell_domain():
    return sorted((d, p, q) for d in U for p in U for q in range(14)
                  if d*q >= 2*(U[d]-6))


def verify(data, interface_degrees):
    require(isinstance(data, dict) and set(data) == FIELDS, 'Wrong allocation fields')
    key = data['cell']
    require(isinstance(key, list) and len(key) == 3 and all(type(x) is int for x in key), 'Bad scalar key')
    require(tuple(key) in cell_domain(), 'Outside scalar cover')
    d, p, q = key
    cells = [q, d-1-q, p-1-q, 43-d-p+q]
    require(data['cell_sizes'] == cells and all(x >= 0 for x in cells) and sum(cells) == 41, 'Cell partition mismatch')
    degrees = data['degrees']
    require(isinstance(degrees, list) and len(degrees) == 43 and all(integer(x, 18, 24) for x in degrees), 'Bad global degrees')
    require(degrees[:2] == [d, p] and graphical(degrees), 'Global degree profile')
    for name in ('deficiencies', 'local_degrees', 'anchors'):
        require(isinstance(data[name], dict) and set(data[name]) == {'red', 'blue'}, 'Color fields')
    totals = {}
    detected = {}
    for color in ('red', 'blue'):
        deficits, profiles = data['deficiencies'][color], data['local_degrees'][color]
        require(isinstance(deficits, list) and len(deficits) == 43 and isinstance(profiles, list) and len(profiles) == 43, 'Missing local sides')
        triangle_sum = 0; detected[color] = set()
        for v in range(43):
            n = degrees[v] if color == 'red' else 42 - degrees[v]
            delta = deficits[v]; word = profiles[v]
            require(integer(delta, 0, U[n]), 'Bad deficiency')
            require(isinstance(word, list) and len(word) == n and all(integer(x, max(0,n-18), 13) for x in word), 'Bad local degree bounds')
            require(sum(word) == 2*(U[n]-delta) and graphical(word), 'Local graphical/density constraint')
            if delta <= 6:
                threshold = (2*(U[n]-6)+n-1)//n
                needed = (2*(U[n]-6)-n*(threshold-1)+(13-(threshold-1))-1)//(13-(threshold-1))
                require(sum(x >= threshold for x in word) >= needed, 'Low-side high-partner multiplicity')
            if n == 22 and delta <= 5:
                require(min(word) >= 5 and (delta == 5 or min(word) >= 6), 'Dense order22 minimum-degree threshold')
            if n == 22 and delta <= 5 and 5 in word:
                require(delta == 5 and word.count(5) == 1, 'Dense-anchor uniqueness/density')
                detected[color].add(v)
            triangle_sum += U[n]-delta
        require(triangle_sum % 3 == 0, 'Color triangle divisibility')
        totals[color] = triangle_sum
    require(data['deficiencies']['red'][0] <= 6, 'Not a low-deficiency root')
    require(q in data['local_degrees']['red'][0] and q in data['local_degrees']['red'][1], 'Selected pair codegree reciprocity')
    wedges = sum(x*(42-x) for x in degrees)
    require(2*(totals['red']+totals['blue']) == 6*math.comb(43,3)-3*wedges, 'Exact Goodman identity')
    prescribed = {(0,1): 'red'}
    def prescribe(i,j,color):
        pair = tuple(sorted((i,j)))
        require(i != j and prescribed.get(pair,color) == color, 'Inconsistent prescribed pair colors')
        prescribed[pair] = color
    charge_totals = {}
    for color in ('red', 'blue'):
        other = 'blue' if color == 'red' else 'red'
        marks = data['anchors'][color]
        require(isinstance(marks,list), 'Bad anchor map')
        seen = set(); fibers = {}; charge = 0
        for mark in marks:
            require(isinstance(mark,dict) and set(mark) == {'vertex','hub','interface'}, 'Bad anchor row')
            v,z,t = (mark[k] for k in ('vertex','hub','interface'))
            require(integer(v,0,42) and integer(z,0,42) and integer(t,0,12) and v!=z and v not in seen, 'Bad anchor indices')
            seen.add(v)
            require(v in detected[color] and sorted(data['local_degrees'][color][v]) == interface_degrees[t], 'Missing/wrong dense type')
            degree_z = degrees[z] if color == 'red' else 42-degrees[z]
            require(degree_z <= 23, 'Hub exceeds degree23')
            require(5 in data['local_degrees'][color][z], 'Hub codegree reciprocity')
            prescribe(v,z,color)
            fibers.setdefault(z,[]).append(v)
            if degree_z == 23:
                gap = GAPS[t]
                require(gap is not None and data['deficiencies'][color][z] >= gap, 'Degree23 pointwise hub gap')
                charge += gap
        require(seen == detected[color], 'Anchor incidence is incomplete')
        for z,vs in fibers.items():
            n = degrees[z] if color == 'red' else 42-degrees[z]
            if n >= 21:
                require(len(vs) <= 1, 'High-degree hub collision')
            elif n in (19,20):
                require(len(vs) <= 4, 'Low-degree fiber capacity')
                for v,w in itertools.combinations(vs,2):prescribe(v,w,other)
        paid = sum(data['deficiencies'][color][v] for v in range(43) if (degrees[v] if color=='red' else 42-degrees[v]) == 23)
        require(paid >= charge, 'Additive hub charges')
        charge_totals[color] = charge
    rows = data['neighbor_selections']
    require(isinstance(rows,list) and len(rows)==43, 'Missing pointwise neighbor rows')
    for v,row in enumerate(rows):
        require(isinstance(row,list) and len(row)==degrees[v] and all(integer(w,0,42) and w!=v for w in row), 'Bad neighbor row')
        require(len(set(row))==len(row), 'Repeated neighbor')
        # Use the unsimplified edge partition, independently of the producer's
        # target sum: m = e(N) + edges(N,outside) + e(outside) + d(v).
        e_red = sum(data['local_degrees']['red'][v])//2
        e_blue = sum(data['local_degrees']['blue'][v])//2
        cross = sum(degrees[w] for w in row) - 2*e_red - degrees[v]
        e_outside = math.comb(42-degrees[v],2) - e_blue
        require(cross >= 0 and sum(degrees)//2 == e_red+cross+e_outside+degrees[v], 'Pointwise neighbor-degree edge partition')
    for (v,w),color in prescribed.items():
        require((w in rows[v]) == (color=='red') and (v in rows[w]) == (color=='red'), 'Prescribed pair missing from neighbor selections')
    return {'status':'VERIFIED_EXACT_INCIDENCE_ALLOCATION' ,'red_anchors':len(detected['red']),
            'blue_anchors':len(detected['blue']), 'red_charge':charge_totals['red'],
            'blue_charge':charge_totals['blue'], 'delta':sum(sum(data['deficiencies'][c]) for c in ('red','blue')),
            'red_triangles':totals['red']//3, 'blue_triangles':totals['blue']//3}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python3 -B verify.py allocation.json parameters.json')
    with open(sys.argv[2],encoding='utf-8') as stream:params=json.load(stream)
    words=[degree_word(g) for g in params['interfaces']]
    require(len(words)==13,'Incomplete interface list')
    with open(sys.argv[1],encoding='utf-8') as stream:data=json.load(stream)
    print(json.dumps(verify(data,words),sort_keys=True))
