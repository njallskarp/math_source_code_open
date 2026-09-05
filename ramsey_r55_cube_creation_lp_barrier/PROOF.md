# A fixed-seed linear composition barrier

## Domain and edit coordinates

Let \(G_0\) be the labeled graph in [SEED.json](SEED.json), with red
adjacency encoded as hexadecimal bit masks, least significant bit first.
Its SHA-256 is
9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916.
Let \(E=\{0,1,2\}\) and \(C=\{3,\ldots,42\}\). Every edge meeting
\(E\) is fixed. The seed has red degrees \(20\) on \(E\) and \(21\)
on \(C\). Each root's red neighborhood has \(92\) red edges; each
root's blue neighborhood has \(107\) blue edges.

For each central pair \(e\), let \(g_e\) be its seed red indicator and
let \(x_e\in[0,1]\) be a relaxed toggle indicator. Its final red value is

\[
y_e=g_e+(1-2g_e)x_e.
\]

For a pair meeting \(E\), set \(y_e=g_e\). A Boolean vector describes
simultaneous central edge flips; a fractional vector is only an LP
pseudomodel.

The signature \(s(v)\) records the three red incidences of \(v\) to
\(0,1,2\), with root \(0\) in the least significant bit. The signature
cell sizes, in numerical order from \(0\) to \(7\), are
\((0,8,8,6,10,4,4,0)\). An edge is *visible* if both endpoints lie
in a common red or blue neighborhood of some root. Equivalently,
\(s(u)\mathbin{\mathrm{xor}}s(v)\ne7\). There are \(656\) visible
central edges and \(124\) invisible central edges. Define

\[
V(x)=\sum_{\substack{e=\{u,v\}\subset C\\s(u)\mathbin{\mathrm{xor}}s(v)\ne7}}x_e.
\]

## The composed relaxation

Define \(P\) by precisely the following constraints.

1. All \(780\) boxes \(0\le x_e\le1\).
2. The \(40\) central degree conservation equalities and the six
   root-neighborhood same-color edge-count conservation equalities.
   These preserve the seed degrees and the values \(92,107\) above.
3. Destruction of every originally monochromatic central five-set:
   for its seed color, at least one of its ten edges is flipped.
   There are \(176\) red and \(177\) blue such rows.
4. Every colored \(K_5\) prohibition on a five-set meeting \(E\).
   Of the \(304590\) such five-sets, the colored rows whose fixed
   root edges are all in the prohibited color number \(31153\).
   Every other row is automatic from a fixed opposite-colored edge
   and the boxes.
5. Both colored prohibitions on every central five-set that is
   coordinate-mixed and has no complementary signature pair.
   Coordinate-mixed means that both bit values occur in each of the
   three signature coordinates.

