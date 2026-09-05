# Conditional completion theorem

## Statement

Let \(G\) be a red-blue coloring of all pairs of \(\{0,\ldots,42\}\).
Assume that it extends [PARTIAL.json](PARTIAL.json), obeys the three degree
intervals in the README, and has exactly the cell-pair counts in
[PROFILE.json](PROFILE.json). Then \(G\) contains a monochromatic \(K_5\).

The argument is a complete finite refutation of these assumptions together
with the absence of both colored \(K_5\)'s. No condition is placed on just
a sampled set of completions.

## Primary variables and global constraints

Number the 400 free pairs in lexicographic order. Variable \(x_e\) is true
exactly when pair \(e\) is red. For a five-set \(Q\), its red prohibition is
the disjunction of the negations of all ten edge variables; its blue
prohibition is the disjunction of the ten positive variables. Substitute
every fixed edge color. A fixed edge of the opposite color discharges the
corresponding clause; otherwise retain exactly the literals on free pairs.

Deduplication leaves 51,624 distinct clauses. They are equivalent to the
absence of a monochromatic five-set in a completion of the partial matrix.
The auditor reconstructs them by enumerating five-cliques in each graph of
edges that could still have the selected color. This differs from the
producer's direct enumeration of all five-subsets.

The parent generator also inserts local-neighborhood clauses. A same-color
four-clique in an anchor neighborhood becomes a global five-clique on adding
that anchor. An opposite-color five-clique is already a global five-clique.
The remaining mixed clauses also prohibit actual global five-cliques.
The auditor checks these assertions at the literal level: after subtracting
every required counter clause, the remaining clause support is exactly the
global support, with possible duplicates and no extra condition.

## Cardinality blocks and canonical extensions

Subtract the known red pairs from each degree bound and cell-count equation.
The resulting bounds concern lists of free-edge literals. Lower bounds are
rewritten as upper bounds on the negated literals. There are 112 nonvacuous
upper-bound blocks.

For a block with Boolean literals \(y_0,\ldots,y_{n-1}\) and bound
\(\sum_i y_i\leq t\), the nontrivial threshold grid has nodes
\(s_{k,j}\), where \(0\leq k<t\) and \(0\leq j<n-t\).
The first-row implication is \(y_j\Rightarrow s_{0,j}\).
Horizontal implications are \(s_{k,j}\Rightarrow s_{k,j+1}\) wherever the
latter node exists. Interior implications are

\[
(s_{k,j}\wedge y_{j+k+1})\Rightarrow s_{k+1,j}.
\]

At the last row the forbidden conjunction is
\(s_{t-1,j}\wedge y_{j+t}\). These implications are exactly the binary and
ternary clauses independently reconstructed in `audit.py`. Bounds zero and
\(n-1\) use negative units and a single all-negative clause respectively;
a bound at least \(n\) is vacuous.

Every assignment satisfying the cardinality bound extends to all grid clauses
by setting

\[
s_{k,j}=1
\quad\Longleftrightarrow\quad
\sum_{i=0}^{j+k}y_i\geq k+1.
\]

The first-row, horizontal and interior implications follow immediately from
prefix counting. A violated last-row clause would force at least \(t+1\)
true literals, contradicting the bound. The same extension works when the
\(y_i\) are negative edge literals. Distinct blocks have disjoint auxiliary
variables. Thus every graph in the asserted family with no monochromatic
\(K_5\) would extend to a satisfying assignment of the final CNF. This
direction alone suffices for the exclusion.

The auditor reconstructs the exact allocation and signs of all 26,320
counter clauses, starting above primary variable 400 and ending at 13,600.
It also checks the header, complete clause count, literal ranges, absence
of tautologies, and exact remaining global-clause support.

## Refutation and removal of discovery assumptions

Discovery used a larger 499,785-clause formula with complete-column decision
diagrams. Its UNSAT trace passed RUP-only checking. Trimming removed all
decision-diagram variables: the resulting trace uses no variable above
13,600 and passes a second RUP-only replay against the final 88,433-clause
formula. The final replay does not receive any decision-diagram clauses.

Consequently the final CNF is unsatisfiable independently of any correctness
or completeness assertion about those discovery aids. Combining this checked
refutation with the canonical extension above proves the stated conditional
completion theorem. Both stages were repeated after fresh source regeneration.

## Boundaries

The exact matrix, degree intervals, and 36 cell counts are hypotheses. They
must not be discarded when using this theorem. Other core pairs, other
profiles, and the complete \(d=22\) or deficiency-six frontier are not
excluded. The underlying height-2951 fractional limitation is not
contradicted. Independent mathematical review of this new encoding bridge
and certificate remains pending.
