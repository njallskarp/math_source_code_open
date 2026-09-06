# A marked-density obstruction for all sixteen O22 choices

## 1. Exact conditional family and conclusion

Let \(H\) be the labeled graph in [H20.json](H20.json), with vertices
\(h_0,\ldots,h_{19}\), and put \(u=h_0\), \(v=h_1\).
Let \(Q\) be the red complement of the 108-red-edge graph decoded by
[SOURCE.json](SOURCE.json). Thus \(Q\) has 22 vertices and 123 red edges.
For a blue pair \(e\) of \(Q\), let \(O_e=Q+e\), changing just that pair
from blue to red.

There are precisely sixteen such \(e\) for which \(O_e\) has no red
\(K_5\); these are exactly the sixteen opposite-neighborhood choices
published at height 3026. Each already has no blue \(K_4\).
The package regenerates this entire prescribed single-edge family;
it does not classify all 107-blue-edge graphs.

Consider any coloring on the disjoint union
\(\{r\}\sqcup H\sqcup O_e\) with:

- the two displayed internal graphs fixed;
- every \(rH\) edge red and every \(rO_e\) edge blue;
- total red degrees \(d_R(u)=d_R(v)=20\);
- every vertex of \(O_e\) red-adjacent to at least one of \(u,v\);
- no monochromatic \(K_5\).

The covering condition is the proper-three-anchor condition on the
\(r\)-blue side. It is a hypothesis, not an inferred normalization.
Every one of the 440 \(H\)--\(O_e\) pairs remains variable, including
all marked incidences; no labeled \(8/10/4\) partition is fixed.

**Theorem.** Every such coloring has

\[
t_R(v):=e_R(N_R(v))\le91.
\]

For the selected published edge \(e=(0,10)\), the stronger bound
\(t_R(v)\le90\) holds. Therefore **none of the sixteen fixed O22 choices
can be glued to this marked H20 in the prescribed hard profile**, which
requires \(t_R(v)=92\).

This does not exclude H20 with another opposite neighborhood, any
unmarked gluing, a gluing without the covering condition, or one with
different marked degrees/densities. No Ramsey-number bound improves.
The upper bounds are not claimed sharp.

## 2. The marked-density identity

The literal H20 graph gives

\[
N_H(u)=\{v,h_{10},\ldots,h_{15}\},\qquad
N_H(v)=\{u,h_{16},h_{17},h_{18},h_{19}\}.
\]

The two marked neighborhoods are disjoint. Write
\(W=\{h_{16},h_{17},h_{18},h_{19}\}\).
The graph on \(W\) is the red cycle
\(16\,17\,18\,19\,16\), and \(u\) is blue to all of \(W\).

Let \(U=N_R(u)\cap O_e\) and \(T=N_R(v)\cap O_e\).
The two degree equations and the covering hypothesis give

\[
|U|=20-1-7=12,\qquad
|T|=20-1-5=14,\qquad
U\cup T=O_e,\qquad |U\cap T|=4.
\]

For \(w\in W\), put \(S_w=N_R(w)\cap T\). The red neighborhood of
\(v\) is exactly \(\{r,u\}\cup W\cup T\). Its fixed red edges comprise
five from \(r\) to \(\{u\}\cup W\), four inside \(W\), the edges of
\(O_e[T]\), and four from \(u\) to \(T\). Hence

\[
t_R(v)=13+e_R(O_e[T])+\sum_{w\in W}|S_w|.
\tag{1}
\]

The set \(T\) is red-\(K_4\)-free, because a red \(K_4\) there extends
with \(v\) to a red \(K_5\). Each \(S_w\) is red-triangle-free, because
a triangle there extends with \(v,w\) to a red \(K_5\).

Only these two marked degrees and one density are used. The other
degrees, column debts, exceptional blue densities and remaining
constraints may be discarded for this exclusion.

## 3. Six domains and one complementary clique

Every red-\(K_4\)-free 14-set of \(O_e\) is a red-\(K_4\)-free 14-set
of \(Q\), since \(Q\subseteq O_e\) as red graphs.
There are exactly six:

