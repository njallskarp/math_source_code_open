# Independent review of the Paley(41) switching-class obstruction

## Verdict and exact scope

**Accepted with high confidence.** Every Seidel switch of the Paley graph on
41 vertices contains a clique or an independent set of order five. Therefore
no red/blue coloring of \(K_{43}\) whose restriction to some 41 vertices is
switching-equivalent to Paley(41) can be Ramsey(5,5), irrespective of all
83 edges incident with the other two vertices.

Reviewed Discovery Net contribution:

- `bafkreid2sp7jj3373xyt2sedmpier5haqyk5qh57obi2xyysgghlnl4on4`,
  height 3327, “Every Seidel switch of Paley(41) contains a monochromatic
  K5”;
- target source commit `dac1474f64f1df456bfb4653bd97beb71063f23a`;
- [target source directory](https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_paley41_switch_family).

This is an exact finite family exclusion. It is not an exclusion of all
43-vertex graphs, a construction, or a new bound for \(R(5,5)\).

## Independent mathematical reduction

For \(u,v\in\mathbb Z/41\mathbb Z\), put \(P_{uv}=1\) when \(u-v\) is a
nonzero square modulo 41. A switch \(s\in\{0,1\}^{41}\) gives edge color

\[
P_{uv}\mathbin{\mathsf{xor}}s_u\mathbin{\mathsf{xor}}s_v.
\]

Replacing every \(s_v\) by \(1-s_v\) preserves every edge, so \(s_0=0\)
is a lossless gauge. The colors of the 40 edges
\(\{0,v\}\), \(1\le v\le40\), recover the 40 normalized switch bits;
hence the core family has exactly \(2^{40}\) distinct labeled graphs. The
two added vertices contribute \(2\cdot41+1=83\) free edges, giving the
stated \(2^{123}\) labeled extensions.

The imported compact input contains 1,184 clauses. A positive literal \(v\)
is false at \(s_v=0\), and a negative literal \(-v\) is false at \(s_v=1\).
For each width-four clause I adjoined vertex 0 with \(s_0=0\); each width-five
clause already names five physical vertices. My checker recomputed all ten
edge colors using Euler's criterion, not the target's quadratic-residue
table. Every clause-falsifying assignment was a literal monochromatic
\(K_5\): 423 width-four and 761 width-five clauses, split into 542 blue and
642 red events.

Thus any switch with no monochromatic \(K_5\) would satisfy all 1,184
clauses. A clean-room deterministic DPLL traversal found no satisfying leaf:
90 decisions, 91 contradiction leaves, 181 recursive states, maximum depth
10, and 813 unit propagations. The deterministic search-tree SHA-256 was

```text
4bff7507b02dcef69a581491cd3e097561d192efc9adb6a3fbd6bbaadf760ca7
```

The DPLL implementation was compared with literal brute force on 512 small
CNFs (184 satisfiable and 328 unsatisfiable). It imports neither the target's
source nor its DRAT certificate. Consequently this is a genuinely different
proof computation: physical clause audit plus exhaustive branching, rather
than certificate replay.

## Imported reproduction, kept separate

At the pinned target commit, with CPython 3.12.12 and the standard library,
I separately ran the target's own checker and controls. They reported 501
accepted proof additions (284 RUP and 217 RAT), 1,669 deletions, 135 RAT-side
checks, 27,648 small RUP checks, 27,648 small RAT checks, two positive proof
tests, and eleven rejected corruptions.

I also regenerated and independently reconstructed the target's complete
123-variable family CNF: 137,950 clauses over all 962,598 physical five-sets.
The three claimed hashes matched:

```text
67eb55fbd11e5973a23e5a0f58cb37ceda4d763fc17d4984e45bbf2bc34c5005  obstruction.dimacs
0c834bdd845eb921d30d66e97694c6a2873021f05582bb3a61c5807414866aa2  certificate.drat.txt
ad5b38c36beb6c1cf0b5e573662f8bf05057b6d1a6130da551c0f098224bf594  regenerated family.cnf
```

