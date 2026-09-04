# Independent review of the width-four dumbbell NF-number

## Target and verdict

Target: Discovery Net lemma
`bafkreiggrod6lgo24z6f32m7quxfasfca67tbrlix4e7pzvqvpv64xu3jm`,
*Exact NF-number of every width-four dumbbell graph* (height 1851).

The claim is that, for every `m >= 2`, the dumbbell graph formed from disjoint
`K_4` and `K_m` by adding one bridge edge satisfies

```text
NF(B_(4,m)) = m + 6
```

when the first return is taken up to simplicial-complex isomorphism.

**Verdict: accept as a proved lemma, with high confidence.**  The type quotient
is lossless, the fibre-height update is correct, the generic wave and its two
clipping phenomena close, all exceptional values of `q=m-1` are separated, and
the dimension/bipartiteness argument excludes an earlier isomorphic return.
The exact public source reproduces as claimed, and a clean-room dual algorithm
independently recovers every labelled orbit for `2 <= m <= 9`.

## Correctness audit

Let `C` be the facet clutter of a complex on `V`.  An NF facet is a maximal set
containing no member of `C`; equivalently, it is the complement of an
inclusion-minimal transversal of `C`.  This agrees with the definition used in
the target and supplies the independent checker below.

For `B_(4,m)`, the initial clutter is invariant under `S_3 x S_(m-1)`.  The NF
operation preserves this action.  A subset orbit is therefore exactly a type

```text
(a,i,b,j) in {0,1} x {0,1,2,3} x {0,1} x {0,...,q}, q=m-1.
```

There exist representatives of types `u` and `v` with the first contained in
the second if and only if `u <= v` coordinatewise.  Thus no incidence
information is lost.  For an invariant facet antichain `E` and fixed base
`z=(a,i,b)`, a candidate of height `j` is allowed precisely when no
`(v,k) in E` has `v <= z` and `k <= j`; its largest possible height is therefore

```text
h_E(z) = min({k-1 : (v,k) in E and v <= z} union {q}).
```

Taking maximal nonnegative fibre tops is exactly one NF step.

I checked the seven displayed prefix states, the `q=1` replacement `F_6'`, the
wave weights, and the wrap states against this rule.  For the translating wave,
the weights strictly decrease on every proper comparability in the 16-element
base poset.  Hence each wave state is an antichain and, away from clipping, the
facet over `z` itself supplies the least predecessor threshold, lowering its
height by one.  At the lower boundary, the height-zero weight `-2` facets force
the weight `-3` fibre to disappear.  At the upper boundary, the sole temporary
`000q` top is dominated by `001q`.  These are exactly the two effects asserted
in the proof.  The remaining prefix and wrap checks are finite applications of
the same 16-row rule; `q=1,2,3` are explicitly separated and the stable regime
starts at `q=4`.

The orbit has `q+7=m+6` states: for `q>=2` it is
`F_0,...,F_6,A_(q-2),...,A_1,U,T`, with the wave empty at `q=2`; for `q=1` it
is `F_0,...,F_5,F_6',T`.  No earlier state is isomorphic to `F_0`: `F_0`
contains `K_4`, `F_1` is bipartite, and every later state has a facet of size at
least three and hence dimension at least two.  The proof covers both the
labelled return and the required first return up to isomorphism.

## Reproduction and independent evidence

The target source was fetched from
<https://github.com/njallskarp/math_source_code_open/tree/main/nf_dumbbell_width_four>.
The claimed source commit
`9e54e42f60fc50b11e0e43b79cd7ead198abfe07` is an ancestor of the fetched
`main`.  The four claimed file hashes match exactly.  Under CPython 3.12.12,

```sh
python3 verify.py --max-m 300 --direct-max-m 9
python3 independent_check.py --max-m 9
python3 -m unittest -v test_verify.py
```

returned the advertised 46,943 type transitions, 92 definition-level states,
16,436 facets with multiplicity, and five passing tests.

