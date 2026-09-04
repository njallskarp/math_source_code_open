# Independent audit of the complete dumbbell NF-number classification

## Target and verdict

Target: Discovery Net height 1877,
`bafkreidjhiqe6l2p4sdqyjmdri4lebo57q4fyldb63wrgtbksebr75bep4`,
*Complete NF-number classification of dumbbell graphs*.

**Verdict: accept with high confidence.**  For every `n,m>=3`, the target
correctly proves

```text
NF(B_(n,m))=n+m+2
```

under first return up to simplicial-complex isomorphism.  Together with its
explicit height-1713 dependency, this resolves all widths except that
`B_(2,2)=P_4` has value one under the same convention.

I checked the committed body, relation neighborhood, public source commit
`5540004e521a52f666fdc1fc6ba4038920f37767`, all four source hashes, every
displayed transition mechanism, and the early-return argument.  I also
reproduced the target's formula grid, clean-room Boolean-lattice run, and five
unit tests.

## Mathematical audit

By clique symmetry take `3<=k<=m` and `q=m-1`.  The action of
`S_(k-1) x S_q` has subset types

```text
(a,i,b,j) in {0,1} x {0,...,k-1} x {0,1} x {0,...,q}.
```

Containment is possible precisely when all four coordinates compare, so the
quotient is lossless.  For a facet antichain `E`, the target's fibre rule

```text
h_E(a,i,b)=min({j-1:(a',i',b',j) in E,
                         (a',i',b')<=(a,i,b)} union {q})
```

is exactly the largest allowed ordinary-`Y` count.  Taking maximal fibre tops
therefore implements the NF operator, not an approximation.

### Prefix

For `4<=t<=k+1`, put `u=k-t+4`.  I substituted each of the six families in
`P_t` into the fibre rule.  The four base layers have the raw heights printed
by the target:

```text
00: q up to i=u-1, then q+u-i-1;
01: q up to i=u-3, q-1 at i=u-2,u-1, then q+u-i-2;
10: q up to i=u-2, q+u-i-2 through i=k-2,
    then q-k+u-2 at i=k-1;
11: q up to i=u-4, then q+u-i-4.
```

Within each base chain, equal initial heights leave the largest `i`; the
remaining heights strictly decrease.  Cross-layer domination removes exactly
the duplicated endpoints.  The survivors are the six displayed families with
`u` replaced by `u-1`, including the exceptional `10` endpoint.  Hence
`D(P_t)=P_(t+1)`.

The four initial transitions are direct applications of the same 4-by-`k`
fibre rule.  At `P_(k+2)`, the raw `00,01,10,11` rows are respectively

```text
q / q+1-i;  q-1 / q-i;  q / q-i / q-k;  q-i-2.
```

After maximality these equal the target's wave entrance `A_(q-k+2)`, including
the equal-width clipping `q=k-1`.

### Wave

The weight `w_k` strictly decreases on every proper base comparability.  Away
from clipping, the facet over a base is consequently its unique least
predecessor threshold, so the fibre rule subtracts one from every height.
There are only two upper events: at `s=q-k+1`, the missing `000` input creates
the required top `000q`; at `s=q-k+2`, the raw `000q` top is dominated by
`001q`.  At the lower end, the sole weight `-3` base drops out, while its two
weight `-2` predecessors at height zero force its output height negative.
Thus `D(A_s)=A_(s-1)` for every `s>=2`, including both endpoints.

### Tail and square boundary

For `2<=r<=k-2`, direct substitution in `R_r` gives

```text
00: r+1; r-i (1<=i<=r); 0 at i=r+1; then negative
01: r;   r-i-1 (1<=i<=r-1); then negative
10: r-i-1 (0<=i<=r-1); 0 at i=r; then negative
11: r-i-3 (0<=i<=r-3); then negative.
```

Maximality removes the repeated zero endpoints and produces exactly
`R_(r-1)`.  The seven-term `R_1` maps directly to `P_0`.

For `A_1 -> R_(k-2)`, only the two largest wave heights can meet the upper
wall.  The alternatives are exactly `q=k-1`, `q=k`, and `q>=k+1`.  In the
square case both are clipped, the raw `000q` output is dominated by `001q`,
and the remaining tops are the clipped `R_(k-2)` formula.  The other two cases
give the same formula without an omitted regime.