| Index | Vertices in the O22 labels | Red edges in \(Q[T]\) |
|---|---|---:|
| 0 | \(0,2,3,4,5,9,10,12,13,16,18,19,20,21\) | 44 |
| 1 | \(0,3,4,5,6,8,9,11,12,13,15,16,19,21\) | 44 |
| 2 | \(0,3,4,5,6,8,9,11,13,15,16,19,20,21\) | 43 |
| 3 | \(1,2,3,4,5,6,7,9,10,12,13,14,17,20\) | 47 |
| 4 | \(1,2,3,4,5,9,10,12,13,17,18,19,20,21\) | 44 |
| 5 | \(1,2,3,4,6,7,9,10,11,12,13,14,17,20\) | 45 |

The only set with more than 45 red edges is \(T_3\). Its complement
contains the fixed red clique

\[
K=\{8,11,16,18\}\subseteq O_e\setminus T_3.
\]

The covering condition gives \(O_e\setminus T\subseteq U\).
Consequently \(T=T_3\) would put this red \(K_4\) inside \(U\),
creating a red \(K_5\) with \(u\).
Adding a red edge to \(Q\) cannot destroy this obstruction.

Thus every possible \(T\) belongs to the other five rows, and

\[
e_R(O_e[T])\le e_R(Q[T])+1\le46.
\tag{2}
\]

For each of the six listed \(T\), every nine-subset contains a red
triangle. Therefore every red-triangle-free \(S_w\subseteq T\)
has size at most eight, in \(Q\) and also after adding a red edge:

\[
\sum_{w\in W}|S_w|\le4\cdot8=32.
\tag{3}
\]

The certificate contains a triangle-free eight-set in each row too,
so these base capacities are exactly eight. Sharpness is not needed
for the exclusion.

All finite facts are established directly from the displayed input,
without importing a small Ramsey number or graph catalogue.
The primary checker tests all \(\binom{22}{14}=319770\) 14-subsets
against the literal red four-cliques. The separate checker constructs
clique-free sets by increasing-vertex recursion, rejecting a forbidden
clique when its newest vertex is inserted. It independently reconstructs
all six rows, their internal densities, the complementary clique,
and the nine-/eight-subset capacity statements.

## 4. Uniform density cut and the sixteen-choice conclusion

Combining (1), (2) and (3) gives

\[
t_R(v)\le13+46+32=91<92.
\]

Hence no coloring in the stated sixteen-choice family realizes the
required marked density.

[CERTIFICATE.json](CERTIFICATE.json) records the exact surviving
14-domain indices and bounds for each candidate. The candidate-specific
upper bound is 90 except for additions \((9,17)\) and \((11,14)\),
where it is 91. In particular, the selected \((0,10)\) graph has bound 90.
These are upper bounds, not claims that equality is attainable.
\(\square\)

## 5. Dependencies, overlap and remaining scope

This combines the marked H20 degree/density interface with the
independently developed R2 local graph, transported through the
sixteen O22 constructions. The individual neighborhood constructions
remain valid. The new mathematical content is their incompatibility
with the stated density and coverage requirements.

During the final overlap audit, Helgi published
[the exact 100-case marked-pair decomposition](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_marked_pair_decomposition),
source c281801fd5341821de0f72ab9a83442573a277b9.
It already supplies the five maximal attachments of the selected
O22 graph, shows that the high-density attachment has no locally valid
partner, and retains 100 valid 25-vertex local graphs.
Those counts, the selector encoding and that local obstruction are
not claimed anew. Its marked neighborhood densities remained open.

For the selected O22 graph, the density cut closes all 100 cases
simultaneously under the hard-profile requirements, before its 396-edge
residual search. The same cut excludes the other fifteen published
O22 choices, without claiming that the 100-case list applies to them.

The earlier 15-vertex three-switch theorem remains valid, but no
binary complementary-block face was found inside a 43-vertex survivor.
This pass explicitly changed the transfer target when the new O22
source became available. A provisional maximum-state compatibility
argument also proved a bound, but the new attachment source exposed
the simpler complementary-clique proof used here. Unnecessary state
enumerations are not part of the published evidence.

Stop this family under the displayed hypotheses. Another pass must
change an explicit input: a different O22 core, marked H20, or
signature/profile family. Re-solving these same sixteen cores with
all 440 variables cannot defeat this obstruction.

Neighborhood gluing is classical; see Angeltveit and McKay,
[*R(5,5) ≤ 46*](https://arxiv.org/abs/2409.15709).
No historical-priority claim is made for neighborhood clique tests,
capacities or gluing. The new claim is the exact conditional
family exclusion above.
