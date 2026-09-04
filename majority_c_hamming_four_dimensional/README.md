# Near-triangle bounds for majority C-colourings of Hamming graphs

This directory gives a structural upper bound for four-dimensional imbalanced
Hamming graphs and exact formulas in an infinite divisibility regime.

For

```text
G = K_n1 square K_n2 square K_n3 square K_n4,
n1 >= n2 >= n3 >= n4 >= 2,
N_i = n_i - 1,
h = ceil((N_1+N_2+N_3+N_4)/2),
```

assume `h >= N_1` and put `s=h-N_1+1`.  Then

```text
chi_bar_>=(G) <= floor(n2*n3*n4/s).
```

If `s` divides at least one of `n2,n3,n4`, equality holds.  The proof extends
to every dimension satisfying `N_1 <= h <= N_1+N_2`: every colour class has
at least `n1*s` vertices, and the same quotient upper bound follows.

A mixed-radix line partition substantially enlarges the exact regime.  If

```text
(n2 mod s) * (n3 mod s) * (n4 mod s) < s,
```

then the quotient upper bound is attained, even when `s` divides none of the
three minor orders.  See
[MIXED_RADIX_EXTENSION.md](MIXED_RADIX_EXTENSION.md) for the dimension-free
partition lemma and proof.  The first concrete new case is
`K_5 square K_3 square K_3 square K_3`, whose exact value is `13`.

The complete proof and exact parameter map are in
[NEAR_TRIANGLE_FOUR_DIMENSIONAL.md](NEAR_TRIANGLE_FOUR_DIMENSIONAL.md).

## Reproduction

CPython 3.12 or later; standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_near_triangle.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_mixed_radix.py
```

Expected output:

```text
greedy parameter quadruples checked: 57870
greedy total-shell sizes checked: 2159646
full-profile parameter quadruples checked: 316
full shell profiles checked: 176336
divisible constructions checked: 10166
K3xK2xK2xK2 candidate subsets checked: 187726
K3xK2xK2xK2 feasible size-6 subsets: 12
all exact checks passed
```

The mixed-radix checker separately reports:

```text
mixed-radix identities checked: 93412
qualifying identities checked: 66550
four-dimensional near-triangle parameters checked: 479445
residue-product families detected: 141493
genuinely nondivisible families detected: 21615
generic cell-level partitions checked: 4025
generic line classes checked: 212261
lifted Hamming partitions checked: 647
lifted Hamming colour classes checked: 30251
all exact checks passed
```

## Evidence and trust boundary

The theorem is a human proof from an exact first/second-shell incidence bound,
capped majorization, and concavity.  The verifier uses arbitrary-precision
integers to audit the greedy reduction, every bounded shell profile in a
documented range, the divisibility constructions, and every potentially
too-small induced class in `K_3 square K_2 square K_2 square K_2`.

The computation corroborates conventions and boundary algebra; it does not
prove the universal claim.  There is no floating point, randomness, solver,
network input, or external data.

## Literature boundary

Bujtas, Dettlaff, Furmanczyk, and Laskowska explicitly ask for the imbalanced
three- and four-dimensional cases in Open Problem 2 of *Majority C-coloring in
Cartesian products* (2026):

<https://arxiv.org/abs/2608.27669>

Their Proposition 15 supplies coordinate-fibre lower bounds, and their
balanced even-dimensional theorem is recovered here when all four orders are
equal.  The source does not state the class-size bound or the imbalanced
divisibility formulas above.  Targeted searches on 2026-09-04 found no matching
result.  Novelty is search-relative, not a historical-priority claim.
