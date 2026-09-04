# Cyclomatic-three core classification for line-graph signature

## Follow-ups: exact responses and two simultaneous leaves

The companion proof [C3_EQUALITY_RESPONSE.md](C3_EQUALITY_RESPONSE.md)
classifies every diagonal entry of `(Q(H)-2I)^(-1)` on the equality family:
the only values are `1/2` and `3/2`.  It follows that adding one leaf at any
vertex lowers the line-graph signature from two to one.  Two additional exact
checkers reproduce the response theorem.

The rank-two continuation
[C3_TWO_LEAF_STABILITY.md](C3_TWO_LEAF_STABILITY.md) proves that adding two
simultaneous leaves, at possibly equal ports, cannot increase line-graph
signature.  Its proof combines the diagonal-response theorem with a
two-dimensional Schur complement.  Two further exact checkers agree on all
1,096 unordered port pairs in the eight reduced equality bases.

Let `H` be a connected simple graph with minimum degree at least two, and set

```text
c(H) = |E(H)| - |V(H)| + 1.
```

Write `s(X) = n_+(A(X)) - n_-(A(X))` for adjacency signature.  This package
proves the following exact cyclomatic-three slice of the sharp conjecture
`2 s(L(H)) <= c(H)+1`.

## Theorem

If `c(H)=3` and `delta(H)>=2`, then

```text
s(L(H)) <= 2.
```

Equality holds exactly for subdivisions of the following three-cycle-chain
kernel.  In the schematic description below, a loop means a terminal cycle
after subdivision.

```text
  loop at u -- connector -- x == two parallel paths == y -- connector -- loop at v
```

The six kernel-edge path lengths must satisfy:

```text
both terminal-cycle lengths        = 1 (mod 4),
the two central-cycle arc lengths  = 1 and 3 (mod 4), in either order,
both connector lengths             = 1 (mod 2).
```

Every equality graph is nonsingular at the boundary: `2` is not an
eigenvalue of its signless Laplacian `Q(H)`.  In particular, no
minimum-degree-two cyclomatic-three graph can supply the simple-`Q`-eigenvalue
`2` required by the boundary-to-zero-response amplifier criterion.

## Structural reduction

Suppress every maximal path whose internal vertices have degree two.  Since
`c(H)=3` and `H` is not a cycle, this produces a connected looped multigraph
kernel `K` of minimum degree at least three.  If `n=|V(K)|`, then
`|E(K)|=n+2`, and the degree sum gives

```text
3n <= 2(n+2), hence 1 <= n <= 4.
```

Thus every kernel is represented by nonnegative multiplicities on the loops
and unordered vertex pairs for one of four possible orders.  Exact enumeration
up to every vertex permutation gives 15 kernels.  This count independently
agrees with the public `rv09_kernels.py` enumerator in the Paone--Paone version
1.3 reproducibility package.

Replacing any subdivided kernel edge of length `ell` by one of length `ell+4`
preserves line-graph signature and nullity.  This is the four-subdivision
integral-congruence lemma: the new line-graph adjacency matrix is integrally
congruent to the old matrix plus two nonsingular hyperbolic planes.  It is
therefore enough to check path lengths modulo four.

For a loop edge the simple representatives have lengths `3,4,5,6`.  For a
nonloop edge they have lengths `1,2,3,4`; if parallel residue-one paths occur,
only one is direct and every later one is represented by length five.  These
choices preserve simplicity and cover every simple subdivision.  Across the
15 kernels this gives 26,688 labeled residue assignments.  Automorphically
equivalent assignments are intentionally retained.

## Exact spectral calculation

For the unsigned vertex-edge incidence matrix `R` of `H`,

```text
A(L(H)) = R^T R - 2I,       Q(H) = R R^T.
```

Here `|E(H)|-|V(H)|=2`, so the two extra zero eigenvalues of `R^T R` become
two negative eigenvalues after the shift.  Consequently, if `(p,z,n)` is the
inertia of `Q(H)-2I`, then

```text
s(L(H)) = p - n - 2,
nullity(A(L(H))) = z.
```

The primary checker applies exact symmetric congruence over
`fractions.Fraction` to `Q(H)-2I` for every residue assignment.  It finds
maximum signature two, exactly eight labeled equality assignments, and
nullity zero in all eight.  They are precisely the congruence pattern in the
theorem.

