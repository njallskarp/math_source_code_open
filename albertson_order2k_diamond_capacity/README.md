# Albertson order \(2k\): conformal-diamond reciprocity and Hall capacity

This note supplies one prose-level structural input after the completed
two-pass \(r=29\) scalar gate.  It neither reruns the frontier recurrence nor
enumerates more profiles.  Its new content is a uniform theorem at a
degree-\(k-1\) vertex of a \(k\)-critical graph on \(2k\) vertices: the one-triple
colouring produces a conformal diamond shared by three deletion factors, and
a two-slot Hall condition upgrades the associated strong immersion to a
subdivision of \(K_k\).

The theorem does **not** prove Albertson's conjecture for \(r=29\) and does not
eliminate any of the surviving order-58 rows.  It strictly sharpens the local
obstruction in the earlier one-triple Kempe lemma and identifies the remaining
cross-deletion input needed before that lane should resume.

**Correction and follow-up (2026-09-05).** The original public version reused
\(a_1\) in the triple and first pair and therefore displayed the wrong size for
\(N_H(v)\). The labels below are repaired. The proof mechanism is unchanged.
[`CORRECTION_AND_ALIGNMENT.md`](CORRECTION_AND_ALIGNMENT.md) proves a uniform
two-vertex-criticality separation family and explains exactly why the Tutte
interfaces at Discovery Net heights 2815 and 2831 do not control these
conformal deletion triangles.

[`ENDPOINT_EXCHANGE.md`](ENDPOINT_EXCHANGE.md) supplies the next structural
step: a unicyclic overlay theorem for the endpoint deletion factors, an exact
characterization of singleton Hall availability by a six-vertex exchange,
and a sharp degree-excess bound on the number of such short exchanges.

[`TWO_LEAF_ESCAPE.md`](TWO_LEAF_ESCAPE.md) sharpens the smallest unresolved
Hall obstruction.  In a subdivision-free critical graph, a two-leaf
same-singleton obstruction forces an induced alternating rectangle and every
factor at the unavailable endpoint must escape through a third pair.

[`MINIMAL_ESCAPE_COUNTERMODEL.md`](MINIMAL_ESCAPE_COUNTERMODEL.md) identifies
the exact limit of that local mechanism.  A fully 6-vertex-critical example
has a minimum four-by-four endpoint escape component that avoids both
Hall-obstructing pairs.  The example contains an explicit \(TK_6\), so it does
not contradict the preceding theorem; it proves that any stronger return-to-
the-target conclusion must use the global no-subdivision hypothesis rather
than criticality and overlay minimality alone.  A standard-library exact
checker accompanies the hand proof.

[`STANDARD_BRANCH_SEPARATION.md`](STANDARD_BRANCH_SEPARATION.md) gives the
uniform closure of that test.  Every target-avoiding four-block escape forces
an isolated outside edge in the representative graph, but a fully
\(k\)-vertex-critical order-\(2k\) family with three low vertices shows that the
canonical branch set still need not route.  The same family has an explicit
shifted \(TK_k\); at \(k=29\) its density is far from the frontier, isolating
degree excess or branch-set mobility as the necessary next input.

## Setup

Let \(G\) be a \(k\)-vertex-critical graph on \(2k\) vertices, let
\(H=\overline G\) be connected, and let \(d_G(v)=k-1\).  Stehlik's theorem gives a
\((k-1)\)-colouring of \(G-v\) in which every colour class has at least two
vertices.  Since \(|V(G-v)|=2k-1\), there are one triple and \(k-2\) pairs.

Every colour occurs in \(N_G(v)\), since otherwise the missing colour could be
assigned to \(v\).  It occurs there exactly once because \(d_G(v)=k-1\).  Thus we
may write

\[
\begin{aligned}
B&=N_G(v)=\{b_0,b_2,\ldots,b_{k-1}\},\\
A&=N_H(v)=\{a_0,a_1,a_2,\ldots,a_{k-1}\},\\
C_0&=\{b_0,a_0,a_1\},\qquad C_i=\{b_i,a_i\}\quad(2\leq i\leq k-1).
\end{aligned}
\]

Each colour class is independent in \(G\) and hence a clique in \(H\).

## Theorem: reciprocal deletion factors

Put

\[
D=\{v,b_0,a_0,a_1\},
\qquad M=\{a_i b_i:2\leq i\leq k-1\}.
\]

Then \(H[D]\) is the diamond \(K_4-vb_0\), and \(M\) is a perfect matching of
\(H-D\).  More precisely, the same matching \(M\) occurs in all three factor
identities

\[
\begin{array}{rcl}
H-v&:&\text{triangle }\{b_0,a_0,a_1\}+M,\\
H-b_0&:&\text{triangle }\{v,a_0,a_1\}+M,\\
H-\{v,b_0\}&:&\text{edge }\{a_0,a_1\}+M.
\end{array}
\]

