# Every 399-coclique in the missing Moore graph extends uniquely

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

## Reproduction

Requires CPython 3.11 or later and only the standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify.py)
shasum -a 256 -c SHA256SUMS
```

The checker uses exact Python integers and `Fraction`.  It verifies every
displayed arithmetic identity, the strict spectral thresholds, and by a
definition-level dynamic program independently confirms that the forced
nonpositive defect moments have exactly one support profile once the spectral
lower bound `58` is imposed.

Expected-output SHA-256:
`97970ec2d49de541797e664372be84a51d533f334b69fa5c4a9d3af42c574500`.

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

## Trust boundary

The proof uses only the strongly regular parameters `(3250,57,0,1)`, exact
integer counting, Rayleigh's variational inequality, and the row-sum bound for
nonnegative matrices.  Reproduction trusts the readable checker, CPython's
arbitrary-precision integer and rational semantics, SHA-256, the interpreter,
OS, and hardware.  It uses no floating point, randomness, solver, external
dataset, graph catalogue, generated certificate, binary, or private state.
