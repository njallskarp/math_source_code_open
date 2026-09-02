# Audit of the 17-vertex Charney--Davis proof candidate

## Status and exact theorem

This is a frozen, audit-ready proof candidate. It makes no priority claim and
has not received independent mathematical acceptance.

Let `K` be a field and let `Delta` be a finite flag generalized homology
5-sphere over `K` with 17 vertices. The claimed conclusion is

```text
gamma_3(Delta) >= 0.                                             (T)
```

The proof below is the complete logical path. No classification, census, or
large computation is used.

## Conventions

`Delta` has dimension 5, so its h-polynomial has degree `d=6`. We use the
standard dimension-indexed face numbers `f_{-1}=1, f_0, f_1, ...` and

```text
h_Delta(t) = sum_{i=0}^6 f_{i-1} t^i (1-t)^(6-i)
           = sum_{i=0}^3 gamma_i t^i (1+t)^(6-2i).               (N1)
```

Labbé--Nevo index faces by cardinality, so their `f_1` and `f_2` are our
`f_0` (vertices) and `f_1` (edges). Every formula below has been translated
to (N1).

Let `G` be the one-skeleton of `Delta` and `H` its simple complement. Put

```text
q_v = degree_H(v),  m = |E(H)|,  T = number of triangles of H,
pi(Delta) = min_v q_v.
```

Thus an "antipode" of `v` in Labbé--Nevo is simply a nonneighbor in `G`, and
there are `q_v` of them. Empty/induced four-cycles and links always mean
simplicial ones in the flag complex; no metric antipodal relation is used.

A generalized homology sphere over `K` means that the link of every face,
including the empty face, has the reduced `K`-homology of the sphere of the
corresponding dimension. Flag means that every clique of `G` is a face.

## External mathematical inputs

The following are trusted published inputs, not Lean theorems in this package.
The numbering refers to the cited papers.

1. **Links.** Labbé--Nevo Lemma 2.1(i): the link of any face of a flag
   homology sphere is an induced flag homology sphere.
2. **Low gamma coefficients.** Labbé--Nevo Lemma 2.2, translated to (N1):
   for a homology `(d-1)`-sphere with `n` vertices and `e` edges,

   ```text
   gamma_1 = n-2d,
   gamma_2 = e-(2d-3)n+2d(d-2).                                  (E1)
   ```

   Equivalently, if `a` is the number of missing edges,

   ```text
   a + gamma_2 = gamma_1(gamma_1+5)/2 + d.                        (E2)
   ```

3. **Suspension and contraction.** Labbé--Nevo Lemma 2.3: suspension
   preserves the gamma-polynomial, and an admissible edge contraction obeys
   the stated gamma recurrence.
4. **Polar size.** Labbé--Nevo Lemma 3.2 for a flag homology `(d-1)`-sphere
   on `2d+ell` vertices:

   ```text
   gamma_1(link(v)) = ell-q_v+1,
   1 <= pi <= ell+1,
   pi=1 iff the sphere is a suspension,
   pi=ell+1 (for d>=3) iff ell=0 and the sphere is octahedral.     (E3)
   ```

5. **The polar-size-two decomposition.** Labbé--Nevo Lemma 3.4: if a vertex
   has exactly two antipodes `x,y`, then `xy` is admissible and

   ```text
   gamma_Delta(t) = gamma_link(v)(t) + t gamma_link(xy)(t).       (E4)
   ```

6. **High polar-size vanishing.** Labbé--Nevo Corollary 4.3: if `pi>=3`,
   then `gamma_j=0` for `j>=ell-pi+2` (under its stated `d>=3` hypothesis).
7. **First gamma coefficient.** Gal Lemma 2.1.14, or equivalently the
   minimum-vertex bound for a flag homology sphere, gives `gamma_1>=0`.
8. **Four-dimensional link nonnegativity.** Gal Corollary 2.2.3 says, in his
   GHS convention, that a flag generalized homology sphere of dimension below
   five has nonnegative gamma-vector. For dimension four, the substantive input is the
   Davis--Okun Theorem 11.2.1 for flag triangulations of rational homology
   3-spheres, applied to vertex links as in Gal Corollary 2.2.2.

