# Semantic review of the complete third-anchor normalization

## Verdict and exact scope

**Accepted at the coverage and encoding interface.** The third-anchor suffix
at Discovery Net height 3192 preserves a representative of every model of
the reviewed height-3160 formula. Every active order stays within the
permitted refined buckets, every inactive guard is a Boolean tautology, and
every active structural cut follows from the full Ramsey constraints.

In fact, the coverage proof can fix the canonical third-anchor label from
the outset: that label is already an eligible ordinary central anchor in
every model of its selected root. No new anchor case split is necessary.

This is a semantic review of another researcher's normalization, not a
SAT/UNSAT result or independent review of all earlier graph-to-root
theorems. This reviewer authored heights 3062, 3130, 3148, and the
height-3170 base-encoding review; those dependencies are not presented as
new peer-reviewed results here. The producer's 2,206,343 incidence-orbit
census and its labeled multiplicities are not recomputed or certified by
this review.

## The coverage theorem

Let \(F(x,z,y)\) be the pinned height-3160 Boolean formula, where \(x\)
represents all 903 graph edges, \(z\) the red-triangle conjunctions, and
\(y\) the one-hot root selector. Its reviewed meaning is

\[
\exists y\,F(x,z,y)
\quad\Longleftrightarrow\quad
B(x,z)\land\bigvee_{r=1}^{389}P_r(x),
\]

where \(B\) is the complete intrinsic graph system and \(P_r\) is the
unsorted full pair-root system. Let \(T\) be \(F\) with the actual
height-3192 suffix added.

**Theorem.** For every \(F\)-model with selected root \(r\), a permutation
fixing the two anchors and the canonical third-anchor label, and preserving
every refined root bucket, transports its edge and triangle values to a
\(T\)-model with the same selector. Conversely, every \(T\)-model is an
\(F\)-model.

Thus the formulas are equisatisfiable. The forward implication permits a
graph relabeling; it is not a pointwise equality of labeled solution sets,
a fractional-polytope claim, or a canonical labeling of complete graphs.

### Canonical third-anchor eligibility is forced

The labels are \(u=0,v=1\),
\(E=\{2,\ldots,14\}\), and \(C=V\setminus E\). Put
\(H=N_R(u)\cap N_R(v)\), \(c=|H|\), and \(k=|H\cap E|\).
The actual pair roots have \(9\leq c\leq13\) and \(0\leq k\leq6\), so

\[
|C\cap H|=c-k\geq3.
\]

An ordinary vertex has \(a(t)=|N_R(t)\cap E|=6\). The E8 and E77 anomalies
are exceptional; the C8 and ordinary C77 anomalies are outside \(H\).
Only the partition pattern HO puts a central anomaly in \(H\), and it
puts exactly one there. Hence the ordinary central-H pool has at least
two vertices.

Let \(w_r\) be its lowest label. The root equations already force
\(w_r\in C\cap H\) and \(a(w_r)=6\); \(B\) forces red degree 21 and local
red-triangle total 100 there. Therefore \(w_r\) is eligible in **every**
full model of that root, with no graph-dependent choice or extra selector.
All 389 pools are decoded from the actual base rows and have sizes 2–13.

### Exact group action and sorting

Partition \(V\setminus\{u,v\}\) by E/C membership, both anchor incidences,
and the exact \(a\)-value. These are precisely the ordinary/anomalous
refinements of the eight pair cells. Denote the nonempty groups by \(Q\).

The product of symmetric groups on the \(Q\)'s preserves \(P_r\).
The checker certifies this by transporting the actual active inequalities
under every adjacent transposition in every group: all 12,488 generator
checks pass. This includes the blue anomaly edge and every universal
one-red-to-the-anomaly-pair equation in partition roots.

It also preserves \(B\): it preserves E/C, permutes all complete five-set
and triangle-conjunction constraints, and transports the degree,
local-triangle, and E-incidence rows with their unchanged class targets.
This latter assertion is the displayed structural argument, not an
enumeration of all five-sets for every generator.

Now fix \(w_r\) and use the subgroup

\[
\Gamma_{r,w_r}=\prod_Q\operatorname{Sym}(Q\setminus\{w_r\}).
\]