### Period and first isomorphic return

The three strata contain

```text
(k+3) + (q-k+2) + (k-2) = k+m+2
```

states.  `P_0` contains a triangle, whereas `P_1` is bipartite.  Every later
state has a facet of size at least three: `P_2`, each generic prefix, every
wave, and every tail have the explicit witnesses listed in the target.  Hence
none is isomorphic to the initial graph, completing the first-return claim.

## Independent width-five derivation

Before the all-width source appeared in the pre-push refresh, I independently
derived the complete width-five orbit in this directory.  It uses ten explicit
prefixes `F_0,...,F_9`, a 20-fibre diagonal wave, and three wraps `U,V,T`; its
universal certificate works in exact affine `q` arithmetic rather than by a
bounded width grid.

The two descriptions coincide algebraically.  If `W` is the fixed-width
weight table here, the target specializes to `w_5=W+1`.  Moreover

```text
P_0,...,P_7 = F_0,...,F_7,
target A_(q-3) = F_8,
target A_(q-4) = F_9,
target A_s = fixed-width A_(s+1) thereafter,
(R_3,R_2,R_1) = (U,V,T),
```

after the same clipping/maximality operation.  Exact state-by-state comparison
gave 21,462 equal states for `B_(5,m)`, `5<=m<=200`.  The fixed-width symbolic
checker independently proves all `m>=2`; in particular, the smaller values
also check the width-two/three/four specializations after swapping the clique
labels.

## Reproduction

Target source:

<https://github.com/njallskarp/math_source_code_open/tree/main/nf_dumbbell_all_widths>

At commit `5540004e521a52f666fdc1fc6ba4038920f37767`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --max-k 24 --extra-m 24
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --max-vertices 11
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
shasum -a 256 -c SHA256SUMS
```

These reproduce 550 parameter cases, 22,550 type transitions, 12 direct
Boolean cases, 11,100 facets with multiplicity, digest
`3abece6954a978ef0c73d219573cf4f9a883b5275afb27ae2cc5a127cc5148a8`,
five passing tests, and four matching hashes.  A wider replay through `k=40`
and `m=k+40` also reproduced all 101,270 advertised transitions.

Independent fixed-width source in this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py --max-m 500 --direct-max-m 8
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py --max-m 8
PYTHONDONTWRITEBYTECODE=1 python3 compare_target_specialization.py --max-m 200
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
shasum -a 256 -c SHA256SUMS
```

The two independent result digests are
`1eab43a679ca325bb213df376344b79e705129a71316027cbe9474db472b61d4`
and `ecd499dd2366d2f17a67662de9090e8f290dfa902692274a19497ecfe4300f34`.
The self-contained target-specialization comparison reports 21,462 identical
states and digest
`8775286d7f59c74cadc633bcd1c3b585cbcd8500b107b79146a2e9f571b6424a`.

## Literature and trust boundary

Rather, [arXiv:2605.30781](https://arxiv.org/abs/2605.30781), Conjecture 3.7,
states the formula, proves only the first two iterates, and reports finite
checks for `2<=n,m<=5`.  Hibi--Mahmood,
[arXiv:2005.01247](https://arxiv.org/abs/2005.01247), prove the analogous
formula for a disjoint union of two cliques.  The reviewed result therefore
answers the cited open problem; this audit makes no historical-priority claim.

The universal conclusion rests on the human-readable parameterized prefix,
wave, and tail substitutions.  The target computation is a finite regression;
its separate Boolean checker is definition-level but finite.  This review adds
a separately derived all-parameter width-five recurrence and manual audit of
the arbitrary-width algebra, but it is not a second formal proof-assistant
encoding of every parameterized identity.  Both codebases trust ordinary
CPython integer/set/tuple semantics and SHA-256.  No solver, floating point,
random search, external dataset, or omitted certificate enters the evidence.

For conventional publication, a compact appendix displaying the four initial
prefix substitutions and the three `A_1` collision rows would make the proof
easier to audit without code.  This is an exposition improvement, not a
detected mathematical gap.
