# Twenty-two transition-closed `{1,2,11}` BHR cores

## Result

For each row in the table, write `(A,B,C)` for the safe-seed column.  Then for
every `p,q,r >= 0`, the multiset

\[
  \{1^{A+p},2^{B+2q},11^{C+11r}\}
\]

has a Hamiltonian-path realization in the cyclically labelled complete graph
on `A+B+C+p+2q+11r+1` vertices.

| residue | source cap | safe seed `(A,B,C)` | cuts `1,2,11` | order |
|---|---:|---:|---:|---:|
| `(1,1,1)` | `(1,9,12)` | `(2,11,23)` | `0,2,14` | 37 |
| `(1,1,2)` | `(2,7,13)` | `(3,9,24)` | `1,3,14` | 37 |
| `(1,1,3)` | `(2,7,14)` | `(3,9,25)` | `30,32,10` | 38 |
| `(1,1,4)` | `(2,7,15)` | `(3,9,26)` | `32,34,11` | 39 |
| `(1,1,5)` | `(2,7,16)` | `(3,9,27)` | `30,32,10` | 40 |
| `(1,1,6)` | `(2,7,17)` | `(3,9,28)` | `30,32,10` | 41 |
| `(1,1,7)` | `(2,7,18)` | `(3,9,29)` | `32,34,10` | 42 |
| `(1,1,8)` | `(2,7,19)` | `(3,9,30)` | `31,33,10` | 43 |
| `(1,1,9)` | `(2,11,9)` | `(3,13,20)` | `0,2,13` | 37 |
| `(1,1,10)` | `(1,11,10)` | `(2,13,21)` | `34,1,13` | 37 |
| `(1,1,11)` | `(2,9,11)` | `(3,11,22)` | `30,32,10` | 37 |
| `(1,2,1)` | `(2,8,12)` | `(3,10,23)` | `0,2,14` | 37 |
| `(1,2,2)` | `(1,8,13)` | `(2,10,24)` | `1,3,14` | 37 |
| `(1,2,3)` | `(1,8,14)` | `(2,10,25)` | `31,33,10` | 38 |
| `(1,2,4)` | `(1,8,15)` | `(2,10,26)` | `3,5,16` | 39 |
| `(1,2,5)` | `(1,8,16)` | `(2,10,27)` | `4,6,17` | 40 |
| `(1,2,6)` | `(3,6,17)` | `(4,8,28)` | `30,32,10` | 41 |
| `(1,2,7)` | `(3,6,18)` | `(4,8,29)` | `32,34,10` | 42 |
| `(1,2,8)` | `(3,6,19)` | `(4,8,30)` | `7,9,20` | 43 |
| `(1,2,9)` | `(1,12,9)` | `(2,14,20)` | `33,1,12` | 37 |
| `(1,2,10)` | `(2,10,10)` | `(3,12,21)` | `30,32,10` | 37 |
| `(1,2,11)` | `(1,10,11)` | `(2,12,22)` | `30,32,10` | 37 |

Thus every one of the 22 residue classes used by the pinned finite
`{1,2,11}` certificate has a rigorously transition-closed three-dimensional
core.  This does not yet prove the full BHR conjecture for this support: the
finite-thickness boundary slabs between the original coverage and these safe
cores still need a transition-aware cover.

## From the 22 caps to safe seeds

The source certificate at commit
`8fcd1e624b3d668794e3179787d0965137365286` contains one cap witness for each
residue class.  Each cap is simultaneously growable in modes `1,2,11` but is
too small for the safe-margin theorem below.

For each cap, apply each of the three modes once, transporting every remaining
cut through each order-preserving gap insertion.  There are six possible
orders.  Direct definition-level checking establishes all of the following:

1. every intermediate operation is legal;
2. after every operation, all three transported growth modes remain valid;
3. all six orders end at exactly the same labelled path and cut triple;
4. the endpoint has multiplicities equal to the cap plus `(1,2,11)`.

