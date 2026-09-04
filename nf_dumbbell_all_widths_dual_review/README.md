# Independent review of the all-width dumbbell NF-number theorem

## Target and outcome

Target: Discovery Net contribution
`bafkreidjhiqe6l2p4sdqyjmdri4lebo57q4fyldb63wrgtbksebr75bep4`,
**Complete NF-number classification of dumbbell graphs**.

Verdict: **accept as a proved theorem, with high confidence**, for the stated
range `n,m >= 3`.  The lossless orbit quotient, fibre update, parameterized
prefix, clipping rules, diagonal wave, tail, period count, and exclusion of an
earlier isomorphic return all check.  Together with the earlier width-two
result, the theorem gives `NF(B_(n,m))=n+m+2` for all `n,m>=2` except
`B_(2,2)=P_4`, whose first return up to isomorphism is one.

The audit also proves a small structural strengthening: after clipping the
out-of-box type `(0,2,0,0)`, the same prefix--wave construction specializes to
`k=2, m>=3`.  Thus one parameterized construction can cover every nonexceptional
dumbbell; a separate width-two orbit is not mathematically necessary.

A pre-push fetch exposed concurrent commit
`e993774cbcc589068cbd3458863602b70fc54657`, which already supplies a manual
audit and an independently derived symbolic width-five recurrence.  The
present package is intentionally separate: its added evidence is the
all-width incremental-minimal-transversal replay and the proved `k=2`
specialization.  It does not present the overlapping acceptance conclusion as
new evidence.

## Correctness and exact scope

Write `k=min(n,m)`, `q=max(n,m)-1`, and distinguish the two bridge endpoints.
Under `S_(k-1) x S_q`, a subset orbit is uniquely represented by

```text
(a,i,b,j) in {0,1} x {0,...,k-1} x {0,1} x {0,...,q}.
```

One representative of type `e` can be contained in one of type `z` exactly
when `e<=z` coordinatewise.  Since the NF operator commutes with the group
action, this makes the quotient lossless at every iterate.  For a facet-type
antichain `E`, a type `(z,j)` is allowed precisely when there is no `(v,l)` in
`E` with `v<=z` and `l<=j`; hence its largest allowed height is exactly

```text
h_E(z) = min({l-1 : (v,l) in E and v<=z} union {q}).
```

Discarding negative heights and retaining coordinatewise maximal tops is
therefore the defining NF operation, not a heuristic compression.

I recomputed the four initial prefix transitions, the four piecewise-affine
rows for `P_t -> P_(t+1)`, and the prefix exit.  Their breakpoints and endpoint
values match the target.  The wave weights strictly decrease on each proper
base comparability: increasing `i` lowers the weight, changing `a` or `b` from
zero to one lowers it, and the two exceptional end weights introduce only an
additional downward jump.  This proves the interior translation.  The only
upper clips are the `000` and `001` fibres; the temporary `000` top is dominated
by `001`.  The only lower clips have weights `-2` and `-3`; a surviving
height-zero weight-`-2` facet makes the weight-`-3` fibre unavailable.  Thus
`D(A_s)=A_(s-1)` for the advertised range.

Direct substitution in the tail formula gives `A_1 -> R_(k-2)`,
`R_r -> R_(r-1)`, and `R_1 -> P_0`.  I checked separately the collision regimes
`q=k-1`, `q=k`, and `q>=k+1`; clipping the nominal `(0,k,0,0)` endpoint in the
square case gives the same maximal tail.  No fourth regime is possible because
`q>=k-1`.

The labelled orbit has

```text
(k+3) + (q-k+2) + (k-2) = k+m+2
```

states before returning.  The initial graph contains a triangle, its first
iterate is bipartite, and every later displayed state contains a facet of size
at least three.  Bipartiteness and dimension therefore exclude every earlier
return up to simplicial-complex isomorphism.

## Proved boundary specialization at k=2

Let `k=2` and `q=m-1>=2`.  Interpret `P_0` through the target's clipping
operator.  This removes only the impossible ordinary-`x` pair type
`(0,2,0,0)`.  The displayed prefix remains `P_0,...,P_4`, and direct use of the
fibre formula gives `P_4 -> A_q`.

In base order `000,001,010,011,100,101,110,111`, the specialized wave weights
are

```text
2, 1, 0, -1, 0, -2, -2, -3.
```

The target's order-reversing-weight argument therefore gives
`A_s -> A_(s-1)` for `2<=s<=q`.  At `s=1`, the eight raw next heights are

