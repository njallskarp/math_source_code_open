# Exact exclusion of the two extreme defect branches in a canonical QLP-42 shell

## Abstract

We consolidate exact finite certificates excluding the two extreme
quarter-turn branches in the canonical norm-32 residual shell arising in the
length-42 quaternary Legendre-pair problem. An exact Chinese-remainder
half-sum/half-difference transform replaces two length-42 fourth-root words by
four coupled length-21 Gaussian words. In the branch with one quarter-turn
cell, a complete third-order classification partitions the search into the
nine rows `b=4,6,...,20`; separately published exact obstructions exclude
every row. In the complementary extreme branch with 41 quarter-turn cells,
a complete third-order classification restricts a binary axis word to weights
`0,4,8,12,16,20`; an exhaustive exact all-weight computation excludes every
weight and global-sum case. The conclusion is conditional on the established
canonical shell reduction and coupled transform. It does not resolve the
full length-42 existence problem. We give immutable source pins, the complete
proof dependency graph, prior-art positioning, and explicit trust boundaries,
with special attention to the exceptional weight-12 orbit manifest.

## 1. Setting and exact bridge

Let `A` and `B` be length-42 words over the fourth roots of unity. In the
Chinese-remainder coordinates `Z/42Z = Z/21Z x Z/2Z`, write for either word
`X`

```text
x_j = X_(22j mod 42),       y_j = X_(22j+21 mod 42),
S_X(j) = (x_j-y_j)/(1+i),   H_X(j) = (x_j+y_j)/(1+i).
```

The ordered pair `(x_j,y_j)` is in bijection with 16 local states
`(S_X(j),H_X(j))`. Direct expansion gives, for `0<=s<=20`,

```text
PAF(X,s)-PAF(X,s+21) = 2(-1)^s PAF(S_X,s),
PAF(X,s)+PAF(X,s+21) = 2 PAF(H_X,s).
```

Inside the selected canonical norm-32 residual shell, the transformed words
satisfy

```text
PAF(S_A,s)+PAF(S_B,s) = 43 at s=0,
                         -2 at s in {4,17},
                         +2 at s in {10,11},
                          0 otherwise;

PAF(H_A,s)+PAF(H_B,s) = 41 at s=0,
                         -2 at every nonzero s.
```

There are six canonical exact-sum cases, represented by

```text
(1,0,5,0), (3,0,4,1), (3,0,3,-2),
(3,2,3,2), (3,2,2,3), (4,1,2,-1).
```

For a representative `(p,r,x,y)` the four transformed sums are

```text
sum(S_A)=(p+r)+(r-p)i,  sum(H_A)=0,
sum(S_B)=(x+y-1)+(y-x)i, sum(H_B)=1.
```

Let `q` denote the total number of quarter-turn local cells. The binary
defect-count restriction gives `q=1 mod 4`. The present paper treats only the
two extreme allowed values `q=1` and `q=41`.

### Theorem 1 (exact coupled bridge, imported)

Within the canonical norm-32 shell, the length-42 fourth-root formulation and
the four length-21 coupled Gaussian formulation above are bijectively
equivalent.

The proof is the local 16-state bijection plus the two displayed
autocorrelation identities. This theorem is imported from the pinned coupled-
transform artifact rather than reproved formally here. Section 7 states the
resulting trust boundary precisely.

## 2. The q=1 branch

When `q=1`, second-order divisibility forces the 20 non-quarter cells of
family `B` to occur in ten reflected equal/opposite pairs. Let `b` be the
number of opposite non-quarter cells in that family. The complete third-order
classification proves that the surviving branch is the disjoint union

```text
b in {4,6,8,10,12,14,16,18,20}.
```

No value is omitted: the classified numbers of reflected `B` masks are

| `b` | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| masks | 10 | 50 | 98 | 140 | 98 | 56 | 25 | 2 | 1 |

and their sum is 480, the complete third-order total.

### Theorem 2 (complete q=1 exclusion)

No candidate in the canonical coupled norm-32 shell with `q=1` satisfies the
exact Gaussian sums and autocorrelation equations. Equivalently, the complete
`q=1` branch is empty.

### Proof

