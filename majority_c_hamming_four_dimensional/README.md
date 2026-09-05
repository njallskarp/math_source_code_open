# Near-triangle bounds for majority C-colourings of Hamming graphs

This directory gives a structural upper bound for four-dimensional imbalanced
Hamming graphs and exact formulas in an infinite divisibility regime.

For

```text
G = K_n1 square K_n2 square K_n3 square K_n4,
n1 >= n2 >= n3 >= n4 >= 2,
N_i = n_i - 1,
h = ceil((N_1+N_2+N_3+N_4)/2),
```

assume `h >= N_1` and put `s=h-N_1+1`.  Then

```text
chi_bar_>=(G) <= floor(n2*n3*n4/s).
```

If `s` divides at least one of `n2,n3,n4`, equality holds.  The proof extends
to every dimension satisfying `N_1 <= h <= N_1+N_2`: every colour class has
at least `n1*s` vertices, and the same quotient upper bound follows.

A mixed-radix line partition substantially enlarges the exact regime.  If

```text
(n2 mod s) * (n3 mod s) * (n4 mod s) < s,
```

then the quotient upper bound is attained, even when `s` divides none of the
three minor orders.  See
[MIXED_RADIX_EXTENSION.md](MIXED_RADIX_EXTENSION.md) for the dimension-free
partition lemma and proof.  The first concrete new case is
`K_5 square K_3 square K_3 square K_3`, whose exact value is `13`.

The complementary one-box construction applies when, for
`r_j = n_j mod s`,

```text
s <= r2*r3*r4 < 2*s
r2+r3+r4 >= s+2.
```

After stripping exact line blocks, the remaining residue box itself has
minimum degree at least `s-1`.  This proves, for every `s >= 3`,

```text
chi_bar_>=(K_(2s+2) square K_(2s-1) square K_(s+2) square K_(s+1))
  = 2*s^2+5*s.
```

See [RESIDUE_BOX_EXTENSION.md](RESIDUE_BOX_EXTENSION.md).

The natural attempt to keep partitioning the final residue box has a sharp
barrier.  If every residue is smaller than `s`, any induced subgraph of
minimum degree at least `s-1` has at least `2*s-2` vertices.  Consequently a
three-coordinate residue box with `floor(r2*r3*r4/s) >= 2` cannot supply all
of those quotient parts for any `s >= 4`.  The unique multi-box exception is

```text
s = 3, (r2,r3,r4) = (2,2,2),
```

where the residual cube splits into two square faces.  It gives a further
exact infinite family.  See
[MULTIBOX_OBSTRUCTION.md](MULTIBOX_OBSTRUCTION.md) for the theorem, the exact
family, and the scope of the obstruction.

A cyclic row--column exchange now crosses that barrier.  Every Hamming
rectangle with both orders at least `s` partitions into exactly
`floor(m*n/s)` coordinate-line sets of size at least `s`.  Consequently, if
two minor coordinates `nj,nk` are at least `s`, and

```text
nl * ((nj*nk) mod s) < s,
```

then the four-dimensional quotient upper bound is exact.  In particular,
pairwise divisibility `s | nj*nk` suffices even when neither factor is
individually divisible by `s`.  The family

```text
K_(k^2+2k+3) square K_(k^2+k) square K_(k^2+k) square K_(k^2+2), k>=2,
```

has residue product exactly `2*s`, cannot use a pure residual completion, and
has exact value `(k+1)^2*(k^2+2)`.  See
[CROSS_BOUNDARY_EXCHANGE.md](CROSS_BOUNDARY_EXCHANGE.md).

A third-coordinate slab composition strengthens that condition. For two
minor orders `m,n >= s`, put `tau=(m*n) mod s`; for the remaining order `p`,
put `c=p mod s`. If

```text
c*tau < s,
```

then the minor box has an optimal line partition. Complete `s`-slabs in the
third coordinate are removed first, so only `c`, rather than the full order
`p`, multiplies the pair remainder. This gives the genuinely new family

