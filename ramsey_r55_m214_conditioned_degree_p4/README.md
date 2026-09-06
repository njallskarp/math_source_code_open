# A complete conditioned M214 LP survivor and a global deficiency separator

The full M214 four-vertex moment relaxation remains feasible after every
triple-state-conditioned degree equation, every monochromatic-triangle
common-neighbor cap, and every incident-edge-conditioned red triangle-total
equation are added to the complete star system. An exact rational point
satisfies all **25,377,662 presentation rows**, including 4,447,009
equalities. Every inherited variable domain and row is retained.

The point violates a global deficiency second-moment bound by **more than
71**. That separator uses only existing three-vertex moments. Thus the
complete stated relaxation is insufficient, and the global inequality
strictly strengthens it. The inequality's addition has not been decided.
No Boolean root, complete M-slice, or Ramsey-number bound is excluded.

## Complete system and graph provenance

Use the original 389-root red-only normalization of the intrinsic M214 hard
branch: 43 vertices, exceptional class \(E=\{2,\ldots,14\}\) of size 13,
central class \(C\) of size 30, red degrees 20 on E and 21 on C, red local
triangle totals 93 on E and 100 on C, and
\(a(h)=|N_R(h)\cap E|\ge6\). The
[reviewed root cover h3148](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_normalization)
is artifact `bafkreiged4ub6uoeisoe7csj6e5t63palrihwzo7foiwymofg7tw57ie5m`.
Its graph-to-root equivalence retains all completion edges. This package
uses that domain, not a new cover or a selected core catalog.

Let \(S\) be exactly the complete system at
[h3581](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_star_p4_survivor),
artifact `bafkreidrt27dansveotqum27ku7hdmgvqssxsym6lgg76ijcpeht3tqj4y`:
the entire h3423 P4 system, the nine selector exclusions
\(48,128,129,201,202,299,300,375,376\), all 83 selector-to-anchor links,
all 11,970 anchor-zero forbidden-state rows, and all 9,625,980 star-event
inequalities. H3581 specifies each inherited layer and domain.
Its point and proposed degree separator were
[independently accepted at h3589](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_star_p4_survivor_review2).
The reviewer independently decoded the star and conditioned-degree layers
and replayed the author's full checker; it did not independently
reimplement every inherited base row.

For a triple \(A\), write \(q_{A,s}\) for its exact three-edge-state
mass. Four-set state masses are \(p_{B,t}\). Bit 1 is red, bit 0 blue;
the edge orders are \((01,02,12)\) and \((01,02,03,12,13,23)\).
All probabilities below are linear sums of these existing coordinates.
Define three complete families:

1. \(D_3\): for every triple A, every \(h\in A\), and all eight
   states s, including zero-mass states,

   \[
   \sum_{w\notin A}\Pr(A\text{ has state }s,\ x_{hw}=1)
   =(d_h-k_s(h))q_{A,s}.
   \tag{1}
   \]

   Here \(k_s(h)\) is h's red degree inside A. These are all
   \(3\cdot8\binom{43}{3}=296,184\) equations. Multiply the
   prescribed degree equation by the state indicator; no division is used.
   Blue-degree versions follow by subtraction from \(40q_{A,s}\).

2. \(T_3\): for every triple A and each color c,

   \[
   \sum_{w\notin A}p_{A\cup\{w\},\text{all }c}
   \le4q_{A,\text{all }c}.
   \tag{2}
   \]

   These are all \(2\binom{43}{3}=24,682\) inequalities. If A is
   a c-triangle, its common c-neighborhood has no c-edge, since such an
   edge would complete a c-K5. It therefore has at most four vertices,
   since five would form an opposite-color K5. If A is not monochromatic
   in c, both indicators vanish. This elementary consequence also occurs
   in the reviewed h3579/h3583 module-resilience argument; no module
   classification is imported into this LP.

3. \(J_1\): for every ordered pair \(h\ne a\),

   \[
   \sum_{\{u,v\}\subset V\setminus\{h\}}
   \Pr(huv\text{ is a red triangle},\ x_{ha}=1)
   =t_hx_{ha},
   \tag{3}
   \]

   where \(t_h=93\) on E and 100 on C. These are all
   \(43\cdot42=1,806\) equations. Multiply the literal red triangle-total
   equation by the incident red edge. A summand has three vertices when
   \(a\in\{u,v\}\), and four otherwise. Conditioning that same red
   total on a blue edge follows by subtraction. No claim includes every
   conditioned blue-triangle total, whose right sides are different.

Put \(Q=S+D_3+T_3+J_1\).

| Complete system | Variables | Rows | Equalities | Decision |
| --- | ---: | ---: | ---: | --- |
| \(S\) | 8,023,409 | 25,054,990 | 4,149,019 | previously feasible |
| \(S+D_3\) | 8,023,409 | 25,351,174 | 4,445,203 | exact feasible here |
| \(Q\) | 8,023,409 | 25,377,662 | 4,447,009 | exact feasible here |
| \(Q\) plus (5) below | 8,023,409 | 25,377,663 | 4,447,009 | undecided |

