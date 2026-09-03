# Diagonal first-drop reduction for Euler up/down preperiods

## Target and outcome

Let `A_n` be the Euler up/down numbers,

\[
 \sum_{n\geq 0} A_n\frac{z^n}{n!}=\sec z+\tan z,
\]

and let `s(q)` be the least preperiod of `(A_n mod q)`.  The classical
Knuth--Buckholtz bound is `s(p^r)<=r`.  Güleç's prime-power criterion
states, for an odd prime `p`, `r>=2`, and
`1<=k<=r-1`, that

\[
 s(p^r)\leq r-k
 \quad\Longleftrightarrow\quad
 p^j\mid A_{r-j}\quad(1\leq j\leq k).                 \tag{1}
\]

The open conjecture is `s(p^r)>=r-2`.  This note gives an exact classification
of the first three possible preperiod levels on the diagonal `r=p`, together
with an exact criterion for a deeper drop.  It does **not** determine the
preperiod inside that simultaneous exceptional case.  The result turns the
first possible failure there into the
intersection of two classical exceptional-prime conditions, one attached
to the Fermat quotient of `2` and one attached to a secant Euler number.

## Endpoint lemmas

Write `v_p` for the additive `p`-adic valuation, also on nonzero rational
numbers.

### Lemma 1 (the last secant residue)

For every odd prime `p`,

\[
 A_{p-1}\equiv
 \begin{cases}
 0&\pmod p,\qquad p\equiv1\pmod4,\\
 -2&\pmod p,\qquad p\equiv3\pmod4.
 \end{cases}                                           \tag{2}
\]

#### Proof

The frequency expansion modulo `p` used by Güleç gives, in
`S_1=F_p[i]`,

\[
 A_n=2\eta^{-1}i^n\sum_{a=1}^{p-1}a^n i^{-a}
 \qquad(n\geq1),                                      \tag{3}
\]

where `i^2=-1` and `eta=i^(1-p)-i` is a unit.  Put `n=p-1` and use
Fermat's theorem.  If `p=1 mod 4`, the sum of the `p-1` powers `i^{-a}`
is a union of complete four-cycles and is zero.  If `p=3 mod 4`, the sum
is `-1-i`; also `eta=-1-i` and `i^(p-1)=-1`.  Equation (3) then gives
respectively `0` and `-2`.  The natural copy of `F_p` in `S_1` is
injective, so these are the claimed integer congruences.  QED

### Lemma 2 (the last tangent valuation)

For every odd prime `p`,

\[
 \boxed{\quad
 v_p(A_{p-2})=v_p(2^{p-1}-1)-1.
 \quad}                                                \tag{4}
\]

Equivalently, if `q_p(2)=(2^(p-1)-1)/p` is the Fermat quotient, then
`v_p(A_(p-2))=v_p(q_p(2))`.  In particular,

\[
 p^2\mid A_{p-2}
 \quad\Longleftrightarrow\quad
 p^3\mid 2^{p-1}-1.                                   \tag{5}
\]

#### Proof

For even `m>=2`, the tangent-number formula is

\[
 A_{m-1}=(-1)^{m/2-1}
 \frac{2^m(2^m-1)B_m}{m}.                             \tag{6}
\]

Take `m=p-1`.  The factors `2^(p-1)` and `p-1` are `p`-adic units.
The von Staudt--Clausen theorem gives

\[
 v_p(B_{p-1})=-1,                                     \tag{7}
\]

because `p-1` divides its own index.  Taking valuations in (6) proves
(4), and (5) follows immediately.  QED

## Diagonal first-drop theorem

### Theorem 3

Let `p` be an odd prime and put `s_p=s(p^p)`.

1. If `p=3 mod 4`, then

   \[
    \boxed{s_p=p.}                                    \tag{8}
   \]

2. If `p=1 mod 4` and `p^3` does not divide `2^(p-1)-1`, then

   \[
    \boxed{s_p=p-1.}                                  \tag{9}
   \]

3. If `p=1 mod 4`, `p^3` divides `2^(p-1)-1`, and `p^3` does not
   divide `A_(p-3)`, then

   \[
    \boxed{s_p=p-2.}                                  \tag{10}
   \]

4. In the only remaining case,

   \[
   p\equiv1\pmod4,\qquad
   p^3\mid 2^{p-1}-1,\qquad
   p^3\mid A_{p-3},                                   \tag{11}
   \]

   one has `s_p<=p-3`.

Consequently the Euler up/down lower-bound conjecture fails at the diagonal
exponent `r=p` if and only if all three conditions in (11) hold.

#### Proof

For `p=3`, `3` does not divide `A_2=1`, so the first row of Güleç's
criterion table gives `s(3^3)=3`.  Now suppose `p>=5`.

By (1), used successively with `r=p`, together with the classical upper
bound `s(p^p)<=p`,

\[
\begin{aligned}
 s_p=p
 &\iff p\nmid A_{p-1},\\
 s_p=p-1
 &\iff p\mid A_{p-1}\ \text{and}\ p^2\nmid A_{p-2},\\
 s_p=p-2
 &\iff p\mid A_{p-1},\ p^2\mid A_{p-2},\
          \ p^3\nmid A_{p-3},                            \tag{12}\\
 s_p\leq p-3
 &\iff p\mid A_{p-1},\ p^2\mid A_{p-2},\
          \ p^3\mid A_{p-3}.
\end{aligned}
\]

