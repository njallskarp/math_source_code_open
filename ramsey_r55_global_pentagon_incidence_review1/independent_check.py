#!/usr/bin/env python3
"""Independent audit of the h3615 global pentagon-incidence theorem.

The finite searches use one integer bit for each physical edge.  They do not
import the target producer/checker, use its truth-vector representation, or
rely on a solver or graph catalogue.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys


TARGET_CERTIFICATE_SHA256 = "684c0d2ad458ac759bfc496cb03b12ad68b33c65a5fb0e497b03a8ce7ffd6de8"
DEPENDENCY_CERTIFICATE_SHA256 = "27afad4676f03c7e9409a1cb72bfe76460db887480ca6f23eb6cfb3f3124a75f"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def pair_data(order: int) -> tuple[list[tuple[int, int]], dict[tuple[int, int], int]]:
    pairs = list(itertools.combinations(range(order), 2))
    return pairs, {pair: index for index, pair in enumerate(pairs)}


def edge_bit(index: dict[tuple[int, int], int], u: int, v: int) -> int:
    return 1 << index[tuple(sorted((u, v)))]


def complete_mask(vertices: tuple[int, ...], index: dict[tuple[int, int], int]) -> int:
    return sum(edge_bit(index, u, v) for u, v in itertools.combinations(vertices, 2))


def cycle_masks(vertices: tuple[int, ...], index: dict[tuple[int, int], int]) -> frozenset[int]:
    """The twelve labelled undirected C5 edge sets on a fixed five-set."""
    first = vertices[0]
    masks = set()
    for tail in itertools.permutations(vertices[1:]):
        cycle = (first,) + tail
        masks.add(sum(edge_bit(index, cycle[i], cycle[(i + 1) % 5]) for i in range(5)))
    require(len(masks) == 12, "a five-set did not have twelve cycle edge sets")
    return frozenset(masks)


def count_vectors(parts: int, total: int) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []

    def visit(prefix: tuple[int, ...], remaining: int) -> None:
        if len(prefix) == parts - 1:
            result.append(prefix + (remaining,))
            return
        for value in range(remaining + 1):
            visit(prefix + (value,), remaining - value)

    visit((), total)
    return result


def normalized_contact_words() -> list[tuple[int, ...]]:
    words = []
    for counts in count_vectors(6, 5):
        words.append(tuple(label for label, count in enumerate(counts) for _ in range(count)))
    return sorted(words)


def normalized_unique_pentagon_search(certificate_path: Path) -> dict:
    """Exhaust all 252*1024 normalized one-pentagon candidates directly."""
    pairs, index = pair_data(10)
    all_triples = list(itertools.combinations(range(10), 3))
    all_fives = list(itertools.combinations(range(10), 5))
    triangle_masks = [complete_mask(q, index) for q in all_triples]
    five_complete = {q: complete_mask(q, index) for q in all_fives}
    five_cycles = {q: cycle_masks(q, index) for q in all_fives}
    root = tuple(range(5))
    root_edges = sum(edge_bit(index, i, (i + 1) % 5) for i in range(5))
    outside_pairs = list(itertools.combinations(range(5, 10), 2))
    outside_masks = [
        sum(edge_bit(index, *pair) for bit, pair in enumerate(outside_pairs) if code >> bit & 1)
        for code in range(1 << 10)
    ]

    words = normalized_contact_words()
    require(len(words) == math.comb(10, 5) == 252, "normalized word count differs")
    admissible_keys: set[tuple[int, int]] = set()
    second_count_histogram: Counter[int] = Counter()
    witness_stream = hashlib.sha256()
    per_word = []
    for word_index, word in enumerate(words):
        base = root_edges
        for outside, label in enumerate(word, start=5):
            if label:
                base |= edge_bit(index, outside, label - 1)
        word_count = 0
        for outside_code, outside_edges in enumerate(outside_masks):
            graph = base | outside_edges
            if any(graph & mask == mask for mask in triangle_masks):
                continue
            if any(graph & mask == 0 for mask in five_complete.values()):
                continue
            second = [
                q for q in all_fives
                if q != root and graph & five_complete[q] in five_cycles[q]
            ]
            require(second, f"unique-pentagon counterexample at {word_index},{outside_code}")
            admissible_keys.add((word_index, outside_code))
            second_count_histogram[len(second)] += 1
            word_count += 1
            witness_stream.update(f"{word_index},{outside_code}:{second[0]}\n".encode())
        per_word.append(word_count)

    raw = certificate_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == TARGET_CERTIFICATE_SHA256,
            "target certificate hash differs")
    certificate = json.loads(raw)
    require(certificate.get("schema") == "r55-two-pentagons-v1", "target schema differs")
    certificate_keys: set[tuple[int, int]] = set()
    for record in certificate.get("records", []):
        require(type(record) is list and len(record) == 3 and
                all(type(value) is int for value in record), "malformed target record")
        word_index, outside_code, witness = record
        key = (word_index, outside_code)
        require(key not in certificate_keys, "duplicate target record")
        require(0 <= word_index < 252 and 0 <= outside_code < 1024,
                "target record key out of range")
        vertices = tuple(v for v in range(10) if witness >> v & 1)
        require(len(vertices) == 5 and vertices != root, "target witness labels differ")
        word = words[word_index]
        graph = root_edges | outside_masks[outside_code]
        for outside, label in enumerate(word, start=5):
            if label:
                graph |= edge_bit(index, outside, label - 1)
        require(graph & five_complete[vertices] in five_cycles[vertices],
                "target witness is not a physical induced pentagon")
        certificate_keys.add(key)
    require(certificate_keys == admissible_keys, "target coverage keys differ entry-for-entry")

    # Relabeling the outside vertices transports all ten free coordinates.
    normalization_count = 0
    outside_local_pairs = list(itertools.combinations(range(5), 2))
    for labeled_word in itertools.product(range(6), repeat=5):
        order = sorted(range(5), key=lambda vertex: (labeled_word[vertex], vertex))
        require(tuple(labeled_word[vertex] for vertex in order) in words,
                "labeled word lacks a normalized representative")
        moved = [
            outside_local_pairs.index(tuple(sorted((order[u], order[v]))))
            for u, v in outside_local_pairs
        ]
        require(sorted(moved) == list(range(10)), "outside edge transport is not bijective")
        normalization_count += 1

    # Directly classify all one-vertex stars on the root C5.
    pairs6, index6 = pair_data(6)
    del pairs6
    core6 = sum(edge_bit(index6, i, (i + 1) % 5) for i in range(5))
    triangles6 = [complete_mask(q, index6) for q in itertools.combinations(range(6), 3)]
    fives6 = list(itertools.combinations(range(6), 5))
    complete6 = {q: complete_mask(q, index6) for q in fives6}
    cycles6 = {q: cycle_masks(q, index6) for q in fives6}
    star_classes: Counter[str] = Counter()
    for star in range(32):
        graph = core6 | sum(edge_bit(index6, i, 5) for i in range(5) if star >> i & 1)
        if any(graph & mask == mask for mask in triangles6):
            star_classes["triangle"] += 1
        elif star.bit_count() <= 1:
            star_classes["zero_or_one_contact"] += 1
        else:
            require(any(q != tuple(range(5)) and graph & complete6[q] in cycles6[q]
                        for q in fives6), "two-contact star lacks its second pentagon")
            star_classes["second_pentagon"] += 1

    return {
        "normalized_words": len(words),
        "outside_graphs_per_word": len(outside_masks),
        "normalized_graphs": len(words) * len(outside_masks),
        "admissible_graphs": len(admissible_keys),
        "per_word_count_sha256": hashlib.sha256(
            (",".join(map(str, per_word)) + "\n").encode()
        ).hexdigest(),
        "second_pentagon_count_histogram": dict(sorted(second_count_histogram.items())),
        "independent_witness_stream_sha256": witness_stream.hexdigest(),
        "certificate_keys_equal": True,
        "labeled_word_normalizations": normalization_count,
        "one_vertex_star_classes": dict(sorted(star_classes.items())),
    }


def zero_pentagon_dependency_check(certificate_path: Path) -> dict:
    """Independently exhaust the degree-two/C7 contact boundary of h3593."""
    pairs, index = pair_data(10)
    del pairs
    triangle_masks = [complete_mask(q, index) for q in itertools.combinations(range(10), 3)]
    five_sets = list(itertools.combinations(range(10), 5))
    five_complete = {q: complete_mask(q, index) for q in five_sets}
    five_cycles = {q: cycle_masks(q, index) for q in five_sets}
    base = sum(edge_bit(index, i, (i + 1) % 7) for i in range(7))
    base |= edge_bit(index, 7, 8) | edge_bit(index, 7, 9)
    found: set[tuple[int, int]] = set()
    classes = Counter()
    for first in range(128):
        for second in range(128):
            graph = base
            graph |= sum(edge_bit(index, vertex, 8) for vertex in range(7) if first >> vertex & 1)
            graph |= sum(edge_bit(index, vertex, 9) for vertex in range(7) if second >> vertex & 1)
            if any(graph & mask == mask for mask in triangle_masks):
                classes["triangle"] += 1
                continue
            if any(graph & five_complete[q] in five_cycles[q] for q in five_sets):
                classes["pentagon"] += 1
                continue
            require(any(graph & mask == 0 for mask in five_complete.values()),
                    f"h3593 degree-two contact counterexample {first},{second}")
            classes["independent5"] += 1
            found.add((first, second))

    raw = certificate_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == DEPENDENCY_CERTIFICATE_SHA256,
            "h3593 dependency certificate hash differs")
    certificate = json.loads(raw)
    supplied: set[tuple[int, int]] = set()
    for row in certificate["contact_pairs"]:
        key = (row["s"], row["t"])
        require(key not in supplied, "duplicate h3593 contact pair")
        independent = tuple(row["independent"])
        graph = base
        graph |= sum(edge_bit(index, vertex, 8) for vertex in range(7) if key[0] >> vertex & 1)
        graph |= sum(edge_bit(index, vertex, 9) for vertex in range(7) if key[1] >> vertex & 1)
        witness = independent + (8, 9)
        require(len(set(witness)) == 5 and graph & complete_mask(witness, index) == 0,
                "invalid h3593 independent-five witness")
        supplied.add(key)
    require(supplied == found, "h3593 contact-pair coverage differs")
    return {"physical_contact_pairs": 128 * 128,
            "outcomes": dict(sorted(classes.items())),
            "certificate_pairs_equal": True}


def global_identity_controls() -> dict:
    """Check counting identities and the J-anchor convention independently."""
    pairs, index = pair_data(6)
    identity_cases = 0
    for graph in range(1 << len(pairs)):
        degrees = [sum(bool(graph & edge_bit(index, vertex, other))
                       for other in range(6) if other != vertex)
                   for vertex in range(6)]
        monochromatic = 0
        for triple in itertools.combinations(range(6), 3):
            colours = [bool(graph & edge_bit(index, u, v))
                       for u, v in itertools.combinations(triple, 2)]
            monochromatic += int(all(colours) or not any(colours))
        require(2 * monochromatic == 2 * math.comb(6, 3) -
                sum(degree * (5 - degree) for degree in degrees),
                "Goodman identity failed on a six-vertex graph")
        q_sum = 0
        for u, v in pairs:
            colour = bool(graph & edge_bit(index, u, v))
            q_sum += sum(bool(graph & edge_bit(index, u, w)) == colour and
                         bool(graph & edge_bit(index, v, w)) == colour
                         for w in range(6) if w not in (u, v))
        require(q_sum == 3 * monochromatic, "pair/triangle incidence identity failed")
        identity_cases += 1

    pairs7, index7 = pair_data(7)
    full7 = (1 << len(pairs7)) - 1
    generated: dict[int, list[tuple[tuple[int, int], int]]] = defaultdict(list)
    for anchor in pairs7:
        core = tuple(vertex for vertex in range(7) if vertex not in anchor)
        cross = edge_bit(index7, *anchor) | sum(
            edge_bit(index7, endpoint, vertex) for endpoint in anchor for vertex in core
        )
        for cycle in cycle_masks(core, index7):
            joined = cross | cycle
            generated[joined].append((anchor, 1))
            generated[full7 ^ joined].append((anchor, 0))
    require(len(generated) == 21 * 12 * 2 and all(len(origins) == 1 for origins in generated.values()),
            "J/complement does not have a unique anchor")
    all_fives7 = list(itertools.combinations(range(7), 5))
    complete7 = {q: complete_mask(q, index7) for q in all_fives7}
    cycles7 = {q: cycle_masks(q, index7) for q in all_fives7}
    require(all(sum(graph & complete7[q] in cycles7[q] for q in all_fives7) == 1
                for graph in generated), "J/complement does not have a unique pentagon core")

    lower = [0] * 10 + [2]
    for order in (11, 12, 13):
        numerator = order * lower[-1]
        denominator = order - 5
        lower.append((numerator + denominator - 1) // denominator)
    require(lower[-4:] == [2, 4, 7, 12], "hereditary lower bounds differ")
    slack = [lower[q] - 2 * (q - 9) for q in range(14)]
    require(slack == [18, 16, 14, 12, 10, 8, 6, 4, 2, 0, 0, 0, 1, 4],
            "linear support correction differs")
    require(43 * 42 * 2 // 4 == 903 and 903 + 3 == 906 and
            (906 + 52 - 1) // 52 == 18, "global arithmetic differs")
    return {"six_vertex_coloured_graphs": identity_cases,
            "labelled_J_or_complement_graphs": len(generated),
            "unique_anchor_and_core": True,
            "hereditary_bounds_q10_to_q13": lower[-4:],
            "support_corrections_q0_to_q13": slack,
            "order43_base": 903,
            "order43_parity_improved_bound": 906,
            "pentagon_bound": 18}


def adjacency_from_edge_list(path: Path) -> list[int]:
    lines = path.read_text().splitlines()
    require(lines, "empty edge list")
    header = lines[0].split()
    require(len(header) == 2, "bad edge-list header")
    order, edge_count = map(int, header)
    require(len(lines) == edge_count + 1, "edge-list length differs")
    rows = [0] * order
    seen = set()
    for line in lines[1:]:
        values = line.split()
        require(len(values) == 2, "bad edge-list row")
        u, v = map(int, values)
        require(0 <= u < v < order and (u, v) not in seen, "bad edge labels")
        seen.add((u, v))
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return rows


def complement_rows(rows: list[int]) -> list[int]:
    full = (1 << len(rows)) - 1
    return [full ^ (1 << vertex) ^ row for vertex, row in enumerate(rows)]


def has_clique(rows: list[int], candidates: int, size: int) -> bool:
    if size == 0:
        return True
    while candidates.bit_count() >= size:
        bit = candidates & -candidates
        candidates ^= bit
        if has_clique(rows, candidates & rows[bit.bit_length() - 1], size - 1):
            return True
    return False


def pentagon_masks(rows: list[int], candidates: int) -> list[int]:
    vertices = [vertex for vertex in range(len(rows)) if candidates >> vertex & 1]
    result = []
    for five in itertools.combinations(vertices, 5):
        mask = sum(1 << vertex for vertex in five)
        if all((rows[vertex] & mask).bit_count() == 2 for vertex in five):
            result.append(mask)
    return result


def audit_control_graph(path: Path) -> dict:
    red = adjacency_from_edge_list(path)
    order = len(red)
    full = (1 << order) - 1
    blue = complement_rows(red)
    require(not has_clique(red, full, 5) and not has_clique(blue, full, 5),
            "control graph is not good")
    pentagons = pentagon_masks(red, full)
    pair_first = 0
    q_histogram = Counter()
    for u, v in itertools.combinations(range(order), 2):
        colour = red if red[u] >> v & 1 else blue
        common = colour[u] & colour[v]
        q_histogram[common.bit_count()] += 1
        pair_first += len(pentagon_masks(red, common))
    core_first = 0
    for pentagon in pentagons:
        vertices = [v for v in range(order) if pentagon >> v & 1]
        for colour in (red, blue):
            universal = full ^ pentagon
            for vertex in vertices:
                universal &= colour[vertex]
            core_first += sum((colour[vertex] & universal).bit_count()
                              for vertex in range(order) if universal >> vertex & 1) // 2
    require(pair_first == core_first, "two W counts differ")
    degrees = [row.bit_count() for row in red]
    monochromatic_triangles = sum(
        1 for triple in itertools.combinations(range(order), 3)
        if len({bool(red[u] >> v & 1) for u, v in itertools.combinations(triple, 2)}) == 1
    )
    degree_delta = sum((2 * degree - (order - 1)) ** 2 for degree in degrees)
    require(sum(q * count for q, count in q_histogram.items()) == 3 * monochromatic_triangles,
            "control pair/triangle incidence differs")
    require(24 * monochromatic_triangles == order * (order - 1) * (order - 5) + 3 * degree_delta,
            "control Goodman identity differs")
    return {"order": order,
            "red_edges": sum(degrees) // 2,
            "pentagons": len(pentagons),
            "joined_edge_pentagons": pair_first,
            "q_histogram": dict(sorted(q_histogram.items())),
            "monochromatic_triangles": monochromatic_triangles,
            "degree_delta": degree_delta}


def verify(target_directory: Path) -> dict:
    dependency_directory = target_directory.parent / "ramsey_r55_induced_pentagon_forcing"
    finite = normalized_unique_pentagon_search(target_directory / "certificate.json")
    dependency = zero_pentagon_dependency_check(dependency_directory / "certificate.json")
    identities = global_identity_controls()
    control = audit_control_graph(target_directory / "control40.edges")
    require(finite["admissible_graphs"] == 1794, "admissible census differs")
    require(dependency["outcomes"] == {"independent5": 141, "pentagon": 700, "triangle": 15543},
            "h3593 contact outcomes differ")
    require(control["pentagons"] == 12477 and control["joined_edge_pentagons"] == 7670,
            "control graph global counts differ")
    return {"status": "INDEPENDENTLY_VERIFIED_GLOBAL_PENTAGON_INCIDENCE",
            "target_certificate_sha256": TARGET_CERTIFICATE_SHA256,
            "dependency_certificate_sha256": DEPENDENCY_CERTIFICATE_SHA256,
            "finite_unique_pentagon_case": finite,
            "zero_pentagon_dependency_boundary": dependency,
            "global_identity_controls": identities,
            "published_control40": control,
            "verified_bounds": {"W_minimum": 906, "P_minimum": 18}}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: independent_check.py /path/to/ramsey_r55_pentagon_incidence")
    print(json.dumps(verify(Path(sys.argv[1])), indent=2, sort_keys=True))
