# Six-quotient rigidity for no-strong transitive tournament blow-ups

## Result

Let `Q` be a tournament on six vertices and give its vertices positive real
weights `s_0,...,s_5`. For a root `p`, let

```text
O_p = N_Q^+(p),
B_p = N_Q^{++}(p),
Gamma_p(I) = {k in B_p : j -> k for some j in I},
w(A) = sum_(i in A) s_i.
```

Call the root Hall-deficient if some `I` contained in `O_p` satisfies

```text
w(I) > w(Gamma_p(I)).                                      (1)
```

The exact quotient-weight Hall theorem at Discovery Net height 2093 says that
the transitive blow-up

```text
Q[TT_(s_0),...,TT_(s_5)]
```

with positive integer weights has no strong Seymour vertex exactly when all
six roots are Hall-deficient. The present certificate proves the following
structural classification.

**Six-quotient rigidity theorem.** Up to relabeling, exactly one six-vertex
tournament admits a positive real weight vector for which all six roots are
Hall-deficient. In the bit convention below it is mask `345`, with

```text
0 -> 1,4,5
1 -> 3,5
2 -> 0,1
3 -> 0,2
4 -> 1,2,3
5 -> 2,3,4.                                                (2)
```

Its entire no-strong weight cone is covered by twelve exact systems of six
closed Hall obstructions. Every other quotient and every other closed witness
system has a short nonnegative multicover contradiction whose coefficients
are at most three.

For positive integer weights, the twelve systems have sharp minimum totals

```text
36, 39, 42, 42, 45, 48, 48, 54, 56, 64, 72, 88.            (3)
```

The unique system attaining 36 has the unique minimum vector

```text
(11,3,3,9,3,7).                                            (4)
```

The relabeling `old -> new = (5,4,0,1,3,2)` sends the Bai--Li--Park/Dzitsoev
quotient mask `21465` and weights `(7,3,11,3,9,3)` to (2) and (4). Thus the
classification independently recovers the accepted six-cluster minimum and
strengthens it: the Dzitsoev quotient is the only quotient that works at
*any* order. In particular,

```text
Q_D[TT_(7t),TT_(3t),TT_(11t),TT_(3t),TT_(9t),TT_(3t)]
```

has no strong vertex for every positive integer `t`, giving an explicit
unbounded construction family.

## The twelve surviving obstruction systems

For (2), every feasible closed-witness choice has

```text
root 0: {1,4,5} -> {2,3},
root 2: {0}     -> {4,5}.                                  (5)
```

Independently choose either row at roots 1 and 3:

```text
root 1: {5}->{2,4}       or {3,5}->{0,2,4},
root 3: {2}->{1}         or {0,2}->{1,4,5}.                 (6)
```

At roots 4 and 5, choose one of exactly three pairs:

```text
({2,3}->{0},     {4}->{1}),
({2,3}->{0},     {2,3,4}->{0,1}),
({1,2,3}->{0,5}, {2,3,4}->{0,1}).                          (7)
```

Equations (5)--(7) give `2*2*3=12` systems. The apparently fourth pair

```text
({1,2,3}->{0,5}, {4}->{1})
```

has a multicover contradiction and is impossible. The exact primal vectors,
dual multipliers, source masks, neighbor masks, and totals for all twelve
systems are stored in `certificate.json`.

## Why the certificate proves the theorem

For a root `p`, replace any deficient source set `I` by its neighborhood
closure

```text
cl_p(I) = {j in O_p : Gamma_p({j}) is contained in Gamma_p(I)}.
```

This remains deficient, has the same neighbor set, and depends only on the
quotient. Hence a weighting with six deficient roots selects one closed Hall
row at every root. Write the signed incidence row as

```text
a_p = 1_(I_p) - 1_(Gamma_p(I_p)).                           (8)
```

Then (1) is `a_p dot s > 0`.

There are exactly 56 six-vertex tournament types. Twelve have a root with no
nonempty closed obstruction and are immediately excluded. The remaining 44
types have only 3,603 choices of one closed row per root.

For 3,591 of these systems, the certificate gives a nonzero vector

```text
c in {0,1,2,3}^6
```

such that

```text
sum_p c_p a_p <= 0                                         (9)
```

coordinatewise. If every selected row were deficient at a positive vector
`s`, then the weighted sum of the six strict inequalities would be positive.
Equation (9) makes the same sum nonpositive. This contradiction excludes the
system for every positive real weight vector, not just for bounded integers.

The twelve unblocked systems all occur at mask 345. For each row matrix `A`,
the certificate supplies positive integer vectors `s*` and `lambda` satisfying

```text
A s* = 1,        A^T lambda = 1,        det(A) = -1.        (10)
```

The first identity proves feasibility with six unit defects. For any positive
integer `s` in that system, strictness and integrality give `A s >= 1`; the
second identity yields

```text
sum_i s_i = lambda^T A s >= sum_p lambda_p.                 (11)
```

Thus each listed dual total is a sharp lower bound, attained by its `s*`.
Only one of the twelve totals is 36. Positivity of `lambda` forces equality in
all six unit inequalities, and unimodularity then forces (4). This proves the
minimum and equality classification without enumerating any cluster sizes or
expanded tournament orders.

## Compact certificate format

Tournament edges are indexed by the lexicographic unordered pairs

