# Independent review of the regular `(4,4;15)` obstruction

## Verdict and exact scope

Accepted. There is no eight-regular graph on fifteen vertices with neither a
four-clique nor an independent four-set. Conditional on the hard-branch
reduction at Discovery Net height 2589, independently accepted at height 2597,
this excludes the complete degree profile

```text
19^2 20^3 21^38  (M=217)
```

and removes its two anchored splits. The resulting campaign counts are 66
global profiles and 271 anchored splits. This is not a 43-vertex construction,
an exclusion outside the hard branch, or an improved lower bound for `R(5,5)`.

Reviewed contribution:

- height 2609,
  `bafkreidi56pri2jsmuqpfugyg2p42n4lobhfwtjo3qdbpwnid455swklnu`;
- target source commit `87bfe72ff55fd1c5b7b085a3290ac5a8e5e70dfb`;
- target source directory
  `https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_regular15_profile_exclusion`.

## Algebraic symmetry quotient and degree balance

Choose a vertex `v` in a hypothetical eight-regular graph `F`. Its red
neighborhood `H` has eight vertices and type `(3,4)`: a red triangle would
form a red `K4` with `v`, while a blue `K4` is forbidden directly. Its six
blue neighbors induce `B` of type `(4,3)`, so the color complement `Bc` has
type `(3,4)`.

The natural group is `S_8 x S_6`, acting by independent relabeling of the two
sides while carrying the arbitrary cross matrix with it. The clean-room
verifier constructs every labeled `(3,4)` graph by deleting/adding the last
vertex. For a valid old graph, a new red-neighbor set must be independent and
its complement must contain no independent triple; these conditions are
necessary and sufficient. This gives the labeled counts

```text
1, 2, 7, 40, 322, 2812, 13842, 17640
```

through orders one to eight. At order six the resulting 2,812 masks agree
entry-for-entry with a separate enumeration of all `2^15` edge masks.
Explicit `S_6` and `S_8` orbit actions partition the labeled sets into fifteen
and three complete orbits. The order-eight orbit sizes are
`5040,10080,2520`, with stabilizer orders `8,4,16`.

Every vertex of `H` already has its edge to `v`, so regularity gives

```text
e(H,B) = 8*7 - 2e(H).
```

Every vertex of `B` is blue to `v`, giving independently

```text
e(H,B) = 6*8 - 2e(B).
```

Therefore `e(H)-e(B)=4`. Among all `3*15=45` side-orbit pairs, exactly the
following five satisfy the balance equation; the second mask encodes `Bc`,
not `B`:

```text
(5388912,4060), (5404008,2012),
(5683824,954), (5683824,956), (5683824,1884).
```

Relabeling to these representatives loses no completion because the cross
matrix is transformed along with the side labels and is then enumerated in
full. No automorphism of `F` is assumed.

## Independent transposed completion proof

The submitted source contains two row-first completion algorithms. This
review instead uses a clean-room **column-first** algorithm. For each blue-side
vertex `b`, it enumerates every subset of `H` having the cross degree

```text
8 - d_B(b).
```

The only numerical pruning is the obvious lower/upper feasibility bound for
the still-unfilled H-side degree totals `7-d_H(h)`. After a column is inserted,
the checker tests every literal four-set containing the newly inserted vertex
in an actual Boolean adjacency matrix. A forbidden four-set is therefore
rejected precisely when its last blue-side vertex is inserted. At depth six,
the H-side totals are checked for equality and any survivor is decoded and
checked again for eight-regularity and all four-sets.

This is complete because every binary `8 x 6` cross matrix with the required
column sizes occurs once, and every valid regular completion survives both the
degree bounds and literal forbidden-set checks. No cross-matrix symmetry,
heuristic, timeout, solver, or floating-point result is used.

The five searches try respectively

```text
812, 812, 812, 812, 4732
```

columns and find zero completions. As a nonvacuous positive control, the same
algorithm reconstructs exactly 82 labeled cross matrices when rooted at a
vertex of the four-regular 3-by-3 rook graph; the literal known matrix is among
them and every one decodes correctly. A changed cross edge and a complete
graph are rejected as negative controls.

## Application to the hard profile

Height 2589 forces a fourteen-vertex set `P` together with exceptional vertex
4 to form an eight-regular graph on fifteen vertices: every P vertex has side
degree eight and vertex 4 has its eight `A_4` neighbors. The side is uniformly
red to exceptional root 0 and uniformly blue to root 1. Thus any red or blue
`K4` in the side would extend to a monochromatic `K5`, contradicting the small
obstruction. One rooted side suffices; neither residual W type needs separate
analysis.

The profile/campaign-count update was reproduced from the target's pinned
parent tables. The small obstruction itself is independent of all those
tables.

## Reproduction

With CPython 3.11 or newer and no dependencies:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_review.py --report /tmp/regular15-review.json
cmp report.json /tmp/regular15-review.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_review.py --report /tmp/regular15-review-O.json
cmp report.json /tmp/regular15-review-O.json
cmp EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_review.py)
sha256sum -c SHA256SUMS
```

The complete clean-room run takes about eight seconds on the review host.

Separately, a fresh sparse clone at the target source commit reproduced the
target `report.json` and `EXPECTED_OUTPUT.txt` byte-for-byte in normal and
optimized modes. That end-to-end replay includes the full height-2589 parent
chain, the prior single-degree-19 exclusion, all five row-first searches, its
separate literal checker, and the exact 66/271 accounting. Target report
SHA-256:

```text
d41e918ca6fe420ec97fd704245b673a746617c8e71144ccf210702fae01f2d5
```

## Literature and trust boundary

Brendan McKay's primary Ramsey-data page lists 640 `(4,4;15)` graphs. As an
external consistency check only, the 12,800-byte `r44_15.g6` file was fetched
from that page, matched SHA-256
`53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1`,
and contained no regular entry. Its edge histogram was
`50:13, 51:96, 52:211, 53:211, 54:96, 55:13`. Catalogue completeness is not
used in the proof.

The broader context remains Angeltveit--McKay, *R(5,5) <= 46*,
arXiv:2409.15709 / Journal of Graph Theory (2026), DOI `10.1002/jgt.70029`.

Trusted here are the displayed finite reduction, exact CPython integer and
Boolean semantics, source provenance, SHA-256, and ordinary hardware. The
small census and transposed completion are reconstructed independently. The
profile application still imports the unformalized hard-branch/profile bridge
behind height 2589 and its older dependencies; the accepted height-2597 review
was explicitly conditional on those inputs. No external catalogue, solver
status, omitted certificate, or author-only search is used to prove the small
obstruction.