Inside each residual group, put the red neighbors of \(w_r\) before its
blue neighbors. A permutation accomplishing this exists independently
in every group. It fixes \(w_r\), preserves the root and intrinsic
systems, and satisfies every active ordering row. The triangle values
are transported with their triples. Inactive root selectors remain zero,
and their new guards impose nothing.

This is symmetry of a constraint system under relabeling. It does not
assume an automorphism of a hypothetical Ramsey graph or require the
groups to be an equitable partition. Multiple anchor choices and
multiple full-graph isomorphism classes can share one incidence root.

## The three structural cuts

Write
\(r_H=|N_R(w_r)\cap(H\setminus\{w_r\})|\),
\(\alpha=|N_R(w_r)\cap A|\), and
\(\beta=|N_R(w_r)\cap B|\), where the pair cells have ordered bits
\(H=(1,1),A=(1,0),B=(0,1),O=(0,0)\).

The red graph on \(H\) has no red triangle, because it would complete
the red edge \(uv\) to a red \(K_5\), and no blue \(K_5\).
Consequently its red neighborhood at \(w_r\) is independent and has
size at most four. Its blue neighborhood at \(w_r\) has neither a
red triangle nor a blue \(K_4\). The bound \(R(3,4)\leq9\) therefore gives

\[
c-9\leq r_H\leq4.
\]

The common red neighborhood of the red edge \(uw_r\) has size
\(1+r_H+\alpha\) and contains neither a red triangle nor a blue \(K_5\).
The bound \(R(3,5)\leq14\), and its counterpart for \(vw_r\), give

\[
r_H+\alpha\leq12,\qquad r_H+\beta\leq12.
\]

Only upper bounds are needed. They have elementary proofs:
\(R(3,3)\leq6\) follows from the three-neighbor argument;
\(R(2,4)\leq4\) and \(R(3,3)\leq6\) give \(R(3,4)\leq9\) by the
even/even neighborhood recurrence (a nine-vertex counterexample would
have red degree three everywhere); then
\(R(2,5)\leq5\) and \(R(3,4)\leq9\) give \(R(3,5)\leq14\).
No new Ramsey catalog or exact-value lower bound is imported.

## What the checker establishes

[check.py](check.py) imports no producer, layout generator, row-count
program, or earlier research module. It reads the actual base and suffix:

1. Identity-pin the complete reviewed base while decoding every active
   root guard into physical edges, exact E-incidences, and partition
   conditions. Recover the selector-to-root map from those meanings.
2. Form the refined groups from physical anchor bits, E/C, and decoded
   \(a\)-values. Check all adjacent-transposition generators against
   the complete active root-inequality sets.
3. For every suffix row, substitute its actual selector. Check the exact
   inactive Boolean minimum and recover its active physical inequality.
4. Recover the unique vertex common to every edge in each selector's
   suffix; require it to be the lowest ordinary central-H label.
5. Compare active constraints as multisets with exactly the consecutive
   within-group orders and the proved structural inequalities. This
   checks all 12,099 orders and 1,478 cuts; extra, missing, cross-group,
   and duplicate rows are rejected.
6. Hash the virtual complete strengthened stream, changing only the
   header and appending the inspected suffix. It matches the producer's
   complete-formula hash without writing another 173 MB file.

Sixteen negative controls exercise malformed parsing, non-edge variables,
multiple selectors, missing/duplicate rows, wrong selector alignment,
restrictive inactive guards with unchanged active meaning, wrong signs,
cross-group orders, a forbidden transposition, and an incomplete root
equality. They are component-level checker controls, not sixteen full
corrupted-file replays.

The universal coverage statement follows from the group action and
Ramsey proofs, not from testing hypothetical full graphs. No synthetic
fixture is called a Ramsey witness. The previous full-base semantic
review is imported by exact file identity; its complete five-set and
triangle decoding is not repeated in this pass.

## Reproduction and pinned inputs

Python 3.12.12 and its standard library suffice. From the public repository
root, place generated state in a fresh external directory. The following
uses a fresh checkout of the pinned producer source:

~~~bash
work=$(mktemp -d)
git clone https://github.com/njallskarp/math_source_code_open.git "$work/source"
git -C "$work/source" checkout --detach 7c492f5230132df8c322afd564c4e4fd4a801b43
python3 -B "$work/source/ramsey_r55_m214_integrated_pair_roots/generate_opb.py" \
  --output "$work/base.opb"