```text
K_(3k+6) square K_(3k+2) square K_(2k+3) square K_(2k+3), k>=2,
```

with exact value `6*k^2+19*k+16`; its first member is
`K_12 square K_8 square K_7 square K_7` with value `78`. See
[THREE_COORDINATE_SLABS.md](THREE_COORDINATE_SLABS.md).

The rectangle theorem admits a balanced strengthening: its
`floor(m*n/s)` line parts can always be chosen with sizes only `s` and
`s+1`, with exactly `(m*n) mod s` of the latter size. This is an explicit
two-consecutive-size star decomposition of `K_(m,n)`. It also makes the
slab condition sharp when the third side `p` is smaller than `s`:

```text
maximum number of line parts in [m] x [n] x [p]
  = p*floor(m*n/s),  1 <= p < s.
```

The exact deficit from the volume quotient is
`floor(p*((m*n) mod s)/s)`. Therefore a carry cannot be repaired without a
part crossing the complete-slab/residual-layer boundary. The family

```text
K_(s+2) square K_(s+2) square K_(s+1) square K_(s-1), s>=3,
```

has exact majority C-chromatic number `s^2+2*s-2` by the nonlinear one-box
construction, but every coordinate-line lift has at most one fewer colour.
See [BALANCED_STARS_THIN_OBSTRUCTION.md](BALANCED_STARS_THIN_OBSTRUCTION.md).

Intersecting that sharp thin bound with the one-box theorem gives an exact
first-carry phase classification.  If `m,n>=s`, `2<=p<s`, the positive
residues are `r=m mod s`, `u=n mod s`, and `r*u*p<2*s`, then the sequential
line stripping plus whole residue tail attains the quotient exactly when

```text
s <= r*u*p < 2*s  and  r+u+p >= s+2.
```

Throughout this region every coordinate-line partition is exactly one part
short.  Every admissible residue pattern also embeds in infinitely many
ordered near-triangle Hamming graphs, with an explicit exact formula for the
majority C-chromatic number.  See
[FIRST_CARRY_SEPARATION.md](FIRST_CARRY_SEPARATION.md).

The whole-tail degree condition is not necessary for arbitrary partitions.
At `s=5`, the residual pattern `(2,2,2)` has tail degree only three, but a
cross-boundary `K_4 square K_2` repairs the carry.  An explicit 19-part
partition of `[7] square [7] square [2]` extends by exact 5-stripping to every

```text
[5a+2] square [5b+2] square [2],  a,b>=1.
```

This yields the exact infinite Hamming family

```text
chi_bar_>=(K_(5(a+b)-4) square K_(5a+2) square K_(5b+2) square K_2)
  = 10ab+4a+4b+1,  a>=b>=2,
```

while every line lift has one fewer colour.  See
[CROSS_BOUNDARY_222.md](CROSS_BOUNDARY_222.md).

There is also a global rigidity principle behind this gadget.  In an
arbitrary Hamming graph, every induced subgraph of minimum degree at least
`s-1` that is not contained in a coordinate line has at least `2s-2`
vertices.  Equality forces `K_(s-1) square K_2`, with no restriction on the
ambient factor orders.  Therefore a first-carry remainder below `2s-2`
cannot be repaired by any boundary-mixing partition; at equality, an optimal
partition has exactly one nonlinear part of that forced type and all other
parts are line `K_s`s.  See
[GLOBAL_NONLINEAR_CLASS_BOUND.md](GLOBAL_NONLINEAR_CLASS_BOUND.md).

At the equality boundary `r*u*p=2*s-2`, layer divisibility completely
classifies when that forced prism can repair the carry.  A quotient-optimal
partition exists exactly in the two cases

```text
p=2 and r*u=s-1,  or  p=s-1 and r*u=2.
```

