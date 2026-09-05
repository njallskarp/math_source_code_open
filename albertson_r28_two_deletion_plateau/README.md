# The two-deletion plateau at the Albertson r=28 frontier

This directory gives an exact obstruction to strengthening the current
Albertson `r=28`, order-55 argument merely by optimizing how complement edges
mix among the surviving degree classes.

## Statement

Let `G` have 55 vertices and let

    x_v = d_G(v)-27,              H = complement(G).

Assume the height-2583 separator conclusion: `H-B` has two singleton
components, their excesses are `{25,25}` or `{24,25}`, there is no edge between
them, and the excess profile is one of the three profiles at `m=768` or eight
profiles at `m=769` listed by that contribution.  Apply the reviewed generic
convex deletion table `F_53(q)` to every two-vertex deletion.  The resulting
averaging bound is

    7063  when m=768,
    7095  when m=769,

for **every** possible mixing of the complement edges.  Thus exact
degree-class edge mixing improves the previous one-deletion bounds `7062` and
`7093`, but it cannot reach `Z(28)=7098`.  Even the most favorable possible
row-769 numerator is short by 3099 before division by
`binom(51,2)=1275`.

This is a method obstruction, not a nonexistence theorem for either row.

## Proof

Deleting vertices `u,v` leaves

    e(G-u-v) = m-53-x_u-x_v-h_uv,

where `h_uv` is one when `uv` is an edge of `H`.  Every crossing survives in
exactly `binom(51,2)` two-vertex deletions, so the recurrence numerator is

    A(x) - sum_{uv in E(H)} delta(x_u+x_v),

where

    A(x) = sum_{u<v} F_53(m-53-x_u-x_v),
    delta(s) = F_53(m-53-s)-F_53(m-54-s).

The table values make the second sum elementary.

At `m=769`, every edge from one of the two singleton vertices to the remaining
53 vertices has weight 26.  Every edge among the remaining vertices has
weight 29, except an edge joining excess classes zero and one, which has weight
30.  If `D` is the sum of the two singleton degrees and `e_01` counts the last
exceptional edges, then, since `e(H)=716`,

    penalty = 29*716 - 3D + e_01,
    0 <= e_01 <= 26*n_1.

Here `D` is four or five and `n_1` is the number of excess-one vertices.  These
bounds put both endpoints of the recurrence in the same rounding interval,
giving 7095 for all eight profiles.

At `m=768`, `e(H)=717`, singleton edges again have weight 26, while the default
remaining weight is 30.  The exceptional weight-29 edges are respectively
`e_01`, `e_02`, or `e_01+e_11` for the three profiles.  The rare vertices have
degrees 26, 25, or `(26,26)`, and each can meet at most the two singleton
vertices.  Therefore

    24 <= e_01 <= 26,
    23 <= e_02 <= 25,
    47 <= e_01+e_11 <= 52,

respectively.  Again both endpoints round identically, now to 7063.

No graphical realization, solver, or labeled graph enumeration is used.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r28_two_deletion_plateau
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 audit.py | diff -u EXPECTED_AUDIT.txt -
shasum -a 256 -c SHA256SUMS
```

The verifier reconstructs the exact rounded convex tables from the five
published affine supports, checks every weight identity and degree-counting
interval, and evaluates all eleven profiles with integer and
`fractions.Fraction` arithmetic.  The independent audit uses a frozen 22-entry
slice of `F_53` and a type-count rather than pair-by-pair decomposition to
check all baselines and rounding intervals by a second route.

## Trust boundary and status

The two-deletion identity and the edge-class calculation are unconditional
once their stated profiles and separator structure are assumed.  The Albertson
application remains review-gated because height 2583 depends on the unreviewed
finite component classification at height 2569.  The checker does not re-prove
that classification, Stehlik's factor-criticality theorem, the published
crossing inequalities, or the generic convex deletion recurrence at height
1813.  No `r=27` terminal theorem, `cr(24,132)>=165`, local crossing
conjecture, floating point, randomness, or external solver is used.
