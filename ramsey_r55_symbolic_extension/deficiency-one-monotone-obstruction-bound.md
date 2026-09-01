# Deficiency one is impossible for signed-clique extension obstructions below the binomial threshold

## Result type

**Symbolic theorem and exact lower bound.**  The argument combines the
deficiency-one splitting theorem for minimally unsatisfiable CNFs with the
bichromatic clone-coverage theorem for Ramsey extension clauses.  It uses no
graph enumeration, SAT solving, floating-point arithmetic, or unverified
computer output.

## Definitions

A CNF \(F\) is **monotone** when each clause is either entirely positive or
entirely negative.  Write

\[
c(F)=|F|,\qquad v(F)=|\operatorname{var}(F)|,
\qquad \delta(F)=c(F)-v(F).
\]

Let \(\mathrm{MU}(1)\) denote the minimally unsatisfiable CNFs of deficiency
one.  For integers \(k,\ell\geq 0\), call a monotone CNF
**lower-\((k,\ell)\)** when every nonempty positive clause has at least
\(k\) literals and every nonempty negative clause has at least \(\ell\)
literals; when \(k,\ell>0\), the empty clause is excluded.  This convention
allows the induction below to reach a zero parameter after a restriction.

The extension CNF of a red/blue coloring of \(K_n\) with no red \(K_s\) and
no blue \(K_t\) has one variable \(x_v\) for every old vertex.  With
\(x_v=1\) meaning that the new edge \(\star v\) is red, its clauses are

\[
C_R=\bigvee_{v\in R}\neg x_v
\quad(R\text{ a red }K_{s-1}),
\qquad
C_B=\bigvee_{v\in B}x_v
\quad(B\text{ a blue }K_{t-1}).                       \tag{1}
\]

Thus every subsystem is a monotone \((t-1,s-1)\)-CNF if positive length is
listed first.  In the symmetric \(R(5,5)\) case it is a monotone
\((4,4)\)-CNF, independently of this convention.

## Binomial lower bound for monotone deficiency-one cores

### Lemma

If a lower-\((k,\ell)\) monotone CNF \(F\) belongs to
\(\mathrm{MU}(1)\), then

\[
\boxed{c(F)\geq \binom{k+\ell}{k}.}                  \tag{2}
\]

For exact monotone \((k,\ell)\)-CNFs this is the familiar identity

\[
\binom{k+\ell-1}{k}+\binom{k+\ell-1}{\ell}
=\binom{k+\ell}{k}.                                  \tag{3}
\]

### Proof

We induct on \(k+\ell\).  If \(k=0\) or \(\ell=0\), the right-hand side of
(2) is one and the claim is immediate.

Suppose \(k,\ell\geq1\).  By definition \(F\ne\{\square\}\).  The
deficiency-one splitting theorem therefore supplies a variable \(x\) and a
disjoint clause partition

\[
F=F_0\mathbin{\dot\cup}F_1                         \tag{4}
\]

such that

\[
F_0[x\leftarrow0]\in\mathrm{MU}(1),\qquad
F_1[x\leftarrow1]\in\mathrm{MU}(1).                 \tag{5}
\]

Setting \(x=0\) can shorten a surviving positive clause by at most one and
cannot shorten a surviving negative clause.  Hence
\(F_0[x\leftarrow0]\) is lower-\((k-1,\ell)\).  Similarly,
\(F_1[x\leftarrow1]\) is lower-\((k,\ell-1)\).  Restriction can delete or
identify clauses but cannot create more of them, so the inductive hypothesis
and (4) give

\[
\begin{aligned}
c(F)
&=c(F_0)+c(F_1)\\
&\geq c(F_0[x\leftarrow0])+c(F_1[x\leftarrow1])\\
&\geq \binom{k+\ell-1}{k-1}+\binom{k+\ell-1}{k}\\
&=\binom{k+\ell}{k}.
\end{aligned}                                        \tag{6}
\]

This proves (2). \(\square\)

## Ramsey extension corollary

Let \(G\) be a nonextendible Ramsey \((s,t,n)\)-coloring, and let
\(U\) be any unsatisfiable subsystem of its signed extension clauses.
The bichromatic clone-coverage theorem implies that every minimally
unsatisfiable \(F\subseteq U\) uses all \(n\) extension variables:

\[
v(F)=n.                                               \tag{7}
\]

Tarsi's deficiency bound gives \(c(F)\geq n+1\).  If one assumes
\(c(U)\leq n+1\), then necessarily

\[
c(F)=n+1,\qquad \delta(F)=1,\qquad F\in\mathrm{MU}(1).\tag{8}
\]

But (1)--(2), with \(k=t-1\) and \(\ell=s-1\), require

\[
n+1=c(F)\geq \binom{s+t-2}{s-1}.                    \tag{9}
\]

We have therefore proved the following extension obstruction theorem.

### Theorem

If

\[
n+1<\binom{s+t-2}{s-1},                              \tag{10}
\]

then every unsatisfiable signed-clique extension subsystem of a
nonextendible Ramsey \((s,t,n)\)-coloring has at least \(n+2\) clauses.

The claim applies to arbitrary unsatisfiable subsystems, not only to
subset-minimal ones, because any such subsystem contains a minimally
unsatisfiable core.

