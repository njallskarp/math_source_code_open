# An exact pointwise survivor of the M=216 exceptional-root relaxation

## Result

The height-2715 vertex-minimal signature-template obstruction does not close
the hard `R(5,5;43)` degree profile

```text
19^2 20^5 21^36,       M=216,
```

when combined with the campaign's aggregate and pointwise exceptional-root
constraints.  [POINTWISE_SURVIVOR.json](POINTWISE_SURVIVOR.json) gives a
complete exact witness for that relaxation:

- a seven-vertex exceptional core with mask `901619`;
- 18 positive signature cells containing 36 central vertices;
- 165 aggregate central cell-pair variables;
- an explicit simple graph of 321 red edges on the 36 named central vertices;
- exact degrees 19,19,20,20,20,20,20 on the exceptional vertices and degree
  21 on every central vertex;
- all 263 exceptional red/blue root-union capacities;
- all 7,299 pointwise central external-root inequalities, of which 4,217 are
  genuinely external to the rooted side;
- 322 fixed-exceptional-vertex root inequalities; and
- the height-2647 density interval on the single rooted side of order 15.

The core has no direct or color-reversed isomorphism to the seven-root template
at height 2715.  Thus every exceptional-core relabeling of that signature cut
is inapplicable.  The construction proves that this cut together with the
stated exceptional-root relaxation is insufficient to exclude the complete
`M=216` degree profile.

This is deliberately not called a Ramsey graph.  The explicit coloring has 32
central vertices violating the inherited hard local cap `t_R,t_B<=100`, and it
contains 317 red and 346 blue `K5`s.  Those exact failure counts identify the
next missing layer rather than hiding it.

## Exact system checked

Let `E` be the seven exceptional vertices and let each central vertex have
signature

```text
X = N_R(v) intersect E.
```

The verifier reconstructs the literal core and checks all signature weights,
Ramsey capacities, exceptional-to-central margins, union cuts, and hard local
profiles.  It then builds the full 43-vertex coloring from the recorded central
edge list.  Every aggregate count `z_XY` is recomputed from the named edges,
and all 43 degrees are checked directly.

For every disjoint red clique `A` and blue clique `B` in `E`, let `S` be the
vertices red to all of `A` and blue to all of `B`.  With

```text
p=5-|A|,       q=5-|B|,
```

the pointwise lifting inequalities are

```text
u red to A   => |N_R(u) intersect S| <= U(p-1,q)-1,
u blue to B  => |N_B(u) intersect S| <= U(p,q-1)-1.
```

They follow because the forbidden clique in either neighborhood extends a
root.  Here `U` is the elementary Ramsey recurrence with the even/even
handshaking improvement.  Unlike the height-2703 witness, the present
certificate assigns individual central edges, so the verifier checks every
one of these bounds vertex by vertex rather than only after summing a cell.

The height-2715 template test is scoped exactly: the verifier examines every
permutation of the seven exceptional roots, in both colors.  It does not claim
that the template is absent from arbitrary seven-subsets of the non-Ramsey
43-vertex coloring.

## Solver-free verification

The proof path uses CPython 3.11 or newer and only the standard library:

```bash
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 python3 verify_survivor.py | cmp - EXPECTED_OUTPUT.txt
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_survivor.py | cmp - EXPECTED_OUTPUT.txt
shasum -a 256 -c SHA256SUMS
```

The checker independently reconstructs the graph and every constraint from
the JSON.  It also counts all monochromatic five-sets, checks the explicit
central-cap failures, and rejects four altered certificates.

## Optional deterministic rediscovery

Numerical search uses NumPy 2.2.6 and SciPy 1.15.3/HiGHS only to propose exact
integer witnesses:

```bash
python3 -m venv /tmp/r55-m216-signature-cut-venv
/tmp/r55-m216-signature-cut-venv/bin/pip install -r requirements-discovery.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  /tmp/r55-m216-signature-cut-venv/bin/python search_survivor.py \
  --output /tmp/POINTWISE_SURVIVOR.json \
  --core-attempts 100 --cell-attempts 100 \
  --edge-time-limit 10 --pointwise-time-limit 10
cmp POINTWISE_SURVIVOR.json /tmp/POINTWISE_SURVIVOR.json
```

With the pinned packages, the first proposed core is `901619`; the 48th
distinct signature vector supplies the recorded pointwise lift.  The replay is
byte-for-byte deterministic.  MILP feasibility is not trusted as proof; only
the recorded edge list and solver-free verifier authorize the result.

## Provenance, literature, and trust boundary

Height 2685 introduced external-root lifting.  Height 2703 gave an exact
aggregate `M=216` witness, and height 2715 then proved that its particular
core/signature vector admits no individual-edge repair by a stronger
vertex-minimal partial-coloring template.  The present construction changes
both the core and signature vector, avoids every exceptional-core embedding of
that template, and adds an individual edge realization of all exceptional-root
bounds.  It does not contradict either predecessor.

The broader primary-source context is Angeltveit--McKay,
*R(5,5) <= 46*, <https://arxiv.org/abs/2409.15709>, whose proof combines
linear programming with computational case checking.  Earlier subgraph-count
and local-neighborhood methods appear in McKay--Radziszowski,
<https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf>.  No literature priority is
claimed for this finite limitation witness.

Trusted are the displayed relaxation, exact JSON integers, literal
standard-library reconstruction, SHA-256, CPython, and ordinary hardware.
Not trusted as proof are SciPy/HiGHS status or randomized objectives.  The
certificate does not enforce the 36 central hard local profiles or forbid all
monochromatic `K5`s; it is not a target graph, a whole-profile feasibility
proof under stronger constraints, or an improved Ramsey-number bound.