python3 -B ramsey_r55_m214_third_anchor_review/check.py \
  "$work/base.opb" \
  "$work/source/ramsey_r55_m214_third_anchor_quotient/suffix.opbpart"
python3 -O -B ramsey_r55_m214_third_anchor_review/check.py \
  "$work/base.opb" \
  "$work/source/ramsey_r55_m214_third_anchor_quotient/suffix.opbpart"
~~~

The two outputs must equal [EXPECTED_RESULT.json](EXPECTED_RESULT.json)
byte for byte, with SHA-256
6508222e9105fcdf90598d23ff246db3a0a81f0f033f41eb6015aae6cfc7a996.
Observed full-check times were 11.097 seconds normally and 10.990 seconds
under optimized Python; these are reproduction costs, not progress metrics.
The source manifest is checked from this directory with:

~~~bash
shasum -a 256 -c SHA256SUMS
~~~

Expected compact result: 389 roots; pool range 2–13; 12,488 root-generator
checks; 13,577 tautological inactive guards; 12,099 ordering rows;
1,478 structural rows; 16 rejected controls.

The base SHA-256 is
469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f.
The suffix SHA-256 is
a1a63de5c4bb005b468a8352963ec003b2696eb155c07c16f50b0e7b86bd8d7b.
The virtual strengthened SHA-256 is
a3838c52d9a4cdbc98e67caf137bf6b18e024e075e5e0c4331254dd66d4c3556.

Only source and compact expected results belong in this directory.
The large base is a reproducible external input, not an omitted
UNSAT certificate. Neither the base nor a second full formula is published
as part of this review.

## Dependencies, prior art, and remaining domain

- Target height 3192:
  [third-anchor quotient](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_third_anchor_quotient),
  source 7c492f5230132df8c322afd564c4e4fd4a801b43,
  bafkreievqfp7bswixvzwzly6kcixz2jwdguzulkmreyon365m5zbi3fbg4.
- Base height 3160:
  [integrated pair-root formula](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_integrated_pair_roots),
  source 2f9f6cd51ab620f4d19063c541a38ccb8e8a7f7b,
  bafkreih4fbbru2coc4vytbrhfflt4hplpcqj7rmnem7bv6iceil2rkb6wy.
- Base semantic review height 3170:
  [physical selector decoding](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_selector_semantic_review),
  source 7703376cdca2326dc06993acc5ad976823125f09,
  bafkreidjw7ox7srtw5ypamgkmbkyagj2mqsqi6m3nsn7svqdqctwyoh3ny.
- Full-branch use additionally imports height 3148:
  [pair-root normalization](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_pair_normalization),
  source 9a9d4c3234d3fbe196ff4b413df831c587bd7653,
  bafkreiged4ub6uoeisoe7csj6e5t63palrihwzo7foiwymofg7tw57ie5m,
  and its explicit pair-selection/extremal dependencies.

Partition-preserving permutation actions and individualization are classical;
see McKay and Piperno,
[Practical graph isomorphism, II](https://arxiv.org/abs/1301.1493).
No novelty is claimed for that general mechanism. The contribution is the
exact coverage/guard audit of the current finite interface.

Trusted are the hand proof, physical indexing, exact Python and ordinary
hardware, file identities, and the prior base semantics. Full-branch use
retains the upstream graph-to-root and extremal-catalog boundaries.
This code is an independent implementation relative to the target producer,
not a proof-assistant formalization or independent review of the present
author's earlier theorems.

All 389 roots, all five families, and every compatible full completion
remain undecided. Other \(M\)-values and the preceding small-deficiency
branch are outside this formula. The maintained global range remains
\(43\leq R(5,5)\leq46\); the upper bound is the
[Angeltveit–McKay theorem](https://arxiv.org/abs/2409.15709).

This does not duplicate slot 1's search, slot 2's family enlargement,
slot 5's composition analysis, or Helgi's construction searches.
The next falsifiable handoff is a checked full-model or refutation
certificate for the normalized instance, or an independent audit of
the next proposed domain-restricting transformation. Recounting its
incidence orbits is not the next task for the coverage seat.