The last input is normalized as follows. For a flag rational homology
3-sphere `S`, Davis--Okun prove `kappa(S)>=0`, where

```text
kappa(S) = sum_{i=0}^4 (-1/2)^i f_{i-1}(S).
```

With (N1), `h_S(-1)=16 kappa(S)=gamma_2(S)`. For a 4-dimensional
Eulerian complex `Y`, Gal Corollary 2.2.2 specializes to

```text
gamma_2(Y) = (1/8) sum_{v in Y} kappa(link_Y(v)).                 (E5)
```

Thus Davis--Okun makes every summand nonnegative for a flag rational
homology 4-sphere. This is the rational-homology version of Gal's proof of
Corollary 2.2.3; it uses only the Eulerian relations and rational
homology-sphere vertex links. There is no sign change and no missing factor.

### Coefficient-field bridge

Davis--Okun state their theorem for rational homology spheres, whereas
Labbé--Nevo allow a homology sphere over a field. The bridge used here is:

> If a finite simplicial complex is a homology sphere over some field `K`, it
> is a rational homology sphere; the same holds for every face link.

Indeed, for each finite integral simplicial chain complex, vanishing over `K`
forces every lower integral homology group to have rank zero. Hence the lower
rational Betti numbers vanish. Euler characteristic is coefficient
independent, so the top rational Betti number is one. Apply this separately
to every link. This elementary field-change argument is written here in full
but is not formalized in Lean. A reviewer should check that their chosen
definition includes all face links, as assumed above.

## Minimal proof

Assume for contradiction that `gamma_3(Delta)<0`.

### 1. Polar size is exactly three

Write `17=2*6+5`, so `d=6` and `ell=5` in (E3).

- If `pi=1`, `Delta` is a suspension. Its base is a flag homology 4-sphere;
  suspension preserves gamma, and a degree-five h-polynomial has no
  `gamma_3`. Thus `gamma_3(Delta)=0`.
- If `pi=2`, (E4) applies. The 4-dimensional vertex link contributes no
  `gamma_3`; the edge link is a flag homology 3-sphere, so Davis--Okun gives
  its `gamma_2>=0`. Hence `gamma_3(Delta)>=0`.
- If `pi=4` or `pi=5`, Corollary 4.3 gives `gamma_3=0`.
- If `pi=6=ell+1`, (E3) would force `ell=0`, contrary to `ell=5`.

Therefore

```text
pi(Delta)=3.                                                      (P)
```

Furthermore (E3) and `gamma_1(link(v))>=0` give

```text
3 <= q_v <= 6  for every vertex v.                               (B)
```

This derivation does not require the separate 16-vertex theorem or the
admissible-edge formalization. Those older artifacts are corroborating but
logically redundant in the shortest proof.

### 2. Three identities

The vertex-link h-polynomial identity for a pure 5-complex is

```text
sum_v h_link(v)(t) = 6 h_Delta(t) + (1-t) h'_Delta(t).            (I1)
```

Differentiate and set `t=-1`. In the gamma basis this is exactly

```text
sum_v gamma_2(link(v)) = 3 gamma_3(Delta)+4 gamma_2(Delta).       (I2)
```

All vertex links are flag homology 4-spheres by Input 1 and the definition of
a generalized homology sphere. The field bridge and Input 8 therefore make
every summand in (I2) nonnegative.

Equation (E2), with `gamma_1(Delta)=17-12=5`, gives

```text
sum_v q_v = 2m = 62-2 gamma_2(Delta).                             (I3)
```

Finally, count triples of vertices by the number of their `H`-edges. Since
`Delta` is flag, its 2-faces are exactly the triangles of `G`. Starting
with all `C(17,3)` triples, subtract `(17-2)m`, restore the pairs of incident
`H`-edges counted at each vertex, and subtract the `H`-triangles. This gives

```text
f_2(Delta) = C(17,3)-15m+sum_v C(q_v,2)-T.
```

Extracting the coefficient of `t^3` in (N1) yields

```text
2 gamma_3(Delta) = 348 + sum_v q_v(q_v-10) - 2T.                 (I4)
```

`audit_check.py` exhaustively verifies the underlying triple identity for
every simple graph on at most six vertices, independently checks the symbolic
specialization at 17 vertices, and enumerates the small integer squeeze below.
This is adversarial self-checking, not an independent proof acceptance.