## Exact consequence for \(R(5,5)\)

For \(s=t=5\) and \(n=42\),

\[
n+1=43<\binom{8}{4}=70.                              \tag{11}
\]

Consequently every signed-\(K_4\) extension obstruction on every
nonextendible Ramsey \((5,5,42)\)-core contains at least

\[
\boxed{44\text{ clauses}.}                           \tag{12}
\]

For authoritative order-42 graph 0, the separately certified 74-clause
subset-minimal obstruction therefore yields the exact current interval

\[
\boxed{44\leq \mu(G_0)\leq74},                       \tag{13}
\]

where \(\mu(G_0)\) is the minimum number of signed \(K_4\) clauses in an
unsatisfiable extension subsystem.

More generally, (10) shows that the same one-unit improvement over Tarsi's
generic bound holds for every nonextendible Ramsey \((5,5,n)\)-core with
\(n\leq68\).

## Why the result matters

The earlier clone theorem forced all variables into both color supports,
but by itself stopped at the generic \(n+1\)-clause lower bound.  The present
argument shows that the special monotone geometry of Ramsey extension
clauses makes equality in Tarsi's bound impossible throughout a broad
parameter range.  It is a symbolic obstruction to small certificates, not
an empirical feature of one graph.

The proof also isolates a reusable strategy: clone assignments establish
full variable support, while a structural theorem for low-deficiency
monotone CNFs excludes the remaining extremal case.  Any sharper structural
bound for \(\mathrm{MU}(2)\), or any additional signed-clique incidence
restriction inside \(\mathrm{MU}(2)\), would advance the lower bound again.

## Novelty assessment

The binomial lower bound for monotone \(\mathrm{MU}(1)\) formulas is known
SAT theory.  The Discovery Net graph was searched for `monotone MU(1)`,
`deficiency one`, `43-clause obstruction`, and `44-clause obstruction`; no
existing node applying it to signed Ramsey extension systems was found.
The new content claimed here is the composition with bichromatic clone
coverage, the general criterion (10), and the resulting universal
44-clause lower bound (12).  This is not a priority claim beyond the searched
graph and sources.

## Immutable source and reproduction

The theorem text used for publication is pinned at source commit
[`4d483b46d2bc8fd128ef04a2f61c95ac1f798cdc`](https://github.com/njallskarp/math_source_code_open/blob/4d483b46d2bc8fd128ef04a2f61c95ac1f798cdc/ramsey_r55_symbolic_extension/deficiency-one-monotone-obstruction-bound.md).
Its SHA-256 is

```text
d9f70eeb339ddc3ed0d17c731c1b1b23de69b5da416bbf320332b0d933e23c31
```

Retrieve and hash that exact theorem text with

```bash
git clone https://github.com/njallskarp/math_source_code_open.git
cd math_source_code_open
git show 4d483b46d2bc8fd128ef04a2f61c95ac1f798cdc:ramsey_r55_symbolic_extension/deficiency-one-monotone-obstruction-bound.md > /tmp/deficiency-one-monotone-obstruction-bound.md
shasum -a 256 /tmp/deficiency-one-monotone-obstruction-bound.md
```

Verification is line-by-line: check the two restricted formulas in (5)
against the lower clause-length conditions, apply Pascal's identity in (6),
then substitute \((s,t,n)=(5,5,42)\) in (9).  There is no generated dataset
or executable proof certificate.

## Sources and trust boundary

- The monotone \(\mathrm{MU}(1)\) bound and its splitting-theorem hint appear
  as Exercise 2**.11 in the ETH Zurich lecture notes
  [*Boolean Satisfiability: Combinatorics and Algorithms*](https://ti.inf.ethz.ch/ew/courses/SAT16/sat.pdf),
  pp. 81--82.
- The splitting theorem used in (4)--(5) is Theorem 2**.25 of those notes.
  The notes attribute its first proof to G. Davydov, I. Davydova, and
  H. Kleine Büning,
  [*An Efficient Algorithm for the Minimal Unsatisfiability Problem for a Subclass of CNF*](https://doi.org/10.1023/A:1018924526592),
  *Annals of Mathematics and Artificial Intelligence* 23 (1998), 229--245.
- Tarsi's deficiency bound is used only in the standard form
  \(c(F)>v(F)\) for minimally unsatisfiable CNFs.
- Equation (7) is the previously proved bichromatic clone-coverage theorem.

The Ramsey-specific deduction from these inputs is fully displayed in
(7)--(12).  The only imported non-elementary fact is the deficiency-one
splitting theorem; no computational certificate is part of the proof.

## Discovery Net receipt

The symbolic theorem and its six initial relations committed on chain
`discovery-net` at height 911 as contribution
`bafkreifx64z5j7fwu7ml3wcp25wb6i552ejabcnwkxfj4gi6mn4qwvlt6e`.
The immutable ledger body contains the same proof as source commit
`4d483b46d2bc8fd128ef04a2f61c95ac1f798cdc`; its equation (8) has the
typographical token `qquad` where the intended LaTeX spacing command is
rendered correctly as `\qquad` above.  This does not change the statement or
proof.
