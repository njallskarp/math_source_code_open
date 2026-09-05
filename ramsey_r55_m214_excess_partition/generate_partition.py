#!/usr/bin/env python3
"""Add an exact ten-cell excess partition to the certified ordered M=214 OPB."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path


N = 43
E = tuple(range(13))
ANCHOR = 13
CELLS = (
    tuple(range(0, 6)),
    tuple(range(6, 13)),
    tuple(range(14, 29)),
    tuple(range(29, 43)),
)
CELL_WEIGHTS = (4352, 4096, 16, 1)
EDGE_COUNT = N * (N - 1) // 2
TRIANGLE_COUNT = N * (N - 1) * (N - 2) // 6
BASE_VARIABLES = EDGE_COUNT + TRIANGLE_COUNT
INPUT_ROWS = 1_974_963
INPUT_EQUALITIES = 128
INPUT_INTERNAL = INPUT_ROWS + INPUT_EQUALITIES
INPUT_SHA256 = "d621bf525bd6e3525ef5f9ccc741dc01c66a07f39b3db4c5e63741190d75eebc"

# Extension variables.  u_v=[a_v>=7], w_v=[a_v>=8], q=[e(E)>=40], and
# y_0,...,y_9 are the ten deterministic pattern selectors.
U_IDS = tuple(BASE_VARIABLES + 1 + v for v in range(N))
W_IDS = tuple(BASE_VARIABLES + 1 + N + v for v in range(N))
Q_ID = BASE_VARIABLES + 1 + 2 * N
Y_IDS = tuple(Q_ID + 1 + p for p in range(10))
OUTPUT_VARIABLES = Y_IDS[-1]

INPUT_HEADER = (
    f"* #variable= {BASE_VARIABLES} #constraint= {INPUT_ROWS} "
    f"#equal= {INPUT_EQUALITIES} intsize= 64\n"
).encode("ascii")

# Internal input constraint identifiers.  The complete base has 1,925,196
# five-set inequalities and 49,364 triangle-gate inequalities before the
# degree equalities.  Each equality occupies two internal identifiers.
DEGREE_FIRST_ID = 1_974_561
DEGREE_LOWER_IDS = tuple(DEGREE_FIRST_ID + 2 * v for v in range(N))
A_MIN_FIRST_ID = 1_974_733
A_MIN_IDS = tuple(A_MIN_FIRST_ID + v for v in range(N))


def edge_id(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    if not 0 <= i < j < N:
        raise ValueError((i, j))
    return i * (2 * N - i - 1) // 2 + (j - i - 1) + 1


def a_coefficients(vertex: int, sign: int = 1) -> dict[int, int]:
    return {
        edge_id(vertex, other): sign
        for other in E
        if other != vertex
    }


def key_coefficients(vertex: int, sign: int = 1) -> dict[int, int]:
    result: dict[int, int] = {}
    for cell, weight in zip(CELLS, CELL_WEIGHTS, strict=True):
        for other in cell:
            if other == vertex:
                continue
            variable = edge_id(vertex, other)
            result[variable] = result.get(variable, 0) + sign * weight
    return result


def sum_coefficients(parts: list[dict[int, int]]) -> dict[int, int]:
    result: dict[int, int] = {}
    for part in parts:
        for variable, coefficient in part.items():
            result[variable] = result.get(variable, 0) + coefficient
    return {variable: coefficient for variable, coefficient in result.items() if coefficient}


def signed_row(coefficients: dict[int, int], rhs: int) -> str:
    terms = " ".join(
        f"{coefficient:+d} x{variable}"
        for variable, coefficient in sorted(coefficients.items())
        if coefficient
    )
    if not terms:
        raise ValueError("empty row")
    return f"{terms} >= {rhs} ;"


def literal_row(literals: list[tuple[int, bool]], rhs: int = 1) -> str:
    # bool=True denotes x, bool=False denotes ~x.
    terms = " ".join(
        f"+1 {'x' if positive else '~x'}{variable}"
        for variable, positive in literals
    )
    return f"{terms} >= {rhs} ;"


def a_row(vertex: int, extra: dict[int, int], rhs: int, sign: int = 1) -> str:
    coefficients = a_coefficients(vertex, sign)
    for variable, coefficient in extra.items():
        coefficients[variable] = coefficients.get(variable, 0) + coefficient
    return signed_row(coefficients, rhs)


def e_edges() -> tuple[int, ...]:
    return tuple(edge_id(i, j) for i, j in itertools.combinations(E, 2))


def pol_sum(ids: list[int]) -> str:
    if not ids:
        raise ValueError("empty pol sum")
    expression = str(ids[0])
    for identifier in ids[1:]:
        expression += f" {identifier} +"
    return f"pol {expression};"


class Builder:
    def __init__(self) -> None:
        self.rows: list[str] = []
        self.proof: list[str] = [
            "pseudo-Boolean proof version 3.0",
            f"f {INPUT_INTERNAL};",
        ]
        self.next_id = INPUT_INTERNAL + 1
        self.named_ids: dict[str, int] = {}

    def add(self, row: str, proof_line: str, name: str | None = None) -> int:
        if not row.endswith(" ;"):
            raise ValueError(row)
        self.rows.append(row)
        self.proof.append(proof_line)
        self.proof.append("core id -1;")
        identifier = self.next_id
        self.next_id += 1
        if name is not None:
            if name in self.named_ids:
                raise ValueError(name)
            self.named_ids[name] = identifier
        return identifier

    def rup(self, row: str, name: str | None = None) -> int:
        return self.add(row, f"rup {row.removesuffix(' ;')};", name)

    def red(self, row: str, witness: str, name: str | None = None) -> int:
        return self.add(row, f"red {row.removesuffix(' ;')} : {witness};", name)

    def pol(self, row: str, ids: list[int], name: str | None = None) -> int:
        return self.add(row, pol_sum(ids), name)

    def pol_expression(self, row: str, expression: str, name: str | None = None) -> int:
        return self.add(row, f"pol {expression};", name)


def adjacent_pairs() -> tuple[tuple[int, int], ...]:
    return tuple((cell[i], cell[i + 1]) for cell in CELLS for i in range(len(cell) - 1))


def order_pairs() -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for cell in CELLS
        for left_index, left in enumerate(cell)
        for right in cell[left_index + 1 :]
    )


ORDER_INPUT_IDS = {
    pair: 1_974_860 + index for index, pair in enumerate(order_pairs())
}


def a_order_pol_expression(left: int, right: int) -> tuple[str, int, int]:
    """Derive a_left<=a_right by weakening residue and dividing by 4096."""
    full = key_coefficients(right)
    for variable, coefficient in key_coefficients(left, -1).items():
        full[variable] = full.get(variable, 0) + coefficient
    target = a_coefficients(right, 4096)
    for variable, coefficient in a_coefficients(left, -4096).items():
        target[variable] = target.get(variable, 0) + coefficient
    expression = str(ORDER_INPUT_IDS[(left, right)])
    weakened = 0
    surplus_sum = 0
    for variable in sorted(set(full) | set(target)):
        full_coefficient = full.get(variable, 0)
        target_coefficient = target.get(variable, 0)
        if target_coefficient == 0:
            if full_coefficient:
                expression += f" x{variable} w"
                weakened += 1
            continue
        if full_coefficient * target_coefficient <= 0:
            raise AssertionError((left, right, variable, full_coefficient, target_coefficient))
        surplus = abs(full_coefficient) - abs(target_coefficient)
        if surplus < 0:
            raise AssertionError((left, right, variable, surplus))
        if surplus:
            # Add the complementary literal axiom to lower the normalized
            # target-literal coefficient from 4096+surplus to 4096.
            complement = f"~x{variable}" if full_coefficient > 0 else f"x{variable}"
            expression += f" {complement} {surplus} * +"
            surplus_sum += surplus
    expression += " 4096 d"
    return expression, weakened, surplus_sum


def selector_conditions() -> tuple[tuple[str, tuple[tuple[int, bool], ...]], ...]:
    # q=1 means the two excess units occur in E (e(E)=40); q=0 means
    # they occur in C (e(E)=39).  Within each ordered pair of cells the five
    # possibilities are: one 8 in left/right, two 7s in left/right, or one
    # 7 in each.  A second-last u bit distinguishes two 7s from one 8.
    result: list[tuple[str, tuple[tuple[int, bool], ...]]] = []
    for prefix, q_positive, left, right in (
        ("E", True, CELLS[0], CELLS[1]),
        ("C", False, CELLS[2], CELLS[3]),
    ):
        q_literal = (Q_ID, q_positive)
        cases = (
            (f"{prefix}_left_8", (q_literal, (W_IDS[left[-1]], True))),
            (f"{prefix}_right_8", (q_literal, (W_IDS[right[-1]], True))),
            (f"{prefix}_left_7_7", (q_literal, (U_IDS[left[-2]], True))),
            (
                f"{prefix}_split_7_7",
                (q_literal, (U_IDS[left[-1]], True), (U_IDS[right[-1]], True)),
            ),
            (f"{prefix}_right_7_7", (q_literal, (U_IDS[right[-2]], True))),
        )
        result.extend(cases)
    return tuple(result)


def build() -> tuple[list[str], list[str], dict[str, object]]:
    builder = Builder()
    sum_a = sum_coefficients([a_coefficients(v) for v in range(N)])

    # The thirteen degree-20 equalities sum exactly to sum_v a_v=260.
    lower_degree_ids = [DEGREE_LOWER_IDS[v] for v in E]
    upper_degree_ids = [identifier + 1 for identifier in lower_degree_ids]
    total_a_lower = builder.pol(signed_row(sum_a, 260), lower_degree_ids, "total_a_lower")
    total_a_upper = builder.pol(
        signed_row({x: -c for x, c in sum_a.items()}, -260),
        upper_degree_ids,
        "total_a_upper",
    )

    # Since every a_v>=6 and their sum is 260, every a_v<=8.
    for vertex in range(N):
        row = a_row(vertex, {}, -8, sign=-1)
        ids = [total_a_upper] + [A_MIN_IDS[w] for w in range(N) if w != vertex]
        builder.pol(row, ids, f"a_upper_{vertex}")

    # Primary-a dominance of K turns each adjacent K-comparison into a_i<=a_j.
    # The explicit CP derivation adds upper-bound literal axioms for every
    # positive lower-signature residue, then divides by 4096.
    a_order_weakened_counts: list[int] = []
    a_order_surplus_sums: list[int] = []
    a_order_ids: dict[tuple[int, int], int] = {}
    for left, right in adjacent_pairs():
        coefficients = a_coefficients(right)
        for variable, coefficient in a_coefficients(left, -1).items():
            coefficients[variable] = coefficients.get(variable, 0) + coefficient
        expression, weakened, surplus_sum = a_order_pol_expression(left, right)
        a_order_weakened_counts.append(weakened)
        a_order_surplus_sums.append(surplus_sum)
        a_order_ids[(left, right)] = builder.pol_expression(
            signed_row(coefficients, 0), expression, f"a_order_{left}_{right}"
        )

    # Exact threshold extensions u_v=[a_v>=7], w_v=[a_v>=8].
    u_forward_ids: list[int] = []
    u_reverse_ids: list[int] = []
    w_forward_ids: list[int] = []
    w_reverse_ids: list[int] = []
    for vertex in range(N):
        maximum = 12 if vertex in E else 13
        u = U_IDS[vertex]
        w = W_IDS[vertex]
        u_forward_ids.append(builder.red(
            a_row(vertex, {u: -7}, 0),
            f"x{u} -> 0",
            f"u_forward_{vertex}",
        ))
        u_reverse_ids.append(builder.red(
            a_row(vertex, {u: maximum - 6}, -6, sign=-1),
            f"x{u} -> 1",
            f"u_reverse_{vertex}",
        ))
        w_forward_ids.append(builder.red(
            a_row(vertex, {w: -8}, 0),
            f"x{w} -> 0",
            f"w_forward_{vertex}",
        ))
        w_reverse_ids.append(builder.red(
            a_row(vertex, {w: maximum - 7}, -7, sign=-1),
            f"x{w} -> 1",
            f"w_reverse_{vertex}",
        ))

    # On 6<=a_v<=8, these threshold definitions give a_v=6+u_v+w_v.
    # Three small redundance bridges expose the convex threshold hull before the
    # final equality: w<=u, a>=6+u, and a<=7+w.
    local_lower_ids: list[int] = []
    local_upper_ids: list[int] = []
    for vertex in range(N):
        builder.red(
            a_row(vertex, {U_IDS[vertex]: -1}, 6),
            f"x{U_IDS[vertex]} -> 0",
            f"u_hull_lower_{vertex}",
        )
        builder.red(
            a_row(vertex, {W_IDS[vertex]: 1}, -7, sign=-1),
            f"x{W_IDS[vertex]} -> 1",
            f"w_hull_upper_{vertex}",
        )
        builder.red(
            literal_row([(W_IDS[vertex], False), (U_IDS[vertex], True)]),
            f"x{U_IDS[vertex]} -> 1",
            f"w_implies_u_{vertex}",
        )
        local_lower_ids.append(
            builder.red(
                a_row(vertex, {U_IDS[vertex]: -1, W_IDS[vertex]: -1}, 6),
                f"x{W_IDS[vertex]} -> 0",
                f"excess_lower_{vertex}",
            )
        )
        local_upper_ids.append(
            builder.red(
                a_row(vertex, {U_IDS[vertex]: 1, W_IDS[vertex]: 1}, -6, sign=-1),
                f"x{U_IDS[vertex]} -> 1",
                f"excess_upper_{vertex}",
            )
        )

    # Threshold bits inherit adjacent cell order.  Add the left forward
    # threshold, the right reverse threshold, and a_left<=a_right, then
    # saturate the normalized row.  These rows come after the local extension
    # witnesses so those witnesses never have to preserve a later monotonicity
    # constraint.
    for left, right in adjacent_pairs():
        builder.pol_expression(
            literal_row([(U_IDS[left], False), (U_IDS[right], True)]),
            f"{u_forward_ids[left]} {u_reverse_ids[right]} + "
            f"{a_order_ids[(left, right)]} + s",
            f"u_order_{left}_{right}",
        )
        builder.pol_expression(
            literal_row([(W_IDS[left], False), (W_IDS[right], True)]),
            f"{w_forward_ids[left]} {w_reverse_ids[right]} + "
            f"{a_order_ids[(left, right)]} + s",
            f"w_order_{left}_{right}",
        )

    all_thresholds = {variable: 1 for variable in U_IDS + W_IDS}
    global_lower = builder.pol(
        signed_row(all_thresholds, 2),
        [total_a_lower] + local_upper_ids,
        "global_excess_lower",
    )
    global_upper = builder.pol(
        signed_row({x: -1 for x in U_IDS + W_IDS}, -2),
        [total_a_upper] + local_lower_ids,
        "global_excess_upper",
    )

    # Expose the incidence identity
    #   2e(E)-sum_E(u+w)=78
    # by summing the thirteen local equalities.
    e_variables = e_edges()
    e_thresholds = {variable: 1 for v in E for variable in (U_IDS[v], W_IDS[v])}
    twice_e = {variable: 2 for variable in e_variables}
    incidence_lower_coefficients = dict(twice_e)
    incidence_lower_coefficients.update({x: -1 for x in e_thresholds})
    incidence_upper_coefficients = {x: -c for x, c in incidence_lower_coefficients.items()}
    builder.pol(
        signed_row(incidence_lower_coefficients, 78),
        [local_lower_ids[v] for v in E],
        "exceptional_incidence_lower",
    )
    builder.pol(
        signed_row(incidence_upper_coefficients, -78),
        [local_upper_ids[v] for v in E],
        "exceptional_incidence_upper",
    )

    # Define q as the disjunction of the two final exceptional-cell u bits.
    # On a valid ordered model the even exceptional excess is 0 or 2, so this
    # deterministic bit is exactly [e(E)=40].  The three defining rows are
    # extension steps and require no modular reasoning in the proof checker.
    e_left_tail = U_IDS[CELLS[0][-1]]
    e_right_tail = U_IDS[CELLS[1][-1]]
    builder.red(
        literal_row([(Q_ID, False), (e_left_tail, True), (e_right_tail, True)]),
        f"x{Q_ID} -> 0",
        "q_implies_exceptional_tail",
    )
    builder.red(
        literal_row([(e_left_tail, False), (Q_ID, True)]),
        f"x{Q_ID} -> 1",
        "left_tail_implies_q",
    )
    builder.red(
        literal_row([(e_right_tail, False), (Q_ID, True)]),
        f"x{Q_ID} -> 1",
        "right_tail_implies_q",
    )

    # Priority definitions make the ten selectors syntactically total for
    # every assignment, while valid M=214 states make the ten mathematical
    # conditions mutually exclusive.  For p<9, y_p is condition_p and no
    # earlier selector; y_9 is the default no-earlier-selector leaf.  The
    # abstract completeness audit proves that this default is precisely the
    # final C_right_7_7 case on every valid state.
    patterns = selector_conditions()
    selector_pair_ids: dict[tuple[int, int], int] = {}
    for selector_index, (name, condition) in enumerate(patterns):
        y = Y_IDS[selector_index]
        if selector_index < len(patterns) - 1:
            antecedents = list(condition) + [
                (Y_IDS[earlier], False) for earlier in range(selector_index)
            ]
        else:
            antecedents = [
                (Y_IDS[earlier], False) for earlier in range(selector_index)
            ]
        for literal_index, literal in enumerate(antecedents):
            identifier = builder.red(
                literal_row([(y, False), literal]),
                f"x{y} -> 0",
                f"selector_{name}_forward_{literal_index}",
            )
            variable, positive = literal
            if not positive and variable in Y_IDS:
                earlier_index = Y_IDS.index(variable)
                selector_pair_ids[(earlier_index, selector_index)] = identifier
        reverse_literals = [(y, True)] + [
            (variable, not positive) for variable, positive in antecedents
        ]
        builder.red(
            literal_row(reverse_literals),
            f"x{y} -> 1",
            f"selector_{name}_reverse",
        )

    # VeriPB propagates the totality row directly.  For at-most-one, expose
    # the clique inequality as nine prefix cutting-planes steps.  For a new
    # y_k, sum its k pairwise exclusions, add (k-1) times the preceding
    # prefix inequality, and divide by k.
    prefix_upper_ids: list[int] = []
    for final_index in range(1, len(Y_IDS)):
        pair_ids = [selector_pair_ids[(earlier, final_index)] for earlier in range(final_index)]
        if final_index == 1:
            expression = str(pair_ids[0])
        else:
            expression = str(pair_ids[0])
            for identifier in pair_ids[1:]:
                expression += f" {identifier} +"
            expression += (
                f" {prefix_upper_ids[-1]} {final_index - 1} * + "
                f"{final_index} d"
            )
        prefix_upper_ids.append(
            builder.pol_expression(
                signed_row({y: -1 for y in Y_IDS[: final_index + 1]}, -1),
                expression,
                f"one_hot_prefix_upper_{final_index}",
            )
        )
    one_hot_lower = builder.rup(
        signed_row({y: 1 for y in Y_IDS}, 1),
        "one_hot_lower",
    )
    one_hot_upper = prefix_upper_ids[-1]

    builder.proof.extend(
        [
            "output EQUISATISFIABLE FILE;",
            "conclusion NONE;",
            "end pseudo-Boolean proof;",
        ]
    )
    summary: dict[str, object] = {
        "added_rows": len(builder.rows),
        "a_order_surplus_sum_max": max(a_order_surplus_sums),
        "a_order_weakened_variables_max": max(a_order_weakened_counts),
        "global_constraint_ids": [global_lower, global_upper],
        "input_internal_constraints": INPUT_INTERNAL,
        "one_hot_constraint_ids": [one_hot_lower, one_hot_upper],
        "output_internal_constraints": builder.next_id - 1,
        "output_rows": INPUT_ROWS + len(builder.rows),
        "output_variables": OUTPUT_VARIABLES,
        "pattern_names": [name for name, _condition in patterns],
    }
    return builder.rows, builder.proof, summary


def write_outputs(source: Path, destination: Path, proof_path: Path) -> dict[str, object]:
    added_rows, proof_lines, summary = build()
    output_rows = INPUT_ROWS + len(added_rows)
    output_header = (
        f"* #variable= {OUTPUT_VARIABLES} #constraint= {output_rows} "
        f"#equal= {INPUT_EQUALITIES} intsize= 64\n"
    ).encode("ascii")
    source_hash = hashlib.sha256()
    output_hash = hashlib.sha256()
    proof_hash = hashlib.sha256()
    output_bytes = 0
    output_lines = 0

    output_tmp = destination.with_name(destination.name + ".partial")
    proof_tmp = proof_path.with_name(proof_path.name + ".partial")
    for temporary in (output_tmp, proof_tmp):
        if temporary.exists():
            temporary.unlink()
    try:
        with source.open("rb") as incoming, output_tmp.open("wb") as outgoing:
            header = incoming.readline()
            source_hash.update(header)
            if header != INPUT_HEADER:
                raise ValueError("input header is not the pinned ordered header")
            outgoing.write(output_header)
            output_hash.update(output_header)
            output_bytes += len(output_header)
            output_lines += 1
            copied = 0
            for line in incoming:
                source_hash.update(line)
                outgoing.write(line)
                output_hash.update(line)
                output_bytes += len(line)
                output_lines += 1
                copied += 1
            if copied != INPUT_ROWS:
                raise ValueError(f"input has {copied} rows, expected {INPUT_ROWS}")
            if source_hash.hexdigest() != INPUT_SHA256:
                raise ValueError("input SHA-256 does not match the certified ordered OPB")
            for row in added_rows:
                data = (row + "\n").encode("ascii")
                outgoing.write(data)
                output_hash.update(data)
                output_bytes += len(data)
                output_lines += 1
            outgoing.flush()
            os.fsync(outgoing.fileno())
        with proof_tmp.open("wb") as raw:
            for line in proof_lines:
                data = (line + "\n").encode("ascii")
                raw.write(data)
                proof_hash.update(data)
            raw.flush()
            os.fsync(raw.fileno())
        os.replace(output_tmp, destination)
        os.replace(proof_tmp, proof_path)
    except BaseException:
        for temporary in (output_tmp, proof_tmp):
            if temporary.exists():
                temporary.unlink()
        raise

    summary.update(
        {
            "formula_bytes": output_bytes,
            "formula_lines": output_lines,
            "formula_sha256": output_hash.hexdigest(),
            "proof_bytes": proof_path.stat().st_size,
            "proof_lines": len(proof_lines),
            "proof_sha256": proof_hash.hexdigest(),
        }
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    args = parser.parse_args()
    paths = [args.input.resolve(), args.output.resolve(), args.proof.resolve()]
    if len(set(paths)) != 3:
        raise ValueError("input, output, and proof paths must be distinct")
    summary = write_outputs(*paths)
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
