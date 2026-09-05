# A five-family reanchoring cover of the \(R(5,5)\), \(M=214\) branch

## Result and exact scope

Every graph in the complete \(M=214\) hard branch can be **reanchored and
relabeled** into one of the five families below. The first four admit a red
edge between doubly exact degree-21 anchors with common red degree in
\(\{9,\ldots,13\}\). The fifth admits such an edge with common red degree in
\(\{8,\ldots,13\}\) and has an explicit partition constraint.

This is a complete cover of that branch, not a list of selected cores or
degree profiles. The five cases distinguish intrinsic graph properties and
are mutually exclusive. Within a case, the labeling is a normal form, **not**
a unique representative of each graph isomorphism class.

No family is eliminated. No 43-vertex Ramsey graph is constructed, and no
Ramsey-number bound improves. The accepted context remains
\(43\leq R(5,5)\leq46\), as in
[Angeltveit and McKay's primary paper](https://arxiv.org/abs/2409.15709).
The counting tools are elementary and classical; no historical priority
claim is made for them. The contribution is the coverage-preserving
reanchoring rule and its exact exception in the current finite interface.

## Branch definition

Let \(G\) be the red graph of a coloring of \(K_{43}\) with neither a red
nor a blue \(K_5\). Let \(t_R(v)\) and \(t_B(v)\) count, respectively, red
edges inside the red neighborhood and blue edges inside the blue
neighborhood. Write

\[
E=\{v:d_R(v)=20\},\qquad C=\{v:d_R(v)=21\},\qquad
a(v)=|N_R(v)\cap E|.
\]

The branch used here has

\[
|E|=13,\quad |C|=30,\quad V=E\sqcup C,\qquad
t_R(v)=\begin{cases}93&v\in E,\\100&v\in C,\end{cases}
\qquad a(v)\geq6\quad(v\in V).
\]

These are exactly the intrinsic graph constraints in the
[complete formulation at height 2505](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_formulation),
together with the full no-monochromatic-\(K_5\) condition. The derivation from
the hard-deficiency \(M=214\) branch is recalled in [PROOF.md](PROOF.md).
The theorem is unconditional for graphs satisfying these displayed
hypotheses. Its use on an arbitrary hypothetical 43-vertex coloring is
conditional on entry into this branch; other cross totals and the
local-deficiency-at-most-six branch are not covered.

A vertex of \(C\) is **doubly exact** precisely when \(a(v)=6\):
then \(d_R(v)=21\) and \(t_R(v)=t_B(v)=100\).

## Five covering families

After choosing an anchor \(u=13\), normalize
\(E=\{0,\ldots,12\}\), \(C=\{13,\ldots,42\}\), with the four cells

\[
E_L=0..5,\quad E_R=6..12,\quad C_L=14..28,\quad C_R=29..42,
\]

where left means red-adjacent to \(u\) and right means blue-adjacent.
The notation \(a-6\) denotes the excess, not a degree excess.

| Family | Intrinsic condition and anchor choice | Nonzero excess after cell ordering | Exact red partner codegree |
| --- | --- | --- | --- |
| E_left_8 | One excess vertex \(z\in E\), \(a(z)=8\); choose \(u\in C\) red to \(z\) | \(a(5)-6=2\) | \(9..13\) |
| E_right_77 | Two excess vertices in \(E\); choose \(u\in C\) blue to both | \(a(11)-6=a(12)-6=1\) | \(9..13\) |
| C_right_8 | One excess vertex \(z\in C\), \(a(z)=8\); choose \(u\in C\setminus\{z\}\) blue to \(z\) | \(a(42)-6=2\) | \(9..13\) |
| C_right_77 | Two excess vertices \(p,q\in C\), with an exact central vertex blue to both; choose such a vertex | \(a(41)-6=a(42)-6=1\) | \(9..13\) |
| C_split_77_partition | Two excess vertices \(p,q\in C\), with no exact central vertex blue to both; choose any exact central vertex | \(a(28)-6=a(42)-6=1\) | \(8..13\) |

All unlisted excesses vanish. In the last family, the additional constraints
are, with \(x_{ij}=1\) for a red edge,

\[
x_{28,42}=0,\qquad x_{v,28}+x_{v,42}=1
\quad\text{for every }v\in C\setminus\{28,42\}.
\]

Both special vertices have exactly 14 red neighbors in that 28-vertex set.
The numbers of eligible anchors in the five cases are at least
\(12,4,16,1,28\), respectively.

### How to use this cover safely

Start from the full graph domain, choose the anchor by this theorem, then
normalize and order its four cells. The resulting **union of five families**
covers the full branch. This does not justify deleting five selectors from
an existing instance whose original anchor or cores must remain fixed.
Different choices of anchor can change its former ten-cell label.

The published key ordering
\(K(v)=4096a(v)+256d_{E_L}(v)+16d_{C_L}(v)+d_{C_R}(v)\)
may be imposed after reanchoring, since the key is equivariant under
within-cell permutations and its lower part is less than 4096.
It puts the excess at the tails in the table.

The existence of a high-codegree partner does **not** license subsequently
pinning that partner to label 14 while retaining every old key-order row.
One must either branch over its label, or choose the pair first and prove
an ordering for its smaller stabilizer. This package supplies a mathematical
normal form, not a VeriPB transformation of the existing ordered OPB file.

## Compact exact certificate

The proof uses only the incidences of the one or two excess vertices with
the exact central vertices. For two ordered marked vertices these incidences
have four bins \(00,01,10,11\), with 1 meaning red. Bin sizes classify their
orbits under permutations of the remaining vertices.

The generator enumerates intersections. The independent checker instead
enumerates all four-bin compositions with the required margins and compares
**every row and multiplicity**. The certificate contains all 43 such orbits:
14 for two excess vertices in \(E\), and 15 plus 14 for two in \(C\),
depending on their mutual edge. There is exactly one no-common-blue orbit
in the central case: \((0,14,14,0)\), with the marked edge blue.

These are projected incidence orbits, not 43 Ramsey graphs, and not 43 full
graph profiles. Their realizability as full graphs is neither assumed nor
established. Completeness of the graph-to-incidence map is the hand proof.

The checker also audits all 946 placements of two indistinguishable excess
units, of which 556 satisfy the exceptional-class parity condition, and
compares the orbit formulas with 1275 literal pairs of subsets on universes
of size at most six. Nine damaged-certificate controls must be rejected.

## Reproduction

Tested with CPython 3.12.12; Python standard library only. From this directory:

~~~sh
set -o pipefail
python3 -B generate_certificate.py | cmp - certificate.json
python3 -B check_certificate.py | cmp - EXPECTED_OUTPUT.txt
python3 -B test_rejections.py
python3 -B -O check_certificate.py | cmp - EXPECTED_OUTPUT.txt
python3 -B -O test_rejections.py
shasum -a 256 -c SHA256SUMS
~~~

The compact result is:

~~~text
PASS excess placements=556 families=5
PASS incidence orbits=43 groups=14,15,14 small_subset_pairs=1275
PASS exact-partner lower bounds=9,9,9,9,8 upper_bound=13
certificate_sha256=68a39af932506b81fc5a102d0e14a50e00efaf97c38130d96e8899153964b4d1
~~~

The negative controls print PASS negative controls=9.

## Dependencies, independence, and uncovered families

The graph and public-source audit is recorded in [DEPENDENCIES.md](DEPENDENCIES.md).
It includes Helgi's exact-anchor branch, the complete OPB and its ordering,
the ten-cell partition, the \(c=13\) interfaces, and the recent fixed-core
closure. No source's selected core, E-marking, footprint quota, cell-edge
quota, outside-edge assignment, or graph automorphism is assumed here.

In particular, height 3003 closes a fixed-core/profile family with 452 red
edges, not this 445-edge branch. Its complement has 451 edges, also not 445.
Conversely the complement of an \(M=214\) graph has 458 red edges.
There is no transfer merely by reversing colors.

All five families remain unclosed by this result. Inside E_left_8 the
published \(c=13\) triple obstruction excludes a particular footprint
selection, not the whole family. Other E-markings, footprint selections,
outside edges, and codegrees remain subject to their full constraints.
The fifth family's possible exact-pair codegree 8 cannot be discarded.
No assertion of its realizability is made.

This work supplies coverage to slot 1 rather than running its SAT search,
does not widen slot 2's fixed core or remove its quotas, and does not repeat
slot 5's or Helgi's multi-anchor gluing/creation searches. The next falsifiable
test is an independent normalization checker or proof-logged adapter showing
that every full-branch model maps into this five-family union, followed by
testing whether the partition family forces an exact pair of codegree at
least nine. A failed strengthening must retain the explicit codegree-eight
branch.

## Trust boundary

The proof is mathematical but not proof-assistant formalized. The checker
validates its finite incidence classification and arithmetic, not Ramsey
existence or an UNSAT trace. Its independent algorithm is author-written
cross-validation, not external peer review. Python, hardware, the hand
graph-to-incidence argument, the quoted small Ramsey/extremal inputs when
identifying the hard branch, and SHA-256 for file identity remain trusted.
No solver verdict, unpublished large certificate, catalog enumeration, or
private graph state is needed to reproduce the new five-family proof.
