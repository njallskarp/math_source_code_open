"""Small exact checks of the algebraic corollary and a false shortcut."""
from itertools import combinations
from audit import reference_axes


def affine_audit():
    counts = dict(maps=0, fixed_point_free=0, involutions=0,
                  fixed_point_involutions=0)
    types = {}
    remaining = []
    for h in range(1, 64, 2):
        for b in range(64):
            phi = tuple((h*j+b) % 64 for j in range(64))
            assert len(set(phi)) == 64
            counts['maps'] += 1
            fixed = any(phi[j] == j for j in range(64))
            unseen = set(range(64))
            lengths = []
            while unseen:
                j = start = min(unseen)
                length = 0
                while j in unseen:
                    unseen.remove(j)
                    length += 1
                    j = phi[j]
                assert j == start and length & (length-1) == 0
                lengths.append(length)
            if not fixed:
                counts['fixed_point_free'] += 1
                assert all(length % 2 == 0 for length in lengths)
            involution = all(phi[phi[j]] == j for j in range(64))
            counts['involutions'] += involution
            if involution and fixed:
                counts['fixed_point_involutions'] += 1
                if (h, b) != (1, 0):
                    types[h] = types.get(h, 0)+1
                    if h not in (31, 63):
                        remaining.append([h, b])
    assert remaining == [[33, 0], [33, 32]]
    return {**counts, 'nonidentity_fixed_point_involution_types':
            {str(h): n for h, n in sorted(types.items())},
            'remaining_after_ordinary_and_mixed_exclusions': remaining}


def reflection_control():
    results = []
    for n in (4, 8, 16):
        total = failures = 0
        example = None
        for plus in combinations(range(n), n//2):
            row = [-1]*n
            for j in plus:
                row[j] = 1
            if not reference_axes(row):
                continue
            total += 1
            if not any(all(row[j] == row[(t-j) % n] for j in range(n))
                       for t in range(n)):
                failures += 1
                if example is None or row < example:
                    example = row
        results.append(dict(length=n, balanced_axis_words=total,
                            without_any_reflection=failures, example=example))
    assert results[-1]['without_any_reflection'] == 16
    return results


def run():
    return dict(affine=affine_audit(), reflection_control=reflection_control())


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
