#!/usr/bin/env python3
"""Independent exact audit of Discovery Net h3795. Standard library only.

No code is imported from the contribution under review. Input files are data.
Polynomial gcd certifies fields, integer rows certify the finite exclusions,
Fraction elimination audits all small groups, and a simple clause-scanning
RUP checker validates the q=11 proof against a coordinate-defined graph.
"""
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys


def check(condition, message):
    if not condition:
        raise ValueError(message)


def trim(a, p):
    a = [x % p for x in a]
    while a and not a[-1]:
        a.pop()
    return a


def remainder(a, b, p):
    a = trim(a, p)
    b = trim(b, p)
    check(bool(b), 'zero polynomial divisor')
    while len(a) >= len(b):
        offset = len(a) - len(b)
        coefficient = a[-1] * pow(b[-1], -1, p) % p
        for j, x in enumerate(b):
            a[offset + j] = (a[offset + j] - coefficient * x) % p
        a = trim(a, p)
    return a


def gcd(a, b, p):
    while trim(b, p):
        a, b = b, remainder(a, b, p)
    a = trim(a, p)
    return [(x * pow(a[-1], -1, p)) % p for x in a] if a else []


def multiply(a, b, modulus, p):
    c = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return remainder(c, modulus, p)


def power(a, k, modulus, p):
    value = [1]
    while k:
        if k % 2:
            value = multiply(value, a, modulus, p)
        a = multiply(a, a, modulus, p)
        k //= 2
    return value


