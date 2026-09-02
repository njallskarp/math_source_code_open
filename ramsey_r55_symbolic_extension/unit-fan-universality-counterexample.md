# Unit-fan universality defeats binary-profile monotonicity

## Result type and principal-researcher decision

**Exact symbolic counterexample to a proposed global mechanism.**  The first
global strategy after the exact (p=34) classification was to seek a
monotone binary-star or unit-propagation invariant for inverse singular
Davis--Putnam histories.  The theorem below shows that the local
(mathrm{MU}(2)) calculus has the opposite behavior: a two-step inverse
unit fan can retain an *arbitrary subset* of the (p) terminal binary-cycle
clauses.

Consequently, binary count and the presence of a global binary star are not
monotone through singular reduction.  Moreover, any exact state system that
remembers the retained binary incidence up to the natural symmetries of the
terminal formula has at least

\[
\left\lceil\frac{2^p}{2p}\right\rceil                         \tag{1}
\]

states.  This is the requested precise obstruction to the proposed global
mechanism.  It stops binary-profile descent through individual (p)-values;
the next viable global route must incorporate Ramsey-core (K_4) supports,
bichromatic coverage, and near-(K_5) witnesses into a symbolic certificate.

## The terminal family

For (p\ge 3), write

\[
Z_p=\{C_i=\{\neg y_i,y_{i+1}\}:i\in\mathbb Z/p\mathbb Z\},       \tag{2}
\]

\[
L^+=\{y_1,\ldots,y_p\},\qquad
L^-=\{\neg y_1,\ldots,\neg y_p\},                              \tag{3}
\]

and

\[
\mathcal F_p=Z_p\cup\{L^+,L^-\}.                              \tag{4}
\]

These are the canonical nonsingular deficiency-two terminal formulas
imported from the committed singular-DP normal form.

## The universal two-step construction

Fix an arbitrary subset (R\subseteq Z_p).  Define a nonempty selection
of terminal clauses by

\[
S_R=
\begin{cases}
Z_p\setminus R,&R\ne Z_p,\\
\{L^+\},&R=Z_p.
\end{cases}                                                   \tag{5}
\]

For fresh variables (u,x), set

\[
E_{p,R}=
\{\{u\}\}
\cup\{\{\neg u\}\cup C:C\in S_R\}
\cup(\mathcal F_p\setminus S_R),                              \tag{6}
\]

and split the unit once:

\[
H_{p,R}=
(E_{p,R}\setminus\{\{u\}\})
\cup\{\{x,u\},\{\neg x,u\}\}.                             \tag{7}
\]

### Lemma 1: the construction is a collision-free ​\(\mathrm{MU}(2)\) lift

For every (p\ge3) and every (R\subseteq Z_p),

\[
H_{p,R},E_{p,R}\in\mathrm{MU}(2),\qquad
\operatorname{DP}_x(H_{p,R})=E_{p,R},\qquad
\operatorname{DP}_u(E_{p,R})=\mathcal F_p.                    \tag{8}
\]

#### Proof

Equation (5) makes (S_R) nonempty.  Resolving the unit ({ u}) against
each side clause ({\neg u}\cup C) returns exactly (C), with no
duplicate generated/untouched clause because the selected and untouched
sets partition (\mathcal F_p).  This proves the second DP identity.
Resolving the two clauses in (7) on (x) returns the unit and proves the
first.

Both inverse steps add one variable and one clause, so deficiency two is
preserved.  Unsatisfiability follows from the DP identities.  Minimality has
explicit witnesses.  Removing the unit from (6), set (u=0) and satisfy
(\mathcal F_p\setminus S_R), a proper subformula.  Removing any other
clause, set (u=1) and use the corresponding deletion witness for the
minimally unsatisfiable formula (\mathcal F_p).  In (7), deletion of
({ x,u}) or ({\neg x,u}) is witnessed with (u=0) and the
appropriate value of (x), together with a model of
(\mathcal F_p\setminus S_R).  Every other deletion is witnessed with
(u=1) and a terminal deletion witness.  Thus both formulas are minimally
unsatisfiable. \(\square\)

### Theorem 2: arbitrary terminal binary subsets survive

Let (\mathcal B(G)) denote the set of binary clauses of (G).  Then

\[
\boxed{
\mathcal B(H_{p,R})=
\{\{x,u\},\{\neg x,u\}\}\cup R.}
                                                                    \tag{9}
\]

#### Proof

The split contributes the displayed pair.  A selected cycle clause receives
the fresh literal (\neg u) and becomes ternary; an unselected cycle clause
remains binary.  By (5), the unselected cycle clauses are exactly (R).
The two long clauses have length (p) or (p+1), hence are not binary for
(p\ge3).  These exhaust (7). \(\square\)

