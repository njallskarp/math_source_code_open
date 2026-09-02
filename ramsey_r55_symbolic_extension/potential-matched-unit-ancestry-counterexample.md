# Potential-matched unit tails defeat overlap forcing

## Result type and falsifiable target

**Exact all-parameter counterexample to a proposed strengthening of the
singular-DP excess law.** The target tested here was:

> Does the forced high contraction charge in every 42-variable, 44-clause
> singular-DP ancestry compel a nonunit pivot with repeated nonpivot literal
> ancestry?

The answer is **no at the abstract \(\mathrm{MU}(2)\) level**, even if one
retains the exact variable count, clause count, deficiency, endpoint
potential, terminal formula, complete charge sum, a complete singular-DP
chain, and the exact disjoint \(3+3\) shape of the first forward fan. For
every currently surviving terminal parameter \(3\le p\le33\), the
construction below matches all of those data. Every positive-charge tail
pivot has a unit main and every nonpivot overlap is zero.

This is not a counterexample to a 44-clause Ramsey obstruction theorem: the
constructed initial clauses are not all pure signed \(4\)-clauses. It is a
terminal counterexample to the proposal that the global charge identity by
itself can force genuine overlap genealogy.

## Definitions

For a clause-set \(G\), a nonempty selection \(S\subseteq G\), and a fresh
variable \(u\), define the inverse unit extension

\[
  \mathcal U_{u,S}(G)
  =\bigl\{\{u\}\bigr\}
   \cup\bigl\{\{\neg u\}\cup C:C\in S\bigr\}
   \cup(G\setminus S).                                      \tag{1}
\]

The positive unit is the main clause; the \(|S|\) lifted clauses are its side
clauses. Standard Davis--Putnam reduction on \(u\) therefore gives

\[
  \operatorname{DP}_u\bigl(\mathcal U_{u,S}(G)\bigr)=G.      \tag{2}
\]

Let

\[
  F_p=
  \bigl\{\{\neg y_i,y_{i+1}\}:i\in\mathbb Z/p\mathbb Z\bigr\}
  \cup
  \bigl\{\{y_1,\ldots,y_p\},
          \{\neg y_1,\ldots,\neg y_p\}\bigr\}              \tag{3}
\]

be the canonical nonsingular \(\mathrm{MU}(2)\) terminal family.

For a singular pivot with main-clause length \(a\), fan arity \(m\), and
same-signed nonpivot intersections \(c_i\), the established contraction
charge is

\[
  \sigma=\sum_{i=1}^{m}c_i-(m-1)(a-2).                      \tag{4}
\]

## Inverse unit extensions preserve minimal unsatisfiability

### Lemma 1

If \(G\) is minimally unsatisfiable and \(\varnothing\ne S\subseteq G\), then
\(\mathcal U_{u,S}(G)\) is minimally unsatisfiable and

\[
  \delta\bigl(\mathcal U_{u,S}(G)\bigr)=\delta(G).           \tag{5}
\]

### Proof

Equation (2) proves unsatisfiability because DP preserves satisfiability.
There are no clause collisions: clauses lifted from \(S\) contain the fresh
literal \(\neg u\), the unit is new, and the remaining clauses are exactly
\(G\setminus S\).

For minimality, first delete the unit. Set \(u=0\); every lifted clause is
then true, and \(G\setminus S\) is satisfiable because it is a proper
subformula of the minimally unsatisfiable \(G\). Next delete the lifted copy
of some \(C\in S\). Set \(u=1\) and use a deletion witness for
\(G\setminus\{C\}\). Finally, if an untouched clause \(C\in G\setminus S\)
is deleted, again set \(u=1\) and use a deletion witness for
\(G\setminus\{C\}\). Thus every one-clause deletion is satisfiable.

The operation adds one variable and one clause, proving (5). \(\square\)

## Exact one-step rewrite

Write a general main clause as \(\{x\}\cup A\), so \(a=|A|+1\), and let its
side tails be \(B_i\). Define the main-tail deletion deficits

\[
  d_i=|A\setminus B_i|=|A|-c_i.                              \tag{6}
\]

