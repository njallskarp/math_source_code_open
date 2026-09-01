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

## Dual-modulus margin theorem

There is a second, smaller canonical modulus.  For any contracting word, let

```text
A = 2^K,       P = 3^q,       d = A-P > 0,
B = B(w),      M = r(w)-z(w).
```

Let `mu` be the least residue in `[0,d)` satisfying

```text
P mu + B == 0 (mod d).
```

Then there is a unique nonnegative integer `kappa` such that

```text
M = mu-d*kappa,
kappa = floor((A*mu+B)/(A*d)).
```

Moreover the least `2^K`-residue is reconstructed exactly by

```text
r(w) = (A*M+B)/d.
```

This follows by substituting `z=r-M` into `A z=P r+B`, which yields
`d r=A M+B`.  The canonical condition `0<=r<A` is precisely the interval

```text
-B/A <= M < d-B/A.
```

That interval has length `d` and hence contains exactly one representative
of the congruence class `mu (mod d)`.  In particular,

```text
M>0  iff  kappa=0 and mu>0
     iff  0<mu and A*mu+B<A*d.
```

Thus the CST target is an exact modular-barrier problem on the coefficient
gap `d`, not only a residue problem modulo `2^K`.

## Cumulative wrap-defect theorem

For a path of adjacent `01 -> 10` exchanges at fixed `(K,q)`, let `J_e` be
the positive coefficient-gap jump on edge `e`, and put

```text
S = sum_e J_e,
W = number of full 2^K-residue wraps,
C = floor((mu_start+S)/d).
```

Here `C` is the winding number of the lifted walk around the coefficient-gap
circle.  Telescoping the two cocycles gives the exact identity

```text
kappa_end-kappa_start = W-C.
```

The right side is therefore path-independent even though `W`, `C`, and the
integer lift `S` can depend on the chosen exchange path.  Starting from a
word with `kappa=0`, cumulative wrapped loss creates a non-descending least
residue exactly when full-residue wrapping outruns coefficient-circle winding
(or when the final circle residue is zero, the cycle boundary).

Lean proves this wrap-defect identity abstractly.  The Python path checker
constructs a canonical insertion path from the mechanical extremizer to every
first-crossing word through length 26 and verifies both the winding equation
and the endpoint window index exactly.

### Single-odd block recurrence

On the canonical insertion path, fix one odd bit and move it left repeatedly.
Its prefix and suffix weights stay constant while the local modulus doubles
from one move to the next.  If `J` is the current coefficient-gap jump and
`J'` the next one, lifting the relevant odd inverse from modulus `L` to `2L`
gives

```text
J' = J/2       if J is even,
J' = (J+d)/2   if J is odd.
```

Equivalently, these jumps follow the canonical inverse-doubling orbit modulo
`d`.  Lean proves the underlying identity `2J'=J+d*epsilon` for the two
possible inverse lifts.  The path audit checks every consecutive pair in all
single-odd insertion blocks through length 26.  This recurrence supplies a
deterministic block skeleton; the next section proves the exact limitation on
using that skeleton alone to compare `W` and `C`.

## Normalized phase-lag theorem and obstruction to `W <= C`

The inverse-doubling skeleton does not by itself give the proposed winding
dominance.  There is an exact cancellation that is easiest to see before
either residue is reduced.

For edge `i`, let

```text
Delta_i = 2^j u                       (positive 2^K-residue displacement),
E_i     = B_i-B_(i+1) = 2^j 3^b      (affine-numerator drop),
J_i     = positive coefficient-gap jump.
```

Writing `A=2^K`, the edge cocycle gives the normalized identity

```text
A J_i = d Delta_i + E_i.
```

Consequently, along any adjacent-swap path, with

```text
D = sum_i Delta_i,       S = sum_i J_i,
```

the numerator drops telescope:

```text
A S = d D + B_0-B_m.
```

The starting coefficient-gap coordinates satisfy

```text
d r_0 = A(mu_0-d kappa_0)+B_0.
```

Combining these equations leaves the exact endpoint phase lag