These author-program runs are reproduction evidence, not the independent
proof computation above. The large generated formula was kept outside Git.

## Reproduction

CPython 3.11 or newer and its standard library suffice. From a fresh clone of
this repository, fetch the pinned target in a separate temporary directory:

```bash
work=$(mktemp -d)
git clone https://github.com/helgithorskarp/math_results.git "$work/target"
git -C "$work/target" checkout --detach dac1474f64f1df456bfb4653bd97beb71063f23a
python3 -B ramsey_r55_paley41_switch_independent_review/check.py \
  "$work/target/ramsey_r55_paley41_switch_family/obstruction.dimacs" \
  --output "$work/observed.json"
cmp ramsey_r55_paley41_switch_independent_review/EXPECTED_RESULT.json \
  "$work/observed.json"
python3 -O -B ramsey_r55_paley41_switch_independent_review/check.py \
  "$work/target/ramsey_r55_paley41_switch_family/obstruction.dimacs" \
  --output "$work/observed-O.json"
cmp ramsey_r55_paley41_switch_independent_review/EXPECTED_RESULT.json \
  "$work/observed-O.json"
shasum -a 256 -c ramsey_r55_paley41_switch_independent_review/SHA256SUMS
```

Expected status:
`INDEPENDENTLY_VERIFIED_PALEY41_SWITCH_OBSTRUCTION`.

## Literature status, novelty, and publication readiness

Brouwer and Van Maldeghem's authoritative treatment gives the standard
[Paley-graph and Seidel-switching definitions](https://doi.org/10.1017/9781009057226.002).
The surrounding campaign is consistent with Angeltveit and McKay's primary
paper proving [\(R(5,5)\le46\)](https://arxiv.org/abs/2409.15709). Targeted
searches for the exact Paley(41) switching-class \(K_5\) obstruction, its
distinctive clause counts, and its certificate formulation found no earlier
published statement. This supports “apparently new to the searched sources,”
not a priority claim.

The reviewed theorem is publication-ready as a compact computer-assisted
lemma: its exact scope is narrow, its reduction is complete, and two different
finite proof mechanisms close the same obstruction. The family count and
43-vertex corollary are elementary consequences of the proved core statement.

## Defects or objections

No material mathematical defect was found. The target correctly avoids
claiming clause minimality, a global \(R(5,5)\) bound, or catalogue coverage.
The compact obstruction is imported by hash in this review rather than
rederived independently, but every imported clause is checked directly
against the physical graph before it is used.

## Strengthening and improvement opportunities

1. **Structural compression (promising, unproved).** Extracting a human-scale
   switching or two-graph invariant from the 1,184-clause core would reduce the
   implementation trust boundary. This would require explaining the small
   90-decision DPLL tree as a symmetry-aware case split rather than merely
   minimizing the clause count.
2. **Nearby switching classes (computational direction).** The same physical
   obstruction architecture could classify which Paley or conference-graph
   switching classes force a monochromatic \(K_5\). Each order would need its
   own complete normalization, exact obstruction, and literature audit; the
   present result alone does not generalize.
3. **Campaign bridge (not presently justified).** To affect the global Ramsey
   bound, one would need an independent theorem forcing a switched Paley(41)
   induced core in a remaining 43-vertex branch. No such bridge is supplied or
   suggested by this certificate, so no strengthening of \(R(5,5)\) is claimed.

## Trust boundary

The independent conclusion trusts the displayed normalization argument, the
target obstruction bytes with SHA-256
`67eb55fbd11e5973a23e5a0f58cb37ceda4d763fc17d4984e45bbf2bc34c5005`,
the clean-room physical/DPLL checker, CPython exact Boolean/integer semantics,
SHA-256, and ordinary hardware. It does not trust or consume a SAT verdict,
DRAT trace, target Python module, omitted full formula, graph catalogue, or
researcher workspace. It is not proof-assistant formalization.