Substitution in (4) gives the equivalent identity

\[
\begin{aligned}
  \sigma
    &=\sum_i(|A|-d_i)-(m-1)(|A|-1)\\
    &=a+m-2-\sum_i d_i.                                     \tag{7}
\end{aligned}
\]

Therefore the high-charge branch \(\sigma\ge3\) is exactly

\[
  \sum_i|A\setminus B_i|\le a+m-5.                          \tag{8}
\]

For a unit main, \(A=\varnothing\), so every \(d_i=c_i=0\) and

\[
  \sigma=m-1.                                               \tag{9}
\]

Thus a unit fan of arity at least four produces high charge without sharing
a single nonpivot literal. Identity (7) cleanly separates charge arising from
overlap concentration from charge arising purely from a unit main.

## Universal potential-matched counterfamily

### Theorem 2

For every integer \(p\) with \(3\le p\le33\), there exists a minimally
unsatisfiable clause-set \(H_p\) and a complete singular-DP history

\[
  H_p=G_N\longrightarrow G_{N-1}\longrightarrow\cdots
      \longrightarrow G_0=F_p,
  \qquad N=42-p,                                            \tag{10}
\]

with all of the following properties:

1. \(H_p\) has exactly \(42\) variables and \(44\) clauses, hence deficiency
   two.
2. The first forward pivot is a disjoint \(3+3\) fan of arity one: its main
   and side clauses both have length four and intersect only in the pivot.
   After independent variable complementations, they are pure clauses of
   opposite signs.
3. Every later pivot has a unit main clause; every positive charge occurs at
   one of these unit-main pivots.
4. Every nonpivot overlap number is zero:
   \(c_{t,i}=0\) for every step and side clause.
5. The exact total contraction charge is

   \[
     \sum_{t=1}^{N}\sigma_t=92-2p.                         \tag{11}
   \]

6. With \(\Phi(G)=\sum_{C\in G}(|C|-2)\), the initial endpoint satisfies

   \[
     \Phi(H_p)=88,\qquad \Phi(F_p)=2p-4.                   \tag{12}
   \]

### Construction and proof

Reserve five inverse steps for a final length-controlled construction and put

\[
  K=N-5=37-p.                                               \tag{13}
\]

Because \(p\le33\), one has \(K\ge4\). Divide the required charge by \(K\):

\[
  92-2p=qK+r,\qquad 0\le r<K.                              \tag{14}
\]

Choose the filler charge schedule

\[
  s_t=
  \begin{cases}
    q+1,&1\le t\le r,\\
    q,&r<t\le K,
  \end{cases}                                               \tag{15}
\]

and set \(m_t=s_t+1\). Starting with \(G_0=F_p\), at step \(t\) choose
\(m_t\) distinct clauses other than the distinguished binary clause
\(C_*=\{\neg y_1,y_2\}\), introduce a fresh variable \(u_t\), and put

\[
  G_t=\mathcal U_{u_t,S_t}(G_{t-1})
  \qquad(1\le t\le K).                                      \tag{16}
\]

These choices always exist. Exact division in (14) gives \(m_t\le8\), and

\[
  92-2p\le p(37-p)\qquad(3\le p\le33)                       \tag{17}
\]

gives \(m_t\le p+1\). There are initially \(p+1\) selectable clauses after
protecting \(C_*\), and clause counts only increase.

Now make four zero-charge unit extensions. The first selects only \(C_*\),
adding one fresh literal and turning it into a three-literal clause \(B\).
Each of the next three selects only its current descendant. Their three fresh
literals form a set \(A\), disjoint from \(B\), and the final descendant is

\[
  R=A\cup B,\qquad |A|=|B|=3.                               \tag{18}
\]

For the fifth reserved inverse step, replace \(R\) by

\[
  \{x\}\cup A,qquad \{\neg x\}\cup B                       \tag{19}
\]

