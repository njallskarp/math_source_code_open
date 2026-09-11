"""Independent orbit-mass, counter, and definition-level interface audits."""

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
from math import factorial
from pathlib import Path

from model import ALL, BALLS, CNF, WORDS3, bits, build, check_words, distance


def canonical_and_stabilizer(mask):
    entries = [WORDS3[i] for i in bits(mask)]
    k = len(entries)
    if not k:
        return (), 82944
    best = None
    repetitions = 0
    for order in permutations(range(k)):
        columns = []
        for axis in range(3):
            seen = {}
            code = 0
            for i in order:
                value = entries[i][axis]
                if value not in seen:
                    seen[value] = len(seen)
                code = 4 * code + seen[value]
            columns.append(code)
        code = tuple(sorted(columns))
        if best is None or code < best:
            best, repetitions = code, 1
        elif code == best:
            repetitions += 1
    unused = 1
    for axis in range(3):
        unused *= factorial(4 - len({w[axis] for w in entries}))
    repeated_columns = 1
    for multiplicity in Counter(best).values():
        repeated_columns *= factorial(multiplicity)
    return best, repetitions * unused * repeated_columns


def labeled_layer_counts():
    """Four distinguished row matchings, disjoint in column-symbol pairs."""
    matchings = [0]
    for size in range(1, 5):
        for columns in combinations(range(4), size):
            for symbols in permutations(range(4), size):
                matchings.append(
                    sum(1 << (4 * c + s) for c, s in zip(columns, symbols, strict=True))
                )
    if len(matchings) != 209 or len(set(matchings)) != 209:
        raise ValueError("row matching generator")
    state = {0: 1}
    for _ in range(4):
        updated = defaultdict(int)
        for used, multiplicity in state.items():
            for row in matchings:
                if not used & row:
                    union = used | row
                    if union.bit_count() <= 7:
                        updated[union] += multiplicity
        state = updated
    counts = [0] * 8
    for union, multiplicity in state.items():
        counts[union.bit_count()] += multiplicity
    return counts


def audit_orbits(levels):
    weighted = []
    for k, representatives in enumerate(levels):
        canonical_codes = set()
        total = 0
        for mask in representatives:
            entries = [WORDS3[i] for i in bits(mask)]
            if len(entries) != k or any(distance(x, y) < 2 for x, y in combinations(entries, 2)):
                raise ValueError("bad orbit representative")
            code, stabilizer = canonical_and_stabilizer(mask)
            if code in canonical_codes or 82944 % stabilizer:
                raise ValueError("duplicate orbit or bad stabilizer")
            canonical_codes.add(code)
            total += 82944 // stabilizer
        weighted.append(total)
    direct = labeled_layer_counts()
    if weighted != direct:
        raise ValueError(f"orbit coverage mismatch: {weighted} != {direct}")
    return weighted


def truth(literal, values):
    if isinstance(literal, bool):
        return literal
    return values[abs(literal)] if literal > 0 else not values[-literal]


def extend_and_check(cnf, initial):
    values = dict(initial)
    for out, a, b, variable in cnf.gates:
        values[out] = truth(a, values) or (truth(b, values) and truth(variable, values))
    return all(any(truth(literal, values) for literal in row) for row in cnf.clauses)


def audit_counters():
    cases = 0
    for n in range(8):
        for lower in range(n + 1):
            for upper in range(lower, n + 1):
                cnf = CNF()
                variables = [cnf.variable() for _ in range(n)]
                cnf.cardinality(variables, lower, upper)
                for word in product([False, True], repeat=n):
                    answer = extend_and_check(cnf, dict(zip(variables, word, strict=True)))
                    if answer != (lower <= sum(word) <= upper):
                        raise ValueError("counter boundary error")
                    cases += 1
    return cases


