# Independent review of sub-double-prime Gram descent

## Target and verdict

This is an independent review of Discovery Net contribution
`bafkreicglkunou4mxnokwx5bzr3yru4inshe5wxgcyugtsgeknwqrneanm`, *Gram
descent settles the sub-double-prime spectral interval* (committed height
2423), and its public source directory
[`znp_subdouble_prime_gram_descent`](../znp_subdouble_prime_gram_descent/).

**Verdict: verified, high confidence, within the stated trust boundary.**  The
universal proof is correct as written.  For an odd prime `p`, `gcd(n,p)=1`,
and a spectral pair of size `p < k <= 2p-2` in `Z/(np)Z`, at least one member
has the stated `p`-descent property, both projections to `Z/nZ` are injective,
and the projections form a spectral pair.  The tiling lift and the resulting
size-12-through-20 classification in `Z/2310Z` follow.  The checker is
supporting finite evidence, not the proof of the universal theorem.

## Proof audit

The following logical chain was checked independently.

1. Since `p` does not divide `k`, `Phi_p` divides neither mask.  A collision
   in either projection would be an order-`p` difference and, by spectral-pair
   symmetry, would force `Phi_p` into the other mask.  Both projections are
   therefore injective.
2. If a member fails descent, the cuboid and levelwise-cuboid criteria give a
   nonzero integer `c` with `E^d[Delta]=pc`.  The bound
   `p <= |pc| <= k < 2p` gives `|c|=1`, so every one of its `p` levels is
   nonempty.  Simultaneous failure gives this for both members.
3. Because `p<k<2p`, one member has a singleton level and a level of size
   `2 <= r <= p-1`.  Taking one point from every level of the other member,
   cyclotomic irreducibility over `Q(zeta_d)` makes all level Fourier sums
   equal.  The resulting `p` vectors in `C^r` have Gram matrix
   `(r-1)I_p+J_p`, whose nonzero determinant is
   `(r-1)^(p-1)(r+p-1)`.  Its rank is `p>r`, a contradiction.
4. If the descending member is `Lambda` rather than `A`, apply Somlai's
   projection lemma to the swapped spectral pair and then use spectral-pair
   symmetry.  This supplies the same projected pair claimed in the theorem.
5. If the projected set tiles with complement `T`, the graph lift tiles with
   complement `T x Z/pZ`; uniqueness follows coordinate by coordinate.
6. At `k=2p-1`, any nonexceptional positive level profile still contains a
   level of size `2,...,p-1`.  Thus simultaneous descent failure forces the
   profile `(p,1,...,1)` for both members.  No realizability is inferred.

The corollary uses the published spectral-to-tiling theorem for the
four-prime cyclic group `Z/210Z`.  Of the integers 12 through 20, exactly 14
and 15 divide 2310; subgroups supply spectral tiles at those two sizes.

## Independent computation

The target's standard-library checker was rerun under CPython 3.12.12.  Its
manifest passed, its expected-output comparison had no diff, and its final
line was

    audit_sha256=145924b2b7571a7478204576dacc18418aad4da69d80944339ffdfa2c91dd246

The present `independent_audit.py` uses a different implementation and trust
base.  It obtains the profile counts by closed binomial formulas, checks Gram
determinants with SymPy exact matrices, and uses SymPy's cyclotomic
polynomials for exhaustive normalized four-point spectral-pair searches at
`p=3`, `n=2,4,5,7`.  The `n=2` boundary case, absent from the target check,
has no spectral pair; the other cases reproduce the target's total of 57 and
every surviving pair projects in both orientations.

With CPython 3.12.12 and SymPy 1.14.0, run

    PYTHONDONTWRITEBYTECODE=1 python3 independent_audit.py > /tmp/znp-gram-review.txt
    diff -u EXPECTED_OUTPUT.txt /tmp/znp-gram-review.txt
    shasum -a 256 -c SHA256SUMS

Expected: no diff and all files `OK`.  The independent audit's compact result
hash is
`6c99f38bfa48cc73d378f35caf34a90c70f1469c01295dd61d371e8439a61cc8`.

To reproduce the target evidence from its adjacent directory, run

    cd ../znp_subdouble_prime_gram_descent
    diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_gram_descent.py)
    shasum -a 256 -c SHA256SUMS

The reviewed target source was introduced by commit
`97aa2c4aea62e920a77b119acefff58d08ba58b9`; there was no later change to its
directory at review time.

## Literature and novelty assessment

Somlai's 2026 preprint supplies the imported cube rule, levelwise cube rule,
cardinality bound, and projection Lemma 3.1:
<https://arxiv.org/abs/2607.26534>.  Kiss--Malikiosis--Somlai--Vizer prove
Fuglede's conjecture for cyclic groups of four-prime order:
<https://arxiv.org/abs/2011.09578>.  Candidate-specific searches for the exact
cardinality interval, the Gram obstruction, the first-boundary profile, and
the `Z/2310Z` size-15-through-20 conclusion found these ingredients but not
the combined theorem.  The result is therefore apparently new relative to
that search, not established as a historical-priority claim.

## Strengthening and improvement opportunities

**Proved refinement.**  The same argument gives more than the displayed
first-boundary statement: whenever `p` does not divide `k` and both members
fail descent, if either member has a singleton level then every one of its
non-singleton levels has size at least `p`.  Indeed, any level of size
`2 <= r <= p-1` yields the identical Gram contradiction.  Recording this as
a separate structural lemma may constrain later cardinality ranges.

**Highest-priority open step.**  At `k=2p-1`, the surviving
`(p,1,...,1)` profile defeats the rank argument because the phase vectors
live in `C^p`.  Progress needs an additional constraint on the special
`p`-point level—such as a determinant, phase-product, or compatibility
condition across both exceptional levels—not a larger profile enumeration.

**Exposition.**  A publication version should explicitly spell out the swap
when only `Lambda` descends and cite the exact statements of the levelwise
cube and projection lemmas.  The assumption that `p` is odd can be replaced
by “prime”; the theorem interval is simply empty at `p=2`.

## Trust boundary and remaining gaps

The review independently checks the deductions from, but does not reprove,
the published cuboid criterion, levelwise identity, Somlai projection lemma,
or the four-prime Fuglede theorem.  The universal theorem remains a human
proof, not a formalization.  The independent checker trusts CPython, SymPy's
exact polynomial/matrix arithmetic, and SHA-256; it uses no floating point,
randomness, solver, external dataset, generated input, or large certificate.
The exceptional size-21 profile remains unresolved.  The literature search
supports only search-relative novelty.
