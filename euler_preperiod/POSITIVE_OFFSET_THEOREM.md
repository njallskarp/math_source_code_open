# Exact positive-offset Euler preperiods through offset 13

## Result

Let `A_n` be the Euler up/down numbers,

\[
 \sum_{n\geq0}A_n\frac{z^n}{n!}=\sec z+\tan z,
\]

and let `s(q)` be the least preperiod of `(A_n mod q)`.  For an odd
prime `p` and a positive integer `t`, put `r=p+t`.  This note proves the
general two-row reduction

\[
 \begin{array}{ll}
 p\nmid A_t &\Longrightarrow s(p^{p+t})=p+t,\\
 p\mid A_t,\ p\nmid A_{t-1}
     &\Longrightarrow s(p^{p+t})=p+t-1.               \tag{1}
 \end{array}
\]

It follows in particular that a drop of two or more at the fixed offset
`t` requires

\[
 p\mid\gcd(A_{t-1},A_t).                              \tag{2}
\]

The finite arithmetic through `t=13`, including one exceptional lift modulo
`43^2`, then gives the following exact classification.

### Theorem

For every odd prime `p` and every `1<=t<=13`,

\[
 \boxed{\quad
 s(p^{p+t})=p+t-\mathbf 1_{\{p\mid A_t\}}.
 \quad}                                               \tag{3}
\]

Thus the only nonmaximal cases in this range are the following; in each
listed case the preperiod is exactly `p+t-1`:

\[
\begin{array}{c|l}
t&\text{odd primes }p\text{ dividing }A_t\\ \hline
4&5\\
6&61\\
7&17\\
8&5,277\\
9&31\\
10&19,2659\\
11&691\\
12&5,13,43,967\\
13&43,127.
\end{array}                                           \tag{4}
\]

There are no exceptions for `t=1,2,3,5`.

## Shift lemma

For every odd prime `p` and every `n>=1`,

\[
 A_{n+p-1}\equiv\epsilon_p A_n\pmod p,
 \qquad
 \epsilon_p=i^{p-1}=(-1)^{(p-1)/2}\in\{1,-1\}.       \tag{5}
\]

Indeed, Güleç's frequency expansion over
`S_1=F_p[i]` has the form

\[
 A_n=2\eta^{-1}i^n\sum_{a=1}^{p-1}a^n i^{-a}
 \qquad(n\geq1).                                     \tag{6}
\]

Replacing `n` by `n+p-1`, Fermat's theorem removes the factor
`a^(p-1)` from every summand and leaves precisely the factor
`i^(p-1)=epsilon_p`.  The natural embedding `F_p -> S_1` is injective,
so (5) is an integer congruence.

## Proof of the two-row reduction

The Knuth--Buckholtz bound gives `s(p^r)<=r`.  Güleç's exact
prime-power criterion says, for `r>=2`,

\[
 s(p^r)\leq r-k
 \quad\Longleftrightarrow\quad
 p^j\mid A_{r-j}\quad(1\leq j\leq k).                \tag{7}
\]

Together, these give

\[
\begin{aligned}
s(p^r)=r
 &\iff p\nmid A_{r-1},\\
s(p^r)=r-1
 &\iff p\mid A_{r-1}\ \text{and}\ p^2\nmid A_{r-2}.
                                                               \tag{8}
\end{aligned}
\]

Set `r=p+t`.  Equation (5), first with `n=t` and then, when `t>=2`,
with `n=t-1`, gives

\[
 A_{r-1}\equiv\epsilon_p A_t\pmod p,
 \qquad
 A_{r-2}\equiv\epsilon_p A_{t-1}\pmod p.             \tag{9}
\]

If `p` does not divide `A_t`, the first row of (8) proves the first
line of (1).  If `p` divides `A_t` but not `A_(t-1)`, then the second
congruence in (9) implies even `p` does not divide `A_(r-2)`, and hence
`p^2` does not divide it; the second row of (8) proves the other line.
For `t=1`, `A_1=1`, so only the first line is needed.  Finally, (7) and
(9) show that `s(p^(p+t))<=p+t-2` forces both divisibilities in (2).

## Exact finite reduction through offset 13

The definition-level Entringer recurrence gives the following complete
factorizations:

