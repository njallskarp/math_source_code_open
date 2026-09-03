# The complete `b = 3` Lucas--Bergeron--Vessenes slice

## Result

Let `F_0 = 0`, `F_1 = 1`, and

```text
F_(n+1) = s F_n + t F_(n-1)
```

in `Z[s,t]`.  Write

```text
{n choose k}_F = F_n! / (F_k! F_(n-k)!).
```

For every nontrivial canonical Lucas--Bergeron--Vessenes comparison

```text
1 <= a < b = 3 <= c < d,       ad = 3c,
```

the sign-normalized difference

```text
(-1)^(a+1) ({c+3 choose 3}_F - {a+d choose a}_F)
```

lies in `N[s,t]`.  Consequently, after `s = q+z` and `t = qz`, it is
elementary-positive and hence Schur-positive in the two variables `q,z`.

This proves the complete `b = 3` slice of the conjecture.  It strengthens
Schur positivity to elementary positivity.

## Two fixed-width identities

We use the convention that a Lucas binomial is zero when its lower index is
outside `[0,n]`.  For `r >= 0`,

```text
{r+2 choose 2}_F = F_(2r+1) + t^2 {r choose 2}_F.             (1)
```

For `r >= 1`,

```text
{r+3 choose 3}_F
  = F_(3r+1) + t^2 F_(r-1) F_(2r-1) + t^6 {r-1 choose 3}_F.  (2)
```

Identity (1) follows from the addition formula

```text
F_(2r+1) = F_(r+1)^2 + t F_r^2
```

and the recurrence for `F_(r+1)`.  Identity (2) is the Lucas image of the
fixed-width KOH identity

```text
Gaussian(r+3,3)
  = [3r+1]_q + q^2 [r-1]_q [2r-1]_q
    + q^6 Gaussian(r-1,3).
```

For completeness, this identity can also be checked directly by inserting
`[m]_q = (1-q^m)/(1-q)` and clearing
`(1-q)(1-q^2)(1-q^3)`.  Homogenization sends the shifts `q^2` and `q^6`
to powers of the second elementary function.  The involution that changes
the ordinary homogeneous recurrence from a minus to a plus sends that
second elementary function to its negative.  Both shift exponents are even,
so (2) has the displayed positive signs.

Both identities hold over `Z[s,t]`; no division or exceptional
specialization is used in the resulting polynomial identities.

## The `a = 1` family

Here `d = 3c`, with `c >= 3`.  Identity (2) gives immediately

```text
{c+3 choose 3}_F - F_(3c+1)
  = t^2 (F_(c-1) F_(2c-1) + t^4 {c-1 choose 3}_F).           (3)
```

Every factor on the right belongs to `N[s,t]`.

## The `a = 2` family

Here `c = 2k` and `d = 3k`, with `k >= 2`.  Iterating (1) at `r=3k`
and (2) at `r=2k` gives

```text
{3k+2 choose 2}_F
  = sum_(0 <= i <= floor(3k/2)) t^(2i) F_(6k-4i+1),          (4)
```

and

```text
{2k+3 choose 3}_F
  = sum_(0 <= j <= floor(k/2)) t^(6j) F_(6k-12j+1)
    + sum_(0 <= j <= floor((2k-1)/4))
        t^(6j+2) F_(2k-4j-1) F_(4k-8j-1).                   (5)
```

The first sum in (5) cancels precisely the terms `i = 3j` in (4).  If `k`
is odd, the single final unpaired term in (4) also cancels the final product
term in (5).  Pairing `i=3j+1,3j+2` in all remaining terms and putting

```text
n_j = 2k - 4j - 1
```

yields

```text
{3k+2 choose 2}_F - {2k+3 choose 3}_F
  = sum_(0 <= j < floor(k/2)) t^(6j+3)
      (F_(n_j-1) F_(2n_j) + t F_(3n_j-4)).                 (6)
```

Indeed, before the last simplification the parenthesis is

```text
F_(3n) + t^2 F_(3n-4) - F_n F_(2n+1),
```

and the standard Lucas addition formula

```text
F_(3n) = F_n F_(2n+1) + t F_(n-1) F_(2n)
```

turns it into `t(F_(n-1)F_(2n) + tF_(3n-4))`.  The indices in (6) satisfy
`n_j >= 3`, and every displayed summand belongs to `N[s,t]`.

## Exhaustiveness of the parameter split

In canonical form, `a` is either 1 or 2.  If `a=1`, the equation `ad=3c`
forces `d=3c`.  If `a=2`, it forces `c=2k,d=3k`.  Thus (3) and (6) cover
every canonical nontrivial comparison with `b=3`.

## Reproduction

The two checkers use deliberately different constructions.

```bash
python3 -m pip install -r lucas_schur_b3/requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b3/verify_sympy.py --max-c 14 --max-k 12
PYTHONDONTWRITEBYTECODE=1 python3 -I lucas_schur_b3/verify_pure.py --max-c 40 --max-k 40
(cd lucas_schur_b3 && sha256sum -c SHA256SUMS)
```

`verify_sympy.py` constructs Lucas binomials from factorial quotients in the
exact domain `QQ[s,t]`, requires exact polynomial division, and checks (1)--
(6) by normal form.  `verify_pure.py` uses only Python integer dictionaries;
it constructs every Lucas binomial independently from the Sagan--Savage
recurrence and checks coefficient arrays directly.

The universal theorem rests on the written identities and addition law.  The
scripts corroborate index ranges, boundary parities, exact division, and
coefficient signs.  They do not replace the proof.  There is no floating
point, randomness, solver, modular reconstruction, or external data.
The recorded run used CPython 3.12.12 and SymPy 1.14.0.

## Primary context and novelty scope

- Francois Bergeron, *A (q,t)-Overview of q-Analogs*, arXiv:2608.30979,
  records the Lucas analogue and verification only through `ad=bc <= 36`:
  https://arxiv.org/abs/2608.30979
- Bruce Sagan and Carla Savage, *Combinatorial interpretations of binomial
  coefficient analogues related to Lucas sequences*, gives positivity and
  recurrences for Lucas binomials: https://arxiv.org/abs/0911.3159
- Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, records the fixed-width KOH decomposition used above in the
  ordinary Gaussian setting: https://arxiv.org/abs/1709.06187

Targeted primary-source and Discovery Net searches found the conjecture, the
ordinary Gaussian result, and the previously proved Lucas `b=2` family, but
no proof of the Lucas `b=3` slice.  The result is therefore apparently new to
the searched sources; this is not a historical priority claim.

## Discovery Net provenance

This directory is the public source for theorem
`bafkreih3wiiepvsgypebnrfbgydurqcjy7rvekdhj2tv2qfx75qnvsms4q`
(height 1451). Independent verification and reproduction were committed at
heights 1453 and 1455. The expected compact result is that both programs exit
zero and print, respectively, `exact QQ[s,t] verification passed` and
`pure Python exact-integer recurrence verification passed`.
