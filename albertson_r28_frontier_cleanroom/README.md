# Clean-room exact frontier for Albertson at r = 28

This directory gives an exact, independently reproducible reduction of the
next Albertson case.  It does **not** prove Albertson's conjecture for
chromatic number 28.  Its main result is the following finite frontier and a
quantified obstruction to continuing by degree-profile enumeration.

## Proposition

Let `G` be a 28-critical counterexample to Albertson's conjecture, and write
`n=|V(G)|`, `m=|E(G)|`.  Then all of the following hold.

1. `n=55` and `m` is either 768 or 769.
2. The universal convex deletion recurrence proved below gives
   `cr(G)>=7060` on row `(55,768)` and `cr(G)>=7092` on row `(55,769)`.
   It gives 7123 at `(55,770)`, hence closes every larger edge row.
3. The complement `H=bar(G)` is connected and factor-critical.  Put
   `x_v=d_G(v)-27`.  If `m=768`, then `sum_v x_v=51` and at least four
   vertices have degree 27.  If `m=769`, then `sum_v x_v=53` and at least two
   vertices have degree 27.
4. For every degree-27 vertex `v`, `H-v` has a perfect matching all of whose
   edges cross the equal bipartition `(N_H(v),N_G(v))`.  In particular, the
   bipartite graph `H[N_H(v),N_G(v)]` has a perfect matching and satisfies all
   corresponding Hall inequalities.
5. For an unordered pair `uv`, set
   `h_uv=1[uv in E(H)]`, `D_uv=x_u+x_v+h_uv`, and `S2=sum_v x_v^2`.  Then

       |E(G-{u,v})| = m-53-D_uv.

   Over all 1485 unordered pairs,

       m=768: sum D_uv=3471,  sum D_uv^2=51*S2+6072;
       m=769: sum D_uv=3578,  sum D_uv^2=51*S2+6387.

The threshold used here is

    Z(28)=floor(28/2)floor(27/2)floor(26/2)floor(25/2)/4=7098.

A counterexample has `cr(G)<cr(K_28)<=Z(28)`, hence `cr(G)<=7097`.

## Exact frontier proof

A counterexample contains no subdivision of `K_28`.  Published critical-graph
results exclude `n<=32` and `n>=3.57*28`, so only the 67 integer orders
`33<=n<=99` need arithmetic inspection.  At each order the exact integral
edge floor is the ceiling of half the maximum of

    Gallai:            27n+(n-28)(56-n)-2       (30<=n<=54),
    Kostochka-Yancey:  (29*26*n-28*25)/27,
    Barat-Toth:        27n+50.

For crossing bounds, start with the following universal affine inequalities
for a graph of order `s` and size `q`:

    0,
    q-3(s-2),
    (7q-25(s-2))/3,
    (37q-155(s-2))/9,
    5q-203(s-2)/9.

At each induced order, first take the integer ceilings of all five lines and
then their greatest convex minorant.  That integer-aware minorant is sampled
over every order `4<=s<=n`.  (Rounding locally can be strictly stronger than
sampling an unrounded rational line.)  The resulting single-stage bounds are
evaluated in exact rational arithmetic.  The complete 67-row provenance table
is `FRONTIER_CERTIFICATE.tsv`; it records the active critical-edge theorem,
the affine supports at both hull endpoints, active sample order and hull
segment, exact rational value, and ceiling.  Only three rows survive this first
dispatch:

    (n,m,ceiling) = (54,754,6912), (55,768,6988), (56,781,7048).

Gallai makes `bar(G)` disconnected at order 54.  The disconnected-complement
edge estimate

    m >= min((n-1)+ceil(26(n-1)/2)+24, 28^2+3*28-19)

raises its floor to 766; direct sampling then gives 7291 and closes that
order.  The same estimate would give `m>=780` at order 55, where direct
sampling gives 7374, so every surviving order-55 complement is connected.

It remains to state the recursively strengthened bound.  Let `F_n(q)` first
be the ceiling of the maximum of the five universal affine bounds.  Let
`C_n` be the greatest convex minorant of the integer points `(q,F_n(q))`.
For every `4<=s<n`, update

    F_n(q) >= ceil[ C(n,s)/C(n-4,s-4)
                    * C_s(q*s*(s-1)/(n*(n-1))) ].                 (R)

This is valid because each crossing occurs in exactly `C(n-4,s-4)` induced
`s`-vertex drawings, the mean induced size is
`q*s*(s-1)/(n*(n-1))`, and Jensen's inequality applies to the convex
minorant.  Computing (R) in increasing order of `n` closes `(56,781)` at
7115.  At order 55 it yields

    F_55(768)=7060,  F_55(769)=7092,  F_55(770)=7123,

and every larger edge count is also closed.  The rounded active witnesses are

    (55,768): samples 52, 53, 54;
    (55,769): sample 54;
    (55,770): samples 52, 53, 54;
    (56,781): samples 53, 54, 55.

`verify.py` prints their exact hull endpoints, sample means, multipliers, and
unrounded fractions.  Recursively tracing every tied active endpoint from
these four roots produces a 471-node proof DAG with canonical digest

    4cff710c62feffb1e9f531f2536659cd069f6eb0ae0ea9832a4af451195920fb.