\[
\begin{array}{c|l}
t&A_t\\ \hline
1&1\\
2&1\\
3&2\\
4&5\\
5&2^4\\
6&61\\
7&2^4\cdot17\\
8&5\cdot277\\
9&2^8\cdot31\\
10&19\cdot2659\\
11&2^9\cdot691\\
12&5\cdot13\cdot43\cdot967\\
13&2^{12}\cdot43\cdot127.
\end{array}                                           \tag{10}
\]

Thus

\[
 \gcd(A_{t-1},A_t)=1\quad(1\leq t\leq12),
 \qquad
 \gcd(A_{12},A_{13})=43.                              \tag{11}
\]

Equations (1) and (11) prove (3) through `t=12`.  At `t=13`, they also
settle every prime except `p=43`.  For this one remaining pair, `r=56`,
and exact modular recurrence gives the nontrivial second-row lift

\[
 A_{54}\equiv774=18\cdot43\not\equiv0\pmod{43^2}.     \tag{12}
\]

The first congruence in (9) gives `43|A_55`, while (12) gives
`43^2` not dividing `A_54`.  The second row of (8) therefore proves

\[
 s(43^{56})=55.                                      \tag{13}
\]

This closes the last case and proves (3)--(4).

## Certificate and independent validation

The only non-hand-sized arithmetic on which the theorem depends is (12).
It was evaluated in two independent exact ways:

1. the Entringer triangle, which constructs every `A_n` directly from the
   permutation recurrence; and
2. the even-index recurrence obtained from `(sec z)(cos z)=1`,

   \[
   A_n=-\sum_{j=1}^{n/2}(-1)^j{n\choose2j}A_{n-2j}
   \qquad(n\geq2\text{ even}),                        \tag{14}
   \]

   evaluated throughout modulo `43^2`.

Both return `A_54 mod 1849 = 774`.  Exact trial division verifies every
factorization in (10).  The deterministic checker also regression-tests
(5) and (3) for every odd prime through 1200: 195 primes, 4,875 shift
checks, and 2,535 exact top-two classifications.  These bounded checks are
not extrapolated to prove the universal shift lemma; that lemma is the
symbolic argument above.

Reproduction with CPython 3.12.12:

```text
python3 -m unittest discover -s research/euler_preperiod -p 'test_*.py' -v
python3 research/euler_preperiod/verify_positive_offsets.py 1200
```

The canonical verification-record digest is
`db9d8d779fb335b78c9bb5ec2de49038f50b703b11f9a29a0dd224e59f7748b3`.

## Scope correction and literature status

The height-1561 contribution with the immutable title *Exact diagonal Euler
preperiod classification via higher Wieferich valuation* should be read as
an exact classification of the first three possible diagonal levels and an
exact criterion for a deeper drop.  It does **not** determine the exact
diagonal preperiod when the higher-Wieferich and Euler exceptional conditions
hold simultaneously.  Nothing in the present positive-offset theorem claims
to settle that simultaneous diagonal case.

Primary-source searches on 2026-09-03 found Güleç's August 2026 paper as the
unique source of the new exact criterion and lower-bound conjecture.  The
paper classifies preperiods through divisibility tests and gives fixed-`r`
examples, but searches for `s(p^(p+t))`, positive/fixed offsets, and the
specific `43^2` lift found no statement of (1) or (3).  The novelty claim is
therefore graph-new and search-relative; no historical priority is asserted.

Primary sources:

- Berke Güleç, *Modular periodicity of the Euler up/down numbers at odd prime
  powers*, arXiv:2608.27058v1 (2026), especially equation (2), Lemmas
  7.1--7.2, and the criterion table:
  <https://arxiv.org/abs/2608.27058>.
- Sanjay Ramassamy, *Modular periodicity of the Euler numbers and a sequence
  by Arnold*, arXiv:1712.08666 (2017):
  <https://arxiv.org/abs/1712.08666>.

## Natural boundary

The uniform positive-offset result is now closed through the first adjacent
odd divisor and required exactly one `p^2` lift.  Extending the range by
enumerating further offsets would be secondary threshold optimization rather
than a new mechanism.  Under the principal advisory, this is therefore the
stopping point for the Euler lane; the next pass should use graph-first
selection to move to a different underdeveloped analytic target.