### Proof

The edge \(vb_0\) belongs to \(G\), while \(va_0\) and \(va_1\) belong to \(H\).
The three vertices of \(C_0\) form a clique in \(H\), so all other pairs in \(D\)
are edges of \(H\).  Therefore \(H[D]=K_4-vb_0\).  Each pair class \(C_i\) gives
the edge \(a_i b_i\) in \(H\); these disjoint edges cover exactly \(H-D\).
The three displayed factor identities follow by adjoining the indicated edge
or triangle.  Notice that this is exact overlap, not merely the existence of
unrelated clique factors after different deletions.

## Theorem: the two-slot Hall-capacity criterion

Let \(J=H[B]\).  For every \(i\geq2\) with \(b_0b_i\in E(J)\), define

\[
S_i=\{s\in\{0,1\}:b_0-a_i-a_s-b_i\text{ is a path in }G\}.
\]

Every \(S_i\) is nonempty.  Suppose that

1. \(d_J(b_i)\leq1\) for each pair-class representative \(b_i\), \(i\geq2\); and
2. the family \(\{S_i:b_0b_i\in E(J)\}\) has an injective system of
   representatives in the two slots \(\{0,1\}\).

Then \(G\) contains a subdivision \(TK_k\).

Equivalently, if \(G\) contains no \(TK_k\), then for every degree-\(k-1\) vertex
and every colouring above, at least one of the following obstructions occurs:

- some pair representative \(b_i\) has \(d_J(b_i)\geq2\); or
- the triple representative has no two-slot Hall assignment, meaning
  \(d_J(b_0)\geq3\), or \(d_J(b_0)=2\) and the two incident nonempty availability
  sets are the same singleton.

This is strictly stronger than the earlier conclusion \(\Delta(J)\geq2\): a
2-star centred at \(b_0\) is now allowed only when its two paths compete for
the same internal triple vertex.

### Proof

For two colour classes, their representatives in \(B\) lie in the same
bichromatic component.  Otherwise, swapping the two colours in the component
of one representative removes a colour from \(N_G(v)\), allowing that colour
on \(v\), contrary to \(k\)-criticality.  Hence representatives adjacent in \(G\)
can be joined directly, while representatives nonadjacent in \(G\) have a
shortest odd bichromatic path of length three.

For \(2\leq i<j\leq k-1\), if \(b_i b_j\) is an edge of \(H\), the only possible
length-three bichromatic path is

\[
b_i-a_j-a_i-b_j.
\]

If \(b_0b_i\) is an edge of \(H\), the only possible length-three paths are

\[
b_0-a_i-a_0-b_i,
\qquad b_0-a_i-a_1-b_i.
\]

This proves \(S_i\) is nonempty.  Choose the direct edge for every branch pair
that is adjacent in \(G\), the forced path above for every edge of
\(J[B-\{b_0\}]\), and, using the injective system of representatives, one
available path for each edge \(b_0b_i\) of \(J\).  Add the direct paths \(vb_i\).
The branch set is \(\{v\}\cup B\).

An internal vertex \(a_i\), \(i\geq2\), occurs only on paths corresponding to
edges of \(J\) incident with \(b_i\); condition 1 therefore permits it on at
most one chosen path.  The special vertices \(a_0,a_1\) occur only on paths
from \(b_0\), and condition 2 assigns them injectively.  Thus the chosen branch
paths are internally vertex-disjoint.  They form a subdivision of \(K_k\).

For a family of nonempty subsets of a two-element set, failure of an
injective system of representatives is equivalent to having at least three
sets, or exactly two equal singleton sets.  This gives the stated
contrapositive.

## Exact \(r=29\) consequence and stop condition

The independently reproducible height-2761 frontier leaves

\[
(n,m)\in\{(58,838),(58,839),(58,840)\}.
\]

Their degree excesses over 28 imply at least 6, 4, and 2 degree-28 vertices,
respectively.  At every such vertex, and for every Stehlik colouring, the
reciprocal-diamond identities hold.  If the graph is a counterexample to
Albertson's conjecture, it contains no \(TK_29\), so every one of these local
diamonds must exhibit one of the two explicit capacity obstructions above.

No row is eliminated by this local dichotomy alone.  For a degree-28 vertex
\(v\), let \(\mathcal F_v\) denote the set of all labelled \(K_3+27K_2\) factors of
\(H-v\) arising from Stehlik colourings as in the setup.  The smallest credible
new input that would justify resuming order 58 is therefore a **cross-diamond
capacity theorem** of the following precise form:

> In the complement of a 29-critical order-58 graph with at least two
> degree-28 vertices, there are a low vertex \(v\) and a factor in
> \(\mathcal F_v\) for which every pair representative has degree at most one in
> \(H[N_G(v)]\) and the availability sets at the triple representative admit an
> injective system of representatives in \(\{0,1\}\).

Together with the theorem above, that statement would produce a \(TK_29\) and
eliminate the entire order-58 family.  It is recorded as a missing theorem,
not asserted or used.  A weaker quantitative overlap result would also be
decisive if it forced at least 225 additional units in the summed
one-deletion crossing bound for the tight row \((58,840)\).

The lane remains stopped until an independent review accepts the present
local theorem and a proof, counterexample, or quantitatively useful weakening
of that cross-diamond statement is available.  Further scalar recurrence or
profile enumeration is outside the gate.

## Exact excess saturation barrier

[`EXCESS_SATURATION_BARRIER.md`](EXCESS_SATURATION_BARRIER.md) pins the
degree-excess route to its sharp classical boundary.  For a genuinely
\(k\)-critical graph of order \(2k\), Kostochka--Stiebitz gives
\(X\geq2(k-3)\), with equality attained.  Below \(X=2k\), only the three values
\(2k-6,2k-4,2k-2\) exist.  At \(k=29\) these are exactly the three surviving
order-58 rows.

This corrects the scope of the standard-branch separation family: that
family is vertex-critical and has \(X=1308\) at \(k=29\), so it does not test the
near-extremal edge-critical input.  Any resumption must exclude the local
four-block footprint in the three exact excess classes, not seek another
generic degree count.

## Edge-deletion absorption dichotomy

[`EDGE_DELETION_ABSORPTION.md`](EDGE_DELETION_ABSORPTION.md) determines
exactly which proper-subgraph criticality tests can add information inside
the two-leaf eight-vertex footprint.  Eleven forced graph edges have explicit
three-clique covers after deletion, so their criticality is automatic from
the base diamond and rectangle.  The only non-absorbed edges are missing
incidences from the unavailable endpoint to the obstructing pairs; deleting
one of those forces the colouring witness to alter a third pair class.

The accompanying exact checker exhausts all seven blocker states.  This is a
structural interface theorem, not a new scalar recurrence or a frontier-row
elimination.

## Dependency pinning

The detailed graph-to-frontier audit is in [`DEPENDENCY_AUDIT.md`](DEPENDENCY_AUDIT.md).
The essential point is that the \(r=27\), \(r=28\), and \(r=29\) results are not a
linear theorem chain:

- the reviewed \(r=27\) terminal result has a topology-free barrier--Gallai
  route, which is the preferred downstream dependency;
- the reviewed \(r=28\) result is independent of the \(r=27\) terminal theorem;
- the \(r=29\) frontier uses the generic convex deletion recurrence and stated
  results from the Cranston and Sadhu preprints, but no \(r=27\) or \(r=28\)
  terminal theorem and no value \(\operatorname{cr}(24,132)\geq165\).

The present theorem depends only on Stehlik's colouring theorem and elementary
Kempe-chain reasoning.  Its conditional \(r=29\) application additionally
depends on the height-2761 frontier.

## Reproduction and trust boundary

There is no numerical computation in this note.  To verify that a local copy
matches the published source, run

```sh
cd albertson_order2k_diamond_capacity
PYTHONDONTWRITEBYTECODE=1 python3 verify_excess_saturation.py \
  | diff -u EXPECTED_EXCESS_SATURATION.txt -
PYTHONDONTWRITEBYTECODE=1 python3 verify_edge_deletion_absorption.py \
  | diff -u EXPECTED_EDGE_DELETION_ABSORPTION.txt -
shasum -a 256 -c SHA256SUMS
```

Expected output is one `OK` line for each source file.  The hash check verifies
source identity only; the proof is the prose argument above and remains
human-audited mathematics.  No private data, solver output, floating-point
calculation, crossing-number table, or topology classification is used.

## Primary-source scope

Primary sources checked on 2026-09-05:

- Matej Stehlik, [*Critical Graphs with Connected
  Complements*](https://doi.org/10.1016/S0095-8956(03)00069-8).
- Daniel W. Cranston, [*Progress on Albertson's
  Conjecture*](https://arxiv.org/abs/2512.08020v1).
- Ankan Sadhu, [*Albertson's Conjecture Holds for r at Most
  26*](https://arxiv.org/abs/2609.01682v1).

The two latter items are recent preprints, not published journal results.
They are relevant only to the conditional frontier application, not to the
unconditional conformal-diamond and Hall-capacity theorems.  The bounded
literature and Discovery Net searches found no statement of these exact
order-\(2k\) overlap and two-slot criteria; this is a scoped novelty audit, not
an exhaustive priority claim.
