#!/usr/bin/env python3
"""Independent exact audit of the Albertson r=27, h=19 recolouring step.

The target checkers specialize the two colour profiles first.  This checker
instead proves the finite transition classification for a general profile
with k active classes of weight b, then solves the target's incidence-weight
degree minimization by a definition-level dynamic program.
"""

from collections import Counter
from hashlib import sha256
import json


def canonical(profile):
    """Forget colour labels while retaining the multiset of class weights."""
    return tuple(sorted(profile))


def surviving_moves(c, k, b):
    """List labelled positive-weight moves preserving a (b^k,0^(c-k)) profile."""
    assert 1 <= k <= c and b >= 1
    profile = [b] * k + [0] * (c - k)
    target_profile = canonical(profile)
    survivors = []
    for source in range(k):
        for target in range(c):
            if source == target:
                continue
            for moved_weight in range(1, b + 1):
                changed = profile.copy()
                changed[source] -= moved_weight
                changed[target] += moved_weight
                if canonical(changed) == target_profile:
                    survivors.append((source, target, moved_weight))
    return tuple(survivors)


def general_transition_sweep():
    """Exhaustively check the general profile-transition characterization."""
    parameter_sets = 0
    labelled_moves = 0
    for c in range(2, 13):
        for k in range(1, c + 1):
            for b in range(1, 9):
                parameter_sets += 1
                actual = surviving_moves(c, k, b)
                expected = tuple(
                    (source, target, b)
                    for source in range(k)
                    for target in range(k, c)
                )
                assert actual == expected
                labelled_moves += len(actual)
    assert parameter_sets == 616
    return parameter_sets, labelled_moves


def minimum_degree_sum(vertex_count, total_weight, b, degree_floor):
    """Minimize the summed local degree floor over all labelled weight vectors."""
    states = {0: (0, ())}
    for _ in range(vertex_count):
        next_states = {}
        for subtotal, (cost, witness) in states.items():
            for weight in range(b + 1):
                new_total = subtotal + weight
                if new_total > total_weight:
                    break
                candidate = (cost + degree_floor(weight), witness + (weight,))
                incumbent = next_states.get(new_total)
                if incumbent is None or candidate[0] < incumbent[0]:
                    next_states[new_total] = candidate
        states = next_states
    return states[total_weight]


def histogram(witness):
    return tuple(sorted(Counter(witness).items()))


def main():
    parameter_sets, labelled_moves = general_transition_sweep()

    b = 19
    target_moves_c8 = surviving_moves(c=8, k=8, b=b)
    target_moves_c9 = surviving_moves(c=9, k=8, b=b)
    assert target_moves_c8 == ()
    assert target_moves_c9 == tuple((source, 8, b) for source in range(8))

    # The K19 supplies eight incidences in each of 19 rows, hence total 152.
    vertex_count = 19
    total_incidence = 19 * 8
    twice_edge_count = 2 * 56

    c8_minimum, c8_witness = minimum_degree_sum(
        vertex_count,
        total_incidence,
        b,
        lambda weight: 12 if weight == 0 else 7,
    )
    c9_minimum, c9_witness = minimum_degree_sum(
        vertex_count,
        total_incidence,
        b,
        lambda weight: 12 if weight == 0 else (7 if weight == b else 8),
    )
    assert c8_minimum == 133 > twice_edge_count
    assert c9_minimum == 145 > twice_edge_count

    certificate = {
        "general_profile_parameter_sets": parameter_sets,
        "general_profile_surviving_labelled_moves": labelled_moves,
        "target_profile_moves": {"c8": len(target_moves_c8), "c9": len(target_moves_c9)},
        "total_incidence": total_incidence,
        "twice_edge_count": twice_edge_count,
        "minimum_degree_sums": {"c8": c8_minimum, "c9": c9_minimum},
        "witness_histograms": {
            "c8": histogram(c8_witness),
            "c9": histogram(c9_witness),
        },
    }
    payload = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(payload).hexdigest()

    print("PASS independent weighted-profile recolouring audit")
    print(
        f"general_profile_parameter_sets={parameter_sets}; "
        f"surviving_labelled_moves={labelled_moves}"
    )
    print(
        f"target_profile_moves=(c8:{len(target_moves_c8)},c9:{len(target_moves_c9)}); "
        f"incidence_total={total_incidence}"
    )
    print(
        f"minimum_degree_sums=(c8:{c8_minimum},c9:{c9_minimum}); "
        f"handshake_value={twice_edge_count}"
    )
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
