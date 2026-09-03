# Transition-closed repairs for BHR support `{1,2,11}`

> Follow-up: [`DEAD_ORTHANT_REPAIR.md`](DEAD_ORTHANT_REPAIR.md) audits all
> 1/2 cross-transitions in the source certificate and repairs all eight
> orthants whose first mixed transition loses a mode completely.  The result
> below is the `c=4` row of that stronger certificate.
>
> Further result: [`TRIMODAL_SAFE_CORES.md`](TRIMODAL_SAFE_CORES.md) derives a
> safe simultaneous `{1,2,11}` seed in every one of the 22 residue classes and
> proves a transition-closed three-dimensional core from each seed.
>
> Global certificate repair: [`CAP_ORTHANT_REPAIR.md`](CAP_ORTHANT_REPAIR.md)
> derives all 66 pairwise face seeds and partitions every one of the 22
> complete cap orthants into transition-closed caps, rays, faces, and
> tri-modal interiors.
>
> First below-cap slab: [`RESIDUAL_SLAB_2_21_1.md`](RESIDUAL_SLAB_2_21_1.md)
> gives a direct four-block formula for all admissible `c=1`, odd `b>=9`
> cases with `a+b>=20`.  Its original `(2+p,21+2q,1)` range is a commuting
> two-mode slab.
>
> New full orthant: [`TARGET_ORTHANT_4_7_23.md`](TARGET_ORTHANT_4_7_23.md)
> gives a simultaneous 1/2/11-growable seed at `(4,7,23)`.  The exact
> safe-margin equality closes every `(4+p,7+2q,23+11r)` and removes 34
> patterns from the conservative residual audit.  Published linear
> realizations already cover this existence range; the contribution is the
> explicit simultaneous-growth certificate.
>
> Boundary completion: [`EVEN_B_C1_COMPLETION.md`](EVEN_B_C1_COMPLETION.md)
> gives two parity-swapped, 2-growable four-block families for
> `(1,20+2q,1)` and `(2,18+2q,1)`.  Together with the prior odd-`b` formula
> and the published `a>=3` theorem, they prove every admissible positive
> `c=1` instance.  This removes 34 more patterns from the conservative audit.
>
> Genuine small-`a` frontier: [`SMALL_A_C3_SLAB.md`](SMALL_A_C3_SLAB.md)
> derives a simultaneous 2/11-growable seed at `(1,9,25)` from two checked
> orders of a source witness.  The safe-margin theorem then closes every
> `(1,9+2q,25+11r)`, adding a new existence slab outside the published
> `a>=3` range and removing 12 more residual patterns.
>
> Full small-`a` mantle: [`SMALL_A_MANTLE.md`](SMALL_A_MANTLE.md) repeats the
> direct two-order repair in every `c mod 11` residue class.  Eleven safe
> 2/11-growable seeds prove the corresponding eleven slabs and, uniformly,
> every `(1,b,c)` with odd `b>=15` and `c>=20`.  Eight new residue classes
> remove 60 further patterns from the conservative audit.

## Result

For every `a >= 1` and every even `b >= 16`, the multiset

\[
\{1^a,2^b,11^4\}
\]

has a Hamiltonian-path realization in the cyclically labelled complete graph
`K_(a+b+5)`.  This repairs exactly the two-coordinate orthant that the record
with counts `(1,16,4)` was intended to cover in the finite certificate at
commit `8fcd1e624b3d668794e3179787d0965137365286`.

This is a local repair, not yet a proof of the full BHR conjecture for support
`{1,2,11}`.  Other multi-coordinate records in that certificate still require
checked transition repairs.

## Context and graph neighborhood

The Buratti--Horak--Rosa (BHR) conjecture asks whether every admissible length
multiset is realized by a Hamiltonian path in the cyclically labelled complete
graph.  Chand and Ollis left `{1,2,11}` as the sole possible exception in their
three-element classification:

- <https://arxiv.org/abs/2202.07733>

The growable-realization method was introduced by Ollis, Pasotti, Pellegrini,
and Schmitt:

- <https://arxiv.org/abs/2105.00980>

The proof of their growth theorem claims that growing in one coordinate
preserves every other growth mode.  The following committed Discovery Net
nodes record the resulting theorem attempt and the explicit failure of that
cross-mode assertion:

- problem: `bafkreibnkfjkin5a2vfc2huks7hic33drqyftzpb3unlal2oy5j752ew5i`;
- attempted finite proof: `bafkreicxvyw74shmrdag6mjxb6k2qawrcscz7a53q3vtad5wte7b7jzdiy`;
- growth lemma: `bafkreigygu7ge26yjpcqjaqlse74g47j6c7w5otrwralcqdkxp7okxqn7m`;
- objection and failing path: `bafkreie7zy3t5aejqdd6avfbn5rawarep7fxlffrm5fj3mtmwxelpgtiga`.

## Definitions

For vertices `r,s` of `K_v`, put

\[
\ell_v(r,s)=\min(|r-s|,v-|r-s|).
\]

For `x <= v/2` and a cut `m`, embed `K_v` in `K_(v+x)` by fixing labels at
most `m` and adding `x` to labels above `m`.  A path is `x`-growable at `m`
when each vertex in `(m-x,m]` is incident with exactly one path edge whose
cyclic length changes under this embedding and no other path edge changes.
Splitting each changed edge at the new copy of its critical endpoint adds
exactly `x` edges of length `x`.

## The two seeds

The original boundary seed is

```text
g = (19,21,10,8,6,17,15,13,11,9,7,18,16,14,12,1,3,5,4,2,0,20).
```

