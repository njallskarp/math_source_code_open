"""Independent, solver-free review of the pinned six-neighborhood projection.

The only upstream code executed is the hash-pinned generator under review.
Our checks import none of its modules. All downloaded/generated state is
temporary; the compact JSON result is written to stdout.
"""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.request

COMMIT = "40a6cd7ffbe45892bd52e3dfcdbb086f1b5afbfd"
BASE = ("https://raw.githubusercontent.com/helgithorskarp/math_results/"
        + COMMIT + "/ramsey_r55_antipodal_degree_projection/")
PINS = {
    "model.py": "f93bc5bdb33f920f4c1483652c6fa8478da76464f57d97ece7898f4bdafb7afd",
    "flow.py": "fa9aa09354729c704a5065b8dd7cbefe50a620c048533f23632c0173f2e8dab0",
    "H92.json": "926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466",
}
CNF_PIN = "ece2f0c1a0ebf7f43fee80bd848b0ff082602e91f36bdc9946cff230e8a4ac25"
DESC_PIN = "0a5407af70b1711597b9bdd7a46753c78ee33a297f4812fc9b271172d6c2331a"
V = frozenset(range(43))
ROOTS = (0, 1, 38)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pairs(vertices):
    return itertools.combinations(sorted(vertices), 2)


def geometry(h):
    require(h["n"] == 20, "H order")
    edges = h["red_edges"]
    require(all(type(e) is list and len(e) == 2
                and all(type(v) is int for v in e)
                and 0 <= e[0] < e[1] < 20 for e in edges), "H edge syntax")
    require(edges == sorted(edges) and len({tuple(e) for e in edges}) == 92,
            "H edge count/uniqueness/order")
    red = {tuple(e) for e in edges}
    stars = {
        0: frozenset([10, 11, 12, 13, 18, 19] + list(range(29, 43))),
        1: frozenset(list(range(14, 29)) + list(range(38, 43))),
        38: frozenset(range(20)),
    }
    fixed = {e: e in red for e in pairs(range(20))}
    for root, neighbors in stars.items():
        for vertex in V - {root}:
            e = tuple(sorted((root, vertex)))
            color = vertex in neighbors
            require(e not in fixed or fixed[e] == color, "fixed-star consistency")
            fixed[e] = color
    neighborhoods = [(root, color, stars[root] if color else V - {root} - stars[root])
                     for root in ROOTS for color in (False, True)]
    free = [e for e in pairs(V) if e not in fixed]
    # Derive removal from actual predicate domains, not named blocks/signatures.
    hidden = {e for e in free if not any(set(e) <= n for _, _, n in neighborhoods)}
    adjacency = {v: set() for e in hidden for v in e}
    for u, v in hidden:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(adjacency)
    blocks = []
    while unseen:
        start = min(unseen)
        component, stack = {start}, [start]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor not in component:
                    component.add(neighbor)
                    stack.append(neighbor)
        right = adjacency[start]
        left = component - right
        require(all(adjacency[v] == right for v in left)
                and all(adjacency[v] == left for v in right), "complete bipartite component")
        if len(left) > len(right):
            left, right = right, left
        blocks.append((sorted(left), sorted(right)))
        unseen -= component
    blocks.sort(key=lambda b: (len(b[1]), b[0]))
    visible = [e for e in free if e not in hidden]
    require(len(fixed) == 276 and len(free) == 627 and len(visible) == 523
            and len(hidden) == 104, "physical pair partition")
    require([list(map(len, b)) for b in blocks] == [[4, 8], [4, 9], [4, 9]],
            "block dimensions")
    # Independently verify the complementary-signature characterization.
    for u, v in free:
        complementary = all((u in stars[r]) != (v in stars[r]) for r in ROOTS)
        require(((u, v) in hidden) == complementary, "signature equivalence")
    return fixed, neighborhoods, visible, hidden, blocks