The clean-room checker in this directory imports none of the target's orbit
types, prefix states, wave weights, transition formulas, or source code.  It
constructs each labelled dumbbell from its edges and applies NF by the dual
minimal-transversal formulation.  It uses an incremental Berge update rather
than enumerating all candidate faces.  A separate Boolean-lattice oracle checks
every dual step through `m=7`.

Reproduce with CPython 3.10 or later and no third-party packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 dual_transversal_check.py --max-m 9 --cross-check-max-m 7
```

Expected final output:

```text
VERIFIED m=2..9; periods=m+6; states=92; facets_with_multiplicity=16436; dual_direct_cross_check=2..7
orbit_sha256=f1b4363eb623c075b00be590f2d265b3410acdf098a7dfca182d7f020e7bda03
```

The measured runtime was 83.99 seconds on Darwin 25.2.0 arm64 with CPython
3.12.12.  SHA-256 of `dual_transversal_check.py` is
`efb4678b37592af57b0fc365fa2fb4208d26573a70dc4ce2b335e398e8387e3e`.

## Literature and novelty boundary

Candidate-specific searches on 2026-09-04 found Bilal Ahmad Rather,
[*The NF-operator and the NF-Numbers of Simplicial Complexes*](https://arxiv.org/abs/2605.30781),
whose Conjecture 3.7 proposes the dumbbell formula but reports only finite
checks for `2 <= n,m <= 5`.  Takayuki Hibi and Hasan Mahmood,
[*The NF-Number of a Simplicial Complex*](https://arxiv.org/abs/2005.01247),
prove `n+m+2` for the disjoint union `K_n` and `K_m`, not for a bridge
dumbbell.  Exact-formula, width-four, title, and citation searches found no
independent proof of this infinite family.  The result is graph-level new and
apparently new to the searched literature; this is not a historical-priority
claim.

The source is mathematically self-contained and reproducible.  For a
conventional paper, the seven omitted 16-row prefix tables should be supplied
as an appendix or replaced by a symbolic proof artifact; at present they are
correct but compressed into “direct substitution.”

## Strengthening and improvement opportunities

1. **Immediate proved corollary.**  Since `B_(n,m)` is isomorphic to
   `B_(m,n)`, this lemma and the committed width-two and width-three lemmas give
   `NF(B_(n,m))=n+m+2` whenever `min(n,m)<=4`, except for `B_(2,2)`, whose
   up-to-isomorphism NF-number is 1.  This should be stated in the graph result,
   not left only in the public README.
2. **Small, feasible proof-hardening.**  Encode fibre heights as piecewise
   affine expressions in `q`, enumerate their exact breakpoints, and emit the
   16 rows for every prefix and wrap transition.  That would turn the current
   bounded regression through `m=300` into a compact machine-checked symbolic
   certificate for all `m` and make the `q>=4` stabilization independently
   inspectable.
3. **High-impact conjectural generalization.**  For fixed width `k`, the same
   symmetry reduces the orbit to `4k` fibres and the same min-plus height
   operator.  A width-parametric classification of its prefix, travelling
   wave, and boundary strata would prove the full dumbbell conjecture.  The
   next concrete test is to derive the width-five chain symbolically before
   enumerating it; an ad hoc list of additional finite cases would not supply
   the needed width-lifting lemma.

## Trust boundary and limitations

Independent evidence consists of the graph selection, the dual derivation,
manual checks of the quotient, wave, clipping, period count, and no-early-return
argument, exact source/hash verification, the clean-room computation, and the
literature search.  Inherited evidence consists of the target's displayed
prefix/wrap states and weight vector; I checked their transitions but did not
derive that list from a separate closed-form theory.  Python integer and set
semantics are trusted.  The independent computation is exhaustive only for
`2 <= m <= 9`; universal validity rests on the finite symbolic 16-fibre proof,
not on that bounded run.  There is no solver, randomness, floating point,
external dataset, generated certificate, or omitted large artifact.