### 3. Rigid complement profile

From (I2), nonnegativity of the link coefficients, and
`gamma_3<=-1`, integrality gives `gamma_2>=1`. From (P), (I3), and
`sum q_v>=51`, one gets `gamma_2<=5`. Equation (I2) then gives
`gamma_3>=-6`.

For every integer `q` in `[3,6]`,

```text
q(q-10) <= -21,
```

and at least one `q_v` is at least four because (I3) gives
`sum q_v >=52`. Its summand is at most `-24`. Since `T>=0`, (I4) gives
`2 gamma_3<=348-16*21-24=-12`. The previous lower bound forces equality
throughout:

```text
gamma_2(Delta)=5,       gamma_3(Delta)=-6,
T=0,                    {q_v : v in Delta} = {3^16,4^1}.          (R)
```

The equality in (I2) also says that the sum of all vertex-link
`gamma_2` coefficients is two.

### 4. The degree-four vertex produces the contradiction

Let `r` be the unique vertex with `q_r=4`, let `N=N_H(r)`, and let
`B=V(H)\({r} union N)`. Thus `|B|=12`. Since `T=0`, `N` is independent.
Every vertex in `N` has complement degree three, so after its edge to `r` it
has exactly two edges to `B`. Consequently

```text
|E(H[B])| = m-4-4*2 = 26-12 = 14.                               (L1)
```

Because `Delta` is flag, its vertex link at `r` is precisely the clique
complex of the induced graph `G[B]`, equivalently the independence complex
of `H[B]`. Thus this 4-dimensional link has 12 vertices and
`C(12,2)-14=52` edges. Formula (E1), now with `d=5`, gives

```text
gamma_2(link_Delta(r)) = 52-7*12+30 = -2.                        (L2)
```

But Input 1 makes this link a flag homology 4-sphere, and the exact
Davis--Okun/Gal bridge above requires its `gamma_2` to be nonnegative. This
contradiction proves (T).

## Lean alignment and trust boundary

Lean 4.33.1/Mathlib v4.33.1 checks the following relevant statements without
`sorry` or custom axioms.

| Lean theorem | What the kernel checks | What is supplied as a hypothesis |
|---|---|---|
| `eval_negOne_derivative_hFive` | top gamma extraction in degree five | nothing |
| `eval_negOne_derivative_vertexLinkRhs` | derivative of (I1) gives the right side of (I2) | nothing |
| `sum_vertexLink_gammaTwo_eq` | (I1) implies (I2) | the polynomial identity (I1) |
| `negative_forces_polarSize_three` | the exhaustive integer case split in Step 1 | the published consequences for `pi=1,2,4,5,6` |
| `gammaTwo_bounds_of_negative` and `gammaThree_lower_bound_of_negative` | first arithmetic squeeze | link nonnegativity and (I3) |
| `negative_forces_rigid_complement_profile` | (B), (I2)--(I4) force all of (R) | those identities and inequalities |
| `degreeFour_linkGammaTwo_eq_negTwo` | (L1), the complement edge count, and (L2) | the local face-count hypotheses |
| `negative_counterexample_impossible_from_degreeFour_link` | the final contradiction | all preceding interfaces, including a degree-four local-count witness and link nonnegativity |

`#print axioms` reports only `propext`, `Classical.choice`, and `Quot.sound` for
the global theorems; the local arithmetic theorem uses only `propext` and
`Quot.sound`. These are standard Lean/Mathlib logical foundations, not
mathematical assumptions. The kernel does **not** verify:

- the definition or topology of generalized homology spheres;
- preservation of flagness/homology-sphere status under links, suspension, or
  the Labbé--Nevo contraction;
- the cited Labbé--Nevo, Davis--Okun, or Gal theorems;
- the coefficient-field bridge;
- the face/link identities (I1), (I3), (I4) from simplicial definitions;
- that the graph-theoretic data supplied to the final Lean theorem arise from
  a particular `Delta`.

Those are human-checked mathematical inputs. The Python checker does not
reduce that trust boundary.

## Adversarial bridge audit

