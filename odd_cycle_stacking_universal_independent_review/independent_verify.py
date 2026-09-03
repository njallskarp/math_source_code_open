#!/usr/bin/env python3
"""Clean-room audit of the universal odd-cycle ancestry certificate.

This program does not import the contributor's verifier.  It transcribes the
published certificate table into a small exact algebra and checks:

* residue assignment, integrality, nonnegativity, and the three leaf bases;
* every unordered disjoint singleton-mask split in both edge directions;
* the two infinite arm families by an exact endpoint/monotonicity lemma;
* all five boundary-edge families for both parities of k;
* the common-root forest bound after an independently implemented residue
  reduction; and
* a direct instantiated replay for 3 <= k <= 128 as an indexing guard.

Only Python standard-library Fractions and arbitrary-precision integers are
used.  The finite replay is a regression check; the universal conclusion comes
from the symbolic checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools


@dataclass(frozen=True)
class Expr:
    """a*2^k + b*2^d + c, stored over the rationals."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)
    c: Fraction = Fraction(0)

    def __add__(self, other: "Expr") -> "Expr":
        return Expr(self.a + other.a, self.b + other.b, self.c + other.c)

    def __sub__(self, other: "Expr") -> "Expr":
        return Expr(self.a - other.a, self.b - other.b, self.c - other.c)

    def __rmul__(self, scalar: int | Fraction) -> "Expr":
        return Expr(scalar * self.a, scalar * self.b, scalar * self.c)

    def replace_two_to_d(self, multiple: int | Fraction) -> "Expr":
        return Expr(self.a, multiple * self.b, self.c)

    def fix_gap(self, h: int) -> "Expr":
        """Use d=k-h, hence 2^d=2^k/2^h."""
        return Expr(self.a + self.b / (2**h), Fraction(0), self.c)

    def fix_depth(self, d: int) -> "Expr":
        return Expr(self.a, Fraction(0), self.b * (2**d) + self.c)

    def evaluate(self, k: int, d: int = 0) -> Fraction:
        return self.a * (2**k) + self.b * (2**d) + self.c

    def canonical(self) -> str:
        return f"{self.a}|{self.b}|{self.c}"


ZERO = Expr()
PP = Expr(a=Fraction(1))
ZZ = Expr(b=Fraction(1))
ONE = Expr(c=Fraction(1))


def qmod3(q: Fraction) -> int:
    den = q.denominator % 3
    assert den != 0
    return (q.numerator % 3) * pow(den, -1, 3) % 3


def residue(expr: Expr, k_parity: int, d_parity: int) -> int:
    return (
        qmod3(expr.a) * (1 if k_parity == 0 else 2)
        + qmod3(expr.b) * (1 if d_parity == 0 else 2)
        + qmod3(expr.c)
    ) % 3


Rows = tuple[tuple[Expr, Expr, Expr], ...]


def by_residue(candidates: list[Expr], kp: int, dp: int) -> tuple[Expr, Expr, Expr]:
    assert len(candidates) == 3
    placed: list[Expr | None] = [None, None, None]
    for candidate in candidates:
        r = residue(candidate, kp, dp)
        assert placed[r] is None, "duplicate residue in candidate row"
        placed[r] = candidate
    assert all(item is not None for item in placed)
    return tuple(placed)  # type: ignore[return-value]


def make_rows(candidate_rows: list[list[Expr]], kp: int, dp: int) -> Rows:
    return tuple(by_residue(row, kp, dp) for row in candidate_rows)


def left_arm(kp: int, dp: int) -> Rows:
    return make_rows(
        [
            [ZZ, 4 * PP - 2 * ZZ, 5 * PP - 2 * ZZ],
            [2 * PP - 2 * ZZ, 3 * PP - 2 * ZZ, 4 * PP - 2 * ZZ],
            [PP + ZZ - 3 * ONE, Fraction(7, 2) * PP - 2 * ZZ,
             Fraction(9, 2) * PP - 2 * ZZ],
            [Fraction(5, 2) * PP - 2 * ZZ,
             Fraction(7, 2) * PP - 2 * ZZ, 3 * PP - 2 * ZZ - 3 * ONE],
        ],
        kp,
        dp,
    )


def right_arm(kp: int, dp: int) -> Rows:
    return make_rows(
        [
            [ZZ, 4 * PP - 2 * ZZ, 5 * PP - 2 * ZZ],
            [2 * PP + ZZ - 3 * ONE, 3 * PP - 2 * ZZ,
             4 * PP - 2 * ZZ],
            [PP - 2 * ZZ, Fraction(7, 2) * PP - 2 * ZZ,
             Fraction(9, 2) * PP - 2 * ZZ],
            [Fraction(5, 2) * PP - 2 * ZZ,
             Fraction(7, 2) * PP - 2 * ZZ, 3 * PP - 2 * ZZ - 3 * ONE],
        ],
        kp,
        dp,
    )