Both cases have uniform constructions for all `m,n>=s` with the prescribed
positive residues.  Every other equality-boundary pattern is impossible:
each orientation of the unique `K_(s-1) square K_2` leaves some thin layer
with a nonzero remainder modulo `s`.  See
[FIRST_CARRY_EQUALITY_CLASSIFICATION.md](FIRST_CARRY_EQUALITY_CLASSIFICATION.md).

A transversal alignment of the larger rectangle stars now eliminates every
modular carry as soon as all three minor sides are at least `s`. Precisely,
every box

```text
[m] x [n] x [p],  m,n,p >= s,
```

partitions optimally into `floor(m*n*p/s)` coordinate-line parts, all of
size `s` or `s+1`. Larger residual stars donate aligned cells to vertical
slab parts; displaced cells form one new horizontal line for each carry.
Consequently the four-dimensional majority C-chromatic quotient is exact
whenever `n4>=s`. The first-carry family

```text
K_(k^2+2k) square K_(k^2) square K_(k^2) square K_(k^2), k>=3,
```

has exact value `k^4+k^3+k^2+k+1` and lies outside every earlier residue
criterion in this suite. See [ALL_LARGE_THREE_BOX.md](ALL_LARGE_THREE_BOX.md).

A specialist literature audit gives two exact reductions. The anchored
rectangle is a direct specialization of Cameron--Horsley Theorem 2: every cut
condition reduces to a two-case nonnegative integer expression, and the
uncentred rows force the common transversal. The full three-box problem is a
fixed-centre, fixed-size hyperstar decomposition in Lonc's 1987 Hall framework;
the new content is the universal all-large capacity choice and explicit carry
exchange, not the general feasibility criterion. See
[SPECIALIST_PRIOR_ART_REDUCTION.md](SPECIALIST_PRIOR_ART_REDUCTION.md).

The complete proof and exact parameter map are in
[NEAR_TRIANGLE_FOUR_DIMENSIONAL.md](NEAR_TRIANGLE_FOUR_DIMENSIONAL.md).

## Reproduction

