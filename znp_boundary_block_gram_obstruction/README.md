# Block-Gram obstruction at the first prime boundary

Let `p>=3` be prime, `gcd(n,p)=1`, and identify

```text
Z/(np)Z = Z/nZ x Z/pZ.
```

This directory proves that a spectral pair with injective projections to
`Z/nZ` cannot have level-size profile `(r,1^(p-1))` on both sides, for any
`r>=2`.  Applied to the independently reviewed sub-double-prime descent
theorem, this eliminates its only exceptional profile at cardinality
`2p-1`.  Therefore the projection/descent theorem extends from

```text
p < k <= 2p-2
```

to the closed interval

```text
p < k <= 2p-1.
```

For `Z/2310Z` (`n=210,p=11`), every spectral set of size 12 through 21 tiles,
and the possible cardinalities in that interval are exactly 14, 15, and 21.

The proof is in [THEOREM.md](THEOREM.md).  The central object is an explicit
block Gram matrix.  Its restriction to vectors constant on the two level
blocks has determinant

```text
-(r-1)(p-2)(r+p-1),
```

so it cannot be positive semidefinite.

## Reproduction

Requires CPython 3.11 or later and only the standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_block_gram.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_block_gram.py)
shasum -a 256 -c SHA256SUMS
```

The checker reconstructs the full block matrix for 40 `(p,r)` cases, verifies
an explicit negative quadratic-form witness using exact integers, and
independently enumerates all normalized five-point spectral pairs in
`Z/6Z`, `Z/12Z`, and `Z/15Z`.  It finds 161 pairs and no pair with the
exceptional profile on both sides.

Expected-output SHA-256:
`ccacb375c310f424bba37a0911892d7b7185fff21c94b549f8f5f7f972312b38`.

The computation corroborates but does not replace the parameter-free Fourier
and positive-semidefinite argument.

## Primary sources and scope

- G. Somlai, *Fuglede's Conjecture on Cyclic Groups of Square-Free Order: The
  Case of Rapidly Growing Prime Factors*,
  [arXiv:2607.26534](https://arxiv.org/abs/2607.26534).  The descent
  application imports its cuboid criterion, levelwise identity, and projection
  lemma through the independently reviewed predecessor theorem.
- G. Kiss, R. D. Malikiosis, G. Somlai, and M. Vizer, *Fuglede's conjecture
  holds for cyclic groups of order pqrs*,
  [arXiv:2011.09578](https://arxiv.org/abs/2011.09578).  This supplies the
  four-prime base case for `Z/210Z`.

Focused primary-source, formula, and graph searches on 2026-09-04 found no
published simultaneous one-fat-level obstruction or this block Gram matrix.
Novelty is search-relative, not a priority claim.

## Trust boundary

The universal claim rests on spectral orthogonality, the elementary degree of
coprime cyclotomic extensions, and positive semidefiniteness of Gram matrices.
The descent corollary additionally imports the reviewed cuboid/projection
machinery named above.  The checker trusts CPython's exact integers and its
definition-level cyclotomic arithmetic.  There is no floating point,
randomness, solver, external dataset, generated certificate, private state, or
large artifact.