```text
d(r_0+D) = A(mu_0+S-d kappa_0)+B_m,

(mu_0+S)/d = (r_0+D)/A + kappa_0 - B_m/(A d).
```

Thus all dependence on the inverse sequence `u_i` is shared by the two
phases.  The only difference after a whole block is the *final* positive
numerator `B_m`; the larger coefficient-circle increments merely reduce the
initial lag from `B_0/(A d)` to `B_m/(A d)`.

Put

```text
X = (r_0+D)/A,       beta_m = B_m/(A d).
```

Then the cumulative wrap counts have the floor normal form

```text
W = floor(X),
C = kappa_0 + floor(X-beta_m),
kappa_m = floor(X)-floor(X-beta_m).
```

In particular, from a zero-index source (`kappa_0=0`) and with `B_m>0`,

```text
C <= W.
```

This is the reverse weak inequality from the proposed proof target.  For one
edge, `W` is zero or one, so `kappa_m=W-C` is also zero or one.  Therefore
proving `W<=C` from a zero-index source is not a loose dominance estimate: it must
prove the exact equality `W=C`, which is precisely the missing stopping-time
statement.  A jump-only or inverse-doubling-only argument cannot do this,
because its entire `u_i` contribution cancels from the phase lag.  Prefix
safety has to control the remaining endpoint barrier `B_m/(A d)`.

### Smallest unrestricted strict defect

The reverse inequality can be strict once coefficient-first-crossing prefix
safety is removed.  The lexicographically first adjacent edge is at length
five (words are written chronologically):

```text
01101 -> 10101.
```

Its exact data are

```text
A=32, P=27, d=5,
source: B=46, r=22, z=20, M=2,  mu=2, kappa=0,
target: B=37, r=1,  z=2,  M=-1, mu=4, kappa=1,
Delta=11, E=9, J=2, W=1, C=0.
```

Indeed `32*2=5*11+9`, while the full phase wraps (`22+11=33`) and
the gap-five phase does not (`2+2=4`).  The source already crosses its
coefficient threshold at its first bit, and the target crosses at its second,
so neither is a coefficient-first-crossing word of length five.  This is not
a counterexample to CST; it is a minimal exact counterexample to any attempt
to prove `W<=C` from contraction and the swap algebra alone.

## Exact prefix/suffix split barrier

The remaining one-edge obstruction admits a sharper symbolic localization.
Consider the *target* word `p10s` of a wrapped exchange.  Let `p` have length
`j`, weight `a`, least residue `rho`, and endpoint `eta`.  Put

```text
F = 2^j,       L = 2^(K-j),       H = 2^(K-j-2),
P0 = 3^(a+1),  e = 3^weight(s),    d = 2^K-3^q.
```

Write the target residue as `r=rho+F*x`.  For the suffix cylinder, write
`r_s`, `z_s`, and `B_s=H*z_s-e*r_s`.  Compatibility of `p10` with the suffix
gives an integer `m` satisfying

```text
P0*x + 3*eta + 1 = 4*r_s + L*m,
z = z_s + e*m.
```

Direct elimination of `m`, `r_s`, and `z_s` gives the exact split identity

```text
L*M = d*x + Q,
Q = L*rho - e*(3*eta+1) - 4*B_s.                 (SB)
```

The reverse source `p01s` wraps under `01 -> 10` precisely when

```text
x < u,       P0*u == 1 (mod L),       0 < u < L.
```

Formula (SB) separates that wrap condition from the descent barrier.  In
particular, `Q>0` certifies `M>0` immediately.  If `Q<=0`, any exact lower
bound `chi<=x` with

```text
d*chi+Q > 0
```

still certifies descent.  There is a canonical hierarchy of such bounds:

```text
chi_m = x mod 2^m,
chi_m == (4*r_s-3*eta-1) * P0^(-1) (mod 2^m).
```

Here `chi_m<=x`, and the last congruence depends only on the prefix data and
the lowest `m-2` bits of the suffix residue.  Thus failure of the simple
prefix-surplus test does not require reconstruction of the whole cylinder;
successively more suffix bits give a monotone family of exact certificates.
Lean proves both the division-free identity (SB) and the abstract lower-bound
certificate.

