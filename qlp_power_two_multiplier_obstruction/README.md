# A half-period obstruction to common fixed multipliers

## Claim

Let \(n\) be divisible by four and let \(X\in\mathbb C^n\) have \(|X_j|=1\). Set \(m=n/2\) and \(h=1+m\). If
\[
X_{hj}=X_j\qquad(j\in\mathbb Z/n\mathbb Z),
\]
then its half-period autocorrelation is nonnegative. Consequently no quaternary Legendre pair of length \(n\) can have \(h\) as a common fixed multiplier.

For every \(n=2^k\), \(k\ge3\), the common fixed multiplier group of a quaternary Legendre pair is therefore one of
\[
\{1\},\qquad\{1,-1\},\qquad\{1,n/2-1\}.
\]
In particular, at the unresolved length 64 the only possibilities are
\[
\{1\},\qquad\{1,63\},\qquad\{1,31\}.
\]
This excludes all common fixed multiplier groups of order at least four. It does not exclude either remaining involution or establish existence at length 64.

## Proof

Multiplication by \(h\) fixes even indices and sends each odd index \(j\) to \(j+m\). Invariance makes the \(m\) odd-index terms in \(C_X(m)\) equal to one. Pair the even-index terms across the half-period. Since \(m\) is even, this gives the exact identity
\[
C_X(m)=m+2\sum_{\substack{0\le j<m\\j\text{ even}}}
\operatorname{Re}(X_j\overline{X_{j+m}})
=\sum_{\substack{0\le j<m\\j\text{ even}}}|X_j+X_{j+m}|^2\ge0.
\]
For a Legendre pair \((A,B)\), both sequences being invariant would give \(C_A(m)+C_B(m)\ge0\), contrary to \(-2\). The same argument works for any finite collection of unit-modulus sequences whose combined half-period autocorrelation is strictly negative.

Now let \(n=2^k\), \(k\ge3\). The four solutions of \(u^2=1\pmod n\) are \(1,-1,1+m,m-1\). Indeed, in \((u-1)(u+1)\), one of the two consecutive even factors has 2-adic valuation one, so the other is divisible by \(2^{k-1}\). The displayed four residues all satisfy the equation.

The unit group has order \(2^{k-1}\), so every element has power-of-two order. An element of order at least four generates a nonidentity involution that is itself a square. Such a square is 1 modulo four, whereas \(-1\) and \(m-1\) are 3 modulo four. Therefore this involution is \(1+m\), which is forbidden. A subgroup avoiding \(1+m\) thus contains only involutions; it cannot contain both \(-1\) and \(m-1\), since their product is \(1+m\) modulo \(n\). The three stated groups are the only remaining possibilities. This is an elementary proof for all \(k\), independent of computation.

The obstruction also excludes the situation in which separate cyclic shifts of the two sequences make \(h\) a common fixed multiplier: shift the sequences first, since their autocorrelations do not change. This covers ordinary shift-to-fixed normalization only. It does not claim to classify multiplier actions with phase twists, conjugation, or interchange of the two sequences.

## Finite audit and reproduction

```sh
python3 qlp_power_two_multiplier_obstruction/verify.py
```

Tested with CPython 3.12.12; only the standard library is used. The exact output is `expected.json`. The audit derives the unit group and all its subgroups modulo 64 from multiplication, with no preloaded group table. It finds 14 subgroups: eleven contain 33, and the other three are precisely the groups above. A separate orbit-based lower bound counts half-period pairs forced equal by each subgroup. All eleven excluded subgroups force at least sixteen of the 32 unordered half-period pairs equal, giving nonnegative autocorrelation for each invariant sequence. Finally it checks the sum-of-squares identity directly on every invariant fourth-root word at lengths 4 and 8 (64 and 4096 words).

These finite checks audit the proof and its length-64 specialization. They do not constitute a search for all length-64 pairs. The all-length claim rests on the proof above; the finite output additionally trusts this short Python program, integer arithmetic, and the execution environment. No solver or floating-point calculation is used.

## Literature and novelty scope

The target is the even-length conjecture of [Kotsireas–Winterhof](https://arxiv.org/abs/2212.10953). [Kotsireas–Koutschan–Winterhof](https://arxiv.org/abs/2408.16318) and [Jedwab–Pender](https://arxiv.org/abs/2408.08472) give the 2025 framework and constructions. [Lebedev, arXiv:2609.04589v1](https://arxiv.org/abs/2609.04589) leaves length 64 open and reports restricted reversible queue exhaustion. That work concerns the \(-1\) symmetry; this lemma removes larger common fixed multiplier groups by a direct half-period argument and leaves \(31\) as the other possible involution at length 64.

A targeted primary-source and committed-graph search on 2026-09-09 found no statement of this specific obstruction or its power-of-two corollary. Its elementary nature makes independent rediscovery plausible: novelty remains search-relative, not a priority claim. No external peer review has yet been performed.