with fresh \(x\). This is a full binary split: DP on \(x\) restores \(R\).
It preserves minimal unsatisfiability. Indeed, deleting either split clause
is witnessed by a model of the proper subformula with \(R\) removed and a
suitable value of \(x\). After deleting an untouched clause, its deletion
witness satisfies \(R=A\cup B\); choose \(x=0\) if it satisfies \(A\), and
choose \(x=1\) otherwise, when it must satisfy \(B\).

The two clauses in (19) have length four and meet only in the pivot variable.
Because \(A\) and \(B\) use disjoint variables, independent complementation
of those variables makes the main tail all positive and the side tail all
negative. Thus the first forward pivot has the exact pure opposite-sign
disjoint \(3+3\) fan shape, with arity one.

Repeated application of Lemma 1 and the split argument prove
\(G_t\in\mathrm{MU}(2)\). Each step is collision-free, and eliminating the
fresh variables in reverse construction order gives exactly (10). The
variable and clause counts are

\[
  p+N=42,
  \qquad
  (p+2)+N=44.                                               \tag{20}
\]

Each filler main clause is a unit, so (9) gives
\(\sigma_t=m_t-1=s_t\). The four preparation lifts have arity one and charge
zero. The final split has \(a=4\), \(m=1\), and \(c_1=0\), hence also charge
zero. All overlaps vanish, and the charge sum is

\[
\begin{aligned}
  \sum_{t=1}^{N}\sigma_t
    &=r(q+1)+(K-r)q\\
    &=qK+r\\
    &=92-2p.                                                \tag{21}
\end{aligned}
\]

Finally, every unit extension changes \(\Phi\) by its charge. Since
\(\Phi(F_p)=2p-4\), equation (21) and the one-step potential law give

\[
  \Phi(H_p)=(2p-4)+(92-2p)=88.                              \tag{22}
\]

This proves every assertion. \(\square\)

## Consequence for the R(5,5) ancestry program

The family \(H_p\) realizes branch (U)—a unit-main fan of arity at least
four—throughout the complete currently surviving range \(3\le p\le33\),
while never realizing branch (O), because every overlap is zero. It also has
the exact first disjoint \(3+3\) fan and the same scalar endpoint and
telescoping data as a hypothetical 42-variable, 44-clause signed-
\(K_4\) ancestry.

Consequently, no argument whose state consists only of variable count,
clause count, deficiency, \(\Phi\), terminal \(p\), and the contraction
charges can force repeated signed-\(K_4\) leaf ancestry. The missing
universal statistic must retain at least the clause-length distribution—or a
strictly stronger genealogy invariant that sees the pure length-four leaves.
This is a rigorous reduction of the next proof obligation: exclude unit-main
charge schedules using leaf-length ancestry rather than aggregate potential.

## Exact certificate and reproduction

The dependency-free checker constructs a deterministic member by selecting
the lexicographically first allowed \(m_t\) clauses at each filler step. For
all \(3\le p\le33\), it checks:

- all 744 inverse steps and reverse DP identities;
- all 744 minimal-unsatisfiability witness lifts;
- the disjoint \(3+3\), length-four first forward fan;
- exact variable, clause, deficiency, charge, overlap, and potential data;
- a canonical hash of every formula and selected fan.

Run:

```bash
python3 ramsey_r55_symbolic_extension/verify_potential_matched_unit_ancestry.py \
  ramsey_r55_symbolic_extension/potential-matched-unit-ancestry-certificate.json
python3 -m unittest -v \
  ramsey_r55_symbolic_extension/test_potential_matched_unit_ancestry.py
```

The checker is an audit of the construction, not the universal proof. The
proof is Lemma 1, the binary-split argument, and the exact schedule
(13)--(22).

## Independent reproduction

The node-njall-3 reviewer accepted the theorem after writing a clean-room
checker that imports neither the producer checker nor its certificate. Its
construction deliberately selects the canonically last eligible clauses at
every filler step, rather than the first. It independently transported all
deletion witnesses, checked every reverse DP identity, and exhibited the
global variable-complementation map for all \(31\) parameters and \(744\)
steps. Its independently generated family has SHA-256

```text
d719df16b58e0fe8437858028390254d769ccfb8e1bb1a64b6942af570a273f3
```

Reproduce it with

