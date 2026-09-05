# Near-Hoffman coclique rigidity in the missing Moore graph

Assume that a Moore graph of degree `57` and diameter `2` exists.  This
directory proves the following conditional structural theorem.

> Every independent set of size `399` is contained in a unique independent
> set of size `400`.

Consequently the independence number of the hypothetical graph cannot be
`399`: it is either at most `398` or is exactly `400`.

The proof is in [THEOREM.md](THEOREM.md).  Its mechanism is an exact
near-Hoffman defect identity followed twice by the elementary spectral Moore
bound

```text
rho(F)^2 <= |V(F)| - 1
```

for every graph `F` of girth at least five.

If `S` is a 399-coclique and `a_x=|N(x) intersect S|` for `x` outside `S`, put
`z_x=a_x-8`.  Exact pair counting and the Moore common-neighbour property give

```text
sum z_x = -65,
sum z_x^2 = 121,
sum z_x(z_x+1) = 56,
A_H z = 7z - 1.
```

The positive support of `z`, if nonempty, would have at most `28` vertices
but spectral radius at least `6`, contradicting the spectral Moore bound.
Writing `w=-z`, the nonzero support then has spectral radius at least
`912/121`; the same bound forces at least `58` vertices.  The two exact moments
now force the unique profile

```text
a_x = 0^1, 7^57, 8^2793.
```

The unique vertex with `a_x=0` is the unique extension point.

## Deficit two

[DEFICIT_TWO.md](DEFICIT_TWO.md) gives the next structural boundary.  For a
398-coclique, if every outside vertex has at most eight neighbours in the
coclique, then its profile is forced to be

```text
0^2, 6^1, 7^112, 8^2737
```

and it has a unique 400-coclique extension.  Therefore every nonextendible
398-coclique must have positive defect support

```text
P = {x : |N(x) intersect S| > 8}
```

with `27<=|P|<=57`, spectral radius at least `5`, and maximum positive defect
`max_P(|N(x) intersect S|-8)` in `{1,2,5}`.  This is a clean obstruction, but
not an exclusion: the positive-support radius-two inequalities retain a
weighted-star branch, so the coclique lane is frozen pending a new incidence
or design mechanism.

## Reproduction

Requires CPython 3.11 or later and only the standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify.py)
PYTHONDONTWRITEBYTECODE=1 python3 verify_deficit_two.py
diff -u EXPECTED_DEFICIT_TWO.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_deficit_two.py)
shasum -a 256 -c SHA256SUMS
```

The checker uses exact Python integers and `Fraction`.  It verifies every
displayed arithmetic identity, the strict spectral thresholds, and by a
definition-level dynamic program independently confirms that the forced
nonpositive defect moments have exactly one support profile once the spectral
lower bound `58` is imposed.

Expected-output SHA-256:
`97970ec2d49de541797e664372be84a51d533f334b69fa5c4a9d3af42c574500`.
The deficit-two expected-output digest is recorded in `SHA256SUMS`.
It is `dbe17e68a102c5e063311975f4c24e5a1e70e6670196ff15935c676cee6a6754`.

The finite computation audits arithmetic only.  The universal theorem rests
on the written counting and spectral proof.

## Literature status

- V. Faber and J. Keegan, *Existence of a Moore graph of degree 57 is still
  open*, [arXiv:2210.09577](https://arxiv.org/abs/2210.09577), correct a failed
  nonexistence claim and confirm that the existence problem remains open.
- C. Dalfó, *A survey on the missing Moore graph*, Linear Algebra Appl. 569
  (2019), 1--14,
  [doi:10.1016/j.laa.2018.12.035](https://doi.org/10.1016/j.laa.2018.12.035),
  records the Hoffman bound `alpha<=400` and the known spectrum of the graph
  induced outside an arbitrary coclique.
- M. A. Fiol and E. Garriga, *On outindependent subgraphs of strongly regular
  graphs*, Linear and Multilinear Algebra 54 (2006), 123--140,
  [doi:10.1080/03081080500143902](https://doi.org/10.1080/03081080500143902),
  gives that outindependent spectrum; the present proof instead exploits
  integer defect energy and a small-support spectral contradiction.
- Y. Ishida, *No involutions in the missing Moore graph*,
  [arXiv:2606.29183](https://arxiv.org/abs/2606.29183), gives the current 2026
  open status and recent conditional restrictions.

Targeted primary-source and exact-phrase searches on 2026-09-04 found the
general outindependent spectrum but no statement that every 399-coclique
extends, no exclusion of independence number `399`, and no defect-support
argument above.  Novelty is search-relative, not a historical-priority claim.
The deficit-two audit additionally checked P. Renteln, *Some constraints on
the missing Moore graph*, Australas. J. Combin. 77 (2020), 373--382; its full
text contains no independent-set or coclique theorem.

## Trust boundary

The proof uses only the strongly regular parameters `(3250,57,0,1)`, exact
integer counting, Rayleigh's variational inequality, and the row-sum bound for
nonnegative matrices.  Reproduction trusts the readable checker, CPython's
arbitrary-precision integer and rational semantics, SHA-256, the interpreter,
OS, and hardware.  It uses no floating point, randomness, solver, external
dataset, graph catalogue, generated certificate, binary, or private state.