The independent replay computes every integer characteristic polynomial by
the Faddeev--LeVerrier recurrence.  Since `Q(H)-2I` is real symmetric, all its
roots are real; Descartes sign variations of `chi(x)` and `(-1)^d chi(-x)`
therefore give the positive and negative root counts exactly.  This second
engine reproduces the full signature/nullity histogram without using the
rational-congruence inertia routine.

The structural reduction and the exact exhaustive replay prove the theorem.
The computation is not presented as evidence for parameters outside
`c(H)=3` or for graphs with pendant trees.

## Reproduction

Python 3.11 or later is sufficient; both programs use only the standard
library.  From this directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_core.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_charpoly.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_responses.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_response_cofactors.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_two_leaves.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_c3_two_leaves_direct.py
shasum -a 256 -c SHA256SUMS
```

The primary run checks 26,688 assignments and ends with:

```text
kernel_count=15 (inside the canonical result)
labeled_residue_assignments=26688
maximum_signature=2
equality_assignments=8
boundary_simple_Q2_cases=0
status=VERIFIED
RESULT_SHA256=f76889e8016a41b0b631d710c880bec798ab6dd3e1b5a6ec2433b8e263ddfa03
```

The independent full replay ends with:

```text
RESULT_SHA256=3c6f3436b318eba058623e80dc014f2fcf6e95f8ea1c32574fc046370d1ca8dd
```

The exact histogram encoded in that result is:

```text
s=-4: z0=44
s=-3: z0=1155, z1=368
s=-2: z0=4392, z1=3368, z2=1278
s=-1: z0=5313, z1=4385, z2=1242, z3=343
s= 0: z0=1726, z1=1764, z2=596, z3=102, z4=44
s= 1: z0=268, z1=160, z2=132
s= 2: z0=8
```

`SHA256SUMS` authenticates the unpacked source files.  No downloaded archive,
raw exploratory search, binary, cache, or generated private state is needed.

## Literature boundary

Paone and Paone formulate the sharp cyclomatic conjecture, enumerate the
`3,15,111` kernels for cyclomatic numbers `2,3,4`, and leave the singular
boundary regime open.  Paone and Paone separately establish the relevant rose
and generalized-theta subclasses.  Paone proves the four-subdivision
congruence and classifies the three-cycle-chain equality family when the two
connecting bridges are unsubdivided.  The theorem here checks all 15
cyclomatic-three kernels and allows arbitrary subdivision of both connectors,
showing that odd connector lengths are exactly the additional equality cases.
Francis and Uptain independently prove that connected line graphs have
unbounded signature, a different phenomenon from this fixed-cyclomatic slice.

Primary sources checked:

- Andrea Paone and Marco Paone, *Line-Graph Signature Beyond the 2-Core*,
  version 1.3, <https://doi.org/10.5281/zenodo.21706797>.
- Andrea Paone and Marco Paone, *Line-graph inertia of roses and generalized
  theta graphs*, <https://doi.org/10.5281/zenodo.21744051>.
- Andrea Paone, *Unbounded signature of line graphs: counterexamples and
  transfer mechanisms*, version 2, <https://doi.org/10.5281/zenodo.21534809>.
- Luke Francis and Trevor Uptain, *The signature of connected line graphs is
  unbounded*, <https://arxiv.org/abs/2607.22874>.
- Saieed Akbari et al., *A new conjecture on the inertia of graphs*,
  <https://arxiv.org/abs/2508.01163>.

## Trust boundary

The kernel suppression, four-subdivision reduction, incidence identity, and
translation from `Q(H)-2I` inertia to line-graph signature are the
human-readable proof.  Completeness of the 15-kernel and 26,688-residue finite
classification is computer-assisted.  Two exact arithmetic methods replay
the spectral conclusion; the independent public kernel enumerator supplies a
third-party check on the kernel count.  Neither program uses floating point or
an external solver.

For provenance, the downloaded Paone--Paone version 1.3 reproducibility ZIP
had SHA-256
`739519f4f18ee84b97c89f1a23dc9512a05dea1687c8aa9a4e1eaff00795213e`.
Its `verification/scripts/rv09_kernels.py` had SHA-256
`2d1a314622b951c7e60213f1398f3a36b43cc3de47b632c58ca2bdfaef967150`
and reported `c=3: 15 kernels (expected 15)` and `RV-09 VERDICT: PASS`.
Those third-party files are cited but are not redistributed here.
