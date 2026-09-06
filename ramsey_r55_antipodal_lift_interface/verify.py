"""Exact full-K5 block-support certificate; no solver or graph search.

Two generators compare every physical (five-set, color), not just totals.
The theorem and the precise conditional-domain boundary are in README.md.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path

N = 43
H_SHA = "926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466"
ROOTS = (0, 1, 38)
STARS = {
    0: set(range(10, 14)) | {18, 19, 38} | set(range(29, 38)) | set(range(39, 43)),
    1: set(range(14, 20)) | set(range(20, 29)) | set(range(38, 43)),
    38: set(range(20)),
}
BLOCKS = (
    (tuple(range(39, 43)), tuple(range(2, 10))),
    (tuple(range(10, 14)), tuple(range(20, 29))),
    (tuple(range(14, 18)), tuple(range(29, 38))),
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def pair(a, b):
    return (a, b) if a < b else (b, a)


def fixed_colors():
    raw = Path(__file__).with_name("H92.json").read_bytes()
    need(sha256(raw).hexdigest() == H_SHA, "H92 identity")
    obj = json.loads(raw)
    need(obj["n"] == 20 and len(obj["red_edges"]) == 92, "core dimensions")
    edges = [tuple(e) for e in obj["red_edges"]]
    need(edges == sorted(set(edges)), "canonical core edges")
    need(all(len(e) == 2 and 0 <= e[0] < e[1] < 20 for e in edges), "core labels")
    red = set(edges)
    fixed = {e: int(e in red) for e in combinations(range(20), 2)}
    for r in ROOTS:
        for v in range(N):
            if v == r:
                continue
            e, c = pair(r, v), int(v in STARS[r])
            need(e not in fixed or fixed[e] == c, "consistent stars")
            fixed[e] = c
    need(len(fixed) == 276, "fixed pair count")
    need(all(sum(fixed[pair(r, v)] for v in range(N) if v != r) == 20
             for r in ROOTS), "root degrees")
    return fixed


def block_owner(blocks, fixed):
    used, owner = set(), {}
    for i, (left, right) in enumerate(blocks):
        vertices = list(left) + list(right)
        need(len(set(vertices)) == len(vertices), "disjoint block sides")
        need(not (set(vertices) & used), "vertex-disjoint blocks")
        used.update(vertices)
        for u in left:
            for v in right:
                e = pair(u, v)
                need(e not in fixed and e not in owner, "unfixed block pair")
                owner[e] = i
    return owner


CHOOSE = [[comb(v, k) if v >= k else 0 for k in range(6)] for v in range(N)]


def address(vertices, color):
    # Colexicographic rank of a 5-subset; color 0 precedes color 1.
    return 2 * sum(CHOOSE[v][i + 1] for i, v in enumerate(vertices)) + color


def literal_atlas(fixed, owner):
    """Direct scan of all physical five-sets and their ten physical pairs."""
    atlas = bytearray(2 * comb(N, 5))
    counts, widths, patterns, examples = Counter(), Counter(), set(), {}
    seen_ranks = bytearray(comb(N, 5))
    for vertices in combinations(range(N), 5):
        pos = address(vertices, 0)
        need(not seen_ranks[pos // 2], "rank collision")
        seen_ranks[pos // 2] = 1
        edges = tuple(combinations(vertices, 2))
        prescribed = {fixed[e] for e in edges if e in fixed}
        if len(prescribed) > 1:
            continue
        groups = Counter(owner[e] for e in edges if e in owner)
        mask = sum(1 << i for i in groups)
        width = sum(groups.values())
        need(mask.bit_count() <= 2, "three-block five-set")
        need(width <= (3 if mask.bit_count() == 2 else 6), "width bound")
        retained = sum(e not in fixed and e not in owner for e in edges)
        patterns.add((retained, tuple(sorted(groups.values()))))
        for color in sorted(prescribed) if prescribed else (0, 1):
            atlas[pos + color] = 8 + mask + 16 * width
            counts[(color, mask)] += 1
            widths[(mask.bit_count(), width)] += 1
            examples.setdefault((color, mask, width), vertices)
    need(all(seen_ranks), "rank coverage")
    return atlas, counts, widths, patterns, examples


def recursive_atlas(fixed):
    """Independent possible-clique recursion and signature-occupancy arity."""
    atlas = bytearray(2 * comb(N, 5))
    signatures = {
        v: sum(fixed[pair(v, r)] << (2 - k) for k, r in enumerate(ROOTS))
        for v in range(N) if v not in ROOTS
    }
    need({s: sorted(v for v, t in signatures.items() if t == s)
          for s in set(signatures.values())} ==
         {1: list(range(2, 10)), 2: list(range(20, 29)),
          3: list(range(14, 18)), 4: list(range(29, 38)),
          5: list(range(10, 14)), 6: list(range(39, 43)), 7: [18, 19]},
         "physical signature classes")
    for color in (0, 1):
        adjacency = [sum(1 << v for v in range(N)
                         if v != u and fixed.get(pair(u, v), color) == color)
                     for u in range(N)]

        def visit(prefix, candidates):
            if len(prefix) == 5:
                occupancy = Counter(signatures[v] for v in prefix if v in signatures)
                products = [occupancy[s] * occupancy[7 - s] for s in (1, 2, 3)]
                width = sum(products)
                mask = sum(1 << i for i, w in enumerate(products) if w)
                pos = address(prefix, color)
                need(atlas[pos] == 0, "recursive duplicate")
                atlas[pos] = 8 + mask + 16 * width
                return
            while candidates and candidates.bit_count() >= 5 - len(prefix):
                bit = candidates & -candidates
                candidates ^= bit
                v = bit.bit_length() - 1
                visit(prefix + (v,), candidates & adjacency[v])

        visit((), (1 << N) - 1)
    signature_owner = {
        (u, v): min(signatures[u], signatures[v]) - 1
        for u, v in combinations(sorted(signatures), 2)
        if signatures[u] ^ signatures[v] == 7
    }
    return atlas, signature_owner


def compare(actual, expected):
    need(actual == expected, "entrywise atlas disagreement")


def local_truth_checks(patterns):
    """Permutation-invariant predicate check for every occurring free-edge shape."""
    cases = 0
    for retained, groups in sorted(patterns):
        for color in (0, 1):
            for bits in product((0, 1), repeat=retained + sum(groups)):
                literal_bad = all(b == color for b in bits)
                enabled = all(b == color for b in bits[:retained])
                factor_bad = enabled
                cursor = retained
                for width in groups:
                    factor_bad &= all(b == color for b in bits[cursor:cursor + width])
                    cursor += width
                need(literal_bad == factor_bad, "factored local predicate")
                cases += 1
    return cases


def join_checks():
    """All binary relations on three two-element domains; not a Ramsey model."""
    checked, nonempty_without_triangle = 0, 0
    for a, b, c in product(range(16), repeat=3):
        direct = [(x, y, z) for x, y, z in product((0, 1), repeat=3)
                  if a >> (2 * x + y) & 1 and b >> (2 * x + z) & 1
                  and c >> (2 * y + z) & 1]
        joined = []
        for x, y in product((0, 1), repeat=2):
            if a >> (2 * x + y) & 1:
                common = ((b >> (2 * x)) & 3) & ((c >> (2 * y)) & 3)
                for z in (0, 1):
                    if common >> z & 1:
                        joined.append((x, y, z))
        need(direct == joined, "joint witnesses, not separate existential witnesses")
        checked += 1
        nonempty_without_triangle += bool(a and b and c and not direct)
    # R01 and R02 are equality, R12 is inequality: every edge has support.
    need(not any(x == y and x == z and y != z
                 for x, y, z in product((0, 1), repeat=3)), "odd compatibility cycle")
    return checked, nonempty_without_triangle


def controls(atlas, reference, fixed):
    accepted = next(i for i, x in enumerate(atlas) if x)
    rejected = next(i for i, x in enumerate(atlas) if not x)
    changes = {
        "omitted_record": (accepted, 0),
        "extra_record": (rejected, 8),
        "changed_block_support": (accepted, atlas[accepted] ^ 1),
        "changed_literal_width": (accepted, atlas[accepted] ^ 16),
    }
    passed = []
    for name, (pos, value) in changes.items():
        broken = atlas.copy()
        broken[pos] = value
        try:
            compare(broken, reference)
        except ValueError:
            passed.append(name)
        else:
            raise ValueError("negative control accepted: " + name)
    try:
        block_owner((BLOCKS[0], BLOCKS[0], BLOCKS[2]), fixed)
    except ValueError:
        passed.append("overlapping_blocks")
    else:
        raise ValueError("overlapping blocks accepted")
    return sorted(passed)


def main():
    fixed = fixed_colors()
    owner = block_owner(BLOCKS, fixed)
    need(len(owner) == 104, "removed edge count")
    atlas, counts, widths, patterns, examples = literal_atlas(fixed, owner)
    reference, signature_owner = recursive_atlas(fixed)
    need(signature_owner == owner, "all physical block-literal identities")
    covered = {v for edge in owner for v in edge}
    need(sorted(set(range(N)) - covered) == [0, 1, 18, 19, 38],
         "outside residual vertices")
    for r in (0, 1):
        blue = set(range(N)) - {r} - STARS[r]
        need(not any(u in blue and v in blue for u, v in owner),
             "density independent of removed pairs")
    compare(atlas, reference)
    need(set(mask for _, mask in counts) == {0, 1, 2, 3, 4, 5, 6},
         "all and only zero/unary/binary block supports")
    truth_cases = local_truth_checks(patterns)
    joins, failures = join_checks()
    report = {
        "scope": "exact labeled full-K5 lifting interface; no Ramsey verdict",
        "n": N,
        "physical_five_sets": comb(N, 5),
        "possible_color_records": sum(counts.values()),
        "fixed_pairs": len(fixed),
        "retained_pairs": comb(N, 2) - len(fixed) - len(owner),
        "removed_pairs": len(owner),
        "physical_pair_ownership_checked": comb(N, 2),
        "atlas_bytes": len(atlas),
        "atlas_sha256": sha256(atlas).hexdigest(),
        "color_and_block_counts": [
            {"color": color, "blocks": [i for i in range(3) if mask >> i & 1],
             "records": count} for (color, mask), count in sorted(counts.items())],
        "arity_width_counts": [
            {"arity": arity, "width": width, "records": count}
            for (arity, width), count in sorted(widths.items())],
        "six_literal_example": list(examples[(1, 1, 6)]),
        "three_literal_cross_example": list(examples[(1, 5, 3)]),
        "local_predicate_shapes": len(patterns),
        "local_truth_assignments": truth_cases,
        "abstract_relation_networks_checked": joins,
        "abstract_nonempty_pair_relations_without_triangle": failures,
        "negative_controls": controls(atlas, reference, fixed),
        "full_retained_assignments_enumerated": 0,
        "matrix_domains_enumerated": False,
        "solver_called": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