It realizes `(a,b,c)=(1,16,4)`, is 1-growable at cut `0`, and is 2-growable
at cut `1`.  Growing it once in either mode destroys the other mode, exactly
as the graph objection reports.  Repeated growth in just the same mode remains
valid, however, and supplies the two boundary rays `b=16` and `a=1`.

The new interior seed is

```text
p00 = (20,18,16,5,7,9,11,13,12,10,8,22,24,1,3,14,15,17,6,4,2,0,23,21,19).
```

It realizes `(2,18,4)`, is 1-growable at cut `18`, and is 2-growable at cut
`19`.  CP-SAT found this path, but the existence claim uses only the displayed
path and the standard-library checker.

## Explicit commuting family

For integers `p,q >= 0`, concatenate the following blocks to define `P[p,q]`:

```text
(20+p+2q),
(18+p+2q, 18+p+2q-2, ..., 18+p),
(17+p, 16+p, ..., 18),
(16,5,7,9,11,13,12,10,8),
(22+p+2q,24+p+2q),
(1,3,14,15,17,6,4,2,0),
(23+p+2q,21+p+2q),
(19+p+2q,19+p+2q-2,...,19+p).
```

An indicated descending interval is empty when its first endpoint is below its
last.  In particular `P[0,0]=p00`.

Direct substitution into the cyclic metric gives all changed path edges:

| operation | parameter case | changed edges |
|---|---|---|
| 1-growth at `18` | `p=0` | `{20,18}` |
| 1-growth at `18` | `p>0` | `{19,18}` |
| 2-growth at `19+p` | `p=0` | `{20,18}`, `{21,19}` |
| 2-growth at `19+p` | `p>0` | `{20+p,18+p}`, `{21+p,19+p}` |

There are no other changed edges.  Thus the critical vertices have exactly the
required incidences, and every `P[p,q]` is both 1-growable at `18` and
2-growable at `19+p`.  Applying the explicit insertion construction and
collecting the displayed blocks gives the identities

\[
G_{1,18}(P[p,q])=P[p+1,q],\qquad
G_{2,19+p}(P[p,q])=P[p,q+1].
\]

Starting from `p00`, induction proves that `P[p,q]` is a permutation of
`0,...,24+p+2q` and realizes

\[
\{1^{2+p},2^{18+2q},11^4\}.
\]

Unlike the false general cross-preservation assertion, this closure is a
calculation for one explicit family.

For completeness, define `A[p]` by applying 1-growth at cut `0` to `g` exactly
`p` times, and define `B[q]` by applying 2-growth at cut `1` to `g` exactly
`q` times.  In `A[0]` the only changed edge for the next 1-growth is `{2,0}`;
in every `A[p]` with `p>0` it is `{1,0}`.  In every `B[q]` the only changed
edges for the next 2-growth are `{1,3}` and `{2,0}`.  Direct induction therefore
gives realizations on the boundary rays:

\[
A[p]:\{1^{1+p},2^{16},11^4\},\qquad
B[q]:\{1,2^{16+2q},11^4\}.
\]

The two rays and the `P[p,q]` interior partition the whole claimed orthant.

## Reproduction

The construction and verification require only CPython's standard library:

```bash
cd research/bhr_1_2_11_transition_repair
python3 verify.py certificate.json
python3 verify_target_orthant.py target_orthant_certificate.json --grid 3
python3 independent_target_check.py target_orthant_certificate.json
python3 verify_even_b_c1.py even_b_c1_certificate.json --grid 64
python3 independent_even_b_c1_check.py even_b_c1_certificate.json --grid 64
python3 verify_small_a_c3_slab.py small_a_c3_slab_certificate.json --grid 6
python3 independent_small_a_c3_check.py small_a_c3_slab_certificate.json --grid 6
python3 -m unittest -v test_verify.py
python3 construct.py --a 7 --b 28 --c 4
```

`verify.py` checks both displayed seeds directly from the definitions, confirms
the cross-mode regression on `g`, checks the boundary recurrences, and checks
both commuting transitions and their closed forms on a parameter grid.  The
grid is a code regression test; the proof for all parameters is the block
calculation and induction above.

To search independently for another interior seed, create an environment with
the pinned dependency and run:

```bash
python3 -m venv /tmp/bhr-repair-venv
/tmp/bhr-repair-venv/bin/pip install -r requirements.txt
/tmp/bhr-repair-venv/bin/python find_seed.py --seconds 300
```

The reference search used CPython 3.12.12, OR-Tools 9.14.6206, one worker,
random seed 1, and a 300-second limit.  It returned the displayed seed and
selected cuts `21` and `19`; the direct checker then found the additional
1-growth cut `18` used by the family.  Observed wall time on an Apple Silicon
Mac ranged from 1.4 seconds on a warm reproduction to 38 seconds on the first
run.  The model has one Boolean for each permitted directed path arc, uses a
dummy vertex to enforce one Hamiltonian path, imposes exact length counts, and
guards the definition-level growth incidences by one selected cut per mode.
CP-SAT is only a feasible-witness generator; neither optimality nor
infeasibility is claimed or trusted.

## Trust boundary and novelty scope

The mathematical claim rests on the two explicit finite seeds, direct cyclic
length and growth-incidence calculations, and ordinary induction.  The checker
uses exact Python integers and no solver, floating point, external data, or
imported certificate.  The remaining machine trust is CPython and the small
checker implementation; the written proof is independently inspectable.

Live searches of the two primary papers, arXiv, the committed graph through
height 1575, and exact parameter phrases on 2026-09-03 found no prior repair of
this orthant.  This supports only “new to the searched sources,” not a priority
claim.
