# Adjacent-swap cocycle for coefficient-first-crossing Collatz cylinders

This artifact couples the `01 -> 10` parity-word order of Rozier--Terracol
with the canonical residue modulo `2^K`.  The resulting exact cocycle explains
why ordering the affine remainder alone does not order the least-residue
descent margin: moving an odd bit earlier increases the margin unless the
canonical residue wraps around, in which case it decreases by a complementary
positive jump.

## Setup

Use the shortcut Collatz map

```text
T(n) = n/2          (n even),
T(n) = (3n+1)/2     (n odd).
```

For a parity word `w` of length `K` and weight `q`, write

```text
T^K(x) = (3^q x + B(w))/2^K.
```

Let `r(w)` be the unique representative in `[0,2^K)` realizing `w`, and let

```text
z(w) = T^K(r(w)),       M(w) = r(w)-z(w),
d = 2^K-3^q.
```

Thus `M(w)>0` means that the least residue descends at time `K`.  When `d>0`,
the previously proved downward-closure lemma says that a counterexample in
the entire cylinder would force `M(w)<=0` at the least residue.

Consider an adjacent exchange

```text
w  = p 01 s,
w' = p 10 s,
```

where `p` has length `j` and weight `a`, and `s` has weight `b`.  Then
`q=a+b+1`.  Set

```text
L = 2^(K-j),
u = the integer in [1,L) with 3^(a+1) u == 1 (mod L),
v = L-u,
e = 3^b.
```

## The adjacent-swap cocycle theorem

Assume `w` is coefficient-first-crossing: `3^q<2^K`, while every proper
prefix of `w` has coefficient at least one.  Then:

1. The known local numerator identity is

   ```text
   B(w)-B(w') = 2^j e.
   ```

2. The canonical residues obey

   ```text
   r(w') = (r(w) + 2^j u) mod 2^K.
   ```

3. The integers

   ```text
   J+ = (d u + e)/L,
   J- = (d v - e)/L
   ```

   satisfy

   ```text
   0 < J+ < d,       0 < J- < d,       J+ + J- = d.
   ```

4. Consequently the exact descent-margin change is

   ```text
   M(w')-M(w) = J+       if r(w)+2^j u < 2^K,
   M(w')-M(w) = -J-      if r(w)+2^j u >= 2^K.
   ```

Equivalently,

```text
M(w') = M(w) + J+ - d * epsilon,
```

where `epsilon` is exactly the canonical-residue wrap indicator.  Thus each
edge is a nonzero rotation modulo the odd circumference `d`; its lift to an
integer margin rises at an unwrapped edge and falls at a wrapped edge.

### Prefix/suffix coordinates for the wrap

Let the common prefix cylinder have least residue `rho` and endpoint `eta`,
and write

```text
r(w) = rho + 2^j t,       0 <= t < L.
```

If `r(s)` is the least residue of the suffix word `s`, then `t` is determined
without replaying the full word by

```text
3^(a+1) t + 3 eta + 2 == 4 r(s) (mod L).
```

The exchange acts locally by

```text
t' = (t+u) mod L,
```

and its full-residue wrap condition is exactly

```text
t >= L-u.
```

Thus the obstruction can be queried from composable prefix/suffix cylinder
data.  The Python unit test checks this split-coordinate formula on every
admissible edge through length 16, and Lean proves the abstract equivalence
between full-residue wrap and prefix-lift wrap.

### Proof

The numerator formula follows by comparing the contribution of the exchanged
odd bit.  The two congruences defining the canonical residues give

```text
3^q (r(w')-r(w)) == 2^j 3^b (mod 2^K),
```

which reduces to the asserted displacement by `2^j u`.

Since

```text
M(w) = (d r(w)-B(w))/2^K,
```

substitution gives `+J+` without wrap and `J+-d=-J-` with wrap.  Integrality
of `J+` follows from the same congruence.  Also

```text
d v == e (mod L).
```

Final contraction and prefix safety at `p0` imply

```text
3^b < 2^(K-j) = L.
```

Because `d v-e` is a multiple of `L` and is greater than `-L`, it is
nonnegative.  Equality would force `d=1`; then `2^K-3^q=1`, which modulo `8`
forces `K=2,q=1`, incompatible with prefix safety of a word beginning with the
relevant `01`.  Hence `d v-e>0`, so `J->0`.  The complementary identity
`J+ + J-=d` then yields `0<J+<d` as well.

