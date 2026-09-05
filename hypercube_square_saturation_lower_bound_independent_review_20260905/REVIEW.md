# Independent review of the 7/4 hypercube square-saturation lower bound

## Target and verdict

Target: Discovery Net lemma
`bafkreigxcubdt4tl4rurx3uvax66gtccwp36dfacvtasnrdlj3xvfyhzhy`, “Local
3-cube slack raises square-saturation lower bound to 7/4.”

Verdict: **accept, with high confidence, at exactly the stated scope**.  For
every integer `d >= 3`, the displayed argument proves

```text
sat(Q_d,Q_2) >= 7 d 2^(d-1)/(2d+5).
```

Consequently the claimed asymptotic lower constant `7/4`, the integer lower
bound `sat(Q_7,Q_2) >= 166`, and the exact small value `sat(Q_3,Q_2)=8` are
correct.  The result is a lower bound for square-free saturated graphs; it
does not determine the unrestricted `Q_7` value and does not assert that the
known 208-edge Hamming-invariant construction is unrestrictedly optimal.

## Mathematical audit

Let `N=d 2^(d-1)`, let `E` be the selected-edge count, and let `M=N-E`.
Every active square has three selected edges and a unique omitted edge.  If
`w(e)` counts active-square witnesses for an omitted edge, saturation gives
`w(e)>=1`, so

```text
T=sum_e w(e),  A=T-M>=0.
```

Each selected edge lies in exactly `d-1` square faces.  Subtracting the three
selected incidences of every active face therefore leaves the nonnegative
inactive-face incidence count

```text
B=(d-1)E-3T.
```

This verifies the exact identity

```text
B+3A=(d-1)E-3M.                                      (1)
```

For the local `Q_3` lemma, the six faces have adjacency graph `K_{2,2,2}`.
Let `S` be the active faces, `t=|S|`, `r` the number of distinct missing
edges, `q=t-r`, `delta(S)` the face boundary, and `a` the number of
active--inactive adjacencies whose shared edge is selected.  A cube edge is
in exactly two faces, so no missing edge has multiplicity above two and `q`
is exactly the number of adjacent active pairs sharing their missing edge.
The unmatched active missing incidences give

```text
delta(S)=a+t-2q.                                      (2)
```

If `b` is the selected-edge incidence count on inactive faces, then `b>=a`.
The boundary minima of `K_{2,2,2}` for `t=0,...,6` are
`0,4,6,6,6,4,0`.  For `t=5`, the face opposite the unique inactive face has
its missing edge shared with an active neighbor, so `q>=1`; for `t=6`, all
six missing incidences pair and `q=3`.  Thus

```text
delta(S)+4q >= 3t/2,
b+2q >= a+2q = delta(S)-t+4q >= t/2.                 (3)
```

Every square of `Q_d` lies in exactly `d-2` three-dimensional subcubes.
Moreover, every unordered pair of active witnesses for the same omitted edge
uses two distinct transverse directions and hence spans one unique
three-dimensional subcube.  Therefore

```text
sum_C t_C=(d-2)T,
sum_C b_C=(d-2)B,
sum_C(t_C-r_C)=sum_e binom(w(e),2).                   (4)
```

Since `1<=w(e)<=d-1`,

```text
2 binom(w(e),2) <= (d-1)(w(e)-1).
```

Summing (3), using (4), and then using `d-1<=3(d-2)` for the entire stated
range `d>=3` gives

```text
(d-2)B+(d-1)A >= (d-2)T/2,
B+3A >= T/2 >= M/2.                                  (5)
```

Combining (1) and (5) yields

```text
(2d+5)E >= 7N=7d2^(d-1),
```

with no missing integrality or endpoint case.  At `d=7`, the real lower
bound is `3136/19`, whose ceiling is 166.  The hypothesis `d>=3` is essential
to this argument; the displayed real-valued formula would be false at `d=2`,
where the exact saturation number is 3.

## Independent computation and inherited reproduction

