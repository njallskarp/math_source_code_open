# Dense five-separator Ramsey neighborhoods

Let \(R(4,5;22)\) denote the 22-vertex simple graphs with no clique of order
four and no independent set of order five. This package extends the reviewed
degree-five classification to **every graph with a small separator**, including
cuts that were not assumed to isolate a single vertex.

**Theorem.** If \(H\in R(4,5;22)\), \(e(H)\ge109\), and deleting at most five
vertices disconnects \(H\), then \(H\) is one of the thirteen graphs in
`inputs.json`. Each has exactly 109 edges, connectivity five, and a unique
five-vertex separator: the neighborhood of its unique degree-five vertex.
Thus there are exactly thirteen marked pairs \((H,S)\) in the stated family,
up to isomorphism. All non-singleton small-separator component cases are excluded.

In particular,

\[
e(H)\ge110\quad\Longrightarrow\quad\kappa(H)\ge6.
\]

The density threshold for this six-connectivity conclusion is sharp: all
thirteen density-109 graphs have connectivity five. We do not claim that six
is the optimal connectivity lower bound at density 110, or a sharp density
threshold for the Hamiltonicity consequences below.

The new universal step is a short combinatorial theorem. The thirteen-class
degree-five census and its nonisomorphism/completeness proof are imported
from the [earlier classification](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification),
commit `8bf27902fba404e35593c90cbc7d2991abeda510`, Discovery Net h3349,
`bafkreih2kf4w7r2t7vzhikr7hwxzhuzxzoqweobk23wsw3oaekq3pxwn3e`.
Its [independent review](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_degree_five_classification_independent_review),
commit `c532b04e3214bb02d0cf799f2e66157a5b523d47`, accepted it; the canonical
formatting-corrected graph review is h3355,
`bafkreibx32qk5i5a4xombv5rsgqi5jkwj7p3w4sxjo67c7t4g7ihwmnl7e`.
That review is of the imported census, not of this new separator theorem.

## The separator-to-degree bridge

We first prove, without a density hypothesis or catalogue enumeration,

\[
H\in R(4,5;22),\quad\kappa(H)\le5
\quad\Longrightarrow\quad\delta(H)\le5.
\]

Let \(S\) be a separating set of size \(s\le5\). The independence numbers
of the components of \(H-S\) sum to at most four. Since there are at least
two components, each has independence number at most three. The classical
bounds \(R(4,2)\le4\), \(R(4,3)\le9\), and \(R(4,4)\le18\) give order
capacities 3, 8, and 17 for independence numbers 1, 2, and 3, respectively.

At least 17 vertices survive. Among independence-budget partitions into
at least two positive parts with sum at most four, only \(1+3\) can hold
17 vertices. In particular, \(2+2\), \(1+1+2\), and \(1+1+1+1\) have
capacities only 16, 14, and 12. Thus there are exactly two components:
a clique \(B\) of order \(b\in\{1,2,3\}\), and \(A\in R(4,4;22-s-b)\).
No edge joins \(A\) and \(B\). The complete order profiles are

| \(s\) | \((|A|,|B|)\) |
|---:|---|
| 2 | (17,3) |
| 3 | (16,3), (17,2) |
| 4 | (15,3), (16,2), (17,1) |
| 5 | (14,3), (15,2), (16,1) |

Suppose for contradiction that every vertex has degree at least six.

- If \(b=1\), the sole vertex of \(B\) has degree at most \(s\le5\).
- If \(b=2\), each vertex of \(B\) has degree at most \(s+1\le6\).
  Hence \(s=5\) and both vertices meet all of \(S\). Any edge in \(S\)
  would make a four-clique with \(B\). Therefore \(S\) is an independent
  five-set, also forbidden.
- If \(b=3\), each vertex of \(S\) meets at most two vertices of the
  triangle \(B\), since otherwise it completes a four-clique. Consequently
  \(\sum_{v\in B}d_H(v)\le6+2s\le16\), whereas minimum degree six
  requires a sum of at least 18.

All cases contradict minimum degree six, proving the bridge. The argument
does not import the older four-separator classification or \(U(22)=114\).

## Density, completeness, and uniqueness of the cut

A vertex of degree at most three would leave at least 18 nonneighbors in
\(R(4,4)\), impossible. For a degree-four vertex \(z\), let \(A\) be its
17 nonneighbors and \(T\) its four neighbors. Every vertex has at most
eight neighbors in \(A\), because those neighbors are triangle-free with
no independent four-set. Thus \(e(A)\le68\), \(e(A,T)\le32\), and
\(e(T)\le4\), giving

\[
e(H)\le68+32+4+4=108.
\]

At density at least 109, the separator bridge therefore forces degree
exactly five. The imported complete census applies and gives precisely the
thirteen density-109 graphs. The two encodings of every representative are
checked here. Each has one degree-five vertex \(z\); every other degree is
at least nine.

Apply the component argument again to any separator of size at most five
in one of these representatives. Every vertex of its clique component
\(B\) has degree at most \(b-1+s\le7\). There is only one vertex of degree
at most seven, so \(B=\{z\}\). Its five neighbors must all lie in \(S\).
Hence \(S=N_H(z)\) and \(|S|=5\). Conversely, deleting those neighbors
isolates \(z\). This proves uniqueness and connectivity five, and upgrades
the graph classification to a marked-separator classification. No new
automorphism-group assumption or symmetry quotient is introduced.