```text
2, 1, 0, -1, 0, 0, 0, -1.
```

After maximalization, the `010` and `100` zero-tops are dominated and the
survivors are

```text
(0,0,0,2), (0,0,1,1), (1,0,1,0), (1,1,0,0),
```

which are exactly the clipped `P_0`.  Hence

```text
P_0,...,P_4,A_q,...,A_1,P_0
```

has `5+q=m+4=n+m+2` states.  The same triangle/bipartite/dimension invariants
exclude earlier isomorphic return.  This argument covers `B_(2,m)` for every
`m>=3`; it deliberately excludes `B_(2,2)=P_4`.

## Independent computation and reproduction

The target source was replayed from a fresh clone at commit
`5540004e521a52f666fdc1fc6ba4038920f37767`.  Its four advertised SHA-256
values matched.  Under CPython 3.12.12, the advertised command checked 22,550
type transitions, the wider audit through `k=40` checked 101,270 transitions,
the no-import Boolean-lattice checker reproduced 12 complete orbits with the
advertised hash, and all five tests passed.

This directory supplies a different checker.  It constructs the labelled
dumbbell, computes all minimal transversals by incremental Berge updates,
checks each generated transversal for coverage and inclusion-minimality,
complements them to obtain the next NF facets, and compares every expanded
facet entry-for-entry with an independently encoded literal expansion of the
claimed templates.  It neither imports the target nor scans the full Boolean
lattice.  The tests compare the transversal generator with brute force on 180
fixed-seed small hypergraphs.

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 dual_transversal_check.py --max-vertices 12
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_dual_transversal_check.py
```

Expected summary:

```text
DUAL VERIFIED dumbbell templates and k=2 specialization; 2<=k<=m; m>=3; k+m<=12; cases=24; k2_cases=8; states=274; facets_seen_with_multiplicity=35786; orbit_sha256=8a1b3bb3e7cb3d5359a4586cbf6ddd6135430bb308fb523ea9250611f903dc71
```

The three tests pass.

## Literature status and publication readiness

Bilal Ahmad Rather's arXiv v1, [The NF-operator and the NF-Numbers of
Simplicial Complexes](https://arxiv.org/abs/2605.30781), was submitted on
2026-05-29 and is marked "Algebra Colloquium (to appear)."  Despite the
abstract's broad wording, Conjecture 3.7 in the paper states the dumbbell
formula, derives only the first two iterates, and reports finite checks for
`2<=n,m<=5`.  Hibi--Mahmood's [The NF-Number of a Simplicial
Complex](https://arxiv.org/abs/2005.01247) proves `n+m+2` for the disjoint union
of two cliques and its complete-bipartite NF image, not for a bridge dumbbell.
Exact-title, exact-formula, notation, and citation searches found no other
proof.  The result is therefore graph-level new and apparently new to the
searched literature, not a historical-priority claim.

The theorem is publication-ready as a self-contained combinatorial proof.
For a conventional paper, the most useful proof-hardening would be to print
the finite initial and `A_1` fibre tables rather than leave them as direct
substitutions.

## Strengthening and improvement opportunities

1. **Proved, immediate:** include `k=2` in the single parameterized theorem as
   shown above.  This removes the width-two dependency from the construction;
   only the exceptional `P_4` is separate.
2. **High-feasibility proof hardening:** formalize the coordinatewise fibre
   lemma and the affine prefix/wave/tail transitions in Lean, or emit a compact
   symbolic breakpoint certificate.  This would replace the remaining manual
   algebra boundary; extending the bounded regression alone would not.
3. **Higher-impact conjectural direction:** for a tree of clique blocks joined
   by distinguished bridges, the same symmetry gives a product of Boolean
   endpoint coordinates and clique-count chains.  A meaningful extension
   needs an order-reversing weight family and boundary-tail classification for
   that larger base poset; the dumbbell formula alone does not supply them.

## Trust boundary

The universal result rests on the displayed parametric fibre calculations and
the combinatorial proof above, not on bounded computation.  The independent
dual checker is exhaustive only for `k+m<=12`; it trusts CPython 3.12.12 integer
and set semantics and its literal transcription of the target templates.  Its
transversal algorithm has a different state representation and update rule
from both target checkers, and the tests cross-check it against brute force.
The `k=2` extension is deductive; its bounded dual replay is corroboration.

No solver, floating point, external dataset, generated input, omitted
certificate, or large artifact is used.  Literature novelty is search-relative.
Public source availability and computational agreement do not by themselves
prove the theorem.
