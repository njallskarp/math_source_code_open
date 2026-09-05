# An exact aggregate-edge witness survives external-root lifting at M=216

## Result

For the hard `R(5,5;43)` degree profile

```text
19^2 20^5 21^36,       M=216,
```

the aggregate exceptional-core/signature relaxation remains feasible after
adding central-cell edge counts, all hard exceptional-neighborhood edge caps,
all rooted union capacities, and the full external-root lifting inequalities
from Discovery Net height 2685.  The file
[EDGE_LIFT.json](EDGE_LIFT.json) is an exact integer pseudomodel:

- a literal seven-vertex exceptional core with mask `409383`;
- 19 positive signature cells containing the 36 degree-21 vertices;
- 184 central cell-pair red-edge counts, 138 of them nonzero;
- all 262 valid exceptional red/blue root pairs;
- 3,828 summed central-cell lifting inequalities, including 2,230 in which
  the cell lies outside the rooted set; and
- 310 corresponding fixed-exceptional-vertex inequalities.

All 42 ordered exceptional-root `(4,4)` sides have order at most 14.  Thus the
order-15/16 density intervals of height 2647 do not activate, while the
stronger external-root inequalities do activate and are satisfied.  This is a
compact exact limitation witness: these aggregate mechanisms do **not** exclude
the complete `M=216` degree profile.

The witness is not a graph.  In particular it does not assign individual
edges inside or between central cells, prove individual degree realizability,
control individual central-neighborhood triangle counts, or establish that the
profile is realizable by a Ramsey `(5,5;43)` graph.

## The relaxation checked

Let `E` be the seven exceptional vertices and `C` the 36 degree-21 vertices.
The red graph induced by `E` is `F`.  Each central vertex has a signature

```text
X = N_R(v) intersect E,
```

and `y_X` is the number of vertices with signature `X`.  The verifier checks
the exact signature capacities, margins, weighted hard-branch inequalities,
and every union capacity from height 2665.

For positive cells `X,Y`, let `z_XY` count red central edges between those
cells, counting an internal edge of `X` once.  The simple-graph boxes are

```text
0 <= z_XY <= y_X y_Y                         (X != Y),
0 <= z_XX <= binom(y_X,2).
```

The aggregate degree equation for every cell is

```text
2 z_XX + sum_(Y != X) z_XY = (21-|X|) y_X.
```

For every exceptional vertex, the checker reconstructs the red edges in its
red neighborhood and the blue edges in its blue neighborhood from literal
unordered vertex pairs.  The hard-branch caps are the inherited local Ramsey
extrema minus seven.  The seven exact `(t_R,t_B)` pairs here are

```text
(85,115), (85,115), (92,107),
(93,107), (93,107), (93,107), (92,107).
```

Their sum identities are checked directly against the global total of 447 red
edges.

## External-root lifting

Let `A` be a red clique of size `a` in `F`, let `B` be a disjoint blue clique
of size `b`, and let `S` be their common red/blue rooted set.  If `u` is red to
all of `A`, then

```text
|N_R(u) intersect S| <= U(4-a,5-b)-1.
```

Indeed, a red `(4-a)`-clique in that intersection extends `A union {u}` to a
red `K5`, and a blue `(5-b)`-clique extends `B` to a blue `K5`.  Color reversal
gives

```text
|N_B(u) intersect S| <= U(5-a,4-b)-1
```

when `u` is blue to `B`.  The proof does not require `u` to belong to `S`.
Summing these inequalities over every central signature cell gives linear
forms in the `z_XY`.  Fixed exceptional members of `S` are checked separately.
Here `U` is the elementary Ramsey recurrence with the even/even handshaking
improvement.

The standard-library verifier expands all 43 named vertices and all literal
unordered pairs.  It accepts aggregation only after verifying that every
literal pair in one cell-pair class has the same coefficient.  It therefore
does not trust the shorter model used for numerical discovery.

## Reproduction

The proof path uses CPython 3.11 or newer and only the standard library:

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify_lift.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_lift.py | cmp - EXPECTED_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

The two verification modes produce the same output, and four altered
certificates are rejected.

Optional deterministic rediscovery uses the pinned versions in
`requirements-discovery.txt`:

```bash
python3 -m venv /tmp/r55-m216-edge-lift-venv
/tmp/r55-m216-edge-lift-venv/bin/pip install -r requirements-discovery.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  /tmp/r55-m216-edge-lift-venv/bin/python search_lifted_witness.py \
  --output /tmp/EDGE_LIFT.json --core-attempts 20 --cell-attempts 20 \
  --edge-time-limit 10
cmp EDGE_LIFT.json /tmp/EDGE_LIFT.json
```

With NumPy 2.2.6 and SciPy 1.15.3, the script visits three core proposals and
finds the recorded lift at the 54th distinct signature vector.  Solver status
is discovery evidence only; the committed integers and `verify_lift.py` are
the proof object.

## Provenance, literature, and trust boundary

Discovery Net height 2665 supplied exact core/signature limitation witnesses
for all five remaining double-degree-19 profiles.  Height 2685 proved the
general external-root lifting lemma and explicitly identified testing those
witnesses as a next phase.  The fixed height-2665 `M=216` witness is excluded
by the new inequalities, but the independently found witness in this directory
survives them.  Height 2647 provides the order-15/16 density intervals; they are
vacuous here because the maximum relevant side has order 14.  Height 2685 had
not received independent mathematical review when this package was prepared.

The broader context is Angeltveit--McKay, *R(5,5) <= 46*,
<https://arxiv.org/abs/2409.15709>, whose proof combines linear programming
with gluing actual pointed neighborhood graphs.  The present aggregate witness
deliberately stops before that individual-edge layer.  McKay's primary Ramsey
data page is <https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>.

Trusted are the displayed finite relaxation, exact integers and Boolean
semantics, the literal standard-library reconstruction, SHA-256, CPython, and
ordinary hardware.  Not trusted as proof are SciPy/HiGHS status, the randomized
objectives, or the shorter discovery model.  No catalog is used.  No claim is
made about an actual 43-vertex graph, feasibility under stronger individual
edge constraints, or an improved bound on `R(5,5)`.
