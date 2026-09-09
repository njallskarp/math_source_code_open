"""Independent signed-component lift and direct-array correlation audit."""
import argparse
from itertools import product
import json
from pathlib import Path
import subprocess


def constraint_lifts(z, h):
    """Solve signed equality components, without the searcher's orbit formulas."""
    m = len(z)
    n = 2*m
    edges = [[] for _ in range(n)]
    forced = {}
    for j in range(n):
        edges[j].append((h*j % n, 1))
    for j, v in enumerate(z):
        sign = -1 if v == 0 else 1
        edges[j].append((j+m, sign))
        edges[j+m].append((j, sign))
        if v:
            forced[j] = forced[j+m] = v
    unseen = set(range(n))
    components = []
    while unseen:
        root = min(unseen)
        relative = {root: 1}
        todo = [root]
        for j in todo:
            for k, sign in edges[j]:
                value = sign*relative[j]
                if k in relative:
                    assert relative[k] == value
                else:
                    relative[k] = value
                    todo.append(k)
        unseen.difference_update(relative)
        required = {forced[j]*v for j, v in relative.items() if j in forced}
        assert len(required) <= 1
        options = required or {-1, 1}
        components.append(tuple(sum(1 << j for j, v in relative.items()
                                    if v*sign == -1) for sign in options))
    words = {0}
    for choices in components:
        words = {word | option for word in words for option in choices}
    return words


def binary(word, n=64):
    return tuple(1-2*((word >> j) & 1) for j in range(n))


def correlation(x, y, k):
    return sum(a*y[(j+k) % len(x)] for j, a in enumerate(x))


def direct_key(xword, yword, h):
    x, y = binary(xword), binary(yword)
    shifts = range(2, 16, 2) if h == 31 else range(1, 16)
    real = [correlation(x, x, k)+correlation(y, y, k) for k in shifts]
    assert all(v % 4 == 0 for v in real)
    real = [v//4 for v in real]
    if h == 63:
        return 1, real
    imag = [correlation(x, y, k)-correlation(y, x, k) for k in range(1, 16, 2)]
    assert all(v % 4 == 0 for v in imag)
    sign = next((1 if v > 0 else -1 for v in imag if v), 1)
    return sign, real+[sign*v//4 for v in imag]


def small_order_audit():
    result = []
    for n in (8, 16):
        for h in (n//2-1, n-1):
            unseen = set(range(n))
            orbits = []
            while unseen:
                j = min(unseen)
                orbit = {j, h*j % n}
                unseen -= orbit
                orbits.append(orbit)
            groups = {}
            for signs in product((-1, 1), repeat=len(orbits)):
                row = [0]*n
                for orbit, sign in zip(orbits, signs):
                    for j in orbit:
                        row[j] = sign
                if sum(row) not in (0, 2):
                    continue
                z = tuple((row[j]+row[j+n//2])//2 for j in range(n//2))
                word = sum(1 << j for j, v in enumerate(row) if v == -1)
                groups.setdefault(z, set()).add(word)
            for z, expected in groups.items():
                assert constraint_lifts(z, h) == expected
            result.append({'n': n, 'h': h, 'compressed_rows': len(groups),
                           'full_rows': sum(map(len, groups.values()))})
    return result


def main(executable, input_path):
    report = {'small_order_direct_orbit_comparisons': small_order_audit(),
              'native_comparisons': []}
    for h in (31, 63):
        process = subprocess.Popen([str(executable.resolve()), str(input_path),
                                    str(h), '--audit'], stdout=subprocess.PIPE,
                                   text=True)
        rows = words = keys = 0
        for line in process.stdout:
            fields = line.split()
            if fields[0] == 'R':
                z = tuple(map(int, fields[1:33]))
                count = int(fields[33])
                actual = list(map(int, fields[34:]))
                expected = constraint_lifts(z, h)
                assert count == len(actual) == len(set(actual))
                assert set(actual) == expected
                rows += 1
                words += count
            elif fields[0] == 'K':
                x, y, sign, *key = map(int, fields[1:])
                assert direct_key(x, y, h) == (sign, key)
                keys += 1
            else:
                raise AssertionError(line)
        assert process.wait() == 0
        report['native_comparisons'].append(
            {'h': h, 'complete_row_sets': rows, 'full_words': words,
             'direct_array_pair_keys': keys})
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('executable', type=Path)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    main(args.executable, args.input)