def audit_binary_interface():
    """All 65536 subsets of H(4,2), using binary flip neighborhoods."""
    full_balls = [(1 << x) | sum(1 << (x ^ (1 << j)) for j in range(4)) for x in range(16)]
    small_balls = [(1 << x) | sum(1 << (x ^ (1 << j)) for j in range(3)) for x in range(8)]
    spectrum = Counter()
    independent_count = 0
    for mask in range(1 << 16):
        chosen = [i for i in range(16) if mask >> i & 1]
        independent = all((i ^ j).bit_count() >= 2 for i, j in combinations(chosen, 2))
        full_coverage = 0
        for i in chosen:
            full_coverage |= full_balls[i]
        direct = independent and full_coverage == (1 << 16) - 1
        slices = [mask & 255, mask >> 8]
        layer_cover = []
        internal = True
        for s in slices:
            cover = 0
            for i in range(8):
                if s >> i & 1:
                    cover |= small_balls[i]
                    if s & (small_balls[i] ^ (1 << i)):
                        internal = False
            layer_cover.append(cover)
        by_layers = (
            internal
            and not (slices[0] & slices[1])
            and all((layer_cover[i] | slices[1 - i]) == 255 for i in range(2))
        )
        if direct != by_layers:
            raise ValueError("binary layer interface mismatch")
        independent_count += independent
        if direct:
            spectrum[len(chosen)] += 1
    return {
        "subsets": 65536,
        "independent_subsets": independent_count,
        "maximal_counts_by_size": dict(sorted(spectrum.items())),
    }


def audit_positive_controls():
    base = Path(__file__).parent
    results = []
    for size in [28, 30]:
        words = [
            tuple(w)
            for w in json.loads((base / f"control{size}.json").read_text())["selected_words"]
        ]
        histogram = check_words(words, size)
        minimum = min(
            sum(w[axis] == value for w in words) for axis in range(4) for value in range(4)
        )
        checked = 0
        for axis in range(4):
            for value in range(4):
                if sum(w[axis] == value for w in words) != minimum:
                    continue
                axes = [axis] + [a for a in range(4) if a != axis]
                values = [value] + [v for v in range(4) if v != value]
                transformed = [
                    (values.index(w[axis]), *(w[a] for a in axes[1:])) for w in words
                ]
                chosen = {WORDS3.index(w[1:]) for w in transformed if w[0] == 0}
                mask = sum(1 << i for i in chosen)
                coverage = 0
                for i in chosen:
                    coverage |= BALLS[i]
                holes = ALL ^ coverage
                labels = {w[1:]: w[0] - 1 for w in transformed if w[0] != 0}
                a = next(bits(holes))
                old0 = labels[WORDS3[a]]
                near = BALLS[a] & ~(1 << a) & holes
                old_order = [old0]
                if near:
                    old_order.append(labels[WORDS3[next(bits(near))]])
                old_order += [c for c in range(3) if c not in old_order]
                if len(old_order) != 3 or len(set(old_order)) != 3:
                    raise ValueError("invalid color symmetry normalization")
                labels = {w: old_order.index(c) for w, c in labels.items()}
                cnf, color, _ = build(mask, size)
                initial = {var: labels.get(WORDS3[i]) == c for (i, c), var in color.items()}
                initial.update({var: WORDS3[i] in labels for i, var in cnf.occupied.items()})
                if not extend_and_check(cnf, initial):
                    raise ValueError("known positive code fails the encoded interface")
                checked += 1
        bad = list(words)
        bad[1] = bad[0]
        try:
            check_words(bad, size)
        except ValueError:
            pass
        else:
            raise ValueError("duplicate corruption accepted")
        results.append(
            {
                "size": size,
                "minimum_slice": minimum,
                "minimum_slice_orientations_checked": checked,
                "coverage_histogram": histogram,
            }
        )
    return results


def run_audits(levels):
    result = {
        "labeled_layer_counts": audit_orbits(levels),
        "counter_assignments": audit_counters(),
        "binary_interface": audit_binary_interface(),
        "positive_controls": audit_positive_controls(),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["audit_sha256"] = hashlib.sha256(encoded).hexdigest()
    expected = Path(__file__).with_name("EXPECTED_AUDIT.json")
    # JSON turns integer dictionary keys into strings.
    if expected.exists() and json.loads(json.dumps(result)) != json.loads(expected.read_text()):
        raise ValueError("audit differs from committed expected result")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("orbits", type=Path)
    args = parser.parse_args()
    levels = json.loads(args.orbits.read_text())["levels"]
    result = run_audits(levels)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