The last family is the complete fully visible mixed-cube interface of
[R2's five-orbit classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_three_cube_mixed_orbits),
not a sampled or one-hole prefix. For each eligible five-set \(Q\),
it is exactly

\[
1\le\sum_{e\in\binom Q2}y_e\le9.
\]

In this proper-six-signature seed the eligible supports are
\(\{1,2,4\}\) and \(\{3,5,6\}\). Each has six positive multiplicity
patterns summing to five. Their literal instances number \(46088\),
giving \(92176\) one-sided rows.

Rows 1–4 are the full creation-sensitive repair relaxation in
[Helgi's source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_creation_sensitive_cover).
We use all its degree/profile equations and all its generated root rows,
not just the selected rows in its public dual certificate.

## Exact barrier theorem

**Theorem.** The rational vector in [primal.json](primal.json) belongs
to \(P\) and has

\[
V(x)=\frac{45941068573726913088165}{1203273626769012071456},
\qquad 38<V(x)<39.
\]

Consequently every valid lower bound on \(V\) obtained solely by linear
combination of the defining inequalities and equalities of \(P\) is
at most this value. In particular, this composition cannot give an LP
lower bound of \(39\), or an LP bound above \(39\) that would round up
to an integer lower bound of \(40\).

**Proof.** Write

\[
D=1203273626769012071456,\qquad x_e=n_e/D,
\]

where the \(780\) integers \(n_e\) are listed in lexicographic order
of central pairs in the certificate. The two supplied implementations
check each box and every defining row with integer arithmetic.
There are \(407\) strictly fractional entries.

For clarity, any colored prohibition can be evaluated directly without
a solver. For color \(c\), let \(M\) be the central pairs in the
five-set originally colored \(c\), and \(B\) its central pairs
originally colored \(1-c\). If all its fixed edges have color \(c\),
the row is

\[
\sum_{e\in M}n_e-\sum_{e\in B}n_e\ge (1-|B|)D.
\]

If a fixed edge has color \(1-c\), the prohibition is automatic.
This formula follows by counting opposite-colored edges after
simultaneous flips; it is valid also for fractional expected edge
counts.

The primary verifier visits all \(962598\) literal five-sets, checks
every required row, and reconstructs the entire mixed family from
the full cube's \(792\) signature multisets. A separately structured
checker instead enumerates compatible rooted rows, finds original
cliques recursively, and constructs mixed sets by products of the
proper signature cells. Both calculate the same exact mixed-row
evaluation table. The sum of visible numerators is the numerator
displayed in the theorem. All operations are finite integer
addition, comparison and exact rational reduction.

For the final assertion, evaluate any proposed linear consequence at
this feasible vector. A lower bound exceeding its objective value
would fail there. No exact optimality assertion is needed. \(\square\)

The inherited integer lower bound of \(39\) is preserved: the older
dual gives a fractional lower bound greater than \(38\). The present
point is compatible with that conclusion and does not establish
integer feasibility at \(39\).

## A minimal-hole missing local invariant

Let

\[
Q=\{3,10,25,28,36\},\qquad f=\{25,28\}.
\]

Its signatures are \((1,1,4,4,5)\). Every vertex is blue-adjacent
to root \(1\); every pair is visible, but the set is not
coordinate-mixed. In the seed, \(f\) is its unique blue edge and
the other nine pairs are red.

The prohibition of a newly created red \(K_5\) on \(Q\) is

\[
x_f\le\sum_{e\in\binom Q2\setminus\{f\}}x_e.
\]

For Boolean toggles this is exactly the statement that flipping
the blue hole red requires destroying at least one old red edge.
It forbids a red \(K_5\) inside the *blue* neighborhood of root
\(1\); it is not a root-containing monochromatic \(K_5\).

The certificate violates this row by

\[
x_f-\sum_{e\in\binom Q2\setminus\{f\}}x_e
=\frac{108899049810134324659}{1203273626769012071456}>0.
\]

This proves that the row is not implied even by the full composed
relaxation \(P\). It is minimum-hole among omitted violated creation
rows: all zero-hole rows are original monochromatic-clique
destruction rows already in \(P\), whereas this row has one hole.
This is not a claim of minimum proof size, a new general neighborhood
classification, or sufficiency of this single added row to prove
an integer lower bound of \(40\).

The primary checker also audits every remaining global linear clause:
this particular point violates six fully visible local clauses and
\(189\) clauses using invisible edges. These counts delimit its
scope, not a further enumeration milestone.

## Stop condition and next test

The proposed sufficiency of old destruction plus creation-sensitive
root rows plus all mixed-cube linear rows is refuted for the stated
LP target. Stop attempting to prove a stronger visible-edit bound
by rearranging only those rows.

The next falsifiable composition test is whether the complete
opposite-color-neighborhood creation interface separates this
fixed-seed low-cost relaxation, with either an exact separating
certificate or a new exact feasible point. That test requires a
fresh ownership audit. It is not permission to duplicate a direct
integer budget-\(39\) solve or Helgi's newer marked-root realization.
