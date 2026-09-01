# Exact Collatz block composition and all-prefix lift intervals

This directory retains the affine offset and residue information that is lost
by coefficient-only counting.  A length-`K` parity word has a least
nonnegative cylinder representative `r`.  If `s_j=T^j(r)` and `q_j` is the
number of odd bits in its first `j` positions, then every full-cylinder lift

```text
n_z = r + 2^K z
```

has the exact prefix margin

```text
T^j(n_z) - n_z
  = (s_j-r) + (3^q_j * 2^(K-j) - 2^K) z.
```

Consequently, the lifts that satisfy `T^j(n_z) >= n_z` simultaneously for all
`j=1,...,K` form one exactly computable integer interval, possibly empty or
unbounded.  This is an all-prefix strengthening of the endpoint-only cylinder
criterion.

## Exact block jump

Let blocks `u` and `v` have affine data `(k,q,C_u)` and `(h,p,C_v)`.  Their
concatenation obeys

```text
k_uv = k+h,
q_uv = q+p,
C_uv = 3^p C_u + 2^k C_v.
```

If `u` has cylinder base `r_u -> s_u` and `v` has base `r_v -> s_v`, choose
the unique `a mod 2^h` with

```text
a = (r_v-s_u) * (3^q)^(-1) mod 2^h.
```

Then the concatenated base is `r_u+2^k a`.  Writing
`s_u+3^q a = r_v+2^h b`, its endpoint is `s_v+3^p b`.  Thus the implementation
can jump a whole block without replaying its individual branches.  Lean checks
the division-free offset composition and compatible-lift transport identities.

## Terras coefficient stopping-time reduction

Terras's coefficient stopping time `kappa(n)` is the first `K` for which the
multiplier `3^q_K/2^K` is below one.  The ordinary stopping time `sigma(n)` is
the first `K` for which `T^K(n)<n`; always `kappa(n)<=sigma(n)`.  Terras
conjectured equality for every `n>=2`.

In the interval language this becomes a precise finite-certificate statement:
every word that is coefficient-noncontracting at each proper prefix and
contracting at its full length must have an empty positive all-prefix lift
interval.  The only nonempty equality case is `10`, whose interval `[0,0]`
represents the trivial start `1` and is outside `n>=2`.

The Python audit checks all 190,069 first-crossing words through depth 26 and
finds only that trivial interval.  The independently written Ruby audit checks
all 4,404 first crossings through depth 20 with the same result.  These are
finite computations, not a proof of the coefficient stopping-time conjecture;
Rozier and Terracol prove substantially deeper related bounds by different
record-table methods.

## Verification

Python exhaustively checks all 8,191 words through length 12, 172,011 lift
probes, and 98,305 block splits.  Ruby independently checks all 2,047 words
through length 10, 42,987 lift probes, and 20,481 block splits.  Their canonical
length-10 interval tables agree at SHA-256

```text
f4fb4c5deab7d4afc583110f92b1228f975eb960db58df99c9e3154666a74325.
```

Tested with Python 3.12.12, Ruby 2.6.10, and Lean 4.33.1:

```bash
python3 verify_block_interval.py --max-length 12 --max-lift 20 --cst-depth 26
python3 -m unittest -v test_block_interval.py
ruby verify_block_interval.rb 10
lean lean/CollatzBlockInterval.lean
```

All computational decisions use exact integers.  Lean uses no `sorry`,
`admit`, custom axioms, `unsafe`, or `native_decide`; `#print axioms` reports
only `propext` and `Quot.sound`.

## Status, novelty, and limitations

- **Theorem/formalization:** exact block-offset composition, compatible lift
  transport, and the linear all-prefix interval characterization.
- **Verified computation:** the exhaustive and first-crossing ranges above.
- **Prior work:** parity/residue cylinders and 2-adic conjugacy are classical
  (Terras; Bernstein--Lagarias).  Angermund (2025) also gives a two-operator
  arithmetic-progression calculus.  No novelty is claimed for affine
  composition by itself.
- **Apparently new reusable packaging:** the searched sources did not state
  this exact all-prefix lift-interval certificate or its direct equivalence to
  finite first-crossing audits of the Terras conjecture.  This is a cautious
  graph-level novelty assessment, not a priority claim.
- **Limitation:** the number of first-crossing words still grows
  exponentially.  The interval theorem makes each word exact and blockable;
  it does not yet supply a global dominance rule or prove that every interval
  is empty.

## Primary sources

- R. Terras, “A stopping time problem on the positive integers,” *Acta
  Arithmetica* 30 (1976), 241–252.
- D. J. Bernstein and J. C. Lagarias, “The 3x+1 conjugacy map,” *Canadian
  Journal of Mathematics* 48 (1996), 1154–1169.
- R. Rozier and E. Terracol, “Paradoxical behavior in Collatz sequences,”
  arXiv:2502.00948.
- S. Angermund, “A two-operator calculus for arithmetic-progression paths in
  the Collatz graph,” arXiv:2506.19115.