The third-order partition is exhaustive, so it is enough to exclude its nine
rows. The following exact finite theorems do so.

| row | decisive certified obstruction | final graph artifact |
|---:|---|---|
| 20 | exact mod-7 compressed `H` contradiction | source-only at initial audit |
| 18 | exact mod-7 compressed `H` contradiction | `bafkreib6xyklj6sa55p34p2dmvm7rtfy6n4djb5ornc4h5ezkcllgeab4a` |
| 16 | sixth-order `S` leaves two case-1 orbits; seventh-order `S` excludes both | source-only at initial audit |
| 14 | sixth/seventh/eighth-order `S` cascade; empty eighth-order frontier | `bafkreiami2ubtcu42ykule36klgia43pstqbrxmxhzg4lhyprxvwv66kfe` |
| 12 | certified `S` and exact-`H` predecessors; seventh-order `H` excludes the final 77 rows | `bafkreia2kh5dj372rgtnh62t5uu6wae5omht6hqvq45oolt4dsu6ki4h3u` |
| 10 | seventh-order `H` excludes all 198 sixth-order orbit pairs | `bafkreigxubee2r7l2p2z5dtwly74spl24lpeu5hjnboggajz7qw4fnd4pe` |
| 8 | exact integer `H` leaves 40 orbit pairs; exact `S` excludes all | `bafkreiamyiuubl5vlsmf3cx5vrtpcshr5nrgvkzqfpxccnwbmpz4ah2hju` |
| 6 | seventh-order `H` excludes four sixth-order orbit pairs | `bafkreidefwgeq7qmnjh7j47ag5wgajz2qjpjcou2m3oepdf55sky6rem3q` |
| 4 | seventh-order `H` excludes two sixth-order orbit pairs | `bafkreidnptijnfiyjmerw75yqhwpib6evpbicubi3cf6dn3zkk6p7maxye` |

Each obstruction is necessary for an exact lift; an empty necessary-condition
frontier excludes that row. The nine rows are disjoint and exhaustive, which
proves the theorem. `SOURCE_PINS.json` records the immutable source for every
row, including the two source-published rows that lacked final graph nodes at
the initial audit.

## 3. The q=41 branch

When `q=41`, family `B` consists of 21 quarter-turn cells and family `A` has
one opposite cell and 20 quarter-turn cells. Second-order divisibility makes
the axes of the 20 unit `H_A` entries reflect about the exceptional cell. The
complete third-order axis/sign classification proves that exact global sums
allow precisely

```text
wt(H_B axis) in {0,4,8,12,16,20}.
```

Weights 4, 8, 12, and 16 occur in all six sum cases, weight 0 only in cases 2
and 5, and weight 20 only in cases 3 and 4.

### Theorem 3 (complete q=41 exclusion)

No candidate in the canonical coupled norm-32 shell with `q=41` satisfies the
exact Gaussian sums and autocorrelation equations. Equivalently, the complete
`q=41` branch is empty.

### Proof

The all-weight verifier enumerates every cyclic orbit of a length-21 binary
axis word at the six admissible weights:

| weight | labeled words | cyclic orbits | exact `H_B` sign assignments evaluated |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 352,716 |
| 4 | 5,985 | 285 | 41,570,100 |
| 8 | 203,490 | 9,690 | 1,163,962,800 |
| 12 | 293,930 | 14,000 | 1,629,936,000 |
| 16 | 20,349 | 969 | 124,710,300 |
| 20 | 21 | 1 | 184,756 |

The total is 523,776 labeled words, 24,946 cyclic orbits, and
2,960,716,672 exact `H_B` sign assignments. Exact `H` matching leaves
frontiers of 4, 42, 198, 252, 24, and 0 axis-orbit pairs at weights
0, 4, 8, 12, 16, and 20, respectively. The subsequent exact `S` support
intersection checks every admissible global-sum case and leaves zero
axis/case pairs at every weight.

The residue level `pi^12`, where `pi=1+i`, is exact here. Each residual
coordinate has modulus strictly below 64, whereas a nonzero Gaussian integer
divisible by `pi^12` has modulus at least 64. Thus equality modulo `pi^12`
is equality in `Z[i]` for these residuals. The exhaustive weight partition and
empty exact-`S` intersections prove the theorem.

