# Quotient-weight Hall and cut compression for transitive tournament blow-ups

## The theorem

Let `Q` be a tournament on vertices `0,...,q-1`, let
`s=(s_0,...,s_(q-1))` be positive integers, and form

```text
D = Q[TT_(s_0),...,TT_(s_(q-1))]
```

by replacing quotient vertex `i` with a transitive tournament `C_i` of order
`s_i` and orienting every cross-cluster edge as in `Q`.

For a quotient vertex `p`, put

```text
O_p = N_Q^+(p),
B_p = N_Q^{++}(p)
    = (union_(j in O_p) N_Q^+(j)) \ (O_p union {p}).
```

For `I` contained in `O_p`, define

```text
Gamma_p(I) = {k in B_p : j -> k in Q for some j in I},
w(A) = sum_(i in A) s_i.
```

Then:

1. The only vertex of `C_p` that can be a strong Seymour vertex of `D` is
   the terminal vertex (the unique sink) of its transitive order.
2. That terminal vertex is strong in `D` if and only if

   ```text
   w(I) <= w(Gamma_p(I))    for every I contained in O_p.       (1)
   ```

Consequently, the strong vertices of `D` are in bijection with the quotient
vertices satisfying (1). In particular, `D` has no strong Seymour vertex if
and only if every quotient vertex `p` has one weighted Hall obstruction

```text
I_p contained in O_p,    w(I_p) > w(Gamma_p(I_p)).              (2)
```

Thus an arbitrarily large transitive blow-up has a certificate involving only
the quotient, its cluster weights, and one quotient subset per failed root.
This is the conceptual replacement for checking a vertex-level matching at
every vertex of every expanded tournament.

There is a further exact quotient-level compression. For `A` contained in
`B_p`, define

```text
F_p(A) = {j in O_p : Gamma_p({j}) is contained in A}.
```

Then the maximum Hall deficiency has the two equal forms

```text
max_(I contained in O_p) [w(I) - w(Gamma_p(I))]
  = max_(A contained in B_p) [w(F_p(A)) - w(A)].               (3)
```

Thus (1) is also equivalent to `w(F_p(A)) <= w(A)` for every right-side cut
`A`. One may use whichever of the `2^|O_p|` left subsets and `2^|B_p|` right
subsets is smaller. Moreover, every deficient `I` can be enlarged to the
closure `F_p(Gamma_p(I))`, which has the same neighbor set and at least the
same deficiency. It is therefore enough to check the neighborhood-closed left
sets, a quotient-dependent family independent of all expanded fiber sizes.

## Proof

Write the vertices of `C_p` in transitive order, so every vertex dominates all
later vertices. For any `x` in `C_p`, direct inspection gives

```text
N_D^+(x)
 = {vertices later than x in C_p} union union_(j in O_p) C_j,

N_D^{++}(x) = union_(k in B_p) C_k.                            (4)
```

Indeed, the transitive cluster contributes no exact internal second neighbor:
every internally reachable vertex is already an out-neighbor. A two-step path
through an out-cluster of `p` reaches precisely the quotient second clusters;
clusters already in `O_p` are removed because exact second neighborhoods omit
first neighbors.

If `x` is not terminal, let `y` be any later vertex of `C_p`. Equation (4)
puts `y` in `N_D^+(x)`. Every `k` in `B_p` is outside `O_p`; because `Q` is a
tournament, `k -> p`, so no vertex of `C_p` dominates any vertex of `C_k`.
Hence `y` is isolated in the directed bipartite graph from `N_D^+(x)` to
`N_D^{++}(x)`. No matching can cover `N_D^+(x)`, proving part 1.

Let `t_p` be the terminal vertex. The same equation becomes

```text
N_D^+(t_p)  = union_(j in O_p) C_j,
N_D^{++}(t_p) = union_(k in B_p) C_k.                          (5)
```

All vertices of a fixed left cluster `C_j` have the same neighbors on the
right: the union of `C_k` over those `k` in `B_p` with `j -> k`. Take an
arbitrary vertex subset `S` of the left side and let `I` be the set of clusters
met by `S`. Then

```text
|S| <= w(I),                  |N(S)| = w(Gamma_p(I)).           (6)
```

If every inequality (1) holds, (6) gives `|S|<=|N(S)|` for every `S`, so
Hall's theorem supplies a complete matching. Conversely, if (1) fails for
some `I`, take `S` to be the union of all `C_j` with `j` in `I`; then both
quantities in (6) are equalities and Hall fails. This proves part 2 and the
certificate characterization (2).

To prove (3), take any `I` and put `A=Gamma_p(I)`. Then `I` is contained in
`F_p(A)`, so the right-cut defect at `A` is at least the left Hall defect at
`I`. Conversely, for any `A`, put `I=F_p(A)`. Its neighbor set is contained
in `A`, so the left Hall defect at `I` is at least the right-cut defect at
`A`. Maximizing gives equality. The same first inclusion shows that
`F_p(Gamma_p(I))` contains `I`; its neighbor set is both contained in and
contains `Gamma_p(I)`, hence is equal to it. This proves the closure assertion
and completes the two-sided compression.

The proof is uniform in `q` and in the positive weights. No enumeration,
minimum-outdegree theorem, or six-vertex classification enters it.

## The six margin-one Dzitsoev certificates

