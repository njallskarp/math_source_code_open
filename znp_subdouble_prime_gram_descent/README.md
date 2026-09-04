# Sub-double-prime Gram descent for cyclic spectral sets

This directory proves a cardinality-local induction theorem for spectral sets
in a cyclic group after adjoining a coprime prime factor.

Let `p` be an odd prime, `gcd(n,p)=1`, and let `(A,Lambda)` be a spectral
pair in `Z/(np)Z` of cardinality `k`.  If

    p < k <= 2p-2,

then the projections of `A` and `Lambda` to `Z/nZ` form a spectral pair.
Consequently, if every `k`-point spectral subset of `Z/nZ` tiles, then every
`k`-point spectral subset of `Z/(np)Z` tiles.

The proof is a rank obstruction.  If neither mask polynomial descends all its
`Phi_(dp)` zeros to `Phi_d`, the levelwise cuboid identity forces both members
of the spectral pair to meet all `p` levels.  A singleton level and a
non-singleton level of size `r<=p-1` then produce `p` vectors in `C^r` with
Gram matrix

    (r-1) I_p + J_p.

This matrix has rank `p`, a contradiction.  At the next cardinality
`k=2p-1`, the same proof gives a sharp structural alternative: simultaneous
failure of descent is possible only if both level-size profiles are
`(p,1,...,1)`.

For `n=210` and `p=11`, the published four-prime Fuglede theorem supplies the
base case.  Therefore every spectral subset of `Z/2310Z` of cardinality
`12,...,20` tiles.  Such a set exists exactly at cardinalities `14` and `15`;
the other seven cardinalities do not divide `2310`.  The cases `12`, `13`,
and `14` were already settled individually in Discovery Net.  The new
consequences are tiling at size `15` and nonexistence at sizes `16,...,20`,
together with the uniform induction theorem and the size-`21` obstruction.

## Reproduce

From this directory run:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_gram_descent.py
    diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_gram_descent.py)
    shasum -a 256 -c SHA256SUMS

The standard-library checker uses exact integers and rational Gaussian
elimination.  It exhausts every positive level-size profile for `p=3,5,7,11`
in the theorem range and at the first boundary, verifies the admissible Gram
rank/determinant formulas, exactly enumerates all normalized four-point
spectral pairs in `Z/12Z`, `Z/15Z`, and `Z/21Z`, and checks the `Z/2310Z`
cardinality classification.  It corroborates but does not replace the
parameter-free proof in `THEOREM.md`.

## Primary sources and novelty scope

Gabor Somlai, *Fuglede's Conjecture on Cyclic Groups of Square-Free Order:
The Case of Rapidly Growing Prime Factors* (2026), especially Proposition
2.1, Lemma 2.2, Corollary 2.2, and Lemma 3.1:

https://arxiv.org/abs/2607.26534

Gergely Kiss, Romanos Diogenes Malikiosis, Gabor Somlai, and Mate Vizer,
*Fuglede's conjecture holds for cyclic groups of order pqrs*:

https://arxiv.org/abs/2011.09578

The levelwise cuboid statement is credited in Somlai's paper to Izabella
Laba and Caleb Marshall's cuboid machinery; the proof used here imports the
stated levelwise identity rather than claiming it.

Targeted searches on 2026-09-04 found the general large-prime induction and
the four-prime base theorem, but no cardinality-local `p<k<=2p-2` Gram-descent
theorem or the `Z/2310Z` size-15-through-20 classification.  Novelty is
therefore search-relative; no historical priority claim is made.
