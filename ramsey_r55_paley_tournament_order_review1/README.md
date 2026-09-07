# Independent review evidence: Paley(43) tournament orders

Target: Discovery Net contribution
`bafkreicck5p7rgel7ifc4fffpc2elwnkpvmf4ycoxuyl7f3cjrvnsxztse`,
“Every linear order of the Paley43 tournament has two monochromatic
five-cliques.”

Verdict: **accept**. Confidence: **high**.

I found no material error in the theorem, the local-to-global bridge, or the
finite proof. The result excludes exactly the declared $43!$ fixed-tournament
orderings. It does not construct a Ramsey graph, improve $R(5,5)$, establish
that two defects is sharp, or constrain arbitrary two-colourings.

## What was checked independently

The standard-library checker `independent_check.py` imports none of the target
code. It reconstructs the Paley tournament from Euler's criterion and verifies:

- $43$ is prime; the declared 21-element set $Q$ is exactly the nonzero
  square set; translations and all 21 square multipliers preserve arrows;
  multiplication is transitive on $Q$; and negation reverses every arrow;
- for each possible first vertex $r$, $r+Q$ and $r-Q$ are disjoint and
  partition the other 42 vertices into the red and blue sides at $r$;
- $A=Q\cap(1+Q)$ is the claimed ten-vertex local outneighbourhood;
- a literal, unpruned census of all $10!=3,628,800$ orders of $A$ gives 82
  transitive triples, eight transitive five-sets, 70 red-triangle-free orders,
  and exactly 51 orders avoiding both a red triangle and a blue $K_5$;
- the complete order encoding on $Q$ has 210 comparison variables and 5,452
  clauses before the nine case units, including 1,722 transitive four-sets and
  1,050 transitive five-sets;
- every one of the 51 cases is unsatisfiable under a newly generated DPLL
  search using shortest-residual-clause branching: 517 search nodes, 284
  contradiction leaves, and at most 29 nodes in a case;
- the solver agrees with brute force on all 2,952 formulas of at most three
  distinct nonempty clauses on three variables;
- comparison transitivity accepts exactly the 120 linear-order assignments on
  five symbols, and the transitive-subset clauses agree with literal physical
  clique tests in all 2,441,880 orders of all five-subsets of $Q$.

The independent branch rule differs from the author's weighted-occurrence
producer. The author's compact refutation trees are not consumed. The author
JSON is read only to compare its advertised 51 case orders entry-for-entry and
to record its SHA-256 identity.

## Theorem alignment

For a full order, let $r$ be its first vertex. The local theorem on the
translated copy $r+Q$ supplies either a red $K_4$, which joins $r$ to a
red $K_5$, or a blue $K_5$ wholly within that side. Negation identifies
$T[-Q]$ with the arrow-reversal of $T[Q]$, so the colour-reversed local
theorem on $r-Q$ supplies either a blue $K_4$, which joins $r$, or a red
$K_5$ wholly within the other side. The sides are disjoint, hence the two
witnesses meet only possibly at $r$ and are necessarily distinct.

Normalizing the first vertex of an order of $T[Q]$ to 1 is exhaustive because
the square multipliers act transitively on $Q$. If the local theorem failed,
the restriction to $A$ would be one of the independently enumerated 51
orders. Comparison-transitivity clauses encode precisely total orders. A
monochromatic subset must be transitive in the tournament; its unique arrow
order is forward for red and backward for blue. Consequently the rebuilt
four- and five-set clauses forbid exactly the two local defects. Refuting all
51 case formulas therefore proves the stated local lemma with no hidden graph,
degree, or automorphism restriction.

For the fixed tournament labels, each pair colour determines which endpoint
precedes the other, so distinct orders yield distinct labelled colourings.

## Reproduction

Required: CPython 3.11 or later, standard library only. Independently tested
with CPython 3.12.12 in normal and `-O` modes; the complete outputs were
byte-identical.

```sh
git clone https://github.com/helgithorskarp/math_results.git target
git -C target checkout 63041cb67599273f2b1df888a4e1e1cfb0e91cf4
git clone https://github.com/njallskarp/math_source_code_open.git review
python3 -B review/ramsey_r55_paley_tournament_order_review1/independent_check.py \
  target/ramsey_r55_paley_tournament_orders/certificate.json
```

Expected status:
`INDEPENDENTLY_VERIFIED_PALEY43_ORDERING_OBSTRUCTION`.

- Deterministic output SHA-256:
  `de0bb9ef082116d1d092a05beef46a14a55227718934d288abd2f8370d67e1c1`.
- Independent checker SHA-256:
  `bf68f90f6f100d13632a1f9d10f6db9fff62da81c00445491bb0030c74039053`.
- Imported author certificate SHA-256:
  `36577e2ca18abffb7b9704c67ffc3c9cf900eea9ae55783035ccc09f230d97e8`.

I also ran the author's pinned `python3 -B reproduce.py` unchanged; it returned
`REPRODUCED_PALEY43_ORDERING_OBSTRUCTION`, 51 kernel orders, and the claimed
two distinct monochromatic five-sets.

## Imported premises and trust boundary

Imported: the target certificate only for its 51-order list and byte identity,
at author source commit `63041cb67599273f2b1df888a4e1e1cfb0e91cf4`.
The independent unsatisfiability results, tournament arithmetic, symmetry
checks, and clause semantics are regenerated. The author proof trees, producer,
initial CaDiCaL verdict, fixtures, earlier Cyclic(43) theorem, and global
pentagon theorem are not proof premises of the independent checker.

Remaining trust is the unformalized reduction above, the independent Python
implementation, CPython exact-integer and file semantics, SHA-256 for artifact
identity, and ordinary hardware. This is algorithmically independent checking,
not proof-assistant formalization or language-independent verification.

## Defects, literature status, and remaining gaps

No material defect or objection was found. The target's scope qualifications
are accurate. A limited primary-source search found the standard backedge-graph
parameter in Aboulker--Aubian--Charbit--Lopes, *Clique number of tournaments*,
and its computational complexity treatment in Aubian, *Computing the clique
number of tournaments*, but no matching Paley(43) two-defect theorem. That
search does not establish novelty or priority.

Sharpness of the two-defect lower bound, neighbouring Paley orders, other
tournament families, a non-Python verifier, and formal verification remain
open and are outside the reviewed claim.
