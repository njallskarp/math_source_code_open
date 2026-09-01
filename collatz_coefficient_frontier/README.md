# Exact Collatz coefficient frontier at depth 300

This directory implements a symbolic quotient of the parity-word tree that
jumps directly to depth 300.  For a parity word, let `q_j` be the number of odd
steps in its first `j` positions.  A prefix is **coefficient-noncontracting**
when

```text
3^q_i >= 2^i for every prefix length i <= j.
```

The exact dynamic program stores only the pair `(j,q_j)` and uses

```text
A(j,q) = 1[3^q >= 2^j] * (A(j-1,q) + A(j-1,q-1)),
A(0,0) = 1.
```

It therefore takes quadratic-time integer arithmetic rather than visiting all
`2^300` words.  A separate Ruby implementation independently recomputes the
result.

There is also a theorem-level exponential lower bound on this frontier.  Fix
`N` and choose `p` with `2^N <= 3^p`.  Give an odd bit weight `N-p` and an even
bit weight `-p`.  Every length-`N` weight-`p` word has total weight zero, and
rotating it just after a minimum partial sum makes all partial sums
nonnegative.  Because a cyclic orbit has at most `N` members, at least

```text
ceil(binomial(N,p) / N)
```

words obey `p i <= N q_i` at every prefix.  Raising the two inequalities to
integer powers proves `2^i <= 3^q_i`, so all of these words are in the
coefficient-safe frontier.  The arithmetic implication is machine checked in
Lean; the cyclic-minimum counting argument is the elementary orbit proof just
given.

## Exact depth-300 result

At depth 300 there are exactly

```text
111358800986904242131297286221730529252986567662022866509378290558038512175289008981
```

coefficient-noncontracting parity words.  Their terminal odd-step counts occupy
111 states, `q=190,...,300`.  By the standard parity-word/residue bijection,
these words represent the same number of distinct residue classes modulo
`2^300`.  This last inference uses the theorem-level bijection; the programs
independently verify injectivity only through their stated finite brute-force
range.

The exact number of first coefficient crossings at depth 300 is

```text
6206542678025330760041752690001599487835420188604033597109748906463205053156170491
```

and the total number of minimal first-crossing words through depth 300 is

```text
10284792983412195745385360038650916821428153534944615861149592459183121508216685005.
```

Taking `N=300` and the minimal admissible `p=190`, the rotation argument alone
certifies at least

```text
6635510034197968091686228009120772324133879705860517338469319939807111040176385952
```

distinct universally non-descending residue cylinders.  More generally, with
`p/N` tending down to `log(2)/log(3)`, this lower bound has exponential rate
`2^H(log(2)/log(3)) = 1.9318...` per step, up to polynomial factors.  The
decimal is explanatory only and is not used by the certificate.

## What this establishes—and what it does not

- **Exact verified computation:** the displayed counts follow from the stated
  recurrence using arbitrary-precision integers.  Python and Ruby agree on the
  entire terminal distribution via its canonical SHA-256 digest.
- **Symbolic compression:** the coefficient layer at depth 300 has 111
  aggregate states, so it does not require depth-by-depth DFS over words.
- **Theorem:** the weighted rational-ballot condition implies coefficient
  noncontraction; Lean checks this without `sorry`, `admit`, custom axioms, or
  `native_decide`.  Cyclic rotation supplies the displayed exponential family.
- **Residue obstruction:** the aggregate counts conceal an 84-digit family of
  distinct 2-adic cylinders.  Counting by `(j,q)` alone cannot decide whether
  the affine offsets and least positive starts satisfy non-descent.
- **No Collatz proof or new verification bound:** Rozier and Terracol prove a
  much stronger absence of paradoxical sequences through length 301,993 using
  stopping-time records.  The result here is infrastructure and a precise
  diagnosis of information lost by the coefficient quotient, not an improved
  bound or a claim that any represented trajectory diverges.

## Run

Tested with Python 3.12.12, Ruby 2.6.10, and Lean 4.33.1:

```bash
python3 verify_frontier.py --depth 300 --brute-force-depth 14
python3 -m unittest -v test_frontier.py
ruby verify_frontier.rb 300
lean lean/CollatzCoefficientFrontier.lean
```

All mathematical decisions use exact integers; there is no floating-point
comparison.

## Primary sources

Retrieved 2026-08-31:

- R. Terras, “A stopping time problem on the positive integers,” *Acta
  Arithmetica* 30 (1976), 241–252.
- R. Rozier and E. Terracol, “Paradoxical behavior in Collatz sequences,”
  arXiv:2502.00948. <https://arxiv.org/abs/2502.00948>