### Coefficient-shadow forcing theorem

Prefix safety can strengthen a truncated lift without revealing its next
binary digit.  For any `2 <= m <= h+2`, put

```text
chi_m = x mod 2^m,
y_m = (P0*chi_m + 3*eta + 1)/4.
```

The quotient is integral because `chi_m` and `x` agree modulo four.  Define
the relative coefficient crossing of an ordinary integer `y` by

```text
sigma_p(y) = min { ell >= 1 :
  P0 * 3^q_ell(y) < 4*F * 2^ell },
```

where `q_ell(y)` counts odd terms in the first `ell` shortcut-Collatz steps
from `y`.  The full suffix has length `h` and is coefficient-safe at every
proper prefix, so its corresponding inequality is weakly reversed for every
`ell<h`.

If `x=chi_m`, suffix compatibility in (SB) becomes

```text
y_m = r_s + H*k
```

for a nonnegative integer `k`.  Thus `y_m` realizes the entire suffix word
and cannot have `sigma_p(y_m)<h`.  Taking the contrapositive gives the exact
forcing rule

```text
sigma_p(y_m) < h  ==>  x != chi_m
                    ==>  x >= chi_m + 2^m.        (SF)
```

Consequently

```text
d*(chi_m+2^m)+Q > 0
```

certifies descent whenever the shadow crossing in (SF) occurs.  This is an
ordinary-integer stopping-time calculation coupled to the symbolic barrier,
not a search over completions of the suffix.  It also generalizes: after
exposing any `m-2` suffix bits, the corresponding integer shadow either lasts
through the suffix or forces at least one further lift bit.

Lean proves the algebraic shadow transport and proves that a certified shadow
mismatch plus the forced next-lift bound implies positive margin.  It does not
formalize extraction of the suffix parity word or the computation of
`sigma_p`; those bridges are checked by the exact Python and C++ programs and
use the classical parity-vector/residue correspondence.

### Exact finite audit and fixed-bit obstruction

Two implementations independently enumerate coefficient-first-crossing
words and all admissible wrapped targets.  The arbitrary-precision Python
and direct fixed-width C++ implementations agree on every aggregate count
through length 26:

```text
first_crossings=190069
candidate_edges=926917
wrapped_edges=383583
positive_prefix_surplus=366092
nonpositive_prefix_surplus=17491
low_two_bit_certificates=14171
base_shadow_certificates=3320
base_shadow_prefixes=2
unresolved_after_base_shadow=0
descent_failures=0
certificate_bits={0:366092, 2:14171, 3:707, 4:2147, 5:466}
symbolic_certificate_bits={0:366092, 2:17491}
sha256=457b622b4bb9a69e5cc7c690bec7bedc5418d83f7c92bf7e8c3094fdf77d9569
```

Thus, through depth 26, all 17,491 wrapped targets missed by `Q>0` are
certified using only `chi_2`: 14,171 directly and the remaining 3,320 by one
coefficient-shadow exclusion.  This compresses what the raw low-bit hierarchy
records as certificates of depths two through five into a uniform two-bit
symbolic certificate on this range.

The C++ audit extends the exact frontier through length 34:

```text
first_crossings=22475498
candidate_edges=151493135
wrapped_edges=73268220
positive_prefix_surplus=70778481
nonpositive_prefix_surplus=2489739
low_two_bit_certificates=1752168
base_shadow_certificates=688589
base_shadow_prefixes=24
unresolved_after_base_shadow=48982
adaptive_shadow_certificates=697630
descent_failures=0
minimum_margin=1 (word 1100)
maximum_certificate_bits=20
maximum_symbolic_certificate_bits=20
```

At depth 34, base shadowing certifies 688,589 of the 737,571 cases missed by
the direct two-bit test.  Allowing (SF) at later truncation depths yields
697,630 shadow-forced certificates in total, but does not reduce the worst
certificate depth below 20.  The method is therefore a large exact
compression of the finite frontier, not a uniform proof.