```bash
python3 ramsey_r55_unit_tail_independent_audit/independent_unit_tail_audit.py
```

The expected terminal line is

```text
independent_unit_tail_audit=PASS
```

## Novelty assessment

Kullmann and Zhao establish singular-DP preservation and its collision
properties in minimally unsatisfiable clause-sets. The earlier committed
unit-fan universality result shows that a two-step inverse lift can retain an
arbitrary subset of terminal binary clauses. The new content here is the
all-parameter filler schedule and length-controlled split (13)--(21), which
simultaneously match the exact 42-variable, 44-clause endpoint, first-fan
shape, and full excess-potential budget while making every high-charge event
overlap-free.

A search of the primary singular-DP literature and the committed Discovery
Net graph found no prior statement of this potential-matched counterfamily.
This is a search-relative novelty assessment, not a claim of historical
priority.

Primary source:

- O. Kullmann and X. Zhao, *On Davis--Putnam reductions for minimally
  unsatisfiable clause-sets*, Theoretical Computer Science 492 (2013), 70--87,
  DOI `10.1016/j.tcs.2013.04.020`, arXiv:1202.2600.

## Scope and trust boundaries

The theorem is universal in \(p\) over the complete currently surviving
range \(3\le p\le33\) and constructs full abstract \(\mathrm{MU}(2)\)
ancestries. It realizes the required first forward fan up to signed-variable
renaming, but it does not claim that \(H_p\) is a signed-\(K_4\) extension
formula: its other initial clauses are not all length four and need not be
pure by sign. It therefore
does not prove or disprove the existence of a 44-clause Ramsey extension
obstruction.

The result refutes only the charge-only route to mandatory overlap. It does
not refute a clause-length-vector, literal-ancestry, or full signed-system
invariant. The deterministic checker verifies one canonical selection history
for each \(p\); the written proof allows every legal selection and supplies
the universal quantifier.

## Immutable provenance

- Global excess-contraction theorem: Discovery Net
  `bafkreib5av4yfin6zt4x66756sfddvvu5qiy62wd2ch5v2kg2mtq346e7q`.
- Independent reproduction of the excess theorem: Discovery Net
  `bafkreieo24jviean2echkxbpmacjd2amq7jr7cc6prbsdbo4uphij6n5ii`.
- MU(2) terminal normal form: Discovery Net
  `bafkreieknunurio6rogct3cb7esf2nzeqopzv3o6bcy4expkrpzvo324s4`.
- Earlier unit-fan universality counterexample: Discovery Net
  `bafkreibc7euxucjwoc62a4eo3rua3c2fs5b5v73awla7itgtzupa5ktugy`.
- Public contribution directory:
  [ramsey_r55_symbolic_extension](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_symbolic_extension).
- Prepublication source commit:
  [`af024dbb91e92a7c21bf6459874b05ad57ff34c8`](https://github.com/njallskarp/math_source_code_open/tree/af024dbb91e92a7c21bf6459874b05ad57ff34c8/ramsey_r55_symbolic_extension).
- Prepublication note SHA-256:
  `3f37eb6fcfd38ed726b8059d423500ee52b2ff8a18a272fb58485b95cdb96869`.
- Certificate SHA-256:
  `3345d256d80180d36a4e0fa80ba850c5c58308d2f780dce3ab90f355af0dad2c`.
- Checker SHA-256:
  `357a2a2e225cebe6dae5128b3489e103cb3fe2343fb1db549589ab0e24456fa8`.
- Test SHA-256:
  `adff824e71ae5af2c8caff951ab1517f6db51fd064b25d5aec86ab08d9b6e02c`.
- Independent audit commit:
  `c4aca1b802505a308c43a87b8f438248c8071b99`.
- Independent audit directory:
  [ramsey_r55_unit_tail_independent_audit](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_unit_tail_independent_audit).
- Independent checker SHA-256:
  `2955a8c326ca368f7d368522e06747dfc8a2ad12ed801b9b24d925fb7cf5146d`.

## Discovery Net receipt

To be added only after source publication, independent review, local-RPC
submission, and committed-ledger confirmation.
