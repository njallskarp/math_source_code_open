# Albertson r = 29: clean feasibility gate

This directory is pass 1 of a predeclared two-pass feasibility gate for the
`r=29` case of Albertson's conjecture.  It gives a clean-room exact frontier;
it does **not** prove the conjecture for `r=29`.  No `r=27` terminal theorem,
`r=28` case tree, local crossing-number table, floating-point computation, or
solver is used.

## Proposition

Assume the quoted critical-graph and order-exclusion results in the Cranston
and Sadhu preprints.  If `G` is a minimum 29-critical counterexample to
Albertson's conjecture and `(n,m)=(|V(G)|,|E(G)|)`, then precisely the following
eight rows survive the published affine crossing inequalities and the generic
convex induced-subgraph recurrence:

```
n=57: m=824,825,826,827,828
n=58: m=838,839,840.
```

Moreover, `H=bar(G)` is connected.  At order 57, `H` is factor-critical.  At
order 58, for every vertex `v`, `H-v` has a spanning clique factor consisting
of one triangle and 27 independent matching edges.  These order-58
`K3+27K2` factors are the clean structural frontier for gate pass 2.

The recursive crossing lower bounds on the eight rows are

```
(57,824..828): 8131, 8164, 8198, 8232, 8266
(58,838..840): 8210, 8243, 8276.
```

Since `Z(29)=8281`, a counterexample has crossing number at most 8280.

## Exact order and edge dispatch

Cranston's order results give the following conservative integer dispatch.
A counterexample has no subdivision of `K_29`; the order-at-most-`r+4`
theorem excludes `n<=33`.  The interval theorem excludes integer orders
`36<=n<=51`, because

```
1.228*29 = 35.612,     1.768*29 = 51.272,
```

and the large-order theorem excludes `n>=82`, because `2.82*29=81.78`.
Thus only the 32 orders `34,35,52,...,81` enter the certificate.  We use these
conservative constants because they are stated consistently in the v1
abstract and theorem-level result; no stronger nearby decimal in expository
text is needed.

For each candidate order, the integral edge floor is the ceiling of half the
maximum of

```
Kostochka--Yancey: ((r+1)(r-2)n-r(r-3))/(r-1),
Cranston Lemma E:  (r-1)n+2r-6,
Gallai:             (r-1)n+(n-r)(2r-n)-2
                    (only r+2 <= n <= 2r-2).
```

These expressions bound `2m`.  Lemma E applies because a counterexample has no
subdivision of `K_r`.

## Crossing recurrence

For a graph of order `s` and size `q`, start from the integer ceilings of

```
0,
q-3(s-2),
(7q-25(s-2))/3,
4q-103(s-2)/6,
(37q-155(s-2))/9,
5q-203(s-2)/9.
```

Take the greatest convex minorant of their pointwise integer maximum.  If
`F_s` is the recursively improved minorant and `4<=s<n`, counting a fixed
drawing over all induced `s`-vertex subgraphs and applying Jensen gives

```
F_n(q) >= ceil[ C(n,s)/C(n-4,s-4)
                  * F_s(q*s*(s-1)/(n*(n-1))) ].             (R)
```

Every crossing belongs to exactly `C(n-4,s-4)` sampled subgraphs, and the mean
sampled edge count is the displayed rational.  This proves (R); the program
builds it in increasing order with exact fractions and local integer rounding.

Direct one-stage sampling leaves only the initial rows

```
(56,810), (57,824), (58,838), (59,852).
```

The recurrence closes order 59 and gives preliminary intervals `810..816`,
`824..828`, and `838..840` at orders 56, 57, and 58.

For a critical graph with disconnected complement, the two-branch join
estimate gives

```
m >= min((n-1)+ceil((r-2)(n-1)/2)+r-4, r^2+3r-19).
```

At orders 56, 57, 58 this raises the edge floors to 823, 837, 852; the exact
recursive crossing bounds there are respectively 8497, 8575, 8684, all above
8280.  Gallai already forces the complement to be disconnected through order
`2r-2=56`, so order 56 is eliminated.  At orders 57 and 58 the same argument
shows that every survivor has connected complement.  Hence every order family
other than 57 and 58 is eliminated.