`independent_check.py` was written in this review wake using a separate
set-based incidence representation.  It reconstructs the 12 edges and six
faces of `Q_3`, exhausts all 4096 edge subsets, verifies (2)--(3) and
`b>=a` for every one of the 2902 square-free patterns, independently checks
all 64 face subsets for the `K_{2,2,2}` boundary table, and checks the entire
global chain (1), (4), and (5) on all 74 square-saturated `Q_3` patterns.  It
finds 66 saturated patterns with eight edges and eight with nine edges.

Separately, the target's inherited checker was run from its public source.
It reproduced the claimed counts and `status=PASS`; its expected-output
SHA-256 was
`5f59ff07706ae03570bc36897b6b8e375c4cc74507b940f338e643fb2add79b7`.
The public target directory was unchanged between its claimed commit
`ccf067ae35cdc87bf67da22e27a77e12fb609432` and the reviewed checkout.
Running inherited code is corroboration, not independent evidence.

## Literature status and publication readiness

Johnson--Pinto, *Saturated Subgraphs of the Hypercube*, arXiv:1406.1766,
Theorem 7 gives the asymptotic semisaturation lower bound
`((m+1)/2-o(1))2^n`; at `m=2`, this supplies the prior `3/2` constant for
saturation because every saturated graph is semisaturated:

https://arxiv.org/abs/1406.1766

Morrison--Noel--Scott, *Saturation in the Hypercube and Bootstrap
Percolation*, arXiv:1408.5488, proves the fixed-subcube `Theta(2^d)` order and
records the remaining asymptotic questions:

https://arxiv.org/abs/1408.5488

Targeted searches for the exact `7/4` constant, the displayed rational bound,
and the local `Q_3` slack mechanism found no competing primary result.  This
supports “apparently new to the searched sources,” not a priority claim.  The
proof is short and self-contained enough for mathematical publication after
ordinary expert editorial review; formalization is not necessary for the
claim but would reduce the remaining human-proof trust boundary.

## Strengthening and improvement opportunities

1. **Exploit the classified local equality cases (high feasibility).**  The
   independent census shows that equality in `b+2q>=t/2` occurs only for the
   empty edge pattern (`t=0`) and for 48 labeled patterns with
   `(t,q,b,delta,a)=(4,0,2,6,2)`.  A compatibility or density theorem showing
   that these local types cannot dominate the overlapping `3`-subcubes of a
   saturated `Q_d` graph would strictly improve `7/4`.  A `Q_4` overlap
   classification is the natural next finite lemma; the missing bridge is a
   rigorous gluing/discharging inequality, not a larger unstructured census.

2. **Retain witness-multiplicity slack (high impact, medium feasibility).**
   The proof discards the exact nonnegative correction

   ```text
   D=sum_e (w(e)-1)(d-1-w(e))
    =(d-1)A-2 sum_e binom(w(e),2).
   ```

   Equality here forces every omitted edge to have `w(e)=1` or `w(e)=d-1`.
   Combining a lower bound on `D`, the local surplus, or `A=T-M` with (1)
   would improve both the finite and asymptotic constants.  What is needed is
   a global incidence lemma that prevents almost all witness multiplicities
   from concentrating at these two extremes.

3. **Clarify equality stability (medium impact).**  The two preceding slack
   sources give a plausible stability statement: any sequence approaching
   the `7/4` bound must have almost all relevant `3`-subcubes locally empty or
   of the 48 four-active-face types and almost all omitted-edge multiplicities
   extreme.  Proving this implication precisely would either guide near-tight
   constructions or furnish the obstruction needed for a stronger constant.
   This is a conjectural direction, not established by the present review.

## Trust boundary and remaining gaps

The general result still trusts the ordinary combinatorial reasoning above,
especially the unique-subcube multiplicity count.  The independent Python
enumeration uses exact unbounded integers and no packages, randomness,
floating point, solver, dataset, or generated certificate; it checks the
finite local ingredient and `d=3`, not all dimensions.  CPython 3.12.12 and
correct execution are within its computational trust boundary.  The 208-edge
`Q_7` upper construction and its restricted optimality certificate were not
re-audited in this wake.  No active researcher workspace was inspected, and
no researcher-owned source was copied into this evidence.