The base-shadow remainder is itself highly compressed: all cases occur over
24 prefix states, and their `y_2` values belong to the ten-element set

```text
{13, 40, 76, 91, 103, 121, 175, 334, 364, 445}.
```

The C++ checker prints the complete per-prefix table, including `sigma`, edge
count, certified count, unresolved count, and maximum raw certificate depth.
The canonical 24-line table has SHA-256
`96c801390a4cd0bd1b04d89277637dd0f973bba28f3f6a975409312894e9b7f0`.

The maximum is attained already at length 27 by

```text
w = 111101011011101111010011000,       j=5,
d=5077565, L=4194304, x=2621441, Q=-5601853.
```

For this edge, `chi_m=1` through `m=19`, so
`d*chi_m+Q=-524288`; at `m=20`, `chi_m=524289` and the certificate becomes
positive.  Its two-bit shadow integer is `y_2=91`, whose relative coefficient
crossing is 47, later than the suffix length 20, so (SF) correctly cannot
force an earlier bit.  Hence no certificate restricted to at most 19 low lift
bits can be universal.  This is a concrete obstruction to the simplest
fixed-small-state proof strategies, not evidence against CST.  Through length
34, all wrapped edges still have positive target margin; the depth-34 claim
rests on the C++ exhaustive audit, while independent implementation agreement
is limited to depth 26.

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
relevant `01`.  Hence `d v-e>0`, so `J- > 0`.  The complementary identity
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
python3 audit_wrap_defect.py --max-length 26
python3 audit_phase_lag.py --max-length 16
python3 audit_split_barrier.py --max-length 26
ruby audit_swap_cocycle.rb 20
ruby audit_phase_lag.rb 16
/opt/homebrew/bin/g++-16 -std=c++20 -O3 -Wall -Wextra -Werror \
  audit_split_barrier.cpp -o /tmp/audit_split_barrier
/tmp/audit_split_barrier 34
/tmp/audit_split_barrier 34 | rg '^shadow_prefix' | shasum -a 256
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
maximum_window_index=0
wrap_defect_failures=0
sha256=29e07fbf05de09bc0c414b50adf9e2bd80b92e077cdacf78f527b480e1ed7bef
```

The canonical path audit traverses 3,787,863 adjacent moves on 190,066 paths,
with at most 63 inversions and 31 full/circle wraps.  It finds no wrap-defect
identity failure, no inverse-doubling failure across 1,732,441 consecutive
jump pairs, and no positive window index.  Its record digest is
`fe62dae02d3c96b43a5760f931fdf3b652d2de3444f8d6837009b50b9eada2bf`.

The independently implemented Ruby checker agrees through length 20 on all
counts, verifies the one-edge window-defect law, and agrees on record digest
`d5ba814280e73c44b5d4b113820ccc3ab59432eabb1ffa725373ae01d2d4b0f3`
for 4,404 cylinders and 14,938 edges.

The normalized phase-lag audit deliberately ranges over every contracting
word, including words without first-crossing prefix safety.  Python and the
independently written direct-affine Ruby implementation agree through length
16 on all 112,907 contracting words, all 404,360 adjacent edges, the minimal
length-five strict defect above, and record digest
`c2dd4accfc16abecb7d0bdc40e383133642fb8e66c7b2cf00e869b1133a9b436`.
There are zero phase-lag, window-identity, or zero-index-source antidominance
failures.  Of the edges, 404,284 have `W=C`, 38 have `W<C`, and 38 have
`W>C`; every one of the 38 `W>C` cases starts at `kappa=0`, while the 38
reverse cases undo those defects.  The maximum window index in this range is
one.

Lean proves the scaled cocycle identities, jump complementarity, modular
divisibility witness, short-multiple sign lemma, strict gap-change
consequences, full-wrap/prefix-lift-wrap equivalence, and the cumulative
wrap-defect and lifted-jump-halving identities without `sorry`, `admit`,
custom axioms, Mathlib, or
`native_decide`.  `#print axioms` reports only Lean's standard logical axioms
(`propext`, `Quot.sound`, and for the `grind` algebraic normalization proofs,
`Classical.choice`).  The Collatz-specific decoding, enumeration, and the
prefix-safety argument in the displayed theorem remain in the exact external
checker and written proof; Lean does not certify the enumeration.

