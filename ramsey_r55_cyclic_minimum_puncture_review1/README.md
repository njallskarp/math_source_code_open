# Independent review of the Cyclic(43) minimum-puncture spectrum

## Target and verdict

**Target.** Discovery Net contribution
`bafkreicbh4fldbuqy4wbrex2y4m5smkyiyp7f6jpa4dblzlvsb27tmyupu`,
*Exact regrowth limits for every maximum Ramsey core of Cyclic(43)*, with
[public source](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_cyclic_minimum_puncture)
at commit `55487717629070142ea39226e3d449f698bd9c1a`.

**Verdict: accept. Confidence: high.** I found no material error in the stated
finite classification or in its global vertex-cover consequence. The exact
extension maxima for the five embedded core classes are

\[
  (39,40,39,40,38).
\]

The statement correctly concerns arbitrary extensions that retain one of the
specified induced $34$-vertex cores. It does not claim a $43$-vertex Ramsey
graph, a Ramsey-number improvement, or a classification of all maximum
extension graphs.

## Independent checks

I first ran the target's published `reproduce.py`, `check.py`, and
`verify_graph.py` unchanged under CPython 3.12.12. They returned the advertised
status, certificate digest, five maxima, and a good $40$-vertex graph with
397 red edges. I then wrote `independent_check.py`; it imports none of the
target's code and uses different finite-search mechanisms:

1. Bit-set clique recursion finds exactly the 43 red $K_5$'s of Cyclic(43)
   and no blue $K_5$.
2. Direct enumeration of positive cyclic gap compositions of 43 into nine
   parts at most five gives 45 rooted gap words and 215 deletion sets. Their
   five dihedral orbits each have size 43 and exactly partition the census.
   The incidence count $8\cdot5<43$ separately excludes deletion sets of
   size at most eight.
3. For each representative core, direct incremental two-colour assignment
   rejects a branch only when a physical monochromatic core $K_4$ is
   completed. It uses neither CNF nor unit propagation. Its complete sorted
   star domains agree entry-for-entry with the certificate.
4. Pair colours are rebuilt from physical core triangles. An independent
   branch-and-bound search gives compatibility clique caps
   $(5,7,5,6,4)$.
5. The unique class-1 compatible seven-star cohort is
   $(0,1,3,6,9,10,12)$. Direct reconstruction of all 64 allowed mutual-edge
   assignments finds zero good graphs. This proves the class-1 improvement
   from pair cap seven to extension cap six without using the supplied
   terminal witnesses.
6. All five supplied lower witnesses are reconstructed from literal edge
   lists, checked against their core and star embeddings, and independently
   found to contain no monochromatic $K_5$.

The audit produced the following independent census. `good/cases` counts good
physical assemblies among all allowed colourings of all maximum compatibility
cliques.

| class | blue/red core $K_4$ | stars | compatible pairs | pair cap | maximum cliques | good/cases | exact order |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 409/519 | 16 | 74 | 5 | 24 | 24/49 | 39 |
| 1 | 370/575 | 13 | 62 | 7 | 1 | 0/64 | 40 |
| 2 | 356/589 | 13 | 59 | 5 | 18 | 54/232 | 39 |
| 3 | 396/547 | 17 | 97 | 6 | 5 | 16/72 | 40 |
| 4 | 435/477 | 36 | 120 | 4 | 27 | 27/27 | 38 |

Exhaustive controls compare the bit-set clique and maximum-clique routines
with literal definitions on all 1,024 labelled graphs of order five, and
compare incremental star enumeration with all 1,024 assignments on a
ten-vertex induced seed core. Normal and `-O` runs have identical output.

## Theorem-to-evidence alignment

The upper-bound reduction is complete. A one-vertex star is admissible exactly
when its red contacts contain no red core $K_4$ and its blue contacts contain
no blue core $K_4$. For two stars, an allowed mutual colour is equivalent to
the absence of the corresponding monochromatic core triangle among their
common contacts. The verified diagonal incompatibility prevents repeated star
types. Hence every extension supplies a clique in the compatibility graph;
the pair caps are valid universal upper bounds. Only class 1 needs a stronger
assembly argument, and all its 64 remaining seven-star assignments are
excluded. The verified witnesses attain every resulting bound.

The global consequence also follows with the stated quantifier. If a labelled
good graph $G$ of order 43 differed from Cyclic(43) only on edges covered by
at most nine vertices, the other at least 34 vertices would induce the same
good core in both graphs. That core would extend inside $G$ to order 43,
contradicting the independently checked maximum of at most 40. Complementing
all colours preserves this argument.

## Inherited premises and trust boundary

Imported rather than independently regenerated: the target's JSON certificate
and lower-witness edge lists at the pinned source commit. Their SHA-256 is
checked before their contents are compared with independently derived domains
and constraints. The optional CaDiCaL producer was not used. Remaining trust
is the two unformalized Python implementations, CPython integer and file
semantics, SHA-256 for artifact identity, and ordinary hardware. The audit is
algorithmically independent but not language-independent or proof-assistant
checked.

The classical Cyclic(43) seed and its 43 red defects are documented in
[Ge et al.](https://arxiv.org/abs/2212.12630) and on
[Exoo's construction page](https://cs.indstate.edu/ge/RAMSEY/). A limited
search found no prior publication of this precise minimum-puncture extension
spectrum; this is not evidence sufficient to certify novelty or priority.

## Defects, objections, and remaining gaps

No substantive defect or objection was found. The contribution appropriately
does not infer that any hypothetical $43$-vertex target contains one of these
cores, does not claim that vertex-cover distance 10 is sharp, and does not
classify extensions up to isomorphism. Those questions, historical priority,
and proof-assistant formalization remain open outside this review.

## Strengthening and improvement opportunities

A useful next strengthening would isolate the star-compatibility reduction and
the class-1 terminal obstruction as a small proof-assistant theorem. A second,
lower-priority improvement would provide a non-Python verifier, reducing the
shared language/runtime trust boundary. Neither is required for the present
verdict.

## Reproduction

```sh
git clone https://github.com/helgithorskarp/math_results.git target
git -C target checkout 55487717629070142ea39226e3d449f698bd9c1a
git clone https://github.com/njallskarp/math_source_code_open.git review
python3 -B review/ramsey_r55_cyclic_minimum_puncture_review1/independent_check.py \
  target/ramsey_r55_cyclic_minimum_puncture/certificate.json
```

Expected status:
`INDEPENDENTLY_VERIFIED_CYCLIC_MINIMUM_PUNCTURE_SPECTRUM`.

- Target certificate SHA-256:
  `a0e1a34d3b35644fba89af36ae56db2a29ead1df01298c2cb6aec731f4ba222b`
- Deterministic checker output SHA-256:
  `52100a1f30cbbad50e42bb2c7c4556c03766a159ba535389882ab663b242b1a0`
- Independent checker SHA-256:
  `1979114e0fbca6d7195fb4031b3fa54a476c47a04d06da58e75cabea40188cd8`

Python 3.11 or newer and the standard library suffice. The checker emits only
compact JSON; no generated artifact is retained or published.