Lemma 1 translates the first condition into `p=1 mod 4`; Lemma 2
translates the second divisibility into
`p^3 | 2^(p-1)-1`.  Substitution into (12) proves all four alternatives
and the final equivalence.  QED

### Corollary 4 (ordinary and higher Wieferich levels)

For `p=1 mod 4`, even the ordinary Wieferich condition
`p^2 | 2^(p-1)-1` is not enough to lower the diagonal preperiod below
`p-1`.  The first possible further drop requires the strictly stronger
valuation

\[
 v_p(2^{p-1}-1)\geq3.                                 \tag{13}
\]

Thus the familiar base-two Wieferich prime `1093` cannot cause a diagonal
failure unless its Fermat quotient vanishes one additional time modulo
`1093`; the theorem itself does not rely on any computation about that
prime.

## Residue-block corollary

The same frequency expansion gives

\[
 A_{n+p-1}\equiv i^{p-1}A_n\pmod p\qquad(n\geq1).     \tag{14}
\]

Hence zero classes have period `p-1`.  Since
`A_1,A_2,A_3,A_4,A_5=1,1,2,5,16`, no three-consecutive-zero block can
contain any of their residue classes modulo `p>=7`.  In particular, for
every prime `p>=7`, the
conjectured bound holds whenever

\[
 r\bmod(p-1)\in\{2,3,4,5,6,7,8\}.                    \tag{15}
\]

Indeed, a failure would force all of
`A_(r-3),A_(r-2),A_(r-1)` to vanish modulo `p` by (1), whereas the
corresponding cyclic block in (15) contains one of
`A_1,A_2,A_3,A_4,A_5`.  For `p=7` these representatives cover every
residue class modulo `p-1`, proving the conjectured bound for all exponents
at that prime.

For `p=3 mod 4`, Lemma 1 also rules out the boundary blocks with
`r=0 or 1 mod (p-1)`.  These residue exclusions are weaker than Theorem 3
on the diagonal but apply to infinitely many exponents.

## Evidence and trust boundary

The universal statements above are proofs, not consequences of the finite
experiment.  They import:

1. the Knuth--Buckholtz upper bound `s(p^r)<=r`, as recorded in Güleç's
   equation (2);
2. Güleç's proved criterion (1) and frequency expansion (3);
3. the classical tangent-number formula (6); and
4. the von Staudt--Clausen theorem.

The local exact checker independently constructs `A_n` from the Entringer
triangle and verifies (2), (4), and the agreement of the two diagonal
classifications for every odd prime up to a configurable bound.  Python
integers are used throughout; there is no floating point, randomness,
solver, or external package.  This computation is regression evidence only.

The publication audit used CPython 3.12.12 and

```text
python3 verify_diagonal_preperiod.py 4000
```

It checked all 549 odd primes through 4000.  The canonical record digest is
`916daa87ed6f601880db9d72921554f16ea7aab64cb89356085ac77e165db40e`;
the complete expected-output file has SHA-256
`adbb50ce602303ea6f870c2f2ae457288268e0eb1932bda01a28dc911635df52`.

## Literature and novelty status

Primary-source searches on 2026-09-03 found Güleç's August 2026 paper as
the unique source for the new preperiod conjecture and its exact divisibility
criterion.  Earlier work of Ramassamy concerns the now-disproved equality
`s(p^r)=r`.  Literature on `A_(p-3)` and on Wieferich primes treats the two
exceptional conditions separately.  Searches for the diagonal expression
`s(p^p)` and for an Euler-up/down preperiod/Wieferich reduction found no
prior statement.  The claim here is therefore graph-new and
search-relative; no historical priority claim is made.

Primary sources:

- Berke Güleç, *Modular periodicity of the Euler up/down numbers at odd
  prime powers*, arXiv:2608.27058v1 (2026), especially Lemmas 7.1--7.2 and
  Conjecture 7.6: <https://arxiv.org/abs/2608.27058>.
- Sanjay Ramassamy, *Modular periodicity of the Euler numbers and a
  sequence by Arnold*, arXiv:1712.08666 (2017):
  <https://arxiv.org/abs/1712.08666>.
- Romeo Mestrovic, *A search for primes p such that Euler number E_(p-3)
  is divisible by p*, arXiv:1212.3602 (2012):
  <https://arxiv.org/abs/1212.3602>.

## Next obstruction

The first possible diagonal drop is now reduced exactly; the exceptional
case's exact preperiod remains undetermined.  The next high-value analytic step is
to determine `A_(p-1)` beyond its first `p`-adic digit and obtain an analogous
classification for `r=p+t` with fixed `t`, or to derive a Kummer-type
compatibility obstruction showing that the two order-three conditions in
(11) cannot occur simultaneously.  A pivot is warranted if that
compatibility reduces only to an unrestricted intersection of two classical
exceptional-prime sets; in that event the theorem above should remain the
finished diagonal result rather than becoming a constant-optimization lane.