## Hamiltonicity and the unrestricted global interface

If \(e(H)\ge110\), deleting at most two vertices leaves connectivity at
least four and independence number at most four. By Theorem 1 of
[Chvátal–Erdős, A note on Hamiltonian circuits (1972)](https://www.renyi.hu/~p_erdos/1972-02.pdf),
every such vertex-deleted graph has a Hamiltonian cycle. Deleting at most
one vertex leaves connectivity at least five, so Theorem 3 of the same
paper makes the remaining graph Hamiltonian-connected: any two specified
distinct endpoints have a spanning path.

These are consequences of classical theorems, not new cycle-enumeration
claims. Cycle/path labels must transport all existing marks and incidences;
they do not assert a cyclic automorphism of a hypothetical global graph.

For any 43-vertex \(R(5,5)\) graph with an order-22 color-neighborhood of
density at least 109 and connectivity at most five, relabel that neighborhood
as one of the thirteen representatives. Label the root 22 and its twenty
other vertices 23 through 42. The root is red to the neighborhood and blue
to the other twenty vertices. All

\[
22\cdot20+\binom{20}{2}=630
\]

remaining global edges are free at this coverage step. Every full Ramsey
completion of one of these interfaces lies in the stated branch, and every
graph in that branch maps to one of them. Color exchange gives the other
color. No opposite neighborhood, global degree sequence, exterior quota,
additional anchor, or global automorphism is fixed.

**All thirteen global completion families remain open.** This result rules
out local non-singleton small cuts at density at least 109 and all local
cuts of size at most five at density at least 110. It excludes no whole
global degree branch, hard deficiency slice, or \(R(5,5;43)\) family.
The density-108 four-separator graph \(H_*\) is outside the theorem and
its 630-edge extension family is unchanged. Local minimum degree at least
six is now known to entail six-connectivity at order 22, but those graphs
are not classified here.

## Reproduction and trust boundary

CPython 3.12.12 and its standard library suffice; Python 3.10 or later
supports the language features used. No graph library, solver, external
executable, or large omitted generated artifact is needed. From this directory:

```sh
set -o pipefail
python3 -B verify.py --verify-import | cmp - EXPECTED.json
python3 -B audit.py | cmp - EXPECTED.json
python3 -B test_checks.py | cmp - EXPECTED_TEST.json
python3 -O -B verify.py | cmp - EXPECTED.json
python3 -O -B audit.py | cmp - EXPECTED.json
python3 -O -B test_checks.py | cmp - EXPECTED_TEST.json
shasum -a 256 -c SHA256SUMS
```

Omit `--verify-import` for entirely offline reproduction. That option fetches
the pinned upstream certificate and checks both its hash and the exact
extracted records. The source certificate SHA-256 is
`905518c06dcd9fc4008dd5caf70eece7dbb67c77e6cd6d708388fca3d22a9da1`.

`verify.py` independently decodes each complete graph6 record, literally
checks all 7,315 four-sets and 26,334 five-sets, and exhausts all 35,443
deletions of at most five vertices per graph: 460,759 deletion tests total.

`audit.py` imports no producer. It uses a different graph6 decoder for the
16-vertex cores and reconstructs the graphs from columns and neighbor-graph
edges. It checks forbidden sets by bitset clique recursion. Instead of
enumerating deletions, it uses integral vertex-splitting flow to find six
internally disjoint paths between every nonadjacent pair after deleting
\(z\). By Menger this proves the remaining graph six-connected, independently
implying that \(N(z)\) is the only cut of size at most five. Both programs
agree entrywise on every edge hash, degree sequence, and complete cut list.
They separately enumerate the component-order profiles, with the audit also
checking all surviving local degree-six incidence cases literally.

Controls compare vertex flow with definition-level terminal separators on
all 1,100 labeled graphs of orders zero through five: 5,325 terminal-pair
comparisons. Both decoders pass all those graphs, all thirteen independent
reconstructions agree, and eighteen malformed/unsupported inputs are rejected.
Normal and optimized execution agree. These are different author-written
checks, not independent peer review of this new theorem or formalization.

The universal bridge trusts only the classical small Ramsey bounds and the
displayed unformalized argument. The dense classification additionally
imports the reviewed thirteen-class theorem, hence its explicitly stated
completeness premise for McKay's two-record \(R(4,4;16)\) catalogue.
Record checking is not a proof of that catalogue's completeness. No other
catalogue is imported. Finite validation trusts exact Python, decoding,
flow and traversal semantics, SHA-256 identities, and ordinary hardware.

Graph-first selection inspected the committed all-author Ramsey neighborhood,
the principal directive, and both peers' latest reports. The existing census
did not classify non-singleton five-separators. Primary literature checked
after selection includes the classical Hamiltonicity paper, the primary
[Ramsey catalogue](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), and
the [Angeltveit–McKay neighborhood/gluing paper](https://arxiv.org/html/2409.15709v2).
The component method also occurs in
[Beveridge–Pikhurko, On the connectivity of extremal Ramsey graphs (2008)](https://ajc.maths.uq.edu.au/pdf/41/ajc_v41_p057.pdf).
Its extremal-order hypothesis concerns order 24 for \((4,5)\), so its stated
connectivity theorem does not directly cover this order-22 density condition.
This limited check found no explicit statement of the present density-109
marked five-cut classification. No historical priority is claimed for the
component method, Menger flow, Hamiltonicity criteria, or imported census.