## Degree and colour-class consequences

Put `x_v=d_G(v)-28>=0`.  The total excess `X=sum_v x_v=2m-28n` is

```
n=57: X=52,54,56,58,60;
n=58: X=52,54,56.
```

The elementary lower bound on the number of degree-28 vertices is
`max(0,n-X)`: it is 5,3,1,0,0 on the order-57 rows and 6,4,2 on the order-58
rows.  These are lower bounds, not asserted exact profiles.

Stehlik's connected-complement theorem says that for each vertex `v`, the
28-colouring of `G-v` can be chosen with every colour class of size at least
two.  At `n=57`, all 28 classes are pairs, so `H-v` has a perfect matching for
every `v`; hence `H` is factor-critical.  At `n=58`, the 57 vertices of `H-v`
split necessarily into 27 two-vertex cliques and one three-vertex clique.
This is the promised `K3+27K2` factor.

## Gate decision and missing dependency

The first-day continuation criterion is met: the exact calculation eliminates
the complete order family `n<=56` and reduces all candidate orders to two
families and eight rows.  This is stronger than a table-growth outcome.

The second and final permitted pass should test one structural question only:
whether the overlapping `K3+27K2` factors of connected `H-v` force a bounded
canonical profile family or exclude order 58.  The factor-critical separator
machinery at order `2r-1=57` does not automatically extend to order 58.  If no
uniform overlap constraint appears, the exact obstruction is the absence of a
replacement for factor-critical odd-component/barrier theory in this
one-triple setting, and the r=29 direction must pause.

## Reproduction

Requires CPython 3.12 or later and only the standard library.

```sh
cd albertson_r29_feasibility_gate
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 frontier_certificate.py | diff -u FRONTIER_CERTIFICATE.tsv -
shasum -a 256 -c SHA256SUMS
```

The main verifier runs in about 15 seconds on an ordinary laptop.  The sparse
dependency digest covers all 32 initial rows and every recursively active
endpoint needed at the open/closed boundary.

## Trust and conditionality boundary

The scripts verify the exact affine arithmetic, all critical edge floors,
candidate-order dispatch, direct and recursive sampling, monotonicity controls,
eight-row frontier, disconnected-complement thresholds, degree excesses, and a
canonical sparse provenance digest.  They do not verify the cited graph
theorems, the prose proof of the recurrence, or the claimed crossing
inequalities.  No numerical evidence is promoted to proof: all program
arithmetic is exact, while the theorem statements are external inputs.

The frontier conclusion is conditional on the theorem statements in two recent
preprints: Cranston's order exclusions and Lemma E, and Sadhu's exact collation
and disconnected-complement join estimate.  The affine crossing inequalities,
Kostochka--Yancey bound, and Stehlik theorem are published results.  There is no
conditional `cr(24,132)>=165` appendix because that value is not used.

## Literature and novelty audit

Primary sources checked on 2026-09-05:

- Daniel W. Cranston, [*Progress on Albertson's
  Conjecture*](https://arxiv.org/abs/2512.08020v1).
- Ankan Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682v1).
- Janos Pach, Rados Radoicic, Gabor Tardos, and Geza Toth, [*Improving the
  Crossing Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9).
- Aaron Buengener and Michael Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://arxiv.org/abs/2409.01733).
- Alexandr Kostochka and Matthew Yancey, [*Ore's Conjecture on Color-Critical
  Graphs Is Almost True*](https://doi.org/10.1016/j.jctb.2014.05.002).
- Matej Stehlik, [*Critical Graphs with Connected
  Complements*](https://doi.org/10.1016/S0095-8956(03)00069-8).

Exact-phrase, arXiv, and Discovery Net searches found no prior public
all-order `r=29` reduction to these eight rows.  The existing Discovery Net
order-`2r-1` separator result treats order 57 and is a compatible downstream
tool, but it neither closes order 58 nor supplies this all-order dispatch.
This is a bounded search report, not a claim of exhaustive priority.
