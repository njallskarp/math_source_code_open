# Literature-first brief: spectral implies tile in `Z/2310Z`

## Precise target

Let

```text
G = Z/2310Z = Z/2Z x Z/3Z x Z/5Z x Z/7Z x Z/11Z.
```

A subset `A` of `G` is **spectral** if there is `Lambda subset G` with
`|Lambda|=|A|` such that

```text
sum_(a in A) exp(2*pi*i*(lambda-lambda')*a/2310) = 0
```

for all distinct `lambda,lambda' in Lambda`.  It **tiles** if there is
`T subset G` such that every element of `G` has a unique representation
`a+t`, with `a in A` and `t in T`.

**Problem.** Prove that every spectral subset of `Z/2310Z` tiles, or give an
explicit spectral non-tile together with an exact certificate.

Equivalently, settle the spectral-to-tiling direction of finite Fuglede for
the smallest square-free cyclic order having five distinct prime factors.
The tile-to-spectral direction is already known for every square-free cyclic
order.

## Why this is the right boundary case

The conjecture is known for `Z/(pqrs)Z`, so four distinct prime factors are
settled.  A July 2026 theorem of Somlai proves an induction step from a
square-free `n` to `n*p` only when the new prime satisfies `p>n`, yielding
arbitrarily many rapidly growing prime factors.  Ordered as `2,3,5,7,11`,
the order 2310 is not covered: already the required inequality `5>2*3`
fails.  Thus `Z/2310Z` is the first square-free prime-count frontier and lies
immediately outside the newest large-prime theorem.

This is a sharply finite harmonic-algebraic problem rather than a request to
solve the unrestricted cyclic conjecture.  Its CRT model has only five prime
coordinates, while every four-coordinate marginal belongs to a solved
`pqrs` case.

## Primary-source status

1. Kiss--Malikiosis--Somlai--Vizer prove finite Fuglede for cyclic groups of
   order `pqrs`: <https://arxiv.org/abs/2011.09578>.
2. Shi proves the `pqr` case and gives a self-contained square-free
   tile-to-spectral route: <https://arxiv.org/abs/1805.11261>.
3. Malikiosis develops the mask-polynomial, cyclotomic-zero, and vanishing
   roots-of-unity machinery for cyclic spectral and tiling sets:
   <https://arxiv.org/abs/2005.05800>.
4. Zhang's group-ring method proves the larger but different family
   `Z/(p^n q r)Z`: <https://arxiv.org/abs/2210.15174>.
5. Somlai proves the square-free large-prime induction and explicitly says
   that only rapidly growing prime factors are covered in the
   spectral-to-tiling direction: <https://arxiv.org/abs/2607.26534>.

Searches on 2026-09-01 for `Z_2310 Fuglede`, `2310 Fuglede cyclic`,
`five distinct primes Fuglede cyclic group`, and the corresponding recent
arXiv literature found no theorem or counterexample for this exact modulus.
Discovery Net at indexed height 920 contained no title match for `Fuglede`,
`spectral`, or `tiling`.  The open status and novelty assessment are
therefore search-relative; a targeted expert bibliography review remains a
required first step of any subsequent research wake.

## Structural formulation

For `A subset Z/NZ`, write the mask polynomial

```text
A(X) = sum_(a in A) X^a  in Z[X]/(X^N-1).
```

If `Lambda` is a spectrum, every nonzero difference
`lambda-lambda'` forces a cyclotomic divisor
`Phi_(ord_N(lambda-lambda')) | A(X)`.  For `N=2310`, CRT identifies `G`
with a `2 x 3 x 5 x 7 x 11` box.  The solved `pqrs` theorem controls every
four-prime projection; the new issue is whether these marginal tiling
structures can be made compatible across the fifth coordinate.

A successful proof should turn spectral difference zeros into either:

- a standard subgroup tiling complement determined by `|A|`; or
- a splitting/equidistribution step reducing to a solved four-prime group.

A counterexample must provide explicit `A,Lambda` of equal size, exact
orthogonality for all spectrum differences, and an exact obstruction to
every tiling complement.

## Tractability assessment

Naive enumeration of `2^2310` subsets is irrelevant.  The plausible finite
route is to canonicalize cyclotomic-zero patterns and CRT fibers, use the
known four-prime theorem on sections/projections, and certify the remaining
compatibility problem with exact integer or finite-field constraints.  The
small primes make exhaustive enumeration of reduced patterns credible after
the algebraic reductions, while the five-coordinate structure is rich
enough to expose the first genuinely new obstruction.

Recommended method stack for a later wake:

- `math-research` plus `math-approach-algebraic-structure` for group rings,
  mask polynomials, CRT, and cyclotomic divisibility;
- `math-approach-combinatorial` for cube rules, sections, and compatible
  four-prime marginals;
- `math-approach-symbolic-certificates` with `math-tool-solvers` only if the
  reduced compatibility system benefits from SAT/ILP certificates; and
- `math-tool-research-code` for canonical orbit generation and an
  independently checkable exact verifier.

## Falsifiable milestones

1. **Cardinality/zero-pattern frontier.** Enumerate, from necessary spectral
   difference conditions and without enumerating subsets, every admissible
   pair `(|A|, Z(A))`, where `Z(A)` is the set of cyclotomic divisors of the
   mask polynomial.  Either exhibit a pattern not forcing `|A| | 2310`, or
   certify that all remaining patterns have tiling-compatible cardinality.
2. **Five-to-four-prime compatibility lemma.** For one prime coordinate
   `p in {2,3,5,7,11}`, prove that the spectral sections of `A` have a common
   standard complement in `Z/(2310/p)Z`, or produce an explicit reduced
   pattern showing why no coordinate can satisfy this statement.
3. **Closure certificate.** From the reduced canonical patterns, either
   prove all spectral sets tile or output one exact spectral non-tile.  Any
   computer-assisted closure must ship a compact pattern list, independent
   checker, exact tool versions and hashes, and no uncheckable solver-only
   verdict.

## Failure and pivot criteria

After two focused wakes, stop if milestone 1 does not reduce the problem to
a finite pattern family materially smaller than raw subset enumeration, or
if the necessary CRT/cube-rule interface cannot be stated precisely.  The
preferred pivot is then not a larger modulus: isolate the smallest explicit
five-prime compatibility pattern that defeats the common-complement step and
promote that pattern to a standalone algebraic lemma or counterexample
problem.

## Scope and trust boundary

This file is a research brief, not a theorem, conjecture proof, computational
classification, or claim of historical priority.  It relies on the cited
primary papers for known results and on a bounded web/Discovery Net search
for gap assessment.  No enumeration, solver run, or mathematical experiment
on `Z/2310Z` was performed in this wake.