def compatible_subsets(vertices, size, color, fixed):
    """Clique-extension recursion, pruning fixed wrong-color pairs early."""
    def visit(chosen, candidates):
        remaining = size - len(chosen)
        if remaining == 0:
            yield chosen
            return
        for i in range(len(candidates) - remaining + 1):
            vertex = candidates[i]
            tail = [v for v in candidates[i + 1:]
                    if fixed.get((vertex, v), color) == color]
            yield from visit(chosen + [vertex], tail)
    yield from visit([], sorted(vertices))


def expected_clauses(fixed, neighborhoods, visible):
    index = {e: i + 1 for i, e in enumerate(visible)}
    clauses = set()
    for _, root_color, vertices in neighborhoods:
        for bad_color in (False, True):
            size = 4 if bad_color == root_color else 5
            for subset in compatible_subsets(vertices, size, bad_color, fixed):
                unknown = [e for e in pairs(subset) if e not in fixed]
                require(unknown and all(e in index for e in unknown), "clique support")
                clauses.add(tuple(sorted((-1 if bad_color else 1) * index[e] for e in unknown)))
    return sorted(clauses, key=lambda c: (len(c), c))


def check_descriptor(data, fixed, neighborhoods, visible, hidden, blocks):
    # Exact schema check deliberately detects omissions, including redundant cuts.
    index = {e: i + 1 for i, e in enumerate(visible)}
    require(data["format"] == "ramsey-six-neighborhood-degree-projection-v1", "format")
    require(data["variables"] == len(visible)
            and data["visible_pairs"] == [list(e) for e in visible]
            and data["removed_pairs"] == [list(e) for e in sorted(hidden)], "physical indices")
    require(data["H_sha256"] == PINS["H92.json"]
            and data["neighborhood_cnf_sha256"] == CNF_PIN, "descriptor identities")
    for v, row in enumerate(data["residuals"]):
        incident_fixed = [e for e in fixed if v in e and fixed[e]]
        incident_visible = [index[e] for e in visible if v in e]
        require(row == {"vertex": v, "constant": (20 if v in ROOTS else 21) - len(incident_fixed),
                        "subtract_variables": incident_visible}, "degree residual")
    require(len(data["residuals"]) == 43, "all residuals")
    endpoints = [v for l, r in blocks for v in l + r]
    require(len(endpoints) == len(set(endpoints)), "disjoint block vertices")
    outside = sorted(V - set(endpoints))
    require(data["residual_zero_vertices"] == outside == [0, 1, 18, 19, 38], "outside equations")
    expected_densities = []
    for root, color, n in neighborhoods:
        if root in (0, 1) and not color:
            es = list(pairs(n))
            require(not hidden.intersection(es), "density independent of hidden edges")
            expected_densities.append({
                "root": root, "equals": 124 - sum(fixed.get(e, False) for e in es),
                "sum_variables": [index[e] for e in es if e in index]})
    require(data["density_equalities"] == expected_densities, "density equations")
    require(len(data["blocks"]) == len(blocks), "number of margin blocks")
    for row, (left, right) in zip(data["blocks"], blocks):
        require(row["left"] == left and row["right"] == right
                and row["row_bounds"] == [0, len(right)]
                and row["column_bounds"] == [0, len(left)]
                and row["equal_margin_totals"] is True, "margin bounds/balance")
        subsets = [tuple(s) for s in row["subset_cuts"]]
        expected = {s for k in range(1, len(left) + 1) for s in itertools.combinations(left, k)}
        require(len(subsets) == len(expected) and set(subsets) == expected, "all labeled cuts")
        require(row["cut_semantics"] ==
                "sum residuals on S <= sum min(residual at j, size(S)) over right j", "cut semantics")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, help="offline directory containing the three pinned inputs")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="r55-projection-review-") as td:
        work = Path(td)
        for name, pin in PINS.items():
            raw = (args.upstream / name).read_bytes() if args.upstream else urllib.request.urlopen(
                BASE + name, timeout=60).read()
            require(digest(raw) == pin, "pinned source " + name)
            (work / name).write_bytes(raw)
        # Generator under review is a black box, not a checker dependency.
        command = [sys.executable]
        if sys.flags.optimize:
            command.append("-O")
        subprocess.run(command + [str(work / "model.py"), "--work", str(work / "generated")],
                       check=True, capture_output=True, text=True, timeout=90)
        fixed, neighborhoods, visible, hidden, blocks = geometry(
            json.loads((work / "H92.json").read_text()))
        clauses = expected_clauses(fixed, neighborhoods, visible)
        expected = ("p cnf 523 " + str(len(clauses)) + "\n" +
                    "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)).encode()
        actual = (work / "generated/neighborhood_clauses.cnf").read_bytes()
        require(actual == expected and digest(actual) == CNF_PIN, "complete physical CNF bytes")
        raw_descriptor = (work / "generated/projection.json").read_bytes()
        require(digest(raw_descriptor) == DESC_PIN, "descriptor bytes")
        data = json.loads(raw_descriptor)
        check_descriptor(data, fixed, neighborhoods, visible, hidden, blocks)
        bad = {}
        for label in ("visible_pair", "residual", "density", "outside", "bound", "balance", "cut"):
            d = copy.deepcopy(data)
            if label == "visible_pair": d["visible_pairs"][0] = d["visible_pairs"][1]
            if label == "residual": d["residuals"][2]["constant"] += 1
            if label == "density": d["density_equalities"][0]["equals"] += 1
            if label == "outside": d["residual_zero_vertices"].remove(18)
            if label == "bound": d["blocks"][0]["column_bounds"][1] += 1
            if label == "balance": d["blocks"][1]["equal_margin_totals"] = False
            if label == "cut": d["blocks"][2]["subset_cuts"].pop()
            try:
                check_descriptor(d, fixed, neighborhoods, visible, hidden, blocks)
            except ValueError:
                bad[label] = "rejected"
            else:
                raise ValueError("mutation accepted: " + label)
        support = {abs(lit) for c in clauses for lit in c}
        require(support == set(range(1, 524)), "every retained edge occurs in local CNF")
        # Small exact stress test of the proof's cut-minimization identity.
        rows, columns = [4, 4, 0, 0], [3, 3, 1, 1, 0, 0, 0, 0]
        require(sum(rows) == sum(columns) == 8, "counterexample balance")
        cut_checks = 0
        for mask in range(16):
            s = [i for i in range(4) if mask >> i & 1]
            demands = sum(rows[i] for i in s)
            cut_minimum = min(
                8 - demands + len(s) * (8 - len(t)) + sum(columns[j] for j in t)
                for k in range(9) for t in itertools.combinations(range(8), k))
            formula = 8 - demands + sum(min(c, len(s)) for c in columns)
            require(cut_minimum == formula, "exact source-cut minimization")
            cut_checks += 256
        require(all(r <= sum(min(c, 1) for c in columns) for r in rows), "singleton cuts pass")
        require(rows[0] + rows[1] > sum(min(c, 2) for c in columns), "two-row cut fails")
        result = {
            "status": "INDEPENDENT_FIXED_SUBSYSTEM_PROJECTION_REVIEW_PASS",
            "source_commit": COMMIT,
            "fixed_pairs": len(fixed), "free_pairs_before": len(visible) + len(hidden),
            "retained_pairs": len(visible), "eliminated_pairs": len(hidden),
            "blocks": [{"left": l, "right": r} for l, r in blocks],
            "local_clauses": len(clauses), "retained_variables_in_local_clauses": len(support),
            "residuals": 43, "outside_residual_equations": data["residual_zero_vertices"],
            "density_equalities": len(data["density_equalities"]),
            "scalar_margin_bounds": 2 * sum(len(l) + len(r) for l, r in blocks),
            "margin_balances": len(blocks),
            "labeled_subset_cuts": sum(len(b["subset_cuts"]) for b in data["blocks"]),
            "cnf_sha256": digest(actual), "descriptor_sha256": digest(raw_descriptor),
            "mutations": bad, "cut_identity_cases": cut_checks,
            "scope": "Exact existential projection of the fixed six-neighborhood subsystem only; no SAT verdict, global branch coverage, or new Ramsey bound."
        }
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