def left_x(kp: int) -> Rows:
    return make_rows(
        [
            [PP, 2 * PP, 3 * PP],
            [ZERO, 2 * PP, Fraction(5, 2) * PP],
            [Fraction(3, 2) * PP, 2 * PP - 3 * ONE, Fraction(5, 2) * PP],
            [Fraction(3, 2) * PP, 2 * PP, Fraction(5, 2) * PP - 3 * ONE],
        ],
        kp,
        kp,
    )


def middle(kp: int) -> Rows:
    return make_rows(
        [
            [PP, 2 * PP, 3 * PP],
            [PP, 2 * PP, 3 * PP - 3 * ONE],
            [Fraction(1, 2) * PP, Fraction(5, 2) * PP, 3 * PP - 3 * ONE],
            [Fraction(3, 2) * PP, 2 * PP - 3 * ONE,
             Fraction(5, 2) * PP - 3 * ONE],
        ],
        kp,
        kp,
    )


def right_y(kp: int) -> Rows:
    dp = 1 - kp
    return make_rows(
        [
            [Fraction(1, 2) * PP, 3 * PP, 4 * PP],
            [2 * PP, Fraction(5, 2) * PP - 3 * ONE, 3 * PP],
            [ZERO, Fraction(5, 2) * PP, Fraction(7, 2) * PP],
            [Fraction(3, 2) * PP, Fraction(5, 2) * PP,
             Fraction(11, 4) * PP - 3 * ONE],
        ],
        kp,
        dp,
    )


def transform(rows: Rows, fn) -> Rows:
    return tuple(tuple(fn(item) for item in row) for row in rows)


def first_parity_at_least(lower: int, parity: int) -> int:
    return lower if lower % 2 == parity else lower + 1


# These are all unordered disjoint partitions of a mask contained in {x,y}.
# Addition of child costs is commutative, so the reversed pairs are identical.
MASK_SPLITS = tuple(
    (left | right, left, right)
    for left in range(4)
    for right in range(left, 4)
    if left & right == 0
)
assert MASK_SPLITS == ((0, 0, 0), (1, 0, 1), (2, 0, 2),
                       (3, 0, 3), (3, 1, 2))


def bellman_differences(children: Rows, parents: Rows):
    for union, left, right in MASK_SPLITS:
        for lr, rr in itertools.product(range(3), repeat=2):
            pr = (lr + rr) % 3
            yield (
                f"m{union}:{left},{lr}+{right},{rr}",
                children[left][lr] + children[right][rr] - parents[union][pr],
            )


class Audit:
    def __init__(self) -> None:
        self.arm_count = 0
        self.fixed_count = 0
        self.residue_rows = 0
        self._hash = hashlib.sha256()

    def _record(self, text: str) -> None:
        self._hash.update((text + "\n").encode("ascii"))

    def arm(self, expr: Expr, d_min: int, h_min: int, dp: int, hp: int,
            label: str) -> None:
        """Prove 2^d(a*2^h+b)+c >= 0 on an infinite parity domain."""
        d0 = first_parity_at_least(d_min, dp)
        h0 = first_parity_at_least(h_min, hp)
        assert expr.a >= 0, (label, expr)
        bracket = expr.a * (2**h0) + expr.b
        assert bracket >= 0, (label, expr, "bracket")
        endpoint = (2**d0) * bracket + expr.c
        assert endpoint >= 0, (label, expr, "endpoint")
        self.arm_count += 1
        self._record(
            f"A|{label}|{expr.canonical()}|{d_min},{dp},{d0}|"
            f"{h_min},{hp},{h0}|{bracket}|{endpoint}"
        )

    def fixed(self, expr: Expr, k_min: int, kp: int, label: str) -> None:
        """Prove a*2^k+c >= 0 on one parity class."""
        assert expr.b == 0, (label, expr, "unfixed depth")
        k0 = first_parity_at_least(k_min, kp)
        assert expr.a >= 0, (label, expr)
        endpoint = expr.a * (2**k0) + expr.c
        assert endpoint >= 0, (label, expr, "endpoint")
        self.fixed_count += 1
        self._record(f"K|{label}|{expr.canonical()}|{k_min},{kp},{k0}|{endpoint}")

    @property
    def digest(self) -> str:
        return self._hash.hexdigest()


def prove_edge_arm(audit: Audit, low: Rows, high: Rows, d_min: int,
                   h_min: int, dp: int, hp: int, name: str) -> None:
    for direction, children, parents in (
        ("low-high", low, high), ("high-low", high, low)
    ):
        for local, expr in bellman_differences(children, parents):
            audit.arm(expr, d_min, h_min, dp, hp, f"{name}:{direction}:{local}")