| Bridge | Counterexample search/check | Outcome and residual risk |
|---|---|---|
| Polar size three | Checked all six values allowed by Lemma 3.2 with `d=6, ell=5`; used Lemma 3.4 directly at two | Only three remains. Reviewer must confirm the cited hypotheses and that suspension removes the top gamma term. |
| Uniform `3<=q_v<=6` | Lower bound is the definition of `pi`; upper bound is `gamma_1(link(v))=6-q_v>=0` | No arithmetic gap. Reviewer must verify Gal's `gamma_1>=0` applies over the chosen field. |
| Link sum (I2) | Direct symbolic differentiation in Lean | Exact conditional result; derivation of the simplicial identity (I1) remains human mathematics. |
| Complement identity (I4) | Inclusion--exclusion derivation plus exhaustive simple-graph test through six vertices | No counterexample found; the finite test is not a proof for 17 vertices, while the triple count is. |
| Rigid profile (R) | Lean proof and independent enumeration of all count vectors with `q_v in [3,6]` | Unique feasible arithmetic profile. Realizability is unnecessary: every counterexample would have to realize it. |
| Degree-four local count | Recounted each edge class; `audit_check.py` checks all numeric conversions | No parallel-edge or loop issue because `H` is a simple graph. Flagness is essential when identifying the full link. |
| `gamma_2=-2` | Both h-coefficient expansion and (E1) give `52-84+30` | Normalization agrees. Reviewer should check face-index translation. |
| Gal/Davis--Okun | Traced dimension, sign, and factor: `h(-1)=16 kappa=gamma_2` in dimension three | Davis--Okun is not applied directly in dimension four; Gal's link argument is. Field change remains unformalized. |
| Link hypotheses | Labbé--Nevo Lemma 2.1(i) and the defining all-links condition | Reviewer must verify the exact generalized-homology-sphere convention and purity. |

No bridge has an internally discovered counterexample. This table records
self-review only and must not be read as independent acceptance.

## Dependency ledger

The shortest proof depends on the primary-source inputs 1--8, the elementary
field-change argument, identities (I1)--(I4), and the graph count (L1). The
older admissible-edge formalization is not needed after using Labbé--Nevo
Lemma 3.4 directly. The Discovery Net dependency edge from the polar
reduction to the admissible-edge artifact records the historical derivation,
not a logically minimal dependency.

Committed Discovery Net artifacts before this audit are:

- problem `bafkreid3obaz2cfq2nyd3v2ernkylaa3iv7l3otwzok7zwyxymqkukstme`
  (height 1252);
- admissible-edge lemma `bafkreigmon4jz2f35532xyk7laypnwyseco2w3eyutlh6icpz2ng5mwlsq`
  (height 1266) and Lean formalization
  `bafkreibcsr3rq3mzwz2sjroaizgdzpwwoz7dkmicq4z7ykngmxa7hfkyb4`
  (height 1272);
- polar-size-three reduction
  `bafkreifnrv4waqgddweuh4bsubdsckwfr4dxbighdakazpyyefytu5l6jy`
  (height 1290) and Lean formalization
  `bafkreic6oixginkapr6e7yfe332d5zyjbxci45lhzptiq5buwl3brl225u`
  (height 1292);
- rigid profile `bafkreib3pqtvco6xcm5q4nvsva2q4seokswkgyl7pvjotxsrxvmss5rxqe`
  (height 1300) and Lean formalization
  `bafkreidhubjjygm6j62cvlzvizd3r2qs4qu3pgncbmtz3zjd3vxk2gtaju`
  (height 1306);
- closure proof attempt
  `bafkreieceq3ktydrabvxlu6fqn7zllvmi6lk4346k4y35ylczmychowcha`
  (height 1308) and Lean formalization
  `bafkreibabtawjk3jj6qw6ebw6g3kjpsllas4mmnpa5vbgbfykupfpkwuwa`
  (height 1310).

The artifact kind `proof_attempt` is intentional pending qualified review.

## Acceptance and stopping rule

The project remains frozen. Independent acceptance requires a qualified
reviewer to verify the primary-source statements and the human bridges listed
above, then record an explicit review disposition. Any objection takes
priority over expansion. No neighboring conjecture, higher vertex count, or
additional structural lemma belongs in this package before that review.