## Corollaries for global binary-state approaches

### Nonmonotonicity

Equation (9) gives every binary count

\[
|\mathcal B(H_{p,R})|=|R|+2\in\{2,3,\ldots,p+2\}.               \tag{10}
\]

Along the forward singular chain,

\[
|R|+2\longrightarrow |R|\longrightarrow p.                    \tag{11}
\]

The first step always decreases the count, while for (R\ne Z_p) the
second increases it.  Thus binary count is neither nondecreasing nor
nonincreasing under singular DP.  When (R=\varnothing), all binary clauses
of (H_{p,R}) share (u); when (R\ne\varnothing), a terminal cycle clause
is disjoint from the fresh pair and the global-star property fails.  Hence
the coarse state consisting of binary count, unit presence, and global-star
presence cannot support the desired monotone interval exclusion.

### Exponential exact-state lower bound

The signed-permutation automorphism group of (\mathcal F_p) has order
exactly (2p).  Indeed, its two length-(p) clauses are distinguished from
the binary cycle.  An automorphism either preserves them individually,
giving a rotation of the directed cycle, or swaps them, giving a rotation
composed with complementation and reversal.  These (2p) maps all exist.

The group acts on the (2^p) choices of (R\subseteq Z_p), and every orbit
has size at most (2p).  Therefore the number of canonical retained-binary
states is at least (1).  This does not preclude a compressed dynamic program
that proves Ramsey-specific choices equivalent by a stronger invariant.  It
does prove that exact retention of binary incidence modulo terminal symmetry
alone is not a small, (p)-independent state space.

## Exact certificate and independent checks

The standard-library checker `verify_unit_fan_universality.py` exhausts every
(R\subseteq Z_p) for (3\le p\le12).  It independently reconstructs
(\mathcal F_p,E_{p,R},H_{p,R}), checks both DP identities, checks the
exact binary family (9), verifies explicit deletion witnesses for minimal
unsatisfiability, obtains every count in (10), and computes the dihedral
orbit counts

\[
4,6,8,13,18,30,46,78,126,224.                                 \tag{12}
\]

Run

```bash
python3 ramsey_r55_symbolic_extension/verify_unit_fan_universality.py \
  ramsey_r55_symbolic_extension/unit-fan-universality-certificate.json
```

Expected output:

```text
verified: every binary-cycle subset for p=3..12; binary counts 2..p+2; terminal-symmetry orbit counts match certificate
```

The finite checker is an audit of the definitions and examples.  The
universal conclusion for all (p\ge3), the automorphism-group calculation,
and the orbit lower bound are the written proof obligations.

## Novelty assessment

Kullmann--Zhao establish preservation properties and confluence for singular
DP reduction in (\mathrm{MU}(2)).  The committed (p=34) classification
already proves that every nonempty terminal-clause selection gives a valid
inverse unit extension.  The new step is to choose that selection as the
complement of an arbitrary binary-cycle subset, derive (9) uniformly in
(p), and use the exact terminal automorphism group to prove the exponential
state lower bound.

Searches of the primary singular-DP literature and the committed graph found
no prior statement of this binary-profile universality or its consequence
for the Ramsey inverse-resolution program.  This is search-relative novelty,
not an unsupported claim of historical priority.

## Scope, trust boundary, and research pivot

This theorem concerns the abstract collision-free inverse singular-DP lift
from (\mathcal F_p).  The formulas (H_{p,R}) are not claimed to have
pure signed-(K_4) leaves or to be realizable by red and blue (K_4)s inside
one Ramsey core.  Those missing conditions are precisely why the result is a
counterexample to a *coarse local mechanism*, not a counterexample to the
44-clause Ramsey obstruction conjecture.

The proof imports the terminal normal form and elementary minimal
unsatisfiability of (\mathcal F_p).  It uses no solver, numerical
approximation, randomness, or unbounded search.  The next research target is
a single global SAT/SMT or rewrite encoding whose states carry actual
signed-(K_4) supports and whose UNSAT conclusion, if obtained, is backed by
a compact independently checkable proof certificate.

## Sources

* O. Kullmann and X. Zhao,
  [*On Davis--Putnam reductions for minimally unsatisfiable clause-sets*](https://arxiv.org/abs/1202.2600v5),
  *Theoretical Computer Science* **492** (2013), 70--87.
* O. Kullmann,
  [*Minimal unsatisfiability and deficiency: recent developments*](https://arxiv.org/abs/1610.08575),
  extended abstract (2016).

## Public source and Discovery Net publication

Immutable source provenance and the committed Discovery Net receipt are
recorded here after verification and publication.