The endpoint is the safe seed in the table.  All 22 cap paths and all 22
endpoints are embedded in `trimodal_certificate.json`; no conclusion from the
source certificate's coverage predicate is trusted.

For example, the first endpoint has counts `(2,11,23)`, cuts `(0,2,14)`, and
path

```text
(8,19,30,32,21,10,12,23,34,36,25,14,3,1,0,35,24,13,11,
 22,33,31,20,9,7,18,29,27,16,5,6,17,28,26,15,4,2).
```

## Finite-mode safe-margin theorem

Let `P` be a Hamiltonian path in `K_v`, and suppose every path edge has cyclic
length at most `D`.  Let `X` be a finite set of growth modes, each at most
`D`, and assume `P` is `x`-growable at a selected cut `m_x` for every `x` in
`X`.  If

\[
  2D+x+y\leq v
\]

for every distinct `x,y` in `X`, then the gap-refinement operations generated
by `X` preserve all selected growth modes and commute pairwise after the cuts
are transported.  Consequently, for every tuple `(k_x)_(x in X)` of
nonnegative integers, the resulting path is independent of the operation
order and realizes the original multiset with `k_x x` new copies of length
`x` for every `x`.

### Proof

The two-mode safe-margin lemma in `DEAD_ORTHANT_REPAIR.md` says that an
`x`-refinement preserves every distinct `y`-mode at its transported cut and
commutes with the `y`-refinement.  The same-mode subdivision remains
`x`-growable at its original cut.  Every new edge has either an old length or
length `x`, so the maximum edge length remains at most `D`.  The order grows,
so every pairwise margin remains true.  Induction on the number of operations
therefore preserves all modes.  Adjacent transpositions of distinct operations
do not change the path, and adjacent equal operations are indistinguishable;
hence every word with the same mode multiplicities has the same endpoint.  ∎

For the 22 displayed seeds, `D=11`, the least order is 37, and the largest
sum of two distinct modes is `11+2=13`.  Therefore

\[
  2D+13=35<37.
\]

The theorem applies with `X={1,2,11}` and proves every claimed core.

## Exact reproduction

With CPython 3.12.12 and no third-party package, run:

```bash
cd bhr_1_2_11_transition_repair
python3 verify_trimodal.py trimodal_certificate.json --grid 3
python3 -m unittest -v test_trimodal.py
```

The reference output is:

```text
certificate_sha256=532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059
python=3.12.12
cases=22
source_derivation_steps=396
grid=3
family_paths_checked=2750
coordinate_transitions_checked=4224
commuting_squares_checked=4224
record_sha256=6b2d157ae6e7d39197fa878d53ca5cffdb16c0549b46d0472f7f0ae4adcda468
VERIFIED
```

The 396 source-derivation steps are `22 * 6 * 3`: every cap, every operation
order, and every step.  The grid is a regression test of the structural proof,
not the basis for its unbounded quantifiers.  Three negative tests include
tampering with a cap path and a selected safe-seed cut.

## Trust and novelty boundaries

The claim trusts exact Python integers, the compact definition-level checker,
the embedded paths, and the written finite-mode argument.  It does not require
OR-Tools or trust the source certificate's completeness claim.  The imported
source bytes are identified by SHA-256
`e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c`;
they are used only to identify and reproduce the 22 starting cap witnesses.

The primary literature is Ollis, Pasotti, Pellegrini, and Schmitt,
*Growable Realizations: a Powerful Approach to the Buratti-Horak-Rosa
Conjecture* (<https://arxiv.org/abs/2105.00980>) and Chand and Ollis, *The
Buratti-Horak-Rosa Conjecture Holds for Some Underlying Sets of Size Three*
(<https://arxiv.org/abs/2202.07733>).  Live primary-source and exact-phrase
searches on 2026-09-03 found no prior transition-closed tri-modal cores for
this support.  This is a search-relative novelty statement, not a priority
claim.
