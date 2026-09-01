#!/usr/bin/env python3
"""Exact H-sum intersection of the QLP-42 q=41 fourth-order survivors."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREDECESSOR = HERE.parent / "qlp42_q41_fourth_order_rank" / "verify_q41_fourth_order_rank.py"
EXPECTED_PREDECESSOR_SHA256 = "cefc2f614980396aaecc9894733e3e8840658966b5d33e1ae6811a7bcc4b3d69"
EXPECTED_HYPERPLANE_VERIFIER_SHA256 = "604a25cf955a9ff18a509711f50a3ce1de8c2fad1192289bcdfe56aac25a5e14"
EXPECTED_TABLE = HERE / "rank_h_intersection_table.tsv"


def load_predecessor():
    digest = hashlib.sha256(PREDECESSOR.read_bytes()).hexdigest()
    assert digest == EXPECTED_PREDECESSOR_SHA256
    spec = importlib.util.spec_from_file_location("q41_fourth_order", PREDECESSOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def enumerate_weight_zero_mod_four_groups(q):
    groups: dict[tuple[int, int, int], list[int]] = defaultdict(lambda: [0, 0])
    rank_b_counts: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    seen = bytearray(1 << q.N)
    orbit_count = 0
    word_count = 0
    for mask in range(1 << q.N):
        if seen[mask]:
            continue
        orbit = []
        value = mask
        while not orbit or value != mask:
            orbit.append(value)
            value = q.rotate(value, 1)
        for value in orbit:
            seen[value] = 1
        if mask.bit_count() % 4:
            continue
        signature = q.autocorrelation_signature(mask)
        columns = q.d_columns(mask)
        rank = len(q.rref(columns))
        orthogonal = q.orthogonal_mask(columns)
        groups[(rank, signature, orthogonal)][0] += len(orbit)
        groups[(rank, signature, orthogonal)][1] += 1
        rank_b_counts[rank][0] += len(orbit)
        rank_b_counts[rank][1] += 1
        orbit_count += 1
        word_count += len(orbit)
    assert orbit_count == 24_946
    assert word_count == 523_776
    assert len(groups) == 585
    return groups, rank_b_counts


def in_image(value: int, orthogonal_mask: int, dimension: int = 10) -> bool:
    for character in range(1 << dimension):
        if (orthogonal_mask >> character) & 1:
            if (value & character).bit_count() & 1:
                return False
    return True


def h_sum_zero_possible(a_half: int, theta_h: int) -> bool:
    active_by_axis = [0, 0]
    for pair in range(10):
        if not ((theta_h >> pair) & 1):
            active_by_axis[(a_half >> pair) & 1] += 1
    return active_by_axis[0] % 2 == 0 and active_by_axis[1] % 2 == 0


def verify_even_a_direction_parity(q) -> int:
    checks = 0
    for a_half in range(1 << 10):
        theta_h, _ = q.theta_masks(a_half, 0)
        base = q.a_word(a_half, theta_h, "H")
        variants = []
        for pair in range(10):
            variant = base.copy()
            shift = pair + 1
            variant[shift] = q.scale(variant[shift], -1)
            variant[q.N - shift] = q.scale(variant[q.N - shift], -1)
            variants.append(variant)
        columns = q.vector_from_deltas(base, variants)
        for column in columns:
            assert column.bit_count() % 2 == 0
            checks += 1
    return checks


def classify(q, groups, rank_b_counts, systems, affine_data):
    fourth_survivors: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    h_survivors: dict[int, list[int]] = defaultdict(lambda: [0, 0])
    stream_records = []
    grouped_axis_tests = 0
    parity_tests = 0

    for (rank, signature, b_orthogonal), (labeled_b, orbit_b) in sorted(groups.items()):
        fourth_a_mask = 0
        h_a_mask = 0
        for a_half in range(1 << 10):
            h_orthogonal, s_orthogonal = systems[a_half]
            h_data, s_data = affine_data[a_half]
            h_value = q.affine_value(h_data[0], h_data[1:], signature, 0)
            s_bases = s_data[0]
            s_columns = s_data[1:]
            assert isinstance(s_bases, tuple)

            if rank == 10:
                fourth_ok = True
            else:
                fourth_ok = q.in_sum_space(h_value, h_orthogonal, b_orthogonal) and any(
                    q.in_sum_space(
                        q.affine_value(base, s_columns, signature, 0),
                        s_orthogonal,
                        b_orthogonal,
                    )
                    for base in s_bases
                )
            grouped_axis_tests += 1
            if not fourth_ok:
                continue
            fourth_a_mask |= 1 << a_half

            # The preceding multiplicity theorem says U_H(a) is contained in
            # image(D_b) on every fourth-order survivor.  Verify that exact
            # inclusion here from orthogonal complements, then verify the
            # affine residual itself lies in image(D_b).
            assert b_orthogonal & ~h_orthogonal == 0
            assert in_image(h_value, b_orthogonal)

            # Here wt(b)=0 mod 4, so the universal H_B sum-one equation has
            # right side zero.  Every A-pair direction has even syndrome
            # parity, and the residual parity is also forced to zero.
            assert h_value.bit_count() % 2 == 0
            parity_tests += 1

            theta_h, _ = q.theta_masks(a_half, signature)
            if h_sum_zero_possible(a_half, theta_h):
                h_a_mask |= 1 << a_half

        fourth_count = fourth_a_mask.bit_count()
        h_count = h_a_mask.bit_count()
        fourth_survivors[rank][0] += fourth_count * labeled_b
        fourth_survivors[rank][1] += fourth_count * orbit_b
        h_survivors[rank][0] += h_count * labeled_b
        h_survivors[rank][1] += h_count * orbit_b
        stream_records.append(
            (
                rank,
                signature,
                b_orthogonal,
                labeled_b,
                orbit_b,
                fourth_a_mask,
                h_a_mask,
            )
        )

    rows = []
    for rank in sorted(rank_b_counts):
        b_words, b_orbits = rank_b_counts[rank]
        fourth_labeled, fourth_orbits = fourth_survivors[rank]
        h_labeled, h_orbits = h_survivors[rank]
        rows.append(
            {
                "rank": str(rank),
                "b_words_wt_0_mod_4": str(b_words),
                "b_orbits_wt_0_mod_4": str(b_orbits),
                "fourth_order_labeled_pairs": str(fourth_labeled),
                "fourth_order_axis_orbits": str(fourth_orbits),
                "h_exact_labeled_pairs": str(h_labeled),
                "h_exact_axis_orbits": str(h_orbits),
            }
        )

    assert sum(int(row["fourth_order_labeled_pairs"]) for row in rows) == 428_622_432
    assert sum(int(row["fourth_order_axis_orbits"]) for row in rows) == 20_410_592
    assert sum(int(row["h_exact_labeled_pairs"]) for row in rows) == 218_347_920
    assert sum(int(row["h_exact_axis_orbits"]) for row in rows) == 10_397_520
    assert sum(int(row["h_exact_labeled_pairs"]) for row in rows if int(row["rank"]) <= 7) == 0

    digest = hashlib.sha256()
    digest.update(
        b"rank\tsignature\tb_orthogonal\tlabeled_b\torbit_b\tfourth_a_mask\th_a_mask\n"
    )
    for rank, signature, b_orthogonal, labeled_b, orbit_b, fourth_mask, h_mask in stream_records:
        line = (
            f"{rank}\t{signature:03x}\t{b_orthogonal:0256x}\t{labeled_b}\t{orbit_b}\t"
            f"{fourth_mask:0256x}\t{h_mask:0256x}\n"
        )
        digest.update(line.encode("ascii"))
    return rows, digest.hexdigest(), grouped_axis_tests, parity_tests


def read_table() -> list[dict[str, str]]:
    with EXPECTED_TABLE.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    q = load_predecessor()
    a_direction_checks = verify_even_a_direction_parity(q)
    systems, affine_data = q.a_systems()
    groups, rank_b_counts = enumerate_weight_zero_mod_four_groups(q)
    rows, digest, grouped_axis_tests, parity_tests = classify(
        q, groups, rank_b_counts, systems, affine_data
    )
    assert rows == read_table()

    print(f"predecessor_sha256={EXPECTED_PREDECESSOR_SHA256}")
    print(f"hyperplane_verifier_sha256={EXPECTED_HYPERPLANE_VERIFIER_SHA256}")
    print("b_words_wt_0_mod_4=523776")
    print("b_rotation_orbits_wt_0_mod_4=24946")
    print(f"grouped_b_systems={len(groups)}")
    print(f"grouped_axis_tests={grouped_axis_tests}")
    print(f"a_direction_even_parity_checks={a_direction_checks}")
    print(f"survivor_residual_parity_checks={parity_tests}")
    for row in rows:
        print(
            "rank_{rank}={fourth_order_labeled_pairs},{fourth_order_axis_orbits},"
            "{h_exact_labeled_pairs},{h_exact_axis_orbits}".format(**row)
        )
    print("fourth_order_wt_0_mod_4_labeled_pairs=428622432")
    print("fourth_order_wt_0_mod_4_axis_orbits=20410592")
    print("h_exact_labeled_pairs=218347920")
    print("h_exact_axis_orbits=10397520")
    print(f"canonical_group_stream_sha256={digest}")
    print("rank_at_most_7_elimination=verified")
    print("rank_table=verified")
    print("certificate=verified")


if __name__ == "__main__":
    main()
