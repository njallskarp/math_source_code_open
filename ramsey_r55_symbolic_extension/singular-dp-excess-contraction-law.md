# A global excess-contraction law for every 44-clause singular-DP ancestry

## Result type

**Universal clause-genealogy identity and structural-family exclusion.**
For every singular Davis--Putnam reduction history from a hypothetical
42-variable, 44-clause signed-\(K_4\) Ramsey extension obstruction to its
nonsingular deficiency-two terminal formula \(F_p\), a simple clause-length
potential gives an exact conservation law. It is independent of the Ramsey
kernel, support representatives, terminal-cycle labeling, and order of later
singular eliminations.

The main consequence is unavoidable concentration: after the first singular
fan, some later pivot has contraction charge at least three. Therefore the
entire structural family of histories with charge at most two at every later
step is impossible, simultaneously for every surviving \(p\) and every first
fan arity \(m\).

## Setup and collision guard

Let \(G\) be a minimally unsatisfiable clause-set and let \(v\) be singular.
Choose the polarity so that the singular literal \(x\) occurs in the unique
main clause \(C\), while \(\bar x\) occurs in side clauses
\(D_1,\ldots,D_m\). Put

\[
  a=|C|,
  \qquad b_i=|D_i|,
  \qquad
  c_i=\left|(C\setminus\{x\})
      \cap(D_i\setminus\{\bar x\})\right|.              \tag{1}
\]

Here \(c_i\) counts common nonpivot literals. A nonpivot variable occurring
with opposite signs would make the candidate resolvent tautological, so on an
actual surviving resolvent the same number is also the shared nonpivot-variable
count.

Singular DP removes \(m+1\) clauses and has at most \(m\) candidate resolvents.
The standard singular-DP theorem for minimally unsatisfiable formulas says
that deficiency is preserved. Since one variable is deleted, the clause count
must fall by exactly one. Hence **all \(m\) candidate resolvents survive as
distinct new clauses**. In particular, no tautology, collision between two
resolvents, collision with an unaffected clause, or subsumption deletion can
silently change the following count. This is the set-CNF collision guard.

The \(i\)-th resolvent therefore has exact length

\[
  |R_i|=a+b_i-2-c_i.                                    \tag{2}
\]

## The potential and one-step identity

Define the clause-excess potential

\[
  \Phi(G)=\sum_{E\in G}(|E|-2).                         \tag{3}
\]

Only \(C,D_1,\ldots,D_m\) change in the step. Before reduction their local
contribution is

\[
  (a-2)+\sum_{i=1}^m(b_i-2),                            \tag{4}
\]

and afterward it is, by (2),

\[
\begin{aligned}
  \sum_{i=1}^m(|R_i|-2)
    &=\sum_{i=1}^m(a+b_i-4-c_i)\\
    &=m(a-2)+\sum_{i=1}^m(b_i-2)-\sum_{i=1}^m c_i.
                                                               \tag{5}
\end{aligned}
\]

Define the contraction charge of this pivot by

\[
  \sigma(v)
    =\sum_{i=1}^m c_i-(m-1)(a-2).                       \tag{6}
\]

Subtracting (5) from (4) gives the exact one-step law

\[
  \boxed{\Phi(G)-\Phi(\operatorname{DP}_v(G))=\sigma(v).}
                                                               \tag{7}
\]

The side-clause lengths cancel completely. Charge is thus a genuine genealogy
quantity controlled only by the main-clause excess, fan arity, and the
nonpivot overlaps created along that fan.

## Global Ramsey ancestry law

### Theorem

Let \(U=G_0\) be any hypothetical minimally unsatisfiable 42-variable,
44-clause signed-\(K_4\) extension subsystem of a \((5,5,42)\) Ramsey core.
Consider any complete singular-DP history

\[
  G_0\longrightarrow G_1\longrightarrow\cdots
      \longrightarrow G_{42-p}=F_p,                    \tag{8}
\]

where the first fan has arity \(m\). Then

\[
  \sum_{t=1}^{42-p}\sigma_t=92-2p.                     \tag{9}
\]

Moreover, because the first pure signed \(4\)-clause fan has disjoint
three-literal wings,

\[
  \sigma_1=-2(m-1),                                     \tag{10}
\]

and the remaining \(41-p\) steps satisfy

\[
  \boxed{\sum_{t=2}^{42-p}\sigma_t=90+2m-2p.}          \tag{11}
\]

Consequently,

\[
  \boxed{
  \max_{2\le t\le42-p}\sigma_t
  \ge
  \left\lceil 2+\frac{2m+8}{41-p}\right\rceil
  \ge3.}                                                \tag{12}
\]

This holds for every currently possible first arity \(1\le m\le10\) and
every terminal parameter \(3\le p\le33\).

### Proof

Every clause of \(G_0\) has length four, so

\[
  \Phi(G_0)=44(4-2)=88.                                 \tag{13}
\]

The canonical terminal formula \(F_p\) contains \(p\) binary cycle clauses
and two clauses of length \(p\). Hence

