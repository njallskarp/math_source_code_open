# Consolidated independent audit of the small-hexadecagon proof candidate

## Result and scope

Let `P` range over planar convex polygons with at most sixteen vertices and
diameter at most one.  The certificate chain in this directory proves that
the unique maximum-perimeter congruence class is the Arb-enclosed
Mulansky--Potschka candidate with half-code

```text
+--+-++-+--+-++-.
```

Uniqueness allows translation, rotation, reflection, central inversion, and
cyclic relabeling.  The perimeter is enclosed by

```text
[3.136547716486607386085967031941228227298136765809232692789218203577745755473817628905857362542821159391634981 +/- 6.62e-109].
```

This is an independent audit of the August 2026 Guo--Luo proof candidate at
commit `a45ff036f9dcd5b297fb4f77a3dea347b8debaac`, not a priority claim for its
underlying proof architecture.  That repository is explicitly
non-peer-reviewed at the time of this audit.

## The strict 32-edge reduction

This section closes the one hypothesis left open by the preceding five
certificates.

Work first in the compact closure of the feasible class, allowing repeated
or collinear labeled vertices.  Translate one labeled point to the origin.
All other points lie in the closed unit disk, the diameter and convex-order
conditions are closed, and planar perimeter is continuous.  Hence a maximum
exists.  The certified candidate is feasible and has perimeter strictly
larger than `p0`, where

```text
p0 = 3.1365477164866073860859670319412282272981367658092326927892182035777457554738176289058573625428211593.
```

A lower-dimensional limit has perimeter at most two, so a maximizer is
two-dimensional.  Delete repeated vertices and merge consecutive collinear
boundary edges; this does not change its convex body or perimeter.  Let `k`
be the resulting number of genuine edges, so `3 <= k <= 16`, and put
`Z=P+(-P)`.

Support functions give all three basic facts without a general-position
assumption:

```text
h_(K+L)=h_K+h_L,
p(K)=integral_0^(2 pi) h_K(u(theta)) dtheta,
p(Z)=2p(P).
```

Moreover, every point of `Z` is a difference of two points of `P`, so
`Z` lies in the closed unit disk.

Let `D` be the `k` oriented edge directions of `P`.  The directions of
`-P` are `D+pi`.  If `r` is the number of unordered antipodal pairs in
`D`, then the two direction sets intersect in exactly `2r` elements.
The cyclic edge merge for a Minkowski sum adds edges of a common direction,
never cancels them, and therefore gives exactly

```text
m = |D union (D+pi)| = 2k-2r
```

genuine edges of `Z`.  Thus `m` is even, `m<=32`, and the only 32-edge case
is `k=16,r=0`.  Every other case has `m<=30`.  This includes zero edges,
repeated vertices, consecutive collinear edges, opposite parallel edge
directions, and polygons with fewer than sixteen genuine vertices; no
perturbation is used.

It remains to exclude `m<=30`.  Here is a short proof of the sharp disk
bound.  If a genuine vertex `q_i` of an `m`-gon in the unit disk has normal
cone of angular width `alpha_i`, integration of its support function over
that cone gives

```text
integral_cone h(u(theta)) dtheta
  = 2 |q_i| sin(alpha_i/2) cos(beta_i-gamma_i)
  <= 2 sin(alpha_i/2),
```

where `beta_i` is the radial angle and `gamma_i` the cone midpoint.  Since
the cone widths sum to `2pi`, Jensen's inequality yields

```text
p(Z) <= 2m sin(pi/m).
```

The function `x sin(pi/x)` is strictly increasing for `x>=2`: its derivative
is `sin(t)-t cos(t)` at `t=pi/x`, and the derivative of the latter expression
is `t sin(t)>0` with value zero at `t=0`.  Consequently, if `m<=30`,

```text
p(P)=p(Z)/2 <= 30 sin(pi/30)
                  < 3.135853898029605
                  < p0.
```

The dependency-free Machin/Taylor checker proves the last comparison with
margin greater than `0.000693818457002`; a separate 512-bit Arb checker
recomputes it.  This contradicts the feasible certified candidate.  Hence
every maximizer has exactly 32 strict difference-body edges.  Necessarily
`k=16,r=0`, so each antipodal pair of difference-body edges contains exactly
one edge contributed by `P`.  Choosing those edges produces the sign code
and closure equation used by the already certified reconstruction theorem.

This argument also resolves compactness and all limit cases: a maximizer in
the compact closure is forced back into the genuine sixteen-vertex,
no-antipodal-edge class before any later strict reconstruction is invoked.

## Dependency and trust table

| Link | Result | Verification route | Remaining trust boundary |
|---|---|---|---|
| Local candidate | Unique KKT zero and strict fixed-code local maximum | 512-bit Arb Krawczyk; interval `LDL^T` | python-flint/Arb implementation |
| Boundary localization | Every candidate-level point lies in the certified gap band and L2 ball | Fraction Machin/Taylor; Arb; SymPy | Jensen and strong-concavity interpretation |
| Fixed-code globality | Unique global maximizer for the displayed code | Fraction bounds; Arb; SymPy derivatives | KKT theorem and two-point argument |
| Reconstruction and saturation | Strict 32-edge competitors reconstruct and all difference-body vertices saturate | Exact incidence cases; Fraction; Arb; SymPy | Minkowski edge merge, openness, and MFCQ/KKT interpretation |
| Competing codes | Exactly 16 normalized formal dihedral survivors | Exact cyclotomic intervals; Arb; SymPy | Taylor remainder and energy-norm interpretation |
| Congruence quotient | The 16 survivors are one geometric congruence class | Free signed module; independent SymPy polynomial identities | Orthogonal-map and cyclic-edge-list interpretation |
| Strict 32-edge reduction | Every unrestricted maximizer enters the preceding strict model | Analytic support-function proof; exact edge counts; Fraction; Arb; SymPy | Standard compactness, Cauchy perimeter formula, and Jensen |

No SAT, optimization, or opaque search solver is used.  Generator/checker
outputs are recorded separately, and `SHA256SUMS` binds the public inputs,
programs, and compact outputs.  The analytic prose is indispensable: the
programs certify finite identities and inequalities, not the semantic
correctness of the convex-geometric interpretation.

## Reproduction record

The terminal strict-edge audit was run on `arm64` macOS with Python
`3.12.12`, python-flint `0.8.0`, and SymPy `1.14.0`.  Starting from a clean
virtual environment, the three independent routes are:

```bash
python -m pip install -r requirements.txt
python verify_strict_edge_exact.py
python verify_strict_edge_arb.py
python verify_strict_edge_identities.py
python -m unittest -v test_strict_edge_reduction.py
shasum -a 256 -c SHA256SUMS
```

The eight strict-edge tests took 20.6 seconds in the recorded run.  The
complete directory suite ran 41 tests in 37.1 seconds (37.7 seconds wall
time), all passing, before publication.

## Primary sources

- Mulansky and Potschka, *A zonogon approach for computing small polygons of
  maximum perimeter*, [DOI](https://doi.org/10.1007/s10107-025-02244-x) and
  [author preprint](https://arxiv.org/abs/2404.01841).
- Guo and Luo, *A computer-assisted proof candidate for Reinhardt's
  maximum-perimeter small hexadecagon*, [public audit source](https://github.com/aster2024/reinhardt-powers-of-two-proof-candidates/blob/a45ff036f9dcd5b297fb4f77a3dea347b8debaac/cases/n16/reinhardt_n16_proof_audit.md).
- Bingane, *Tight bounds on the maximal perimeter of convex equilateral
  small polygons*, [author preprint](https://arxiv.org/abs/2106.11831).
