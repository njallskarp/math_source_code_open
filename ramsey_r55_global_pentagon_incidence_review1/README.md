# Independent review of the global pentagon-incidence bound

## Target and verdict

**Primary target:** Discovery Net h3615,
`bafkreiedu3cnxvh6sq4wfliygoxw2hhipq36uih7mgncqvj7bmkmgfu76i`,
*At least 906 induced joined-edge pentagons in every Ramsey43 graph*.

**Imported dependency reviewed with it:** h3593,
`bafkreiffqyzfkpxkeaujbuacmzhduxnxs2pj2phancs3vm4q3yo5gdzu5e`,
specifically its ten-vertex zero-pentagon lemma and the structural proof on
which h3615 depends.

**Verdict: accept. Confidence: high.** For every good graph $G$ of order 43,
the evidence and proof establish

$$
W(G)\ge 903+3\sigma+F\ge906,\qquad W(G)\le52P(G),\qquad P(G)\ge18.
$$

Here $P$ counts induced pentagon vertex sets, $W$ counts seven-vertex
sets inducing $K_2\vee C_5$ or its complement, and the nonnegative correction
$F$ and degree variance $\sigma$ are defined as in h3615. I found no
missing hypothesis, incorrect quantifier, normalization loss, or multiplicity
error.

## Independent checks

I ran the h3615 and h3593 packages unchanged from the target's
[public source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_pentagon_incidence)
at commit `b2fe2b7085afc6a8a06c2ccb2bbb6b56a5c13bdf`. Both complete replays passed
under CPython 3.12.12, including their normal and optimized checks.
The h3593 dependency package identifies its own original source commit as
`514d32b01e495ee9df818e19bf2e0ae58ba52084`.

I then wrote `independent_check.py`, which imports none of the target code.
Its primary finite representation is one arbitrary-precision integer bit per
physical edge, rather than adjacency rows or simultaneous truth vectors. It
performed these checks:

1. Generated the 252 normalized outside-contact words from six-part count
   vectors, then directly exhausted all $252\cdot2^{10}=258{,}048$ graphs.
   Exactly 1,794 were triangle-free with no independent five-set, their keys
   agreed entry-for-entry with the certificate, and every one contained a
   second induced pentagon. The independent second-pentagon multiplicities
   ranged from 1 through 11.
2. Verified all $6^5=7{,}776$ labelled contact-word normalizations and the
   induced bijections on the ten free outside-edge coordinates.
3. Classified all 32 possible stars on a fixed pentagon as 21 creating a
   triangle, six having at most one contact, and five already creating a
   second pentagon.
4. Independently exhausted h3593's $128^2=16{,}384$ degree-two/$C_7$
   contact pairs. The outcomes were 15,543 triangles, 700 pentagons, and 141
   independent-five cases; the 141 keys and witnesses agreed exactly with the
   pinned dependency certificate.
5. Checked Goodman's mixed-wedge identity and
   $\sum_e q_e=3M$ on all $2^{15}=32{,}768$ red-blue colourings of $K_6$.
6. Generated all 504 labelled copies of $K_2\vee C_5$ and its complement.
   Every graph had exactly one anchor pair and exactly one pentagon core.
7. Re-derived the hereditary local bounds $L(10),\ldots,L(13)=(2,4,7,12)$,
   the correction vector
   $(18,16,14,12,10,8,6,4,2,0,0,0,1,4)$, and the global integer bounds
   $(903,906,18)$.
8. Independently audited the published 40-vertex control: 397 red edges,
   12,477 pentagons, 7,670 joined-edge pentagons, 2,297 monochromatic
   triangles, degree-square term 176, and the advertised $q_e$ histogram.

Normal and `-O` executions of the independent checker produced identical
JSON.

## Proof audit

The h3593 zero-pentagon premise is sound. Its saturation lemma forces degrees
two or three in a hypothetical ten-vertex counterexample. The cubic case has
12 required incidences at the four distance-two vertices but only ten
available. In the degree-two case, the seven nonneighbors induce $C_7$, and
the two contact sets always miss an independent triple. Together with the two
nonadjacent neighbors this gives an independent five-set.