Counts retain redundant presentation rows, including the 11,970
anchor-zero rows already implied by the complete star family. Removing
only those gives 25,365,692 rows for the same Q. No other global constraints
or graph contributions are silently included in the word “complete.”

## A global deficiency second moment strictly separates Q

The root-cover domain implies

\[
\sum_{h\in V}a(h)=\sum_{u\in E}d_u=260,
\qquad \epsilon_h=a(h)-6\ge0,
\qquad \sum_h\epsilon_h=2.
\]

For nonnegative excesses, \(\sum\epsilon_h^2\le(\sum\epsilon_h)^2=4\).
Since actual graph counts are integers, also
\(\sum\epsilon_h^2\ge\sum\epsilon_h=2\). Expanding the square gives

\[
1574\le\sum_h a(h)^2\le1576.
\tag{4}
\]

The two possible excess partitions, one 2 or two 1s, respectively give the
upper and lower values. This statement concerns allowed count patterns;
it does not assert that either pattern is realized by a Ramsey graph.
The upper bound itself needs only nonnegative excesses and total two.

For distinct u,v,h, let \(m_{uv,h}\) be the existing blue-wedge moment
\(\mathbb E[(1-x_{hu})(1-x_{hv})]\). The red wedge is
\(m_{uv,h}+x_{hu}+x_{hv}-1\). Therefore the lifted upper bound is

\[
\sum_h\left(
 \sum_{u\in E\setminus\{h\}}x_{hu}
 +2\sum_{\{u,v\}\subset E\setminus\{h\}}
   (m_{uv,h}+x_{hu}+x_{hv}-1)
\right)\le1576.
\tag{5}
\]

This is valid for every graph lift in the full M214 intrinsic domain and
for every convex combination of such lifts. It introduces no new
coordinates. In the inherited variable numbering it is one 3,666-term row:

\[
-46\sum_{\{u,v\}\subset E}x_{uv}
-25\sum_{u\in E,\,v\in C}x_{uv}
-2\sum_h\sum_{\{u,v\}\subset E\setminus\{h\}}m_{uv,h}
\ge-7972.
\tag{6}
\]

There are 78 E–E edges, 390 E–C edges and 3,198 wedges. The square expansion
has constant \(-2(13\binom{12}{2}+30\binom{13}{2})=-6396\), explaining
the right side \(-6396-1576=-7972\). The coefficient 46 comes from both
exceptional centers; 25 comes from the central center.

The exact Q point has first-moment total 260, but the left expression in
(5) exceeds 1576 by a rational number strictly greater than 71. The entire
fraction is in `EXPECTED_RESULT.json` and independently in
`EXPECTED_INDEPENDENT.json`. `emit_deficiency.py` emits (6); its SHA-256 is
`307dd90f1f81cc849e2a2fdeddd584e4ac1ddade839cbfdb71bc8f21c63a8339`.
The checker reconstructs every coefficient by centered-square expansion
and evaluates it exactly. Thus (5) is not a linear consequence of Q.
This is a demonstrated global separator, not a claim that Q+(5) is infeasible.

## Exact point and reproduction

The candidate selects \(y_{278}=1\), all other selectors zero, with root
\((C77,12,0,BB)\). The anomaly labels are 29 and 30. Its nine classes are
\(\{0\},\{1\},\{2,\ldots,7\},\{8,\ldots,13\},\{14\},
\{15,\ldots,26\},\{27,28\},\{29,30\},\{31,\ldots,42\}\).
There are 345 four-class templates and 4,149 positive canonical state
orbits, with a common denominator of 254 decimal digits. Missing states
are zero; class-preserving permutations transport the six physical edges.
The inherited decoder specifies all 8,023,409 coordinates.

The generated rational point has SHA-256
`d957b35da176b786f85b8df85db37b1080ef1d04723a184be4a0cc8cae92f442`.
Its 1,082,976-byte serialization, the 511 MB base, model, solution and logs
are generated in local scratch and omitted from this public source
package. The package supplies their deterministic production route and
compact exact expected results. The omitted point is regenerated before
checking; its hash alone is not mathematical evidence.

From a full repository checkout, with CPython 3.12.12 and its standard
library, and SoPlex 8.0.3 on PATH (GMP 6.3.0, revision `13e2ab24`):

```sh
python3 -B ramsey_r55_m214_conditioned_degree_p4/reproduce.py /tmp/new-r55-conditioned-degree
(cd ramsey_r55_m214_conditioned_degree_p4 && shasum -a 256 -c SHA256SUMS)
```

