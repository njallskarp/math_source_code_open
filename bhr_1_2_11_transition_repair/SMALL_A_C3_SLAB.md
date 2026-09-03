# A transition-closed small-`a`, `c=3 mod 11` BHR slab

## Result

For every pair of integers `q,r>=0`, the multiset

\[
  \{1,2^{9+2q},11^{25+11r}\}
\]

has a Hamiltonian-path realization in the cyclically labelled complete graph
on `36+2q+11r` vertices.  This is a genuinely small-`a` existence range: the
published Ağırseven--Ollis theorem for `\{1^a,2^b,y^c\}` requires `a>=3`.

## Derivation of the safe seed

The pinned Chand--Ollis finite certificate contains the path

```text
g = (4,15,17,6,8,19,21,10,11,22,20,9,7,18,16,5,3,14,2,13,1,12,0).
```

It realizes `(a,b,c)=(1,7,14)`, is 2-growable at cut 2, and is
11-growable at cut 11.  Its order 23 is too small for the safe-margin
theorem, so no general cross-preservation claim is used.  Instead, both
one-step orders are checked directly:

```text
G_(11,13)(G_(2,2)(g)) = G_(2,2)(G_(11,11)(g)) = p,
```

where transported cuts are shown and

```text
p = (6,17,28,30,19,8,10,21,32,34,23,12,13,24,35,33,22,11,
     9,20,31,29,18,7,5,16,27,2,4,15,26,1,3,14,25,0).
```

Thus `p` realizes `(1,9,25)`.  No solver is involved in this derivation.

## Exact growth incidences

For 2-growth at cut 2, the only changed oriented edges of `p` are

```text
(2,4), (1,3).
```

For 11-growth at cut 13, they are

```text
(6,17), (19,8), (10,21), (23,12), (13,24), (22,11),
(9,20), (18,7), (5,16), (4,15), (3,14).
```

The first list covers the critical vertices `{1,2}` once each.  The second
list covers `{3,...,13}` once each.  Hence `p` is simultaneously growable in
modes 2 and 11 at the displayed cuts.

Every edge of `p` has cyclic length at most `D=11`, and

\[
  2D+2+11=35\leq36=|V(p)|.
\]

The finite-mode safe-margin theorem in
[`TRIMODAL_SAFE_CORES.md`](TRIMODAL_SAFE_CORES.md) therefore preserves the
transported cuts and makes the two refinements commute forever.  Repeating
2-growth `q` times and 11-growth `r` times proves the stated slab.

The source path belongs to residue class `(1,1,3)`, witness 1, in the pinned
certificate.  That provenance is not a trust dependency: `g`, `p`, both
one-step orders, their length counts, and every growth incidence are copied
into or reconstructed from the compact new certificate and checked directly.

## Conservative audit effect

This slab covers all 12 residual symbolic representatives with `a=1` in the
largest previous residue class `(1,1,3)`: six odd-`b` representatives starting
at 9, each at the finite and high `c=25 mod 11` representatives.  Cumulative
transition-aware coverage rises from 8,139 to 8,151 of 9,544 and the residual
falls from 1,405 to 1,393.  These are construction-coverage statements, not
nonexistence statements about the remaining records.  The new residual-record
SHA-256 is
`3d0e81150a2e5147b0b47e3a8ffdc3bb10085a54430e7562fac84bcace348e1a`.

## Reproduction

Only CPython's standard library is needed:

```bash
cd bhr_1_2_11_transition_repair
python3 verify_small_a_c3_slab.py small_a_c3_slab_certificate.json --grid 6
python3 independent_small_a_c3_check.py small_a_c3_slab_certificate.json --grid 6
python3 -m unittest -v test_small_a_c3_slab.py
```

Both checkers return certificate SHA-256
`1e2af60896b1f3e5970c877cb630fe8d4171eb0b1e5335d063689767b9187e1f`
and transition-record SHA-256
`c055f79fe35cb909c89821de96f02aad2746346b5b74f07cf6a18fb406554625`.
The independent checker also returns seed-path SHA-256
`5c53526c7cbaa125fbd4d3344a148c420695e96466ec48205169b8b8a18b5953`
and `safe_margin=35<=36`.  The grid is a regression check; the universal
quantifiers follow from the written safe-margin proof and induction.

## Trust and novelty boundaries

The theorem trusts the displayed finite paths, exact cyclic-length and
changed-edge calculations, the previously proved finite-mode safe-margin
lemma, ordinary induction, CPython, and either small checker implementation.
It does not trust a solver, floating point, the source certificate's coverage
predicate, network data, or a bounded grid as a proof of the infinite claim.
The coverage count additionally trusts the external finite certificate with
SHA-256
`e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c`.

Primary-source checks used Chand--Ollis, *The Buratti--Horak--Rosa Conjecture
Holds for Some Underlying Sets of Size Three*
(<https://arxiv.org/abs/2202.07733>) and Ağırseven--Ollis, *Grid-based graphs,
linear realizations and the Buratti--Horak--Rosa conjecture*
(<https://arxiv.org/abs/2402.08736>).  Live exact-parameter and committed-graph
searches through height 1764 on 2026-09-03 found no prior publication of this
small-`a` slab.  This supports only “new to the searched sources,” not a
priority claim.
