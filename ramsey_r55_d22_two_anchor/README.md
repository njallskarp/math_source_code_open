# A two-anchor incidence witness and an eight-vertex diagonal obstruction

This package resolves the bounded reanchoring test after Discovery Net height
2789. It constructs a coloring of `K_43` with a deficiency-six red neighborhood
of order 22 and an eligible adjacent partner whose **full** red and blue
neighborhoods are also valid `(4,5)` graphs. A short certificate then excludes
every completion that preserves these four labeled neighborhoods. This identifies
the missing interface as consistency of the two diagonal cell pairs.

The result does not exclude every `(4,5;22)` core with at least 108 edges.
The witness is feasible for the stated two-anchor incidence constraints, but
it has monochromatic five-cliques and is not an `R(5,5;43)` graph. No further
anchor, aggregate pseudomodel extension, or larger census is used.

## Exact witness

Label vertices `u=0`, `A={1,...,22}`, `B={23,...,42}`. Color `uA` red and
`uB` blue. The red graph `H` on `A` is the graph6 record in `WITNESS.json`
after the six listed edge deletions; the blue graph `J` on `B` is the second
record. Row `i` of `cross_rows`, with zero-based row and column indices,
colors `(i+1,j+23)` red exactly when its `j`th character is `1`.

The selected partner is `v=3`. The following facts are directly checked:

| Root | Color | Neighborhood order | Same-color edges | Deficiency |
| --- | --- | ---: | ---: | ---: |
| 0 | red | 22 | 108 | 6 |
| 0 | blue | 20 | 100 | 0 |
| 3 | red | 21 | 99 | 8 |
| 3 | blue | 21 | 97 | 10 |

Each of the four indicated graphs has clique number three and independence
number four. Thus this checks the full outside neighborhood of `v`, not only
the portion inside `A`. The root edge `uv` is red and has ten common red
neighbors, so `v` is an eligible high partner. The complete coloring has 452
red edges and red degree profile `20^8,21^26,22^9`; all color degrees are in
`20..22`, and `sum_x (d_R(x)-21)^2=17`.

The exact edge list, sorted by its two zero-based endpoints and serialized as
`a b\n`, has SHA-256

```text
af4d730dd4efe5813c1c009cc9095b8119869ec9e952a3cfba618e712da02ebc
```

## The diagonal interface lemma

For two fixed distinct roots, partition the other vertices into cells
`C_ij`, where `i,j` record red adjacency to `u,v`. Fix the root incidences,
the edge `uv`, and all four induced color neighborhoods.

**Lemma.** The only edges not fixed by these data lie between `C_11,C_00`
or between `C_10,C_01`. Every assignment of these edges preserves the four
neighborhoods. Any monochromatic `K_5` in such an assignment must avoid both
roots and use at least one edge in those two interfaces.

**Proof.** Two nonroot vertices lie in a common color neighborhood of a
root precisely when the corresponding bits agree. Neither root sees them in
one color exactly when both bits differ. This gives the two diagonal pairs.
A five-clique through a root would give a forbidden four-clique in its
same-color neighborhood. A monochromatic five-clique wholly inside any of
the four neighborhoods is also forbidden by the `(4,5)` properties (a
same-color five-clique contains a four-clique). Finally, any set of binary
signatures varying in both coordinates contains an antipodal pair: if it
has only two types they must be antipodal, and any three of the four types
contain one. Hence a remaining five-clique uses a diagonal edge. QED.

Here the cell sizes, in order `11,10,01,00`, are `10,11,10,10`. Thus exactly
`10*10+11*10=210` pair colors are omitted by the four neighborhoods.

## An exact obstruction to all diagonal completions

The only omitted edge within each of the following sets is `e={5,25}`:

```text
R = {5,25,28,34,41}: the other nine edges are fixed red;
B = {5,8,9,10,25}:   the other nine edges are fixed blue.
```

Vertices `5,25` lie in `C_10,C_01`, respectively. The red triple
`{28,34,41}` lies in `C_00`; the blue triple `{8,9,10}` lies in `C_11`.
All 18 displayed colored edges belong to the fixed neighborhoods.
If `e` is red, `R` is a red `K_5`; if `e` is blue, `B` is a blue `K_5`.
Therefore **all `2^210` labeled diagonal completions are excluded**, even
without imposing any global degree constraints on those completions.

This gives an exact transferable incidence inequality. Let `x_f=1` for a red
edge, and let `E_R,E_B` be the nine nonhole edges in the red and blue sets.
The usual two five-clique inequalities are