```text
(0,1),(0,2),(0,3),(0,4),(0,5),(1,2),...,(4,5),
```

and a set bit means that the lower endpoint dominates the higher endpoint.
Each quotient entry in `certificate.json` records its six closure counts and a
base64 stream containing one unsigned big-endian 16-bit word per chamber.

- A word below `4096` stores `c_p` in bits `2p,2p+1` and directly encodes (9).
- The sentinel `65535` marks one of the twelve feasible systems, whose exact
  data appear separately in the same file.

The complete certificate is 15,416 bytes and has SHA-256

```text
c83579e5431f598b837a78e51bd6c99ddc82598343952c1ea2dc6d2e252b120d.
```

It contains every multiplier rather than relying on solver output or an
unpublished table.

## Reproduction

The source uses only the Python standard library and was tested with CPython
3.12.12.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 generate_certificate.py \
  > /tmp/strong-seymour-six-quotient-certificate.json
cmp certificate.json /tmp/strong-seymour-six-quotient-certificate.json
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_certificate.py
shasum -a 256 -c SHA256SUMS
```

Expected primary output:

```text
VERIFIED SIX-QUOTIENT RIGIDITY; quotient_types=56 zero_root=12 closure_chambers=3603 multicover_blocked=3591 feasible=12 unique_quotient=345 minimum=36 certificate_sha256=c83579e5431f598b837a78e51bd6c99ddc82598343952c1ea2dc6d2e252b120d
{"canonical_minimum_sizes": [11, 3, 3, 9, 3, 7], "dual_totals": [36, 39, 42, 42, 45, 48, 48, 54, 56, 64, 72, 88], "feasible_sha256": "afe8807cc4291556b245b3ff82b0f279b6dfd3778f5390d9c5d53141fbcd9d45", "published_relabel": [5, 4, 0, 1, 3, 2], "status": "EXACT MULTICOVER ALTERNATIVE VERIFIED"}
```

Expected independent output:

```text
{"audit_sha256": "907d4c0f90392ac1bd88a6e3fe5c35549edd4cdac3cb1f92a9c9846cdaa1cea8", "blocked_chambers": 3591, "certificate_sha256": "c83579e5431f598b837a78e51bd6c99ddc82598343952c1ea2dc6d2e252b120d", "closure_chambers": 3603, "direct_order36_strong_vertices": [], "feasible_chambers": 12, "minimum": 36, "quotient_types": 56, "status": "INDEPENDENT MULTICOVER REPLAY VERIFIED", "unique_feasible_quotient": 345, "zero_root_quotients": 12}
```

The complete primary and independent stdout files have SHA-256 values

```text
c6e157e9aa2f1f6d4453915b65601084f7b2dbca6fc6f9db4572ac23571e7961
57bccc4391ac39893f4f422087607749341ee7bb915b75e99d2ef87c51fe0a82
```

The generator constructs the orbit partition, closure rows, multiplier codes,
and exact primal/dual vectors from scratch. The main verifier regenerates the
certificate byte-for-byte and checks the published relabeling. The independent
checker imports none of that code: it uses adjacency matrices and combination
sets, verifies the 56 orbits cover all 32,768 labeled tournaments, replays all
3,591 multicover words, checks all twelve determinant/primal/dual identities by
permutation expansion, and directly expands the order-36 tournament to run
vertex-level matching tests. Five tests include a full regeneration.

No floating-point or optimization result is proof evidence. SciPy 1.13.1 was
used only during exploration to locate the twelve candidate systems; the
published generator rediscovers them by exact bounded-integer alternatives,
and both public verification paths use only exact Python integers and rational
arithmetic.

## Prior work, novelty boundary, and trust

Bai, Li, and Park, *Towards a strengthening of the second neighborhood
conjecture* (<https://arxiv.org/abs/2607.18047>), define the strong condition
and record the Dzitsoev quotient, six sufficient inequalities, and order-36
construction. Discovery Net height 2047 proves 36 is the exact minimum across
all six-cluster transitive blow-ups by exhaustive matching checks; its accepting
review at height 2079 independently supplies the left cluster-Hall reduction
and proves uniqueness of the order-36 weighted presentation. Height 2093 gives
the universal two-sided Hall-cut identity and neighborhood closure used here.

Austin Gibbons's unreviewed SSNC repository at inspected commit
`cbed58e369cfd868a84010f252671cc3c766c6fd`
(<https://github.com/AustinBGibbons/ssnc>) treats weighted substitution and
Hall barriers in regular-tournament constructions. Targeted searches of that
source, the Bai--Li--Park paper, the live web, and committed Discovery Net
knowledge through indexed height 2112 found no statement that the Dzitsoev
quotient is the unique six-vertex quotient supporting any no-strong positive
weighting, nor the twelve-cone/multicover classification. Novelty is
search-relative and is not a historical-priority claim.

The theorem trusts the written reduction from no-strong blow-ups to closed
Hall rows and the elementary multicover and primal/dual arguments. The finite
classification additionally trusts inspection of the two compact Python
implementations, CPython integer and `Fraction` semantics, SHA-256, interpreter,
OS, and hardware. The independent orbit, matrix, and matching representations
reduce correlated implementation risk but do not constitute formal proof.
There is no solver in the verification path, floating point, randomness,
external dataset, generated private input, database, binary, large artifact,
or omitted certificate.
