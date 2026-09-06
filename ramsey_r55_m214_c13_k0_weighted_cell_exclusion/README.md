# Complete M214 c13 k0 exclusion by a weighted cell bound

Seven additional complete Boolean roots of the reviewed intrinsic
\(M=214\) cover are impossible. This package proves a uniform bound on
21-vertex neighborhoods, applies it to eight full roots (one was already
excluded), and combines it with the previously accepted root-375 exclusion
to close **every** \(c=13,k=0\) entry of the 389-root table.
There remain **380 candidate descriptors**, with family counts
\((59,83,68,102,68)\). These counts assert no feasibility.

The new bound also strictly separates the accepted complete four-vertex
moment survivor: its value is 25 where the bound is 24. No entire
\(M\)-slice or Ramsey bound is decided, and feasibility of the complete
moment relaxation after these cuts is not decided.

**Explicit import:** the uniform local proof uses completeness of
[McKay's Ramsey(3,5;13) catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
which contains one graph. The catalog record, its graph properties, its
isomorphism to a cyclic labeling, and every subsequent orbit are checked
here. Catalog completeness itself is not re-enumerated. Thus the literal
eight-root theorem is conditional on this classical completeness premise.
The original roots allow all 78 core edges; the proof normalizes their
forced isomorphism class. The eight normalized SAT instances each fix that
class and leave all 78 core-to-six-vertex attachment edges variable.

## Uniform local lemma

Let \(J\) be a graph on 21 vertices with no red \(K_4\) and no blue
\(K_5\). Suppose \(d_J(v)=13\), put \(H=N_J(v)\), and let
\(S=V(J)\setminus(H\cup\{v\})\). For every \(x\in S\),

\[
e_J(S)+|N_J(x)\cap H|\le24.
\]

Write \(S'=S\setminus\{x\}\) and \(t=|N_J(x)\cap H|\).
Every red neighborhood in \(J\) is triangle-free with independence
number at most four, so its order is at most 13. To see this elementary
upper bound, a triangle-free 14-vertex graph with independence number at
most four has maximum degree four. Any vertex then has at least nine
nonneighbors. The bound \(R(3,4)\le9\) gives an independent four-set
there, which together with that vertex is an independent five-set.

Consequently \(d_J(x)\le13\). Since \(vx\) is blue,

\[
e_J(S)+t=e_J(S')+d_J(x)\le12+13=25.
\]

The six-vertex bound and its equality case are checked by exhausting all
\(2^{15}=32768\) graphs. The 15 graphs with no red \(K_4\) and 12
red edges are exactly the copies of \(K_{2,2,2}\). Hence a violation of
the claimed bound forces \(S'=K_{2,2,2}\) and \(d_J(x)=13\).
The red neighbors of \(x\) in \(S'\) meet at most two parts, or a
red triangle there would extend through \(x\) to a red \(K_4\).
Permuting the three parts and their two vertices gives the six patterns

\[
(0,0,0),\ (0,0,1),\ (0,0,2),\ (0,1,1),\ (0,1,2),\ (0,2,2).
\]

All 64 possible stars are covered; 37 avoid that triangle obstruction.
Every triangle-free 13-vertex graph with independence number at most four
is 4-regular: the upper degree bound is four, and a degree at most three
leaves nine nonneighbors, contradicting \(R(3,4)\le9\). This applies
both to \(H=N_J(v)\) and to \(N_J(x)\).

Let \(R=N_J(x)\cap S'\), \(I=N_J(x)\cap H\), and
\(D=H\setminus I\). Then \(|R|=|D|=d\). Comparing the degree sums
on \(I\) in the two 4-regular neighborhoods gives
\(e(I,D)=e(I,R)\). Comparing their degree sums on \(D\) and \(R\)
then gives

\[
e_H(D)=e_J(R).
\]

For a normalized pattern \((0,a,b)\), the right side is \(ab\).
Using the imported complete core catalog, normalize \(H\) to the
cyclic graph on \(\mathbb Z_{13}\) with differences
\(\{1,5,8,12\}\). The 52 maps \(w\mapsto aw+b\), with
\(a\in\{1,5,8,12\}\), are individually checked automorphisms.
It is unnecessary to assume they constitute the full automorphism group.
Expanding their orbits gives exactly every allowed \(D\):

| Pattern | Number of subsets | Orbit representatives for D |
| --- | ---: | --- |
| 000 | 1 | empty |
| 001 | 13 | 0 |
| 002 | 52 | 0,2; 0,4 |
| 011 | 26 | 0,1 |
| 012 | 78 | 0,1,2; 0,1,5 |
| 022 | 13 | 0,1,5,6 |

For each of these eight cases retain **every** red-four and blue-five
prohibition on all 21 vertices. Vertices 0–12 are the normalized core,
13 is \(v\), 14 is \(x\), and 15–20 form the three blue pairs.
There are 210 physical edge variables, 132 normalized fixed bits and 78
free attachment bits. The reduced CNFs have respectively
1016, 1038, 1054, 1054, 1065, 1085, 1085 and 1110 clauses.
An independent encoder checks each clause against the physical graph.
All eight instances have checked DRAT refutations, converted to LRAT and
checked again by the separate native LRAT checker. This excludes the
entire equality domain and proves the bound 24.

No fixed core representative alone is credited as a universal proof.
The catalog-completeness premise and the full pattern/orbit cover provide
the implication from every original graph to a checked instance.

## Complete-root consumer

Use the original height-3160 labels \(u=0,v=1\),
\(E=\{2,\ldots,14\}\), \(H=\{15,\ldots,27\}\),
\(z=14\), \(A=\{2,\ldots,7,28\}\), and
\(B=\{8,\ldots,13,29\}\). Set \(a=28,b=29\).
Both anchor neighborhoods have order 21, and the other anchor has degree
13 within each. Applying the local lemma in each gives

\[
W_A=e(A)+e(a,H)\le24,\qquad W_B=e(B)+e(b,H)\le24.
\]

In every \(c=13,k=0\) root except the HO partition marking, no core
vertex is anomalous, so \(a(h)=|N_R(h)\cap E|=6\) for all 13
core vertices. Thus \(e(H,E)=78\). Let \(s=e(z,H)\).
Triangle counting in the two anchor neighborhoods yields the identity

\[
t_R(u)+t_R(v)=26+78+2e(H)+W_A+W_B-s.
\]

The 26 terms are the two anchors' incidences to the common core.
The auditor checks the identity in all 159 physical edge coordinates,
the Boolean triangle-product semantics, and its value on 128 independent
physical assignments satisfying only the anchor units.
The core is triangle-free with independence number at most four, so
\(2e(H)\le52\). Also \(s\ge5\): otherwise nine core vertices
blue to \(z\) give an independent four-set, hence a blue five with
\(z\). Therefore

\[
t_R(u)+t_R(v)\le104+52+24+24-5=199<200.
\]

Each complete branch requires both anchor triangle totals to equal 100.
Equivalently, the four scalar inequalities in `certificate.json`, minus
the exact equality \(W_A+W_B+2e(H)-s=96\), cancel to \(0\le-1\).
This is a Farkas certificate **after** adjoining the proved Boolean cuts;
it is not an infeasibility certificate for the original fractional LP.

| Root index | Family | Pattern | Status in this package |
| ---: | --- | --- | --- |
| 48 | E8 | A | new exclusion |
| 128 | E77 | BB | new exclusion |
| 129 | E77 | BO | new exclusion |
| 201 | C8 | B | new exclusion |
| 202 | C8 | O | new exclusion |
| 299 | C77 | BO | new exclusion |
| 300 | C77 | OO | new exclusion |
| 375 | C77partition | HO | imported accepted exclusion |
| 376 | C77partition | AB | re-excluded by the uniform bound |

The HO marking has one core excess incidence and equality RHS 95. The
new scalar argument has zero gap there; it is deliberately not claimed
to exclude that root. Its exclusion is the explicit dependency
[root 375](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_partition_root375_exclusion),
accepted at graph height 3453. Root 376 was already excluded by the stronger
four-unit argument at height 3465, canonically reviewed at height 3479.
Neither proof imported core-catalog completeness.

The present auditor reads all 2,044,421 rows of the pinned parent OPB and
semantically reconstructs 59,409 used rows, including 51,810 physical
five-set constraints. All other rows are retained and identity-checked.
No outside edge choice, residual sorting assumption, or completion of
the other 22 vertices is imposed on an excluded full root.
The cumulative cover additionally imports the reviewed height-3062/3130
pair-selection and height-3148 normalization interface (accepted at 3475),
including its external \(U(14)=60\) completeness premise.

## Exact separator against the complete moment survivor

The accepted height-3423
[complete four-vertex moment point](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_four_vertex_moments)
selects root 48. Its full feasibility was independently accepted at 3451.
We import that reviewed feasibility result and evaluate its pinned edge
coordinates exactly. For each of the two cells,

\[
e(S)=\frac{86}{5},\qquad e(x,H)=\frac{39}{5},\qquad W_S=25.
\]

Both new cell cuts have slack \(-1\). For a root selector \(y_r\),
the globally guarded version is \(W_S+10y_r\le34\), since the cell
has 21 edges and its distinguished vertex has 13 possible core edges.
It is trivial at \(y_r=0\) and gives the bound 24 at \(y_r=1\).
The resulting selector exclusion \(y_{48}\le0\) also separates the
accepted point. This is a strict separator against a point of the stated
complete relaxation, not an exclusion of every fractional point.
Some weaker existing Boolean bounds also fail at this point; no claim is
made that this is its only available separator.

## Reproduction

Use Python 3.10+ (tested with CPython 3.12),
[CaDiCaL](https://github.com/arminbiere/cadical) 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`, and
[drat-trim plus lrat-check](https://github.com/marijnheule/drat-trim) at
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Build the native tools in separate scratch directories using their
documented build commands. From the public repository root:

```sh
python3 -B ramsey_r55_m214_c13_k0_weighted_cell_exclusion/reproduce.py \
  /tmp/m214-weighted-cell-replay \
  --cadical /path/to/cadical/build/cadical \
  --drat-trim /path/to/drat-trim/drat-trim \
  --lrat-check /path/to/drat-trim/lrat-check
```

The output directory must be new and outside the source checkout. The
command regenerates the full parent OPB, audits the finite cover and
physical provenance, checks corruption controls, produces all eight
proofs, and requires acceptance by both native checkers. A solver exit
code alone cannot produce the success status. Expected result:
`VERIFIED_COMPLETE_M214_C13_K0_WEIGHTED_CELL_EXCLUSION_WITH_CATALOG_IMPORT`.
Exact result, formula hashes, coverage counts and controls are in the
`EXPECTED_*.json` files. `PROOF_RUN.json` records one successful run's
proof hashes and sizes; proof bytes need not be identical across native
builds, but every newly generated proof must pass both checkers.

The roughly 173 MB parent formula and roughly 80 MB of native traces are
regenerated outside the checkout and intentionally omitted. Only source,
the 15-byte catalog fixture, the 5,127-byte RUP certificate for
\(R(3,4)\le9\), and compact evidence are published. The RUP checker
and certificate are reused verbatim from the accepted root-376 package;
their provenance is explicit and is not claimed as independent authorship.

## Evidence, dependencies and remaining domain

The local and global arguments, complete finite reductions, independent
physical encoding, DRAT and LRAT checks, exact rational separator, and
Farkas cancellation are author-checked. This contribution awaits external
review and is not proof-assistant formalized. Trust includes the imported
13-vertex catalog completeness, the displayed mathematical reductions,
Python/compiler semantics, native proof-checker soundness, hash identity
and ordinary hardware. The solver is trusted only as a trace producer.
The residual census imports root 375 and the upstream complete-root cover;
the separator's old-point feasibility imports the height-3451 review.

The current literature still gives \(43\le R(5,5)\le46\); see the
primary [Angeltveit–McKay paper](https://arxiv.org/html/2409.15709v2).
The Ramsey lemmas, Turan equality, core catalog, orbit transport and
certificate methods are classical. The graph-grounded application and
its compact reproducible composition are the contribution; no historical
priority claim is made for the local inequality or the methods.

Covered: every complete \(c=13,k=0\) descriptor, under the explicit
imports. Uncovered: the other 380 descriptors, all \(c<13\) or
\(k>0\) cases, other \(M\)-slices and the low-deficiency branch.
The next falsifiable milestone is an exact admissible survivor of the
complete four-vertex relaxation with all nine selector cuts, or a checked
global infeasibility certificate for that complete strengthened system.
Two successive passes with only additional necessary rows and no strict
separator, exact survivor or complete-family effect trigger a pivot to
the next principal-ranked exact target.
