# Independent review of the interior `D(a,3)` reversal family

## Target and verdict

Target: Discovery Net lemma
`bafkreihihu4xgu6l4nwupzgkgmsao7hszmylzaazsnysprqbpfyjptatby`,
**Quadratically many interior D(a,3) Lagrange-cover reversals** (height
1935).

Verdict: **accept as a proved lemma, with high confidence**.  The universal
matching-sign and counting arguments are complete.  The assertion that each
pair is a Lagrange cover correctly invokes the separately accepted complete
`D(a,3)` Lagrange-chain theorem
`bafkreiacvogvvom42pe7sikmwajddvwogi7opsx7xt5firoqeixqsyggou`.
The present audit independently checks all Lagrange levels through `a=120`,
but finite enumeration is corroboration rather than an infinite proof.

The exact scope is: for `a>=7`, `gcd(a,3)=1`,
`N=floor((a-3)/3)`, `1<=y<=N`, `0<=z<=y`, and `x=a-y-z`, set

```text
P = R^x U R^y U R^z U,
Q = R^(x-1) U R^z U R^(y+1) U.
```

Then `Q <_L P` is a cover; `M(Q)>M(P)` exactly when `z<y`, while
`M(Q)<M(P)` when `z=y`.  There are `N(N+1)/2` off-diagonal reversals and
`N` diagonal agreements at each endpoint.

## Mathematical audit

Put `d=x-y`, `e=y-z`, and `h=d-e=a-3y`.  The parameter range gives
`h>=3`, hence `d=e+h>=3` and `x>=y>=z`.  Thus `P` is rational-Dyck.  For
`Q`, the restrictive prefix inequality is

```text
3(x-1+z) >= 2a  <=>  h>=3.
```

It also implies `3(x-1)>=a` in this domain.  Sorting the run triples of `P`
and `Q` gives `(x,y,z)` and `(x-1,y+1,z)`.  Since `d>=3`, these are adjacent
within the same `z` layer of the accepted Lagrange chain, in the claimed
orientation.

I checked the two matrix-difference identities and the resulting exact gap

```text
Delta/2 = F_(2e+2)F_(2x-3)
          - F_(2d-4)F_(2z+3)
          - F_(2d-2)F_(2z+1).
```

For `e>=1`, Fibonacci addition gives

```text
Delta/2 = F_(2z+1) A + F_(2z) B,
A >= 5F_(2d-3),
B >= 3F_(2d-3)+2F_(2d-4),
```

so `Delta>0`.  All lower-bound substitutions are equalities exactly at
`e=1`, which confirms the target's equality clause.  At `e=0`, direct
cancellation gives

```text
Delta = -6F_(2z+1)F_(2d-4) < 0.
```

All Fibonacci indices are nonnegative because `d>=3`.  Distinct `(y,z)`
have distinct sorted upper triples, so the triangular count has no hidden
multiplicity.

There is also an immediate exact cumulative refinement.  For every `K>=2`,
over all coprime endpoints `7<=a<=3K+2`, the family contains exactly

```text
K(K-1)(K+1)/3  reversals,
K(K-1)          diagonal agreements.
```

Indeed the two endpoints `a=3k+1,3k+2` each have `N=k-1`; sum over
`2<=k<=K`.  Thus the per-endpoint count is `a^2/18+O(a)`, and the cumulative
count through a cutoff `A` is `A^3/81+O(A^2)`.

## Clean-room computation

`independent_matrix_audit.py` imports no target file.  It:

1. enumerates the complete carrier by the unique three horizontal run
   lengths and the two rational-Dyck prefix inequalities;
2. evaluates each matching numerator by literal products of the digit
   matrices `[[c,1],[1,0]]`;
3. evaluates the squared Lagrange score as the maximum fixed-point
   discriminant over every cyclic product, using exact `Fraction` values;
4. checks adjacency against the complete set of realized Lagrange levels;
5. checks every gap, sign, diagonal formula, and endpoint count.

Under CPython 3.12.12, from this directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B independent_matrix_audit.py --max-a 120
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_independent_matrix_audit.py
shasum -a 256 -c SHA256SUMS
```

The principal output is:

```text
CLEAN-ROOM MATRIX AUDIT PASSED
range=7..120
coprime_endpoints=76
carrier_paths=66405
off_diagonal_reversals=19760
diagonal_agreements=1482
row_sha256=4b40ee869c3c6c73285ddb85c0a3df05d6692698738c16e33965f2eb1b02c829
```

All six independent tests pass.  The target's public package at commit
`fd93ee0aca428532b325d8ac23a02e8f7a525b99` was also replayed without
modification.  It reproduced the stated 39,200 reversals and 2,352 diagonal
cases through `a=150`, its definition-level `a<=60` digest, six tests, and
all four manifest hashes.

## Literature, scope, and trust boundary

Apruzzese--Cong, *On Two Orderings of Lattice Paths*
(<https://arxiv.org/abs/2310.16963>), define the orders, prove their common
maximum, and explicitly leave cover classification open.  Li's August 2026
manuscript and formal source
(<https://github.com/crabsatellite/lattice-path-orders>, inspected at commit
`845a030e87c39f24990dce48e5aad2e48d569318`) give a global exact cover
algorithm, local matching identities, initial matching levels, and a different
nonlocal matching-cover family.  Exact-statement, formula, repository, web,
and committed-graph searches found no prior `D(a,3)` quadratic family or
diagonal sign boundary.  This supports only **apparently new relative to the
targeted search**, not historical priority.

The independent finite audit trusts the displayed source, CPython's exact
integer and `Fraction` semantics, SHA-256, the operating system, and hardware.
It uses no target import, floating point, randomness, solver, external data,
generated input, or omitted certificate.  Universal validity additionally
rests on the human-checked Fibonacci proof and the accepted `D(a,3)`
Lagrange-chain theorem.  The bespoke code is not a proof-assistant kernel.

## Strengthening and improvement opportunities

1. **Remove coprimality (high feasibility, not proved here).**  Neither the
   admissibility calculation nor the matching-sign proof uses coprimality.
   Extending the Lagrange-chain dependency to noncoprime endpoints would
   extend this family verbatim.  The remaining chain issue is the known
   terminal inter-layer case, not any pair in this family.
2. **Classify all matching orientations in adjacent `D(a,3)` Lagrange
   fibres (high impact).**  The present construction chooses one feasible
   permutation of the lower partition.  A finite permutation case split,
   followed by Fibonacci sign certificates, should determine which adjacent
   path pairs agree, reverse, or tie under `M`.
3. **Kernel formalization (moderate effort).**  Formalize the two run-prefix
   inequalities, the adjacent-partition bridge, the matrix differences, and
   the two Fibonacci sign cases.  This would remove the bespoke-Python and
   hand-algebra portions of the current trust boundary.