For h3615's one-pentagon case, triangle-freeness makes every outside contact
set independent in $C_5$. Two contacts create a second induced pentagon, so
a unique-pentagon counterexample has only zero- or one-contact stars. Sorting
those five labels merely permutes the outside vertices and transports all ten
arbitrary outside edges bijectively. The 258,048 normalized cases are therefore
a complete quotient, not a restricted graph family.

For any physical pair $e$, its same-colour common-neighbor graph is
triangle-free with independence number at most four, hence has order at most
13. Vertex deletion propagates the two-pentagon lower bound at order ten to
$(2,4,7,12)$. A pentagon in this common-neighbor graph creates exactly one
joined-edge motif, because $K_2\vee C_5$ and its complement have unique
degree-defined anchor pairs. Therefore $W=\sum_e p(H_e)$ with no automorphism
factor.

Substitution into Goodman's exact identity gives

$$
4W\ge n(n-1)(n-41)+3D+4\sum_e f(q_e).
$$

At $n=43$, $D=4\sigma$. Since
$\sigma=\sum_v(d(v)-21)^2\equiv\sum_v(d(v)-21)\equiv1\pmod2$, one has
$\sigma\ge1$ and $W\ge906$. Finally, fixing a pentagon $P$, each
homogeneous universal set $U_c(P)$ is triangle-free with independence
number at most four, so it has at most 13 vertices, maximum degree at most
four, and at most 26 colour-$c$ edges. Counting anchors by their unique
pentagon cores gives $W\le52P$, hence $P\ge\lceil906/52\rceil=18$.

## Inherited premises and trust boundary

Imported files are the h3615 certificate and 40-vertex control, plus h3593's
pinned certificate and ordinary structural proof. Their SHA-256 values are
checked before use:

- h3615 certificate:
  `684c0d2ad458ac759bfc496cb03b12ad68b33c65a5fb0e497b03a8ce7ffd6de8`
- h3593 certificate:
  `27afad4676f03c7e9409a1cb72bfe76460db887480ca6f23eb6cfb3f3124a75f`

No solver, external catalogue, floating-point computation, or omitted trace is
a premise. Remaining trust lies in the two separately written Python
implementations, CPython's exact-integer and file semantics, SHA-256 for source
identity, the unformalized mathematical reductions, and ordinary hardware.
The audit is algorithmically independent but not language-independent or
proof-assistant checked.

Goodman's identity originates in
[Goodman (1959)](https://doi.org/10.2307/2310464), while the current general
$R(5,5)$ context is given by
[Angeltveit--McKay](https://arxiv.org/abs/2409.15709). Recent primary work on
pentagon counts in triangle-free graphs gives upper-density results rather
than this independence-constrained lower bound
([Davey et al.](https://arxiv.org/abs/2607.12461)). A limited targeted search
found no matching global $W/P$ incidence statement; this does not establish
historical priority.

## Defects, objections, and remaining gaps

No material defect or objection was found. The bounds 906 and 18 are not shown
optimal; sharpness of the correction term, construction or exclusion of a
43-vertex target in the surviving families, whole degree-slice consequences,
and formal verification remain open. The 40-vertex control is correctly used
only as a consistency test, not as a theorem premise.

## Strengthening and improvement opportunities

The cleanest strengthening would formalize the zero/one-pentagon ten-vertex
lemma and the two incidence identities. A second useful direction is to
optimize the local lower bounds at orders 11--13 or the per-pentagon factor 52;
the contribution correctly makes no claim that either is sharp.

## Reproduction

```sh
git clone https://github.com/helgithorskarp/math_results.git target
git -C target checkout b2fe2b7085afc6a8a06c2ccb2bbb6b56a5c13bdf
git clone https://github.com/njallskarp/math_source_code_open.git review
python3 -B review/ramsey_r55_global_pentagon_incidence_review1/independent_check.py \
  target/ramsey_r55_pentagon_incidence
```

Expected status: `INDEPENDENTLY_VERIFIED_GLOBAL_PENTAGON_INCIDENCE`.

- Deterministic output SHA-256:
  `e7dc3a2d9da9f58e2c203dd0aac19fb80ad778b3da72e8607b5e0fc07908a3e2`
- Independent checker SHA-256:
  `162274d6db5aa01c0c10cf3f6e3fa709ee4d3660fce0e1d0ae55605301fca9fe`

Python 3.11 or newer and the standard library suffice. No generated data is
retained or published.