This establishes items 1 and 2 without using any terminal result at r = 27.

## Complement and pair consequences

Since `G` is critical, `d_G(v)>=27`.  Connectedness of `H` also excludes a
universal vertex of `G`, so `0<=x_v<=26`.  The identities

    sum_v x_v = 2m-55*27

give 51 and 53, and counting positive excesses gives the asserted numbers of
degree-27 vertices.

Stehlik's theorem says that for every vertex `v` of a critical graph with
connected complement, `G-v` has a 27-colouring whose colour classes all have
size at least two.  Here 54 vertices force 27 pairs, which are the edges of a
perfect matching of `H-v`; hence `H` is factor-critical.  If `d_G(v)=27` and
one matching edge lay wholly in `N_H(v)`, its two endpoints and `v` would be
an independent triple, producing a 27-colouring of `G`.  Thus the matching
crosses from `N_H(v)` to `N_G(v)`, whose sides both have size 27.

For the pair identities, deletion gives

    |E(G-{u,v})| = m-d_G(u)-d_G(v)+1[uv in E(G)] = m-53-D_uv.

Also `|E(H)|=1485-m` and

    sum_{uv in E(H)}(x_u+x_v) = sum_v x_v(27-x_v)=27*sum_v x_v-S2.

Expanding the first two moments of `D_uv` yields the formulas in item 5.

## Exact compression barrier and missing inequality

Deleting one vertex from an optimal drawing counts each crossing 51 times,
so every hypothetical counterexample must satisfy

    sum_v F_54(m-27-x_v) <= 51*7097.                         (D)

The verifier enumerates only relaxed excess histograms: 55 entries in
`{0,...,26}` with the required total excess.  It does **not** assert that a
histogram is realised by a critical graph or by a factor-critical complement.
Even this weak compression leaves

    m=768: 232605 profiles; minimum RHS 360044 at 0^4,1^51;
    m=769: 318199 profiles; minimum RHS 361659 at
           0^28,1^1,2^26 and 0^29,2^25,3^1.

Thus the predeclared 100-profile stop threshold is exceeded.  Raw
degree-profile enumeration should not be extended.

The failure is quantitatively sharp for mechanism (D).  Eliminating row 769
needs RHS at least `51*7097+1=361948`, a gap of 289.  A uniform improvement of
6 in the order-54 values on the queried band `716<=q<=742` suffices; 5 does
not.  Improving the row-768 lower bound by ten, from 7060 to 7070, needs RHS
360520, a gap of 476.  A uniform improvement of 9 on `715<=q<=741` suffices;
8 does not.  These are missing-inequality certificates, not claims that such
improvements are presently known.

## Reproduction

Requires CPython 3.12 or later and only the Python standard library.

```sh
cd albertson_r28_frontier_cleanroom
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 frontier_certificate.py | diff -u FRONTIER_CERTIFICATE.tsv -
shasum -a 256 -c SHA256SUMS
```

The main verifier takes about 22 seconds on an ordinary laptop.  No solver,
floating-point arithmetic, random choice, downloaded data, or precomputed
r=27 table enters the result.

## Trust boundary

The scripts verify exact transcription arithmetic, convex-minorant recursion,
the 67-row dispatch, active supports, profile counts, minima, and sensitivity
gaps.  They do not verify the cited graph-theoretic and crossing-number
theorems, the prose proofs above, or realisability of relaxed profiles.  The
only nontrivial computational primitives are Python integers,
`fractions.Fraction`, binomial coefficients, deterministic recursion, and
SHA-256.

## Conditional appendix

There are no conditional claims in this contribution.  In particular,
`cr(24,132)>=165` is not used, and no r=27 terminal theorem or r=27 case tree
is imported.

## Literature and novelty boundary

Primary sources checked on 2026-09-04:

- Aaron Buengener and Michael Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://arxiv.org/abs/2409.01733), Theorem 6.
- Janos Pach, Rados Radoicic, Gabor Tardos, and Geza Toth, [*Improving the
  Crossing Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9).
- Janos Barat and Geza Toth, [*Towards the Albertson
  Conjecture*](https://doi.org/10.37236/345).
- Alexandr Kostochka and Matthew Yancey, [*Ore's Conjecture on Color-Critical
  Graphs Is Almost True*](https://doi.org/10.1016/j.jctb.2014.05.002).
- Matej Stehlik, [*Critical Graphs with Connected
  Complements*](https://doi.org/10.1016/S0095-8956(03)00069-8).
- Ankan Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682), for a recent exact collation of the
  published bounds and a self-contained disconnected-complement estimate.

Live exact-phrase and arXiv searches found no public r=28 reduction to the two
rows above.  That is a search report, not a claim of exhaustive priority.

An independently authored [Lean sampling-mechanism
audit](https://github.com/njallskarp/math_source_code_open/tree/main/researcher4_albertson_sampling_mechanism_lean)
already verifies the abstract support-counting bridge and the direct r=28
diagnostics 6988 and 7048.  The present code is clean-room Python and agrees on
those two diagnostics; its non-overlapping contribution is the full 67-row
support certificate, recursive closure to two rows, exact 7060/7092 values,
complement/pair consequences, and quantified compression barrier.