def irreducible(modulus, p):
    # A degree d reducible polynomial has an irreducible factor of degree
    # <=d//2. Such a factor divides X^(p^j)-X for its degree j.
    x_power = [0, 1]
    for _ in range(1, (len(modulus) - 1) // 2 + 1):
        x_power = power(x_power, p, modulus, p)
        difference = x_power + [0] * max(0, 2 - len(x_power))
        difference[1] -= 1
        if len(gcd(modulus, difference, p)) != 1:
            return False
    return True


class Arithmetic:
    def __init__(self, p, modulus):
        self.p, self.modulus = p, modulus
        self.d = len(modulus) - 1
        self.n = p ** self.d
        self.digits = [tuple((v // p**j) % p for j in range(self.d))
                       for v in range(self.n)]

    def encode(self, a):
        return sum((x % self.p) * self.p**j for j, x in enumerate(a))

    def add(self, a, b):
        return self.encode(x + y for x, y in zip(self.digits[a], self.digits[b]))

    def subtract(self, a, b):
        return self.encode(x - y for x, y in zip(self.digits[a], self.digits[b]))

    def scale(self, a, k):
        return self.encode(k * x for x in self.digits[a])

    def norm_one(self, a, q):
        return power(list(self.digits[a]), q + 1, self.modulus, self.p) == [1]


def finite_fields(certificate):
    expected_parameters = []
    for q in range(2, 23):
        for p in range(2, q + 1):
            if any(p % d == 0 for d in range(2, p)):
                continue
            f, value = 1, p
            while value < q:
                f, value = f + 1, value * p
            if value == q:
                expected_parameters.append((q, p, f))
    rows = certificate['cases']
    check([(r['q'], r['p'], r['f']) for r in rows] == expected_parameters,
          'complete ordered prime-power coverage')
    square_count = pair_count = 0
    summary = []
    for row in rows:
        q, p, f = row['q'], row['p'], row['f']
        modulus = row['modulus']
        check(len(modulus) == 2 * f + 1 and modulus[-1] == 1,
              'field degree and leading coefficient')
        check(irreducible(modulus, p), 'reducible field modulus')
        field = Arithmetic(p, modulus)
        generators = {a for a in range(field.n) if field.norm_one(a, q)}
        check(generators == set(row['generators']) and len(generators) == q + 1,
              'full norm-one set')
        edges = {(a, b) for a, b in combinations(range(field.n), 2)
                 if field.subtract(b, a) in generators}
        pair_count += field.n * (field.n - 1) // 2
        check(row['vertices'] == q*q and len(edges) == row['edges'] == q*q*(q+1)//2,
              'graph dimensions')
        relation = row['redundancy']
        squares = 0
        if q != 3:
            s = relation['target']
            check(s in generators and s != 0, 'nonzero target generator')
            steps = []
            for t, k in relation['terms']:
                check(t in generators and t not in {s, field.scale(s, -1)},
                      'transverse norm-one generator')
                check(type(k) is int and 0 < k < p, 'relation coefficient')
                steps.extend([t] * k)
            endpoint = 0
            for t in steps:
                endpoint = field.add(endpoint, t)
            check(endpoint == s, 'additive dependence')
            total = Counter()
            for k in range(p - 1):
                x = field.scale(s, k)
                for t in steps:
                    cycle = (x, field.add(x, s), field.add(field.add(x, s), t),
                             field.add(x, t))
                    check(len(set(cycle)) == 4, 'degenerate rhombus')
                    check(all(tuple(sorted((a, b))) in edges
                              for a, b in zip(cycle, cycle[1:] + cycle[:1])),
                          'nonedge in rhombus')
                    for vertex, sign in zip(cycle, (1, -1, 1, -1)):
                        total[vertex] += (p - 1 - k) * sign
                    x = field.add(x, t)
                    squares += 1
            check({v: c for v, c in total.items() if c} == {0: p, s: -p},
                  'literal integer collision certificate')
        else:
            check(relation is None, 'exceptional parameter')
            check(generators == {1, 2, 3, 6}, 'q3 Cartesian factor generators')
        if q == 11:
            # Independent of quotient-field exponentiation and certificate S.
            direct = {(a, b) for a, b in combinations(range(121), 2)
                      if (((a % 11 - b % 11)**2 + (a // 11 - b // 11)**2) % 11) == 1}
            check(edges == direct, 'q11 coordinate-to-field interface')
        square_count += squares
        summary.append([q, len(edges), squares])
    return {'cases': summary, 'all_pair_tests': pair_count,
            'integer_rhombus_rows': square_count}


def q3_drawing():
    # Coordinates have integer numerators in Q(sqrt(3)), common denominator 10.
    # Tuple (a,b) represents (a+b*sqrt(3))/10 for a coordinate.
    triangle = [(0, 0, 0, 0), (10, 0, 0, 0), (5, 0, 0, 5)]
    rotated = [(0, 0, 0, 0), (6, 0, 8, 0), (3, -4, 4, 3)]
    points = {v: tuple(x+y for x, y in zip(triangle[v[0]], rotated[v[1]]))
              for v in product(range(3), repeat=2)}
    check(len(set(points.values())) == 9, 'drawing collision')
    edge_count = 0
    for u, v in combinations(points, 2):
        a, b, c, d = (x-y for x, y in zip(points[u], points[v]))
        norm = (a*a + 3*b*b + c*c + 3*d*d, 2*a*b + 2*c*d)
        edge = sum(x != y for x, y in zip(u, v)) == 1
        check((norm == (100, 0)) == edge, 'q3 strict drawing interface')
        if edge:
            check(sum(u) % 3 != sum(v) % 3, 'q3 colouring')
            edge_count += 1
    return {'vertices': 9, 'pairs': 36, 'edges': edge_count, 'chromatic_number': 3}


def cnf_for_graph(n, edges):
    clauses = []
    for v in range(n):
        colors = list(range(4*v + 1, 4*v + 5))
        clauses.append(frozenset(colors))
        clauses.extend(frozenset((-a, -b)) for a, b in combinations(colors, 2))
    for u, v in sorted(edges):
        for c in range(4):
            clauses.append(frozenset((-4*u-c-1, -4*v-c-1)))
    u, v = min(edges)
    clauses.extend([frozenset((4*u+1,)), frozenset((4*v+2,))])
    return clauses


def unit_conflict(clauses, assumptions):
    # Deliberately simple whole-database scans: no producer's occurrence-index
    # implementation and no SAT solver status are used.
    true = set(assumptions)
    if any(-x in true for x in true):
        return True
    while True:
        previous = len(true)
        for clause in clauses:
            if clause & true:
                continue
            remaining = [x for x in clause if -x not in true]
            if not remaining:
                return True
            if len(remaining) == 1:
                true.add(remaining[0])
        if len(true) == previous:
            return False


def rup(clauses, proof, nvars):
    database = list(clauses)
    additions = deletions = 0
    ended = False
    for line in proof.splitlines():
        check(not ended, 'text after terminal empty clause')
        words = line.split()
        check(bool(words), 'blank proof line')
        deletion = words[0] == 'd'
        if deletion:
            words = words[1:]
        values = list(map(int, words))
        check(values and values[-1] == 0, 'clause terminator')
        check(all(0 < abs(x) <= nvars for x in values[:-1]), 'literal range')
        clause = frozenset(values[:-1])
        if deletion:
            deletions += 1
            continue
        check(unit_conflict(database, [-x for x in clause]), 'invalid RUP addition')
        database.append(clause)
        additions += 1
        ended = not clause
    check(ended, 'missing empty clause')
    return additions, deletions


def chromatic_q11(word, proof):
    edges = {(u, v) for u, v in combinations(range(121), 2)
             if ((u % 11 - v % 11)**2 + (u // 11 - v // 11)**2) % 11 == 1}
    check(len(edges) == 726 and min(edges) == (0, 1), 'q11 direct graph')
    check(len(word) == 121 and all(type(c) is int and 0 <= c < 5 for c in word),
          'colour word shape')
    check(all(word[u] != word[v] for u, v in edges), 'q11 colour clash')
    clauses = cnf_for_graph(121, edges)
    additions, deletions = rup(clauses, proof, 484)
    return {'vertices': 121, 'edges': len(edges), 'cnf_variables': 484,
            'cnf_clauses': len(clauses), 'rup_additions': additions,
            'ignored_deletions': deletions, 'chromatic_number': 5}


def group_types(n, least=2):
    if n == 1:
        yield ()
    for divisor in range(least, n + 1):
        if n % divisor == 0:
            for tail in group_types(n // divisor, divisor):
                if not tail or tail[0] % divisor == 0:
                    yield (divisor,) + tail


def rational_basis(rows):
    basis = {}
    def reduce(row):
        row = list(map(Fraction, row))
        for pivot in sorted(basis):
            coefficient = row[pivot]
            if coefficient:
                row = [a - coefficient*b for a, b in zip(row, basis[pivot])]
        return row
    for row in rows:
        reduced = reduce(row)
        if any(reduced):
            pivot = next(i for i, x in enumerate(reduced) if x)
            basis[pivot] = [x/reduced[pivot] for x in reduced]
    return basis, reduce


def small_groups():
    counts = Counter()
    census = []
    for n in range(1, 13):
        for moduli in group_types(n):
            counts['group_types'] += 1
            vertices = list(product(*(range(m) for m in moduli)))
            lookup = {v: i for i, v in enumerate(vertices)}
            add = [[lookup[tuple((x+y) % m for x, y, m in zip(a, b, moduli))]
                    for b in vertices] for a in vertices]
            neg = [lookup[tuple(-x % m for x, m in zip(a, moduli))] for a in vertices]
            representatives = [s for s in range(1, n) if s <= neg[s]]
            def span(gens):
                answer = {0}
                for s in gens:
                    old = list(answer)
                    x = s
                    while x:
                        answer.update(add[t][x] for t in old)
                        x = add[x][s]
                return answer
            good = bad = 0
            for mask in range(1 << len(representatives)):
                selected = [s for j, s in enumerate(representatives) if mask >> j & 1]
                criterion = all(span([s]) & span([t for t in selected if t != s]) == {0}
                                for s in selected)
                connections = set(selected) | {neg[s] for s in selected}
                adjacency = [{add[v][s] for s in connections} for v in range(n)]
                # Enumerate all 4-cycles via pairs of opposite vertices, with
                # no assumption that their edge labels alternate generators.
                rows = []
                for a, c in combinations(range(n), 2):
                    for b, d in combinations(sorted(adjacency[a] & adjacency[c]), 2):
                        row = [0] * n
                        for v, coefficient in ((a, 1), (b, -1), (c, 1), (d, -1)):
                            row[v] += coefficient
                        rows.append(row)
                _, reduce = rational_basis(rows)
                collision = False
                for u, v in combinations(range(n), 2):
                    row = [0] * n
                    row[u], row[v] = 1, -1
                    if not any(reduce(row)):
                        collision = True
                        break
                check(collision == (not criterion), 'rational census mismatch')
                good += criterion
                bad += collision
            counts['presentations'] += good + bad
            counts['direct_products'] += good
            counts['forced_collisions'] += bad
            census.append([list(moduli), good, bad])
    return {'counts': dict(counts), 'by_invariant_factors': census,
            'arithmetic': 'rational, not modular'}


def negative_controls(certificate, proof, word):
    rejected = []
    def reject(name, operation):
        try:
            operation()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('negative control accepted: ' + name)
    corrupt = json.loads(json.dumps(certificate))
    corrupt['cases'][0]['redundancy']['terms'].pop()
    reject('false additive relation', lambda: finite_fields(corrupt))
    corrupt2 = json.loads(json.dumps(certificate))
    corrupt2['cases'][0]['modulus'] = [0, 0, 1]
    reject('reducible modulus', lambda: finite_fields(corrupt2))
    corrupt3 = json.loads(json.dumps(certificate))
    corrupt3['cases'].pop()
    reject('omitted parameter', lambda: finite_fields(corrupt3))
    reject('monochromatic q11 word', lambda: chromatic_q11([0]*121, proof))
    reject('unsupported empty clause', lambda: chromatic_q11(word, '0\n'))
    reject('contradiction to pinned colour', lambda: chromatic_q11(word, '-1 0\n' + proof))
    reject('missing proof terminator', lambda: chromatic_q11(word, '\n'.join(proof.splitlines()[:-1])))
    # A satisfiable tiny formula must reject an empty-clause proof; a genuine
    # unit contradiction must accept it. These audit the checker itself.
    reject('satisfiable one-variable formula', lambda: rup([frozenset((1,))], '0\n', 1))
    check(rup([frozenset((1,)), frozenset((-1,))], '0\n', 1) == (1, 0),
          'positive RUP control')
    return rejected


def main():
    check(len(sys.argv) == 2, 'usage: python3 verify.py /path/to/input-directory')
    directory = Path(sys.argv[1])
    manifest = json.loads(Path(__file__).with_name('inputs.json').read_text())
    for name, digest in manifest['sha256'].items():
        check(hashlib.sha256((directory/name).read_bytes()).hexdigest() == digest,
              'input SHA256: ' + name)
    certificate = json.loads((directory/'certificate.json').read_text())
    proof = (directory/'q11_four_unsat.drat').read_text()
    word = json.loads((directory/'q11_five_colouring.json').read_text())
    result = {'fields': finite_fields(certificate), 'q3': q3_drawing(),
              'q11': chromatic_q11(word, proof), 'small_groups': small_groups(),
              'negative_controls': negative_controls(certificate, proof, word),
              'status': 'PASS'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
