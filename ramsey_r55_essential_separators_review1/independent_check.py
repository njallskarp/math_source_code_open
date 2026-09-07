#!/usr/bin/env python3
"""Independent audit of the Ramsey(5,5;43) essential-separator theorem.

No target module is imported.  This checker reconstructs the complete
side-profile arithmetic, searches the abstract attachment populations for a
survivor, checks the component-grouping and connectivity corollary, tests the
contact-class lemma on small graphs, and scans every physical five-set in the
two advertised F27 cut branches.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import sys


N = 43
ORDER_BY_ALPHA = {1: 4, 2: 13, 3: 24}
CONTACT_CAPACITY = {10: 24, 11: 13, 12: 4, 13: 0}
A = tuple(range(2, 12)) + (27, 28)
B = tuple(range(12, 22)) + (29, 30)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def compositions(total: int, length: int):
    """Generate weak compositions without using the target implementation."""
    if length == 1:
        yield (total,)
        return
    for cuts in itertools.combinations(range(total + length - 1), length - 1):
        boundaries = (-1,) + cuts + (total + length - 1,)
        yield tuple(boundaries[i + 1] - boundaries[i] - 1 for i in range(length))


def side_domain() -> set[tuple[int, int, int, int, int]]:
    result = set()
    for separator in range(21):
        for left in range(2, (N - separator) // 2 + 1):
            right = N - separator - left
            for alpha_left in (1, 2, 3):
                for alpha_right in (1, 2, 3):
                    if alpha_left + alpha_right > 4:
                        continue
                    if left <= ORDER_BY_ALPHA[alpha_left] and right <= ORDER_BY_ALPHA[alpha_right]:
                        result.add((separator, left, right, alpha_left, alpha_right))
    return result


def classify_profile(profile: tuple[int, int, int, int, int]) -> dict[str, object]:
    separator, left, right, alpha_left, alpha_right = profile
    if 1 in (alpha_left, alpha_right):
        clique_order = left if alpha_left == 1 else right
        require(clique_order in (2, 3, 4), "clique side outside the K5-free range")
        if clique_order in (2, 3):
            common_lower = (
                clique_order * (18 - clique_order + 1)
                - (clique_order - 1) * separator
            )
            common_upper = {2: 13, 3: 4}[clique_order]
            require(common_lower > common_upper, "abstract common-neighbor case survives")
            return {
                "status": "EXCLUDED",
                "rule": "common_neighbors",
                "lower": common_lower,
                "upper": common_upper,
            }
        required_separator = 2 * 18 - 14
        require(separator < required_separator, "abstract K4 contact case survives")
        return {
            "status": "EXCLUDED",
            "rule": "K4_contact_types",
            "required_separator": required_separator,
        }

    require((alpha_left, alpha_right) == (2, 2), "unexpected nonclique alpha profile")
    capacity = CONTACT_CAPACITY[left] + CONTACT_CAPACITY[right]
    if capacity < separator:
        return {"status": "EXCLUDED", "rule": "contact_cover", "capacity": capacity}
    maximum_minimum_degree = (13 * 8 + 8 * separator) // 13
    require(profile == (20, 10, 13, 2, 2), "unexpected contact-class residual")
    require(maximum_minimum_degree == 20, "incorrect order-20 degree boundary")
    return {
        "status": "NECESSARY_RESIDUAL_ONLY",
        "rule": "contact_cover_and_degree",
        "capacity": capacity,
        "maximum_minimum_degree": maximum_minimum_degree,
    }


def audit_attachment_populations(domain: set[tuple[int, int, int, int, int]]) -> int:
    visited = 0
    for separator, left, right, alpha_left, alpha_right in sorted(domain):
        if 1 not in (alpha_left, alpha_right):
            continue
        clique_order = left if alpha_left == 1 else right
        feasible = 0
        for population in compositions(separator, clique_order + 1):
            visited += 1
            if population[0] > {2: 13, 3: 4, 4: 0}[clique_order]:
                continue
            if clique_order == 4 and population[1] > 16:
                continue
            total_blue = sum(j * population[j] for j in range(clique_order + 1))
            maximum_blue = clique_order * (separator - 18 + clique_order - 1)
            if total_blue <= maximum_blue:
                feasible += 1
        require(feasible == 0, "clique attachment population survives")
    require(visited == 49054, "attachment population count differs")
    return visited


def audit_cases(target_directory: Path) -> dict[str, object]:
    path = target_directory / "cases.json"
    document = json.loads(path.read_text())
    require(document.get("n") == N, "case-certificate order")
    require(document.get("maximum_separator") == 20, "case-certificate boundary")
    require(document.get("external_bound") == "R(4,5)<=25", "case-certificate premise")
    domain = side_domain()
    rows = document.get("cases")
    require(isinstance(rows, list), "case-certificate rows")
    row_by_profile = {}
    for row in rows:
        key = tuple(row[name] for name in ("s", "a", "b", "alpha_a", "alpha_b"))
        require(key not in row_by_profile, "duplicate case row")
        row_by_profile[key] = row
    require(set(row_by_profile) == domain, "case domain is incomplete")

    residuals = []
    for profile in sorted(domain):
        expected = classify_profile(profile)
        row = row_by_profile[profile]
        prefix = {"s", "a", "b", "alpha_a", "alpha_b"}
        require({k: row[k] for k in row if k not in prefix} == expected,
                "case classification differs")
        if expected["status"] == "NECESSARY_RESIDUAL_ONLY":
            residuals.append(profile)

    populations = audit_attachment_populations(domain)
    require(len(domain) == 21, "unexpected profile count")
    require(sum(profile[0] <= 19 for profile in domain) == 16, "order-19 domain count")
    require(residuals == [(20, 10, 13, 2, 2)], "wrong residual profile")
    return {
        "profiles": len(domain),
        "profiles_through_19": 16,
        "excluded_profiles": 20,
        "residual_profiles": [list(profile) for profile in residuals],
        "attachment_populations": populations,
        "cases_json_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def integer_partitions(total: int, minimum: int = 1):
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def component_grouping_control() -> dict[str, object]:
    checked = 0
    exceptional = []
    for remaining in range(23, 44):
        exceptions_at_order = []
        for parts in integer_partitions(remaining):
            if len(parts) < 2:
                continue
            checked += 1
            subset_sums = 1
            for part in parts:
                subset_sums |= subset_sums << part
            groupable = any((subset_sums >> size) & 1 for size in range(2, remaining - 1))
            if not groupable:
                require(parts == (1, remaining - 1), "unclassified component partition")
                exceptions_at_order.append(parts)
        require(exceptions_at_order == [(1, remaining - 1)], "singleton exception mismatch")
        exceptional.append([1, remaining - 1])

    # Encode the cut-size argument for every possible good43 minimum degree.
    connectivity_bounds = {}
    for minimum_degree in range(18, 25):
        claimed = min(minimum_degree, 21)
        for cut_size in range(claimed):
            if cut_size <= 19:
                # A nontrivial cut is excluded; a singleton component would give
                # d(v)<=|S|<delta.
                require(cut_size < minimum_degree, "singleton cut not contradicted")
            else:
                # At size 20, a singleton gives delta<=20 and a nontrivial cut invokes
                # the unique residual, which also gives delta<=20.
                require(cut_size == 20 and minimum_degree >= 21,
                        "order-20 boundary applied at wrong degree")
        connectivity_bounds[str(minimum_degree)] = claimed
    return {
        "component_partitions_checked": checked,
        "singleton_exceptions_by_remaining_order": exceptional,
        "connectivity_lower_bound_by_delta": connectivity_bounds,
    }


def graph_rows(n: int, word: int) -> list[int]:
    rows = [0] * n
    for bit, (u, v) in enumerate(itertools.combinations(range(n), 2)):
        if (word >> bit) & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def homogeneous(rows: list[int], vertices: tuple[int, ...], color: int) -> bool:
    return all(((rows[u] >> v) & 1) == color for u, v in itertools.combinations(vertices, 2))


def vertices_from_mask(mask: int) -> tuple[int, ...]:
    return tuple(i for i in range(mask.bit_length()) if (mask >> i) & 1)


def small_contact_growth_control() -> dict[str, int]:
    """Seek a counterexample for every labelled graph/core through five vertices."""
    graphs = cores = clique_extensions = 0
    for n in range(1, 6):
        edge_count = comb(n, 2)
        for word in range(1 << edge_count):
            rows = graph_rows(n, word)
            graphs += 1
            for core_mask in range(1, 1 << n):
                core = vertices_from_mask(core_mask)
                if any(homogeneous(rows, triple, 0)
                       for triple in itertools.combinations(core, 3)):
                    continue
                cores += 1
                contact = []
                for z in range(n):
                    if (core_mask >> z) & 1:
                        continue
                    nonneighbors = tuple(u for u in core if not ((rows[z] >> u) & 1))
                    if homogeneous(rows, nonneighbors, 1):
                        contact.append(z)
                for chosen_mask in range(1 << len(contact)):
                    chosen = tuple(contact[i] for i in range(len(contact))
                                   if (chosen_mask >> i) & 1)
                    if not homogeneous(rows, chosen, 1):
                        continue
                    clique_extensions += 1
                    union = core + chosen
                    require(not any(homogeneous(rows, triple, 0)
                                    for triple in itertools.combinations(union, 3)),
                            "small counterexample to contact-class growth")
    return {
        "all_labeled_graphs_orders_1_to_5": graphs,
        "eligible_labeled_cores": cores,
        "clique_extensions_checked": clique_extensions,
    }


def frame_pins() -> dict[tuple[int, int], int]:
    fixed = {(0, 1): 1}
    for base in (2, 7, 12, 17, 22):
        block = tuple(range(base, base + 5))
        cycle = {tuple(sorted((block[i], block[(i + 1) % 5]))) for i in range(5)}
        for pair in itertools.combinations(block, 2):
            fixed[pair] = int(pair in cycle)
    for root in (0, 1):
        for vertex in range(2, 7):
            fixed[root, vertex] = 1
    return fixed


def audit_branches(target_directory: Path) -> dict[str, object]:
    path = target_directory / "branches.json"
    document = json.loads(path.read_text())
    require(document.get("n") == N, "branch order")
    all_pairs = tuple(itertools.combinations(range(N), 2))
    physical_identifiers = {pair: index for index, pair in enumerate(all_pairs, 1)}
    for u, v in all_pairs:
        closed_form = u * (2 * N - 1 - u) // 2 + v - u
        require(physical_identifiers[u, v] == closed_form, "physical variable numbering")
    pins = frame_pins()
    require(Counter(pins.values()) == Counter({1: 36, 0: 25}), "frame pin colors")
    free_pairs = tuple(pair for pair in all_pairs if pair not in pins)
    identifiers = {pair: index for index, pair in enumerate(free_pairs, 1)}
    require(len(identifiers) == 842, "frame variable count")
    require(document.get("frame_pins") == [[u, v, pins[u, v]] for u, v in sorted(pins)],
            "target frame differs")
    require(tuple(document.get("a", ())) == A and tuple(document.get("b", ())) == B,
            "target branch parts differ")
    separator = tuple(sorted(set(range(N)) - set(A) - set(B)))
    require(tuple(document.get("separator", ())) == separator, "branch separator differs")
    require((len(A), len(B), len(separator)) == (12, 12, 19), "branch profile")

    cross = tuple(sorted(tuple(sorted(pair)) for pair in itertools.product(A, B)))
    require(len(cross) == len(set(cross)) == 144, "cross-pair count")
    require(not set(cross) & set(pins), "cross pair is already pinned")
    target_rows = document.get("branches")
    require(isinstance(target_rows, list) and [r.get("cross_color") for r in target_rows] == [0, 1],
            "branch colors")

    result_rows = []
    physical_events = 0
    truth_checks = 0
    for target_row, cross_color in zip(target_rows, (0, 1)):
        fixed = pins | dict.fromkeys(cross, cross_color)
        counts = Counter()
        lengths = Counter()
        digest = hashlib.sha256()
        body_bytes = 0
        for forbidden_color in (1, 0):
            for five in itertools.combinations(range(N), 5):
                physical_events += 1
                pairs = tuple(itertools.combinations(five, 2))
                if any(pair in fixed and fixed[pair] != forbidden_color for pair in pairs):
                    continue
                sign = -1 if forbidden_color else 1
                literals = tuple(sign * identifiers[pair] for pair in pairs if pair not in fixed)
                payload = (" ".join(map(str, literals)) + (" " if literals else "") + "0\n").encode("ascii")
                digest.update(payload)
                body_bytes += len(payload)
                counts[forbidden_color] += 1
                lengths[len(literals)] += 1

        expected_cut = [(1 if cross_color == 0 else -1) * identifiers[pair] for pair in cross]
        require(target_row.get("fixed_pairs") == len(fixed) == 205, "fixed branch pairs")
        require(target_row.get("free_physical_pairs") == 698, "free branch pairs")
        require(target_row.get("red_clauses") == counts[1], "red branch clauses")
        require(target_row.get("blue_clauses") == counts[0], "blue branch clauses")
        require(target_row.get("ramsey_clauses") == sum(counts.values()), "total branch clauses")
        require(target_row.get("length_histogram") ==
                {str(length): lengths[length] for length in sorted(lengths)},
                "branch length histogram")
        require(target_row.get("literal_body_bytes") == body_bytes, "branch body bytes")
        require(target_row.get("literal_body_sha256") == digest.hexdigest(), "branch body hash")
        require(target_row.get("cut_nogood_in_F27_variables") == expected_cut, "cut-clause transport")
        require(lengths[0] == lengths[1] == 0, "empty or unit initial clause")

        # The constant branch falsifies its cut clause; flipping any cross bit satisfies it.
        for flipped in (None,) + tuple(expected_cut):
            satisfied = any(
                (cross_color ^ int(literal == flipped)) == int(literal > 0)
                for literal in expected_cut
            )
            require(satisfied == (flipped is not None), "cut clause has wrong truth semantics")
            truth_checks += 1

        physical_cut = [
            (1 if cross_color == 0 else -1) * physical_identifiers[pair]
            for pair in cross
        ]
        require(len(physical_cut) == 144 and len({abs(v) for v in physical_cut}) == 144,
                "physical cut clause")

        result_rows.append({
            "cross_color": cross_color,
            "fixed_pairs": len(fixed),
            "free_pairs": len(all_pairs) - len(fixed),
            "red_clauses": counts[1],
            "blue_clauses": counts[0],
            "clauses": sum(counts.values()),
            "length_histogram": {str(length): lengths[length] for length in sorted(lengths)},
            "literal_body_bytes": body_bytes,
            "literal_body_sha256": digest.hexdigest(),
            "cut_literals": len(expected_cut),
        })

    require(physical_events == 4 * comb(N, 5), "physical-event coverage")
    return {
        "physical_monochromatic_events": physical_events,
        "frame_fixed_pairs": len(pins),
        "frame_free_variables": len(identifiers),
        "physical_variable_numbers_checked": len(physical_identifiers),
        "cut_clause_truth_checks": truth_checks,
        "branches": result_rows,
        "branches_json_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main(target_directory: Path) -> dict[str, object]:
    target_directory = target_directory.resolve()
    require(target_directory.is_dir(), "missing target directory")

    # Elementary Ramsey inputs used by the displayed proof.
    require(6 + 3 == 9, "R(3,4) recurrence arithmetic")
    require(9 + 5 == 14, "R(3,5) recurrence arithmetic")
    require(43 - 1 - 24 == 18, "good43 minimum-degree arithmetic")
    require(12 - (9 - 1) == 4, "order-13 complement minimum degree")
    require(12 - 4 == 8, "order-13 red degree")

    return {
        "status": "INDEPENDENTLY_VERIFIED_ESSENTIAL_SEPARATOR_THEOREM",
        "cases": audit_cases(target_directory),
        "component_grouping": component_grouping_control(),
        "small_contact_growth": small_contact_growth_control(),
        "branches": audit_branches(target_directory),
        "imported_R45_25_reproduced": False,
        "solver_invoked": False,
        "good43_graph_constructed": False,
        "ramsey_bound_improved": False,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: independent_check.py TARGET_SEPARATOR_DIRECTORY")
    print(json.dumps(main(Path(sys.argv[1])), indent=2, sort_keys=True))
