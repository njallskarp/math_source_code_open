# Parity-boundary completion of the BHR `c=1` slice

## Result

For every integer `q>=0`, the following two multisets have explicit cyclic
Hamiltonian-path realizations:

\[
 \{1,2^{20+2q},11\},\qquad
 \{1^2,2^{18+2q},11\}.
\]

Each displayed family is 2-growable at cut 1, and one application of the
gap-insertion construction sends its parameter `q` to `q+1`.  These two
transition-closed rays are precisely the even-`b` frontier not covered by the
published `a>=3` theorem or the earlier odd-`b`, `c=1` four-block formula.
Consequently every admissible multiset `\{1^a,2^b,11\}` with positive
exponents is realizable.

## Why these are the only missing cells

For `c=1`, the order is `v=a+b+2`.  Requiring 11 to be a cyclic length gives
`v>=22`, or `a+b>=20`.  The usual divisor conditions add nothing: if `2|v`,
then `b<=v-2=a+b`; and if `11|v`, then `1<=v-11`.  Hence positive
`(a,b,1)` is admissible exactly when `a+b>=20`.

Ağırseven and Ollis prove that `\{1^a,2^b,y^c\}` has a linear realization
when `y>=5`, `a>=3`, and `a+b>=y-1`; take `y=11` and `c=1`.  The formula in
[`RESIDUAL_SLAB_2_21_1.md`](RESIDUAL_SLAB_2_21_1.md) realizes every remaining
case with odd `b`, `a>=1`, and `a+b>=20`.  Thus only

\[
 (a,b,c)=(1,20+2q,1)\quad\hbox{or}\quad(2,18+2q,1)
\]

remains.  The primary source for the published theorem is:

- A. Ağırseven and M. A. Ollis, *Grid-based graphs, linear realizations and
  the Buratti--Horak--Rosa conjecture*, Theorem 1.3(5) / “When `x=2`”
  theorem, <https://arxiv.org/abs/2402.08736>.

## Two explicit four-block paths

All ranges below advance by 2, and an arrow indicates their direction.
For `q>=0`, concatenate

```text
A_q = (8+2q,6+2q,...,0)
      (21+2q,19+2q,...,13+2q)
      (1,3,...,11+2q)
      (10+2q,12+2q,...,22+2q),

B_q = (8+2q,6+2q,...,0)
      (20+2q,18+2q,...,12+2q)
      (11+2q,13+2q,...,21+2q)
      (10+2q,9+2q,7+2q,...,1).
```

The even and odd ranges visibly partition `0,...,22+2q` for `A_q` and
`0,...,21+2q` for `B_q`.

In `A_q`, the four blocks contain respectively `q+4`, 4, `q+5`, and 6
internal 2-edges.  The first join, from 0 to `21+2q`, is another 2-edge in
cyclic order `23+2q`; the other joins have lengths 11 and 1.  Thus `A_q`
has length counts `(1,20+2q,1)`.

In `B_q`, the blocks contain `q+4`, 4, 5, and `q+4` internal 2-edges; the
first join, from 0 to `20+2q`, is one more cyclic 2-edge.  The first edge in
the last block and the second join have length 1, while the third join has
length 11.  Thus `B_q` has counts `(2,18+2q,1)`.

## Transition closure

Embed at cut 1 with gap size 2.  For `A_q`, the only path edges whose cyclic
length strictly increases are the oriented edges `(2,0)` and `(1,3)`.  For
`B_q`, they are `(2,0)` and `(3,1)`.  In either case each critical vertex
in `{0,1}` has incidence exactly one, so the path is 2-growable at cut 1.
Splitting those two edges through the inserted copies 2 and 3 and shifting
all old labels above 1 gives, block for block,

\[
 G_{2,1}(A_q)=A_{q+1},\qquad G_{2,1}(B_q)=B_{q+1}.
\]

The two seed paths `A_0` and `B_0` occur as witnesses 5 and 13 in residue
case `(1,2,1)` of the pinned finite certificate.  This provenance is not a
trust dependency: both paths are copied into the compact new certificate and
checked directly.

## Reproduction

Only CPython's standard library is needed:

```bash
cd research/bhr_1_2_11_transition_repair
python3 verify_even_b_c1.py even_b_c1_certificate.json --grid 64
python3 independent_even_b_c1_check.py even_b_c1_certificate.json --grid 64
python3 -m unittest -v test_even_b_c1.py
```

The first two commands independently return certificate SHA-256
`15516e949d8a480593a23629a2977bee9b234ae5ed41ffe790eb250efc2a5578`
and record SHA-256
`e3154bc873f4bc254b166ecc1b7ea0c68744aec20da5cbe272d62e4d6eb70d46`.
The parameter grid is a regression check; the proof for every `q>=0` is the
block count and transition identity above.

## Trust boundary and novelty scope

The construction claim depends on exact integer arithmetic, the two displayed
finite paths, the written block calculation, and induction.  The checkers use
no solver, floating point, network data, or imported certificate.  Remaining
machine trust is CPython plus either small checker implementation; their
agreement is additional defense, not a substitute for the proof.

The completeness corollary additionally trusts the cited published linear
theorem and the separately certified odd-`b` formula.  Live searches of the
two primary `{1,2,11}` papers, arXiv exact-parameter phrases, and Discovery Net
through height 1740 on 2026-09-03 found no prior publication of these two
even-`b` formulas.  This supports only “new to the searched sources,” not a
priority claim.
