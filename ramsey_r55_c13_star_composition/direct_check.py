#!/usr/bin/env python3
"""Separate literal-graph reduction and bounded Boolean deletion checker.

No imports from verify.py, the footprint checker, or the cube classifier.
"""

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    raw = (ROOT / "selection.json").read_bytes()
    check(sha256(raw).hexdigest() ==
          "ebe63f742ec0fe25ace4aa14eecfada571592440001cb682e41389c834acedcc",
          "input identity")
    selection = json.loads(raw)
    certificate = json.loads((ROOT / "certificate.json").read_text())
    red = set()
    fixed = set(combinations(range(43), 2)) - set(combinations(range(15, 43), 2))
    red.add((0, 1))
    for h in range(13):
        red.update({(0, h + 2), (1, h + 2)})
        for difference in (1, 5, 8, 12):
            red.add(tuple(sorted((h + 2, (h + difference) % 13 + 2))))
    for x, text in enumerate(selection["footprints"]):
        binary = format(int(text, 16), "013b")[::-1]
        for h, bit in enumerate(binary):
            if bit == "1":
                red.add((h + 2, x + 15))
        if x < 7:
            red.add((0, x + 15))
        elif x < 14:
            red.add((1, x + 15))

    # Each row is a literal monochromatic-five-set prohibition.
    origins = []
    for x, y, triple in certificate["blue_pair_witnesses"]:
        origins.append((f"blue-{x}-{y}", 0, sorted([x + 15, y + 15] + [h + 2 for h in triple])))
    for x, y, pair in certificate["red_pair_witnesses"]:
        origins.append((f"red-{x}-{y}", 1, sorted([1, x + 15, y + 15] + [h + 2 for h in pair])))
    origins.append(("star", 1, [x + 15 for x in certificate["five"]]))
    clauses = []
    truth_cases = 0
    for name, forbidden, vertices in origins:
        check(len(set(vertices)) == 5, "five distinct vertices")
        pairs = list(combinations(vertices, 2))
        known = [e for e in pairs if e in fixed]
        unknown = [e for e in pairs if e not in fixed]
        check(all(int(e in red) == forbidden for e in known), "literal row fixed colors")
        check(len(unknown) == (10 if name == "star" else 1), "literal row width")
        clauses.append((name, forbidden, unknown))
        for bits in product((0, 1), repeat=len(unknown)):
            assignment = dict(zip(unknown, bits))
            colors = [int(e in red) if e in fixed else assignment[e] for e in pairs]
            nonmonochromatic = not (all(colors) or not any(colors))
            disjunction = any(assignment[e] != forbidden for e in unknown)
            # For the ten-free-edge row we check just the specified red clause.
            expected = not all(colors) if name == "star" else nonmonochromatic
            check(disjunction == expected, "literal truth table")
            truth_cases += 1

    b_vertices = tuple(x + 15 for x in range(7, 14))
    b_pairs = list(combinations(b_vertices, 2))
    star_pairs = clauses[-1][2]
    units = {edges[0]: 1 - color for _, color, edges in clauses[:-1]}
    check(len(units) == 17, "17 distinct units")
    forbidden_b = {e for e in b_pairs if units.get(e) == 0}
    check(len(forbidden_b) == 8, "B capacity")
    target = 61 - sum(int(selection["footprints"][x], 16).bit_count() for x in range(7, 14))
    check(target == certificate["target_edges"] == 13, "derived B quota")
    propagated = units.copy()
    for e in b_pairs:
        propagated[e] = int(e not in forbidden_b)
    check(sum(propagated[e] for e in b_pairs) == target, "saturated B")
    check(all(propagated[e] == 1 for e in star_pairs), "forced literal red K5")

    # Find a Boolean model for each one-row deletion by enumerating only the
    # ten star edges, then filling the unconstrained B edges to the quota.
    # This is a bounded verifier, not a SAT/UNSAT claim from a solver.
    all_names = [name for name, _, _ in clauses] + ["quota"]
    deletion_models = 0
    for dropped in all_names:
        kept = [(name, color, edges) for name, color, edges in clauses if name != dropped]
        found = False
        for bits in product((0, 1), repeat=10):
            assignment = dict(zip(star_pairs, bits))
            valid = True
            for _, color, edges in kept:
                if len(edges) == 1:
                    e = edges[0]
                    if e in assignment and assignment[e] == color:
                        valid = False
                        break
                    assignment[e] = 1 - color
            if not valid:
                continue
            if any(all(e in assignment for e in edges) and
                   all(assignment[e] == color for e in edges)
                   for _, color, edges in kept):
                continue
            free = [e for e in b_pairs if e not in assignment]
            current = sum(assignment.get(e, 0) for e in b_pairs)
            needed = 0 if dropped == "quota" else target - current
            if not 0 <= needed <= len(free):
                continue
            assignment.update({e: int(k < needed) for k, e in enumerate(free)})
            for e in set(b_pairs) | set(star_pairs):
                assignment.setdefault(e, 0)
            violations = []
            for name, color, vertices in origins:
                colors = [int(e in red) if e in fixed else assignment[e]
                          for e in combinations(vertices, 2)]
                if all(c == color for c in colors):
                    violations.append(name)
            if sum(assignment[e] for e in b_pairs) != target:
                violations.append("quota")
            check(violations == [dropped], "direct deletion model")
            found = True
            break
        check(found, "missing deletion model")
        deletion_models += 1

    signatures = []
    for x in certificate["five"]:
        signatures.append([int((h + 2, x + 15) in red) for h in certificate["anchors"]])
    check(sorted(signatures) == [[0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0]],
          "literal cube star")
    print(json.dumps({
        "status": "DIRECT LITERAL COMPOSITION AUDIT PASS",
        "K5_origins": len(origins),
        "literal_truth_table_cases": truth_cases,
        "Boolean_deletion_models": deletion_models,
        "B_red_capacity_before_mixed_cut": 13,
        "forced_red_edges_on_star": sum(propagated[e] for e in star_pairs),
        "star_vertices_full_labels": [x + 15 for x in certificate["five"]],
        "anchor_vertices_full_labels": [h + 2 for h in certificate["anchors"]],
        "signature_coordinate_vectors": signatures,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