### Weight 12

Weight 12 is the only exceptional orbit manifest. Five cyclic orbits have
size 7 and 13,995 have size 21, so

```text
5*7 + 13,995*21 = 293,930 = C(21,12).
```

The production coordinator and the separately written NumPy verifier both
reconstruct these multiplicities. Exact `H` leaves 252 axis pairs on 116
family-`B` orbits, and the terminal exact-`S` check excludes every associated
case. The independent NumPy route fully rechecks the terminal orbits and all
terminal cases, but it does not independently replay the complete production
enumeration for every nonterminal weight-12 orbit. This asymmetry is an
explicit trust boundary, not a hidden assumption.

The source package's README and one hard-coded summary field say 524,776
labeled words. This is an aggregate typo: the six displayed binomial counts,
the independently generated manifest, and their correct sum are 523,776.
Orbit-key coverage and every exclusion count use the generated 24,946-record
manifest rather than the mistyped aggregate. `ERRATA.md` gives the exact
audit.

## 4. Combined result

### Corollary 4 (extreme-branch closure)

In the established canonical norm-32 residual shell, a quaternary Legendre-
pair lift cannot have total quarter-turn count `q=1` or `q=41`.

This follows immediately from Theorems 2 and 3. It says nothing negative
about the remaining defect-count branches. In particular, it does not turn
the positive fourth-layer `q=5/q=37` witnesses into full QLPs or exclusions.

## 5. Certificate architecture

The decisive computations use exact integer or Gaussian-integer arithmetic.
They avoid floating point, heuristic cutoffs, randomized proof steps, and
time-limited solver statuses. Large enumerations use independently structured
implementations, deterministic orbit identifiers, exact manifest coverage,
canonical stream hashes, and sanitizer builds. Parallel q=41 workers operate
in separate processes; the coordinator rejects missing, duplicate,
unexpected, or wrongly sized orbit records and compares independently sharded
runs after deterministic sorting.

These controls support reproducibility but are not a proof-assistant kernel.
The complete trust ledger appears in `TRUST_BOUNDARIES.md`.

## 6. Prior-art position

Kotsireas and Winterhof introduced quaternary Legendre pairs and their
connection to quaternary and binary Hadamard matrices. Jedwab and Pender gave
the first general constructions at even lengths, but their two families do
not cover length 42. Kotsireas, Koutschan, and Winterhof developed the
even/odd separation and cyclotomic-PSD restrictions and identified 42 as the
smallest unresolved even length in their 2024 preprint, later published in
2025. Djokovic and Kotsireas provide the general compression framework.

The present result is not a construction or a nonexistence theorem for all
QLP-42 candidates. It is a new exact exclusion of two branches inside one
canonical residual shell, relative to the searched primary literature and
committed Discovery Net graph. This is not a claim of historical priority.

## 7. Scope and remaining trust boundaries

The closure relies on:

1. the imported reduction from the length-42 problem to the selected
   canonical norm-32 residual shell and its six sum representatives;
2. the imported coupled 16-state transform and local `H`/`S` sign
   independence statements;
3. the completeness of the `q=1` third-order `b` partition and the `q=41`
   third-order weight partition;
4. the published finite certificates for every row or weight;
5. source inspection, language and fixed-width integer semantics, compilers,
   interpreters, operating system, and hardware.

The coupled-transform verifier checks the local bijection, the identities on
all `4^6` length-six test words, the target derivation, and all six sum cases;
it is still imported rather than formalized in a proof assistant. At weight
12, the short-orbit manifest is independently reconstructed, while complete
nonterminal `H` enumeration is not duplicated wholesale by the NumPy route.

The theorem does not close other residual shells, other values of `q`, or the
full QLP-42 existence problem.

## 8. Structural next step for q=5/q=37

No deeper cell census is proposed. A return to the `q=5/q=37` frontier should
first state a falsifiable family-level lemma, for example an exact identity
linking several `H`/`S` autocorrelation cells, a cyclotomic incompatibility,
or an algebraic invariant constant across an orbit family. Isolated witnesses
and bounded searches are not exclusion progress.
