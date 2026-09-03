# A transition-closed BHR orthant from `(4,7,23)`

## Result

For all integers `p,q,r >= 0`, the multiset

\[
  \{1^{4+p},2^{7+2q},11^{23+11r}\}
\]

has a Hamiltonian-path realization in the cyclically labelled complete graph
of order `35+p+2q+11r`.  This closes the first canonical residual cell after
the preceding transition repairs and, in the pinned symbolic audit, 33 other
previously residual patterns.

This is a transition-certificate strengthening, not a new existence range:
Theorem 1.3(5) of Ağırseven--Ollis already supplies linear realizations here,
because `a>=4` and `a+b>=11>=10`.  The new content is one compact cyclic seed
whose three simultaneous growth modes certify the entire orthant inside the
audited growable-realization framework.

## Explicit seed

The seed at `(a,b,c)=(4,7,23)` is

```text
(23,34,10,12,1,25,27,3,14,13,2,26,24,0,11,22,33,9,20,21,
 19,8,32,31,7,18,16,5,29,30,28,4,15,17,6).
```

It is a permutation of `0,...,34`.  Direct calculation in the cyclic metric
gives exactly four edges of length 1, seven of length 2, and twenty-three of
length 11.  Directly from the definition, it is simultaneously growable at

```text
mode 1:  cut 22
mode 2:  cut 23
mode 11: cut 10.
```

The changed path edges are respectively

```text
1:  (22,33)
2:  (23,34), (22,33)
11: (10,12), (12,1), (3,14), (13,2), (0,11), (9,20),
    (19,8), (7,18), (16,5), (4,15), (17,6)
```

Thus each of the 1, 2, or 11 critical vertices has exactly one required
incidence.  The canonical JSON encoding of the path has SHA-256
`5b42c507459a1633675821b84935894dea9f14a959e70e2d11760172f399227b`.

The bundled checker performs each of these calculations without a solver.

## Why every transition order is valid

The finite-mode safe-margin lemma proved in `TRIMODAL_SAFE_CORES.md` applies.
If every edge of a path in `K_v` has cyclic length at most `D`, the path is
growable in each selected mode, and

\[
  2D+x+y\leq v
\]

for every two distinct selected modes `x,y`, then one gap insertion preserves
all transported selected cuts.  Distinct insertions commute, the maximum edge
length stays at most `D`, and the order only increases.  Induction therefore
allows every nonnegative number of insertions in every selected mode.

Here `D=11`, `v=35`, and the largest pair sum is `11+2=13`, so the tight
margin is

\[
  2\cdot11+11+2=35=v.
\]

Consequently the displayed seed generates a well-defined commuting family.
Each mode-1 insertion adds one edge of length 1, each mode-2 insertion adds
two edges of length 2, and each mode-11 insertion adds eleven edges of length
11, proving the stated multiplicities.

This argument uses the explicit path as the finite certificate; it does not
use the solver's status as evidence and is not an isolated finite search.

## Coverage effect

The pinned source certificate contains 9,544 admissible symbolic patterns.
The previous cap and slab repairs covered 8,071.  Adding this full orthant
covers 34 previously residual patterns, raising coverage to 8,105 and reducing
the residual from 1,473 to 1,439.  The canonical residual-record SHA-256 then
is

```text
217b94f1e96e8774296cac220d6b6c133d4a880ca647151153f5c04e445a8625
```

The new first residual is `(6,5,23)` in residue class `(1,1,1)`.  This audit
measures only coverage by the certified construction regions; it is not an
unrealizability claim about any residual cell.

## Reproduction and trust boundary

With CPython 3.12.12 and no third-party package, run:

```bash
cd bhr_1_2_11_transition_repair
python3 verify_target_orthant.py target_orthant_certificate.json --grid 3
python3 independent_target_check.py target_orthant_certificate.json
python3 -m unittest -v test_target_orthant.py
```

The checker verifies the seed, the exact safe-margin equality, all six orders
of one insertion in each mode, and a three-dimensional regression grid.  The
unbounded conclusion rests on the written finite-mode lemma and induction;
the grid is only regression evidence.  Remaining machine trust is CPython,
exact Python integers, the compact certificate, and the checker implementation.

The optional discovery command is

```bash
python3 find_seed.py --counts 4 7 23 --modes 1 2 11 --seconds 300
```

It uses OR-Tools 9.14.6206, CPython 3.12.12, one worker, and random seed 1.
Two fresh runs returned the stored path and cuts byte-for-byte.  Solver
feasibility and optimality are outside the theorem's trust boundary.

Chand--Ollis leave support `{1,2,11}` as the possible exception in
<https://arxiv.org/abs/2202.07733>.  The relevant existing linear-realization
theorem is Theorem 1.3(5) of <https://arxiv.org/abs/2402.08736>.  Live
support-specific and exact-parameter searches on 2026-09-03 found no prior
version of this simultaneous-growth certificate.  This is search-relative
novelty for the certificate, not a priority or new-existence claim.
