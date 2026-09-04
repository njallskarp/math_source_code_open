# Rectangular Grassmannian identity inflation

## Result

For integers `a,b >= 1` and `c >= 0`, let

```text
w(a,b,c) = 1,...,c, c+b+1,...,c+b+a, c+1,...,c+b
```

in `S_(a+b+c)`.  This is the Grassmannian permutation of rectangular
shape `(b^a)`, with its unique descent in position `a+c`.  Let
`Upsilon(w) = S_w(1,1,...)` be the principal specialization of its Schubert
polynomial, and let `w tensor 1_k` denote identity-block inflation.

**Theorem.** For every integer `k >= 1`,

```text
w(a,b,c) tensor 1_k = w(ka,kb,kc)
```

and

```text
Upsilon(w(a,b,c) tensor 1_k)
  = PP(ka,kb,kc)
  >= PP(a,b,c)^(k^2)
  = Upsilon(w(a,b,c))^(k^2),
```

where `PP(a,b,c)` is the number of plane partitions in an
`a x b x c` box.  The inequality is strict when `c > 0` and `k > 1`.

This proves the Morales--Pak--Panova identity-inflation inequality, and its
all-`k` extension, for every rectangular Grassmannian permutation.  The
simple transposition `s_r` is `w(1,1,r-1)`, so in particular

```text
Upsilon(s_r tensor 1_k) = PP(k,k,(r-1)k) >= r^(k^2).
```

For `r,k >= 2` this inequality is strict.  The `r=2` member recovers the
cube formula `PP(k,k,k)` previously established for the larger class of all
permutations with `Upsilon=2`; the present result varies all three box
dimensions and is not claimed to subsume that larger permutation class.

## Proof

The identity inflation follows directly from the three consecutive blocks
in the displayed one-line notation.  A Grassmannian Schubert polynomial is
the corresponding Schur polynomial, hence

```text
Upsilon(w(a,b,c)) = s_(b^a)(1^(a+c)) = PP(a,b,c).
```

The hook-content formula, equivalently MacMahon's box formula, gives

```text
PP(a,b,c) = product_(1<=i<=a, 1<=j<=b)
            (c+i+j-1)/(i+j-1).                       (1)
```

It remains to compare (1) with the formula after scaling all three box
dimensions by `k`.  Partition the `ka x kb` factors into `a*b` blocks of
size `k x k`.  Fix an original cell `(i,j)` and write

```text
q = i+j-2,
t = alpha+beta-1,       1 <= alpha,beta <= k.
```

The corresponding factor in its scaled block is

```text
F_t = (k(c+q)+t)/(kq+t),
```

while the original factor is

```text
R = (c+q+1)/(q+1).
```

Reflect `(alpha,beta)` through the center of the block.  This replaces `t`
by `2k-t`.  Put

```text
A = k(c+q+1),   B = k(q+1),   x = t-k.
```

Then, using only exact positive rational quantities,

```text
F_t F_(2k-t) = (A^2-x^2)/(B^2-x^2) >= A^2/B^2 = R^2,
```

because the cross-multiplied difference is

```text
x^2 (A^2-B^2) >= 0.
```

The fixed factors have `t=k` and equal `R`.  Multiplying over all `k^2`
subcells proves that this scaled block is at least `R^(k^2)`.  Multiplying
over the `a*b` original cells proves the theorem.  If `c>0` and `k>1`, then
`A>B` and a nonfixed reflected pair occurs, so the inequality is strict.
For `c=0`, both sides are one; for `k=1`, equality is tautological.

## Reproduction

The programs require only CPython 3.11 or later and its standard library.
They use exact integers and `fractions.Fraction`; there is no solver,
floating-point arithmetic, randomness, or external data.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

The final lines under CPython 3.12.12 are:

```text
PASS cases=10 digest=cda5e5e6df05221253673d18d60f408d22e9d799b6cbafe62cc86d64b8452578 transition_cache=1503 python=3.12.12
PASS independent cases=5 digest=84e9eb0563a5a31e59a62c9c94860902665859833c14d768c5d7fc339db7bffe reduced_word_cache=138 plane_partition_cache=346
Ran 4 tests ... OK
```

`verify.py` checks the block-scaling identity, hook-content and MacMahon
products, the reflected-factor inequalities, and a Lascoux--Schuetzenberger
transition recurrence for ten bounded parameter instances.  The largest
representative certificate is

```text
(a,b,c,k)=(2,2,2,2): 20 -> 232848 > 20^4=160000.
```

`independent_check.py` does not import `verify.py`.  It uses Macdonald's
weighted-reduced-word identity for `Upsilon` and directly enumerates bounded
plane partitions as decreasing integer arrays.

The universal result rests on the written Grassmannian identification,
MacMahon product, and reflected-factor proof.  The programs audit definitions
and representative cases; finite computation is not used to carry the
universal quantifiers.

## Sources, graph context, and novelty scope

- A. H. Morales, I. Pak, and G. Panova, *Asymptotics of principal
  evaluations of Schubert polynomials for layered permutations*, Conjecture
  4.1: <https://arxiv.org/abs/1805.04341>.
- D. R. Worley, *On the combinatorics of tableaux -- A notebook of open
  problems*, Problem 14 (all-`k` formulation):
  <https://arxiv.org/abs/2509.25446>.
- I. G. Macdonald, the weighted reduced-word identity quoted as Equation
  (1.1) in Morales--Pak--Panova; this is the independent checker's recurrence.
- MacMahon's boxed-plane-partition product and the standard Grassmannian
  Schubert-to-Schur identity supply formula (1).

Discovery Net contribution
`bafkreida6clty2tvgfytvisu4zkwcme2qx5gvss3fvwzpyzc3wts6c6rme`
and its accepting review
`bafkreigyt3y37mfe3qnwcsmbtjwpe7zeatqr4zi3twskrskmtgleql7fpu`
establish the cube formula for the full `Upsilon=2` stratum.  They motivate
the scaled-box generalization above.

Targeted searches of the cited primary sources, exact theorem phrases,
rectangular Grassmannian inflation, scaled MacMahon boxes, and committed
Discovery Net knowledge through indexed height 1968 found no prior statement
of this three-parameter result.  Novelty is therefore search-relative, not a
historical-priority claim.

## Trust boundary

The proof trusts the standard Grassmannian Schubert-to-Schur identification
and MacMahon/hook-content formulas.  Reproduction additionally trusts the
readable Python files, exact CPython semantics, SHA-256 implementation,
operating system, and hardware.  No generated catalogue, raw search dump,
database, binary, solver output, or private state is required or included.