CPython 3.12 or later; standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_near_triangle.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_mixed_radix.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_residue_box.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_multibox_obstruction.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_cross_boundary.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_three_coordinate_slabs.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_balanced_stars_thin.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_first_carry_separation.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_cross_boundary_222.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_cross_boundary_222.py
ruby verify_cross_boundary_222_independent.rb
PYTHONDONTWRITEBYTECODE=1 python3 verify_global_nonlinear_class_bound.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_global_nonlinear_class_bound.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_first_carry_equality_classification.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_first_carry_equality_classification.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_all_large_three_box.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_specialist_star_reduction.py
```

Expected output:

```text
greedy parameter quadruples checked: 57870
greedy total-shell sizes checked: 2159646
full-profile parameter quadruples checked: 316
full shell profiles checked: 176336
divisible constructions checked: 10166
K3xK2xK2xK2 candidate subsets checked: 187726
K3xK2xK2xK2 feasible size-6 subsets: 12
all exact checks passed
```

The residue-box checker reports:

```text
generic residue-box partitions checked: 1158
generic partition parts checked: 97035
generic exact line classes checked: 95877
four-dimensional near-triangle parameters checked: 479445
previous mixed-radix parameters detected: 141493
new complementary parameters detected: 5648
lifted Hamming constructions checked: 79
lifted majority-C colour classes checked: 4484
explicit infinite-family indices checked: 9998
all exact checks passed
```

The mixed-radix checker separately reports:

```text
mixed-radix identities checked: 93412
qualifying identities checked: 66550
four-dimensional near-triangle parameters checked: 479445
residue-product families detected: 141493
genuinely nondivisible families detected: 21615
generic cell-level partitions checked: 4025
generic line classes checked: 212261
lifted Hamming partitions checked: 647
lifted Hamming colour classes checked: 30251
all exact checks passed
```

The multi-box checker reports:

```text
capped shell profiles checked: 133518
small residue boxes checked exhaustively: 23
small residue subsets checked exhaustively: 14539
multi-box volume contradictions checked: 24360931
exceptional residue partitions reconstructed: 64
exceptional partition parts checked: 5816
explicit Hamming-family parameters checked: 353500
all exact checks passed
```

The cross-boundary checker reports:

```text
rectangle partitions reconstructed: 9129
rectangle line parts checked: 498902
rectangle cells checked: 7393776
cyclic corner switches checked: 7140
four-dimensional near-triangle parameters checked: 479445
pair-remainder parameters detected: 157292
genuinely new pair-exchange parameters detected: 44467
lifted Hamming partitions reconstructed: 1582
lifted Hamming line parts checked: 118501
lifted Hamming minor cells checked: 771730
explicit infinite-family indices checked: 9999
explicit family partitions reconstructed: 4
explicit family line parts checked: 1652
all exact checks passed
```

The three-coordinate slab checker reports the compact expected output in
`expected_three_coordinate_slabs_stdout.txt`.

The balanced-star/thin-coordinate checker reports the compact expected
output in `expected_balanced_stars_thin_stdout.txt`.

The first-carry classification checker reports the compact expected output in
`expected_first_carry_separation_stdout.txt`.

The `(2,2,2)` cross-boundary checker reports the compact expected output in
`expected_cross_boundary_222_stdout.txt`; its five unit tests are in
`test_cross_boundary_222.py`.  The separate Ruby owner-map audit reports the
four lines in `expected_cross_boundary_222_independent_ruby_stdout.txt`.  It
checks the base certificate and 250,000 count identities, not the universal
stripping or Hamming upper-bound arguments.

The global nonlinear-class checker reports the compact expected output in
`expected_global_nonlinear_class_bound_stdout.txt`; its seven unit tests are
in `test_global_nonlinear_class_bound.py`.

The all-large three-box checker reports the compact expected output in
`expected_all_large_three_box_stdout.txt`.

The specialist star-reduction checker reports the compact expected output in
`expected_specialist_star_reduction_stdout.txt`.

## Evidence and trust boundary

The theorem is a human proof from an exact first/second-shell incidence bound,
capped majorization, and concavity.  The verifier uses arbitrary-precision
integers to audit the greedy reduction, every bounded shell profile in a
documented range, the divisibility constructions, and every potentially
too-small induced class in `K_3 square K_2 square K_2 square K_2`.

The computation corroborates conventions and boundary algebra; it does not
prove the universal claim.  There is no floating point, randomness, solver,
network input, or external data.

## Literature boundary

Bujtas, Dettlaff, Furmanczyk, and Laskowska explicitly ask for the imbalanced
three- and four-dimensional cases in Open Problem 2 of *Majority C-coloring in
Cartesian products* (2026):

<https://arxiv.org/abs/2608.27669>

Their Proposition 15 supplies coordinate-fibre lower bounds, and their
balanced even-dimensional theorem is recovered here when all four orders are
equal.  The source does not state the class-size bound or the imbalanced
divisibility formulas above.  Targeted searches on 2026-09-04 found no matching
result.  Novelty is search-relative, not a historical-priority claim.

Under the identification of a rectangle with the edge set of a complete
bipartite graph, its coordinate-line parts are stars. The divisible
all-size-`s` rectangle case is therefore classical; see Yamamoto et al.,
*On claw-decomposition of complete graphs and complete bigraphs* (1975),
<https://doi.org/10.32917/hmj/1206136782>, and the modern discussion by
Cameron--Horsley, <https://arxiv.org/abs/1807.10738>. The claimed new scope
is restricted to the closed-form cyclic construction and its Hamming/slab
consequences; existence of the balanced and anchored rectangle is a direct
corollary of Cameron--Horsley Theorem 2. Coordinate-line decompositions of a
three-box are fixed-centre hyperstar decompositions covered abstractly by
Lonc's Hall criterion, <https://doi.org/10.1016/0012-365X(87)90128-2>. The
all-large theorem contributes an explicit universal capacity choice and carry
exchange within that framework.