\[
  \Phi(F_p)=p(2-2)+2(p-2)=2p-4.                         \tag{14}
\]

Telescoping (7) along (8) proves (9). At the first step, the main and each
side clause are pure signed \(4\)-clauses of opposite signs. Their supports
meet only in the pivot, by the Ramsey opposite-color intersection bound, so
all \(c_{1,i}=0\), while \(a_1=4\). Equation (6) gives (10), and subtracting
(10) from (9) proves (11).

There are \(41-p\) remaining steps. Their average charge is

\[
  \frac{90+2m-2p}{41-p}
   =2+\frac{2m+8}{41-p}>2.                              \tag{15}
\]

At least one integer charge is at least the ceiling in (12), which is at
least three. \(\square\)

### Refined thresholds

The exact ceiling yields useful strata without choosing a kernel:

\[
\begin{array}{rcl}
p+2m>33 &\Longrightarrow& \max_{t\ge2}\sigma_t\ge4,\\
p+m>37  &\Longrightarrow& \max_{t\ge2}\sigma_t\ge5,\\
3p+2m>115&\Longrightarrow& \max_{t\ge2}\sigma_t\ge6.
\end{array}                                             \tag{16}
\]

For example, the extreme allowed pair \((p,m)=(33,10)\) has eight later
steps carrying total charge \(44\), so some step has charge at least six.

## Structural interpretation

Equation (12) is not another selected-support condition. It applies after
intermediate clauses have become mixed and long, and it constrains every full
resolution ancestry. Written out, the mandatory pivot satisfies

\[
  \sum_i c_i\ge(m_t-1)(a_t-2)+3.                        \tag{17}
\]

Thus any complete proof search may reject a partial history as soon as its
remaining potential budget makes (11) impossible. More conceptually, every
ancestry must create a genuinely high-contraction event: through repeated
nonpivot overlap, through a sufficiently strong unit-main fan, or through a
combination of the two. Changing the marked kernel or matching-cover witness
cannot avoid this requirement.

The theorem eliminates, for all \(p\) at once, every inverse-resolution family
whose forward history has \(\sigma_t\le2\) after the first pivot. The refined
thresholds eliminate larger low-charge families in the corresponding
\((p,m)\)-strata.

## Exact checker

Run:

~~~bash
python3 ramsey_r55_symbolic_extension/verify_singular_dp_excess_contraction.py \
  ramsey_r55_symbolic_extension/singular-dp-excess-contraction-certificate.json
python3 -m unittest -v \
  ramsey_r55_symbolic_extension/test_singular_dp_excess_contraction.py
~~~

The standard-library checker verifies the serialized endpoint potentials,
the one-step identity on 250,000 exact integer parameter instances, all 310
admissible \((p,m)\) pairs, the universal lower bound, and every threshold in
(16). These checks audit conventions and arithmetic; the universal theorem is
the algebraic proof (1)--(15), not bounded enumeration.

## Novelty and literature positioning

Kullmann and Zhao establish preservation of minimal unsatisfiability and
deficiency under singular DP and analyze confluence and singularity indices.
The committed Ramsey-extension work supplies the pure signed first fan and the
canonical \(F_p\) endpoint. A search of that primary SAT literature and the
committed Discovery Net graph found no statement of the potential (3), the
charge identity (11), or its Ramsey-specific concentration consequence (12).
The novelty claimed here is this elementary global accounting law and its
application to the 44-clause ancestry problem, not the imported singular-DP or
MU(2) classification.

Primary references:

- O. Kullmann and X. Zhao, *On Davis--Putnam reductions for minimally
  unsatisfiable clause-sets*, Theoretical Computer Science 492 (2013), 70--87,
  DOI `10.1016/j.tcs.2013.04.020`, arXiv:1202.2600.
- H. Abbasizanjani and O. Kullmann, *Classification of minimally
  unsatisfiable 2-CNFs*, arXiv:2003.03639.

## Scope and trust boundary

This is a necessary ancestry constraint, not a proof that no 44-clause
obstruction exists. It does not say that satisfying the charge budget is
sufficient, nor does it reconstruct intermediate clauses from charges. Unit
main clauses can contribute positive charge even with zero overlap, so
"charge" must not be read as overlap alone. The collision guard imports the
standard preservation of deficiency for singular DP on minimally
unsatisfiable clause-sets; all remaining algebra is proved here.

No SAT solver, floating point, kernel enumeration, or full-completion search
is used. Independent review is required before this theorem is used as a
dependency.

## Provenance

- MU(2) terminal normal form: Discovery Net
  `bafkreieknunurio6rogct3cb7esf2nzeqopzv3o6bcy4expkrpzvo324s4`.
- First-fan normalization \(m\le10\): Discovery Net
  `bafkreiczonudlk7sum6rdokvjzlm63isi6yriqchfiwdwpn2fkgcguyzpu`.
- Audited source commit: to be filled after publication.
- Note SHA-256: to be filled after publication.
- Certificate SHA-256: to be filled after publication.
- Checker SHA-256: to be filled after publication.