## Structural CST reduction

For fixed first-crossing `(K,q)`, every prefix-safe word is obtained from the
latest admissible mechanical word by a sequence of `01 -> 10` moves.  The
mechanical word was checked separately through `K=200000`, but that cap-only
check cannot control unrelated residues.

The cocycle identifies the exact missing obstruction:

- Every unwrapped move preserves descent and increases its margin.
- Only a wrapped move can create a counterexample.
- If a wrapped edge is the first edge on a path to cross from descent to
  non-descent, its source margin lies in the finite boundary window
  `1 <= M(w) <= J-`.

This is a rigorous reduction, not a proof of CST.  It replaces arbitrary
failure along the majorization lattice with an explicit modular-wrap boundary
problem.

## Verification

Run with Python 3.12.12, Ruby 2.6.10, and Lean 4.33.1:

```bash
python3 -m unittest -v test_swap_cocycle.py
python3 audit_swap_cocycle.py --max-length 26
ruby audit_swap_cocycle.rb 20
lean lean/CollatzSwapCocycle.lean
```

The Python audit checks every coefficient-first-crossing cylinder and every
admissible adjacent edge through length 26:

```text
first_crossing_cylinders=190069
adjacent_edges=926917
unwrapped_edges=543334
wrapped_edges=383583
minimum_jump=2
maximum_jump=23686172
sha256=29e07fbf05de09bc0c414b50adf9e2bd80b92e077cdacf78f527b480e1ed7bef
```

The independently implemented Ruby checker agrees through length 20 on all
counts and on canonical record digest
`d5ba814280e73c44b5d4b113820ccc3ab59432eabb1ffa725373ae01d2d4b0f3`
for 4,404 cylinders and 14,938 edges.

Lean proves the scaled cocycle identities, jump complementarity, modular
divisibility witness, short-multiple sign lemma, strict gap-change
consequences, and full-wrap/prefix-lift-wrap equivalence without `sorry`,
`admit`, custom axioms, Mathlib, or
`native_decide`.  `#print axioms` reports only Lean's standard logical axioms
(`propext`, `Quot.sound`, and for the `grind` algebraic normalization proofs,
`Classical.choice`).  The Collatz-specific decoding, enumeration, and the
prefix-safety argument in the displayed theorem remain in the exact external
checker and written proof; Lean does not certify the enumeration.

## Relation to prior work and novelty boundary

Rozier and Terracol introduced the partial order generated by `01 -> 10` and
proved that this move decreases their affine remainder `E_K`; equivalently,
it gives the local numerator difference used above.  That result is prior art,
not new here.  Classical work of Terras, Everett, and Lagarias supplies the
parity-vector/residue bijection.

The apparently new piece, relative to the sources searched below, is the
explicit coupling of this adjacent exchange to the *canonical least residue*,
the complementary jump pair `(J+,J-)`, and the exact wrap/no-wrap sign law for
the least-residue descent margin.  This is a negative literature search, not a
priority claim.

Primary sources checked:

- O. Rozier and C. Terracol, “Paradoxical behavior in Collatz sequences,”
  *Discrete Mathematics* 349 (2026), 115167; arXiv:2502.00948v5,
  especially Section 2 and Lemma 2.3.
- R. Terras, “A stopping time problem on the positive integers,” *Acta
  Arithmetica* 30 (1976), 241--252.
- C. J. Everett, “Iteration of the number-theoretic function
  `f(2n)=n, f(2n+1)=3n+2`,” *Advances in Mathematics* 25 (1977), 42--45.
- J. C. Lagarias, “The 3x+1 problem and its generalizations,” *American
  Mathematical Monthly* 92 (1985), 3--23.
- T. Niu, “Parity vectors and paradoxical sequences in the accelerated
  Collatz map,” arXiv:2605.13886 (2026).

## Limitations and next target

The theorem does not bound how often wraps occur, nor how a source margin
compares to its edge-specific `J-`.  The next target is to express the wrap
indicator and boundary inequality in prefix/suffix cylinder coordinates, then
seek a path-independent or blockwise bound on cumulative wrapped loss over
Sturmian/Christoffel intervals.