Lean additionally proves the division-free path phase-lag identity, the
zero-index-source one-edge antidominance consequence, and the complete arithmetic
certificate for the minimal length-five strict defect.  It also proves the
division-free split-barrier identity, exact equal-lift suffix transport, and
the direct and shadow-forced lower-bound certificates used by the Python and
C++ audits.

## Relation to prior work and novelty boundary

Rozier and Terracol introduced the partial order generated by `01 -> 10` and
proved that this move decreases their affine remainder `E_K`; equivalently,
it gives the local numerator difference used above.  That result is prior art,
not new here.  Classical work of Terras, Everett, and Lagarias supplies the
parity-vector/residue bijection.  Fernández and Ibáñez independently study
the same affine numerator via rotations and adjacent transformations and
prove a Christoffel-word extremality theorem.  Christoffel/mechanical
extremality and numerator ordering are therefore explicitly not novelty
claims of this artifact.

Bernstein--Lagarias's 2-adic conjugacy and Laarhoven--de Weger's De Bruijn
graph formulation already imply that congruence modulo `2^m` fixes an
`m`-step parity prefix.  That finite shadowing principle is also prior art.
The coefficient-shadow rule (SF) is claimed only as an apparently new
coupling of that classical principle to the split barrier and the forced
next-lift inequality.

The apparently new pieces, relative to the sources searched below, are the
explicit coupling of this adjacent exchange to the *canonical least residue*,
the complementary jump pair `(J+,J-)`, the dual-modulus margin window, and the
path-independent full-wrap-minus-winding defect.  The normalized phase-lag
telescoping and its antidominance consequence are new within this artifact and
were not found in the targeted source search; they are best viewed as a
rigorous obstruction/clarification of the proposed proof strategy, not as a
historical priority claim.  The exact split barrier and its low-bit certificate
hierarchy were likewise not found in the sources searched, but no historical
priority is asserted.  The denominator `2^K-3^q`, affine endpoint equation,
and affine-numerator swap order are classical; novelty is claimed only for
this margin/cocycle/phase/split packaging.

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
- A. Fernández and M. Ibáñez, “Christoffel Words as Extremal Structures in
  Collatz Dynamics,” arXiv:2607.24844 (2026).
- D. J. Bernstein and J. C. Lagarias, “The 3x+1 conjugacy map,” *Canadian
  Journal of Mathematics* 48 (1996), 1154--1169.
- T. Laarhoven and B. de Weger, “The Collatz conjecture and De Bruijn
  graphs,” *Indagationes Mathematicae* 24 (2013), 971--983;
  arXiv:1209.3495.

## Limitations and next target

The theorems identify but do not eliminate the defect `W-C`.  The phase-lag
normal form rules out a proof based only on the inverse-doubling jump orbit:
from a zero-index base, `W<=C` is already the equality target rather than an
available one-sided estimate.  The split identity makes the remaining target
more local, but the length-27 example rules out a uniform bound of 19 or fewer
low lift bits.  Coefficient shadows supply such bounds for most of the exact
frontier, but long-lived shadows such as `y=91` remain.  The next target is to
classify the 48,982 depth-34 cases left by the base shadow test and derive a
quantitative relation between the ten observed shadow integers, shadow
lifetime, the negative surplus `-Q`, and the forced size of `x`, strong enough
to prove `d*x+Q>0` without exposing an unbounded number of suffix bits.
Equivalently,
one must exclude the exact one-edge barrier

```text
A <= r+Delta < A+B'/d
```

(with integer endpoints understood after clearing denominators), or find a
stronger prefix potential that controls it.  A terminal coefficient-circle
residue of zero must still be excluded separately; it is the exact cycle
boundary.