Use a new scratch directory outside the source checkout. Allow several
minutes and roughly 2 GB scratch space. The producer uses rational input,
exact solve/check mode, zero primal/dual tolerances, internal presolve and
equilibrium scaling. The final discovery solve took 30.58 seconds and
16,025 iterations in this environment. Those figures and solver status
are not evidence of feasibility. Different solver builds may yield a
different point and fail the expected-byte comparison; they do not imply
an infeasibility result.

The reproducer regenerates the complete base through five hash-pinned
builders, generates and exactly checks the rational discovery solution,
then evaluates every physical row with a separate checker importing no
producer or solver. Discovery has 8,558 variables and 19,631 rows under a
candidate-only class symmetry and root-278 restriction. It does not encode
all inherited suffixes during discovery; the full checker evaluates them
all afterward. Its infeasibility could not decide unrestricted Q.

Expected final status: `EXACT_COMPLETE_DEGREE_TRIANGLE_P4_SURVIVOR`,
25,377,662 rows, zero violations in D3, T3 and J1, and deficiency gap >71.
The exact point's red and blue deficiency totals are 301 and 303; blue
local triangle totals are 107 on E, 99 at 29 and 30, and 100 elsewhere.

Given the regenerated files, verification is solver-free:

```sh
python3 -B ramsey_r55_m214_conditioned_degree_p4/check.py \
  --certificate /tmp/new-r55-conditioned-degree/certificate.json \
  --opb /tmp/new-r55-conditioned-degree/m214-3323.opb \
  --links /tmp/new-r55-conditioned-degree/anchor-links.opbpart \
  --forbidden /tmp/new-r55-conditioned-degree/forbidden.opbpart \
  --degree-separator /tmp/new-r55-conditioned-degree/degree-separator.opbpart \
  --deficiency-separator /tmp/new-r55-conditioned-degree/deficiency-separator.opbpart
python3 -B ramsey_r55_m214_conditioned_degree_p4/independent_square.py \
  /tmp/new-r55-conditioned-degree/certificate.json
```

The old named degree separator is now satisfied exactly. Its emitted row
is retained as a regression check, not as the current separating row.

## Validation, literature, trust and next boundary

The physical checker verifies all 2,983,003 inherited OPB rows and 87
base equalities, all original suffix rows, all 123,410 four-sets, 3,949,120
shared triple marginals, 74,513 footprint identifications, 9,625,980 star
inequalities, 296,184 conditioned degree identities, 24,682 triangle caps
and 1,806 conditioned triangle totals. Semantic coefficient checks cover
44,343 source rows, including all 43 original red triangle-total equations
at rows 1,974,604 through 1,974,646.

Controls verify 529,920 physical state transports, 245,760 conditioned-degree
Boolean cases, 20,480 conditioned-triangle Boolean cases, 2,048 triangle-cap
implications, 5,120 literal square expansions and all 946 excess placements,
besides the inherited star/emitter controls. Twenty-nine altered inputs
are rejected. Normal and optimized controls agree. A second edge-set
implementation imports no main checker or producer and independently
recovers the same global square and exact gap; its scope is that scalar,
not the full LP. The complete fresh regeneration is compared byte for byte
with all expected outputs.

Primary literature checked after graph selection includes
[Angeltveit–McKay, R(5,5) at most 46](https://arxiv.org/abs/2409.15709),
and Sherali–Adams (1990), DOI 10.1137/0403036, for the classical indicator
multiplication and relinearization mechanism. The
[official SoPlex source](https://github.com/scipopt/soplex) documents the
exact solver used only to regenerate a candidate. The squared-count
expansion and nonnegative-excess bound are elementary. No historical
priority for any of these methods is claimed. The result is the exact
survivor of the specified complete Q and its quantified global separator.

The new contribution is author-checked; external review is pending.
The main checker adapts the author's h3581 inherited routines, whose scope
and independent review are linked above. Literal rational feasibility
requires no Ramsey catalog or trusted solver verdict. Interpretation as
necessary conditions for canonical M214 Ramsey candidates retains the
reviewed root-cover, local-extrema and nine-exclusion premises. The global
separator uses the intrinsic degree/class/excess domain. Remaining trust
is the unformalized reductions and code, exact Python arithmetic,
hash-pinned production, SHA-256 and ordinary hardware. There is no
proof-assistant formalization or proof of Boolean realizability.

The graph was refreshed through indexed height 3596 across signers.
The new induced-pentagon theorem h3593 and Cyclic(43) regrowth theorem
h3595 have separate complete domains and are not extra LP premises here.
Adjacent M-slices, the low-deficiency branch and all Boolean completions
remain uncovered. No more rows or linear combinations from the completed
D3/T3/J1 families can remove this same point.

**Next falsifiable milestone:** decide the complete Q plus the single
global inequality (5), by an exact full-system survivor or a checkable
infeasibility certificate with unrestricted coverage. Refresh the live
graph and principal advice first. Do not infer full-system infeasibility
from the symmetric root-278 search. Two consecutive passes with only
incremental rows and no strict separator, complete survivor or family
closure trigger a pivot to the next principal-ranked exact target.