```text
x_e + sum_{f in E_R} x_f <= 9,
-x_e - sum_{f in E_B} x_f <= -1.
```

Add them with exact nonnegative multipliers `1,1`, eliminating the unassigned
edge. The resulting guarded cut is

```text
sum_{f in E_R} x_f - sum_{f in E_B} x_f <= 8.
```

The fixed incidence witness makes the left side `9`, so it violates the cut
by exactly one, independently of every diagonal color. Equivalently, the 18
colored literals cannot all hold. This is a small Farkas-style certificate
for the fixed-neighborhood family, using two ordinary Ramsey constraints.
The familiar implication carries no novelty claim; the substantive certificate
is its realization by four valid full neighborhoods in the assigned
deficiency-six branch. The checker verifies the exact coefficient cancellation.

The exhibited full coloring has 273 red and 280 blue five-cliques. All avoid
the two roots and cross a diagonal. Their full lists, rather than only their
counts, are compared between exhaustive five-subset enumeration and
NetworkX maximal-clique enumeration. The common list digest is

```text
18a90df71ad0cd96b91199551e2c5dd111dde24efe75acf9fcb058651225997f
```

The table of four valid neighborhoods is an exact incidence witness for the
specified relaxation. The diagonal contradiction supplies the precise next
omitted global condition; it also rules out repairing this instance by
recoloring only edges absent from all four neighborhoods. The question whether
every `d=22,t>=108` instance has an analogous obstruction remains open.

## Reproduction

Tested with CPython 3.12.12. The main check uses only the standard library.
The second checker uses NetworkX 3.6 and imports no source from the first.

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - EXPECTED_OUTPUT.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py | cmp - EXPECTED_OUTPUT.json
python3 -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py | cmp - EXPECTED_INDEPENDENT.txt
PYTHONDONTWRITEBYTECODE=1 python3 controls.py | cmp - EXPECTED_CONTROLS.txt
shasum -a 256 -c SHA256SUMS
```

The primary checker checks the graph definitions, all four forbidden-subset
conditions, the 210-edge interface entry by entry, and the fixed colors of the
18 edges in the two forcing sets. The second checker uses a separate graph6
decoder and maximal-clique algorithm and checks the forcing certificate from
the graph object. Matching five-clique digests are entry-level agreement, not
just aggregate agreement. These are different internal checks, not external
peer review. The ordinary Python/runtime, NetworkX, hardware and SHA-256
remain trusted.

## Provenance, literature, and scope

The two graph6 records are the first records of McKay's `r4522.114.g6` and
`r4520.100.g6`, also used at height 2789. All properties of the specific
records are checked here; no catalog completeness is needed for their
validity. The deficiency labels use the external extrema
`U(20)=100, U(21)=107, U(22)=114`.

The cross matrix was discovered using python-sat 1.9.dev15 with its Glucose42 backend
in a 440-variable cross-edge model. The model imposed both `(4,5)` conditions
in all four neighborhoods, red degrees `21..22` on `A`, `20..21` on `B`,
and 232 red cross edges. Search stopped at the first model (about two seconds
including generation). Solver output, auxiliary cardinality encodings, and
search completeness are outside the proof path; only the explicit matrix is
accepted after direct verification. Compact optional rediscovery source is
provided in `discover.py`; its output is advisory and must be audited:

```bash
python3 -m pip install -r requirements-discovery.txt
PYTHONDONTWRITEBYTECODE=1 python3 discover.py --seconds 60
```

On the tested version this ends with `MATCHES_CERTIFICATE True`. A solver
timeout is reported as `SOLVE None`; it is not an infeasibility certificate.

Primary context, checked live on 2026-09-05:

- Angeltveit and McKay, [*R(5,5) <= 46*, arXiv:2409.15709v2](https://arxiv.org/html/2409.15709v2),
  Sections 2 and 5, describe pointed-neighborhood gluing and the need to fill
  interfaces beyond the chosen neighborhoods. No novelty is claimed for the
  general gluing viewpoint.
- [McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
  supplies the extremal `(4,5)` records. They are attributed to Brendan McKay
  under the [data collection's CC BY 4.0 terms](https://users.cecs.anu.edu.au/~bdm/data/).

This package concerns `d=22,t>=108`, not the distinct M=214 codegree-13 lane.
It adds no Ramsey bound, no classification of all such cores, and no claim
that the remaining global constraints are feasible. Its durable outcome is
one fully checked two-anchor incidence witness, a complete exclusion of its
fixed-neighborhood completion family, and the exact missing edge interface.
