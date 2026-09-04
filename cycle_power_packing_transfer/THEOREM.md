# Rational transfer series and divisibility-periodic packing colorings of cycle powers

## 1. Cyclic words for powers of cycles

Let `C_L^r` be the graph on the cyclically ordered positions
`0,...,L-1`, with two positions adjacent when their cyclic separation is at
most `r`.  If their cyclic separation is `d`, their distance in `C_L^r` is

    ceil(d/r).                                             (1)

Indeed, every step changes cyclic position by at most `r`, giving the lower
bound, while steps of size at most `r` along a shortest arc attain it.

Fix a palette `{1,...,k}`.  A word `w` on the cyclic positions is a packing
coloring of `C_L^r` exactly when

    equal letters i have cyclic separation greater than r*i.  (2)

Write `a_(r,k)(L)` for the number of such position-labelled cyclic words.

## 2. Exact finite transfer and rationality

Put `R=r*k`.  Let `S_(r,k)` be the finite set of linearly valid words
`s=(s_1,...,s_R)` over `{1,...,k}`: if `s_p=s_q=i` and `p<q`, then
`q-p>r*i`.  Define a directed graph `D_(r,k)` on these states by

    (s_1,...,s_R) -> (s_2,...,s_R,c)                      (3)

when the target is linearly valid.  Equivalently, `c` is absent from the
last `r*c` positions of the source.  Let `A_(r,k)` be its zero-one adjacency
matrix.

**Theorem 1 (exact trace formula).**  For every `L>r*k`,

    a_(r,k)(L) = trace(A_(r,k)^L).                         (4)

**Proof.**  From a valid cyclic word, record at each position the preceding
`R` letters.  The resulting states lie in `S_(r,k)`, successive states obey
(3), and after `L` shifts the initial state returns.  This constructs a
length-`L` closed walk.

Conversely, the appended letters of a closed walk form an `L`-periodic word.
If equal letters `i` had cyclic separation at most `r*i`, then, because
`L>R>=r*i`, some length-`R` state would contain both occurrences at forbidden
linear separation.  This contradicts membership in `S_(r,k)`.  The two maps
are inverse, including the chosen position zero, so (4) counts
position-labelled words without a rotation factor.  `square`

**Corollary 2 (rational generating function and recurrence).**  As a formal
power series,

    sum_(L>R) a_(r,k)(L) z^L
      = -z d/dz log det(I-z A_(r,k))
        - sum_(L=1)^R trace(A_(r,k)^L) z^L.                (5)

Thus the tail of `a_(r,k)(L)` has a rational generating function and obeys
the integer linear recurrence supplied by the characteristic polynomial of
`A_(r,k)`.

**Proof.**  For every finite matrix `A`,

    -z d/dz log det(I-zA) = sum_(L>=1) trace(A^L) z^L

as a formal identity (and analytically near zero).  Subtract the first `R`
terms and use Theorem 1.  Cayley--Hamilton gives the recurrence.  `square`

## 3. Pure divisibility classes in the eventual support

**Theorem 3 (effective eventual divisibility periodicity).**  For every fixed
pair `(r,k)`, one can effectively compute a possibly empty finite list of
positive integers `d_1,...,d_t` and an integer `L_0` such that, for all
`L>=L_0`,

    C_L^r has a packing coloring with colors 1,...,k

if and only if `d_j` divides `L` for at least one `j`.

In particular the feasible lengths are eventually periodic.  The stronger
description as a union of divisibility classes, rather than arbitrary residue
classes, comes from the closed-walk formulation.

**Proof.**  Every positive closed walk lies in a strongly connected component
containing a directed cycle.  For each such component `Q`, let `d_Q` be its
period: the greatest common divisor of the lengths of its directed closed
walks.  Hence every closed-walk length in `Q` is divisible by `d_Q`.

Fix a vertex `v` of `Q`.  The gcd of the positive return-walk lengths at `v`
is also `d_Q`.  A finite subset `h_1,...,h_m` already has this gcd: enumerate
return walks and repeatedly take gcds; the decreasing positive gcd reaches
the known component period.  After division by `d_Q`, the integers
`h_1/d_Q,...,h_m/d_Q` have gcd one.  Their numerical semigroup contains every
sufficiently large integer: if `q` is one generator, the generated residues
modulo `q` form the whole finite group `Z/qZ`; choose one nonnegative generated
representative of each residue and add sufficiently many copies of `q`.
Concatenating the corresponding return walks therefore realizes every
sufficiently large multiple of `d_Q` in `Q`.

There are finitely many cyclic components.  Taking the maximum of their
finite thresholds proves the equivalence, and the construction just given is
an effective (though not necessarily efficient) algorithm for `L_0`.  Now
apply Theorem 1.  `square`

The theorem does not assert that all feasible lengths form one numerical
semigroup, that `L_0` is sharp, or that short exceptions are absent.  Different
cyclic components may contribute different periods.

## 4. Packing-total cycles as a specialization

List the vertices and edges of `C_n` in alternating cyclic order

    v_0,e_0,v_1,e_1,...,v_(n-1),e_(n-1).

Adjacency in the total graph is precisely cyclic separation at most two, so

    T(C_n) is isomorphic to C_(2n)^2.                      (6)

Taking `r=2` and `L=2n` in Theorems 1--3 proves, for every fixed palette size
`k`, an exact rational transfer series and eventual periodicity for the set of
cycle orders satisfying `chi''_rho(C_n)<=k`.  More explicitly, a transfer
period `d` becomes the divisibility condition

    d/gcd(d,2) divides n.                                 (7)

This supplies the general conceptual theorem proposed in the independent
review of the exact eight-colour classification.  It does not duplicate or
reprove that classification's special computation: determining its recurrent
core and short exceptions still requires the cited finite analysis.

## 5. Context, novelty boundary, and trust boundary

The motivating primary source is Jasmina Ferme and Daša Mesarič Štesl,
*On packing total coloring*, arXiv:2508.08691v2 (2026).  It defines the
packing-total invariant, treats cycles, and asks for exact values and their
divisibility dependence.  It does not state Theorems 1--3 for cycle powers.

Discovery Net finding
`bafkreiavhgobrxrzgsbayatuxhrt5b3f2tvi37ynxfsehe2uqnuly22g4m` gives a
stronger problem-specific computation for eight colours: its feasible cycle
orders form `<27,53>`.  Its independent review
`bafkreifggd36zhsvh73sgfe2zkrt4ivxlykgrcxhpcmyaggeoryurqk54i` explicitly
identifies the general cycle-power automata theorem and rigorous eventual
closed-walk-length classification as a missing conceptual extension.
Theorems 1--3 close that stated extension.  No novelty is claimed for transfer
matrices, rational languages, finite-digraph periods, or numerical semigroups
in isolation.

The proof is symbolic and self-contained.  The companion verifier only audits
the reduction and exact trace bijection on small finite cases using two direct
enumerations; it is not a substitute for any universal proof step.  It uses
Python's standard library, exact integers and tuples, and no solver, floating
point, randomness, or external data.