For the quotient in Bai--Li--Park Remark 3.1,

```text
0 -> 1,4,5       sizes (7,3,11,3,9,3)
1 -> 3,4,5
2 -> 0,1,3
3 -> 0,4
4 -> 2,5
5 -> 2,3,
```

choose the following obstruction subsets:

| root `p` | `I_p` | `Gamma_p(I_p)` | `w(I_p)` | `w(Gamma)` |
|---:|---|---|---:|---:|
| 0 | `{1,4,5}` | `{2,3}` | 15 | 14 |
| 1 | `{4,5}` | `{2}` | 12 | 11 |
| 2 | `{0,1,3}` | `{4,5}` | 13 | 12 |
| 3 | `{0}` | `{1,5}` | 7 | 6 |
| 4 | `{2,5}` | `{0,1,3}` | 14 | 13 |
| 5 | `{2}` | `{0,1}` | 11 | 10 |

These are exactly the six strict inequalities displayed in the paper, now
identified as one Hall obstruction for each of the only six candidate strong
vertices. Every obstruction has deficiency one. This proves the no-strong
property of the order-36 tournament with a six-row quotient certificate.

For a general quotient, the criterion checks the smaller of the left and right
subset families at each root, or just its neighborhood-closed source sets; a
no-strong certificate needs only one failed subset per root.
It does not by itself prove that 36 is minimal across all six-vertex quotients:
that separate finite theorem is Discovery Net contribution
`bafkreigrc4pytxtfbmdcuoe647rbmxogxsx4be36a3rx3qvprnavc2odli`.

## Reproduction

The source uses only the Python standard library and was tested with CPython
3.12.12.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
shasum -a 256 -c SHA256SUMS
```

Expected principal outputs:

```text
VERIFIED QUOTIENT-WEIGHT HALL AND CUT COMPRESSION; orders=1..4 weight_max=3 cases=5421 vertex_instances=42846 audit_sha256=bc67742dd888088a1ef40b3af3cc22ee7a333af4eef8731c0b280e2cfc9cac8e
{"audit_sha256": "dcc72b730b0f639771da120f4cd708c6a9d5c45d2c535ba72d5f31f9d432c171", "cases": 1098, "published_defect_margins": [1, 1, 1, 1, 1, 1], "published_strong_clusters": [], "quotient_orders": [1, 2, 3, 4], "status": "INDEPENDENT HALL-CUT DUALITY VERIFIED", "vertex_instances": 6459, "weight_values": [1, 2]}
```

When redirected separately, the complete primary and independent outputs have
SHA-256 values

```text
2f033039ae31a5c220254549c5cdd4e919fd14fc5bf55aeb5ba93ee9673be206
ffc9ed5464dccb3b6365d67964f8876acd013a4ab621894da5ad57194bcb093a
```

The main verifier constructs expanded tournaments and uses an augmenting-path
maximum matching. It compares the direct strong-vertex set with the compressed
criterion and checks the two maximum deficiencies in (3) on all 5,421 labeled
quotient/weight pairs through quotient order four and weights at most three,
covering 42,846 vertex instances. It also checks the expanded order-36
tournament directly and prints the six-row certificate.

The independent checker imports none of the main verifier. It represents
graphs by Python sets, checks strongness through all Hall subsets rather than
a matching algorithm, and compares independently written left-subset and
right-cut maximum-deficiency functions on 1,098 quotient/weight pairs and
6,459 vertices. All six unit tests pass.
These bounded audits test definitions and implementation bridges; the written
proof above establishes the universal theorem.

## Relation to existing work and trust boundary

Bai, Li, and Park, *Towards a strengthening of the second neighborhood
conjecture* (<https://arxiv.org/abs/2607.18047>), define strong Seymour
vertices and give the quotient, six sufficient inequalities, and order-36
construction. They do not state the full iff compression (1)--(2).

Austin Gibbons's unreviewed SSNC source at inspected commit
`cbed58e369cfd868a84010f252671cc3c766c6fd`
(<https://github.com/AustinBGibbons/ssnc>) explicitly uses strongness
factorization across balanced positive/regular tournament substitutions. The
present theorem is an independently derived, nonbalanced transitive-fibre
specialization with arbitrary positive weights, exact second-neighborhood
notation, and the explicit weighted Hall iff criterion needed for the
six-cluster minimum. It should not be read as a claim to have invented the
general substitution-factorization idea.

After this package was first prepared, Discovery Net review
`bafkreiaid3vz6b6hbc63itbfq5y5rdi6khnwnjwgy24kmo2wgtpmemn2va` at height
2079 independently derived the left-side cluster-Hall reduction while
accepting the six-cluster minimum. The distinct addition here is the universal
arbitrary-quotient formulation together with the two-sided maximum-deficiency
identity (3), neighborhood-closure obstruction rule, and its two independent audits.
Committed searches through indexed height 2088 found no prior contribution
stating that cut-duality/closure compression. Apparent graph novelty is
search-relative; no historical-priority claim is made.

The theorem trusts Hall's matching theorem and the displayed elementary
neighborhood decomposition. Reproduction additionally trusts readable CPython
integer/set semantics, SHA-256, the interpreter, operating system, and hardware.
There is no solver, floating point, randomness, external data, generated
input, database, binary, large certificate, or private state.