def prove_edge_fixed(audit: Audit, first: Rows, second: Rows, kp: int,
                     name: str) -> None:
    for direction, children, parents in (
        ("first-second", first, second), ("second-first", second, first)
    ):
        for local, expr in bellman_differences(children, parents):
            audit.fixed(expr, 3, kp, f"{name}:{direction}:{local}")


def empty_forest_options(empty_row: tuple[Expr, Expr, Expr]):
    yield 0, ZERO, "zero"
    for r in range(3):
        yield r, empty_row[r], f"one:{r}"
    for r1, r2 in itertools.product(range(3), repeat=2):
        yield (r1 + r2) % 3, empty_row[r1] + empty_row[r2], f"two:{r1},{r2}"


def forest_differences(rows: Rows, target_residue: int, required: Expr):
    special = [(r, rows[3][r], f"joint:{r}") for r in range(3)]
    special += [
        ((rx + ry) % 3, rows[1][rx] + rows[2][ry], f"split:{rx},{ry}")
        for rx, ry in itertools.product(range(3), repeat=2)
    ]
    for sr, scost, slabel in special:
        for er, ecost, elabel in empty_forest_options(rows[0]):
            if (sr + er) % 3 == target_residue:
                yield f"{slabel}:{elabel}", scost + ecost - required


def symbolic_audit() -> Audit:
    audit = Audit()

    # Candidate rows and nonnegativity on both infinite arms.
    for dp, hp in itertools.product(range(2), repeat=2):
        kp = (dp + hp) % 2
        for name, rows, d_min, h_min in (
            ("left", left_arm(kp, dp), 0, 1),
            ("right", right_arm(kp, dp), 1, 2),
        ):
            audit.residue_rows += 4
            for mask, r in itertools.product(range(4), range(3)):
                audit.arm(rows[mask][r], d_min, h_min, dp, hp,
                          f"nonnegative:{name}:{mask}:{r}")

    # The three exceptional vertices.
    for kp in range(2):
        for name, rows in (("x", left_x(kp)), ("middle", middle(kp)),
                           ("y", right_y(kp))):
            audit.residue_rows += 4
            for mask, r in itertools.product(range(4), range(3)):
                audit.fixed(rows[mask][r], 3, kp,
                            f"nonnegative:{name}:{mask}:{r}")

    # Leaf bases, with identities required rather than inequalities.
    for kp in range(2):
        pile = transform(left_arm(kp, 0), lambda e: e.fix_depth(0))
        assert pile[0][1] == ONE
        assert left_x(kp)[1][0] == ZERO
        assert right_y(kp)[2][0] == ZERO
        audit._record(f"BASE|{kp}|pile=1|x=0|y=0")

    # Infinite arm edges.
    for dp, hp in itertools.product(range(2), repeat=2):
        kp = (dp + hp) % 2
        prove_edge_arm(
            audit,
            left_arm(kp, dp),
            transform(left_arm(kp, 1 - dp), lambda e: e.replace_two_to_d(2)),
            0,
            2,
            dp,
            hp,
            "left-edge",
        )
        prove_edge_arm(
            audit,
            right_arm(kp, dp),
            transform(right_arm(kp, 1 - dp), lambda e: e.replace_two_to_d(2)),
            1,
            3,
            dp,
            hp,
            "right-edge",
        )

    # Five boundary edge types.
    for kp in range(2):
        l0 = transform(left_arm(kp, 0), lambda e: e.fix_depth(0))
        r1 = transform(right_arm(kp, 1), lambda e: e.fix_depth(1))
        lh1 = transform(left_arm(kp, 1 - kp), lambda e: e.fix_gap(1))
        rh2 = transform(right_arm(kp, kp), lambda e: e.fix_gap(2))
        lx, mid, ry = left_x(kp), middle(kp), right_y(kp)
        for name, a, b in (
            ("seam", l0, r1),
            ("left-h1-x", lh1, lx),
            ("x-middle", lx, mid),
            ("middle-y", mid, ry),
            ("y-right-h2", ry, rh2),
        ):
            prove_edge_fixed(audit, a, b, kp, name)

    threshold = Fraction(5, 2) * PP - 3 * ONE
    outer = Fraction(5, 2) * PP

    # Outer roots have h>=3.  Modulo 3, threshold and M_k differ by 3.
    for dp, hp in itertools.product(range(2), repeat=2):
        kp = (dp + hp) % 2
        target_r = residue(threshold, kp, dp)
        for name, rows, d_min in (
            ("left", left_arm(kp, dp), 0),
            ("right", right_arm(kp, dp), 1),
        ):
            for local, expr in forest_differences(rows, target_r, outer):
                audit.arm(expr, d_min, 3, dp, hp, f"forest-outer:{name}:{local}")

    # Six central roots.
    for kp in range(2):
        target_r = residue(threshold, kp, 0)
        central = (
            ("left-h2", transform(left_arm(kp, kp), lambda e: e.fix_gap(2))),
            ("left-h1", transform(left_arm(kp, 1 - kp), lambda e: e.fix_gap(1))),
            ("x", left_x(kp)),
            ("middle", middle(kp)),
            ("y", right_y(kp)),
            ("right-h2", transform(right_arm(kp, kp), lambda e: e.fix_gap(2))),
        )
        for name, rows in central:
            for local, expr in forest_differences(rows, target_r, threshold):
                audit.fixed(expr, 3, kp, f"forest-central:{name}:{local}")

    assert audit.residue_rows == 56
    assert audit.arm_count == 1232
    assert audit.fixed_count == 1596
    return audit


def concrete_rows(k: int, vertex: int) -> list[list[int]]:
    n = 2 * k + 1
    kp = k % 2
    if vertex < k:
        d, rows = vertex, left_arm(kp, vertex % 2)
    elif vertex == k:
        d, rows = k, left_x(kp)
    elif vertex == k + 1:
        d, rows = k, middle(kp)
    elif vertex == k + 2:
        d, rows = k - 1, right_y(kp)
    else:
        d = n - vertex
        rows = right_arm(kp, d % 2)
    answer: list[list[int]] = []
    for mask, row in enumerate(rows):
        converted = []
        for r, expr in enumerate(row):
            value = expr.evaluate(k, d)
            assert value.denominator == 1
            integer = value.numerator
            assert integer >= 0 and integer % 3 == r, (k, vertex, mask, r, integer)
            converted.append(integer)
        answer.append(converted)
    return answer


def concrete_bellman(children: list[list[int]], parents: list[list[int]]):
    for union, left, right in MASK_SPLITS:
        for lr, rr in itertools.product(range(3), repeat=2):
            yield children[left][lr] + children[right][rr] - parents[union][(lr + rr) % 3]


def concrete_forest_min(rows: list[list[int]], target_r: int) -> int:
    empties = [(0, 0)]
    empties += [(r, rows[0][r]) for r in range(3)]
    empties += [
        ((r1 + r2) % 3, rows[0][r1] + rows[0][r2])
        for r1, r2 in itertools.product(range(3), repeat=2)
    ]
    specials = [(r, rows[3][r]) for r in range(3)]
    specials += [
        ((r1 + r2) % 3, rows[1][r1] + rows[2][r2])
        for r1, r2 in itertools.product(range(3), repeat=2)
    ]
    return min(
        ec + sc for er, ec in empties for sr, sc in specials
        if (er + sr) % 3 == target_r
    )


def finite_replay(max_k: int = 128) -> tuple[int, int, int, str]:
    digest = hashlib.sha256()
    states = local_checks = roots = 0
    for k in range(3, max_k + 1):
        n = 2 * k + 1
        tables = [concrete_rows(k, vertex) for vertex in range(n)]
        assert tables[0][0][1] == 1
        assert tables[k][1][0] == 0
        assert tables[k + 2][2][0] == 0
        for vertex, rows in enumerate(tables):
            for mask, row in enumerate(rows):
                for r, value in enumerate(row):
                    digest.update(f"D,{k},{vertex},{mask},{r},{value}\n".encode("ascii"))
                    states += 1
            nxt = (vertex + 1) % n
            for children, parents in ((rows, tables[nxt]), (tables[nxt], rows)):
                differences = list(concrete_bellman(children, parents))
                assert min(differences) >= 0
                local_checks += len(differences)

        target = Fraction(5, 2) * (2**k) - 3
        assert target.denominator == 1
        threshold = target.numerator
        target_r = threshold % 3
        for vertex, rows in enumerate(tables):
            observed = concrete_forest_min(rows, target_r)
            expected = threshold if k - 2 <= vertex <= k + 3 else threshold + 3
            assert observed == expected, (k, vertex, observed, expected)
            digest.update(f"F,{k},{vertex},{target_r},{observed}\n".encode("ascii"))
            roots += 1
    return states, local_checks, roots, digest.hexdigest()


def main() -> None:
    audit = symbolic_audit()
    states, local_checks, roots, finite_digest = finite_replay()
    print("CLEAN-ROOM UNIVERSAL CERTIFICATE AUDIT: VERIFIED")
    print(f"residue_rows={audit.residue_rows}")
    print(f"symbolic_arm_checks={audit.arm_count}")
    print(f"symbolic_fixed_k_checks={audit.fixed_count}")
    print(f"symbolic_obligation_sha256={audit.digest}")
    print(
        "finite_replay_k=3..128 "
        f"states={states} local_checks={local_checks} roots={roots}"
    )
    print(f"finite_replay_sha256={finite_digest}")


if __name__ == "__main__":
    main()
