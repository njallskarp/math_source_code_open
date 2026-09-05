# Independent review of the common-root squeeze at height 2589

## Verdict

Accepted at the new-lemma and application level, conditional on the imported
height-2509/2557 hard-branch data.  The common-root capacity is valid, the
strengthened paired inequality has the claimed constants, exactly one of the
seven normalized patterns survives, and equality forces both rooted
15-vertex sides to be eight-regular `(4,4)` graphs.

This is not a construction or exclusion of an `R(5,5;43)` graph, a whole
degree profile, or either remaining `k=e_R(W)` case.

Reviewed contribution:

- Discovery Net height 2589,
  `bafkreiagv4mryvhvcznaxmqni7yyipvzitm33vd5e4o44iug4qmxogwvhq`;
- source commit `614510d0273e408293a246b1d70e0696f31501b8`;
- source directory
  `https://github.com/helgithorskarp/math_results/tree/main/ramsey_r55_common_neighbor_squeeze`.

## Independent proof audit

For `u in U`, every vertex of `N_R(u) intersect P` is red to the two red
roots `z,u` and blue to `w`.  A red triangle in that set extends with `z,u`
to a red `K5`; a blue `K4` extends with `w` to a blue `K5`.  Hence the set has
at most eight vertices by `R(3,4)<=9`.  Swapping `z,w` gives the same cap for
`Q`.

The bound `R(3,4)<=9` used here has the elementary parity proof.  In a
nine-vertex red-triangle-free graph with no blue `K4`, every red degree is at
most three.  A blue neighborhood has neither a red nor a blue triangle, so
`R(3,3)<=6` makes its size at most five.  Thus every red degree is at least
three and therefore exactly three, contradicting the odd degree sum 27.

Let

```text
sigma_P = 8|P|-2e(P)-e(P,F_z),
sigma_Q = 8|Q|-2e(Q)-e(Q,F_w),
alpha   = 8c-e(U,P),
beta    = 8c-e(U,Q),
gamma2  = c(c-1)-2e(U).
```

Every quantity is a nonnegative integer.  Direct expansion gives the exact
gap identity

```text
RHS(3)-LHS(3) = sigma_P+sigma_Q+2alpha+2beta+2gamma2.
```

This checks both the constants in the displayed inequality and the equality
case.  In the application, substituting `|P|=|Q|=14`, `c=2`,
`e(J)+e(K)=154-D` gives `D>=16`.  Direct enumeration of the seven inherited
integer patterns leaves only

```text
A=(4,2,8), B=(4,8,2), D=16.
```

The gap is then zero, so every slack above vanishes.  Consequently `U` is a
red edge, `e(U,P)=e(U,Q)=16`, and both U vertices have P/Q/W degrees `8/8/2`.
The fourteen P-vertex degrees in `P union {4}` are each at most eight and sum
to 112, while root 4 has degree eight; hence the 15-vertex graph is
eight-regular with 60 edges.  The Q side is identical.  Uniform joins to the
two exceptional roots prove the `(4,4)` property.

The final aggregate identities were also recomputed.  For `k=11,12`,

```text
e(P,W)=e(Q,W)=70-k,  e(P,Q)=76+k,
```

and all four cell degree sums give exactly `e(C)=357`.

## Reproduction

With CPython 3.11 or newer and no dependencies:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_review.py
cmp EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_review.py)
sha256sum -c SHA256SUMS
```

The verifier is independent of the reviewed implementation and contains no
solver call or imported target code.  It checks the degree/parity endgame, a
literal sharp cap-eight fixture, the exact gap decomposition, all seven
patterns, the equality consequences, and both remaining central aggregate
identities.

Separately, in a fresh sparse clone of the reviewed repository pinned at the
source commit, both normal and `python3 -O` executions of the target verifier
reproduced `report.json` and `EXPECTED_OUTPUT.txt` byte for byte.  That target
replay included the complete paired-neighborhood and ten-edge parent replay,
163,520 small graph/root/set cases, 5,814 large-fixture partitions, both exact
aggregate witnesses, and four negative controls.

## Literature and trust boundary

The classical small Ramsey bounds are consistent with Greenwood and Gleason,
*Combinatorial Relations and Chromatic Graphs*, Canadian Journal of
Mathematics 7 (1955), 1--7, DOI `10.4153/CJM-1955-001-4`.  The current global
context is Angeltveit and McKay, *R(5,5) <= 46*, arXiv:2409.15709 and Journal
of Graph Theory (2026), DOI `10.1002/jgt.70029`.

Trusted here are the displayed finite argument, exact CPython integer
arithmetic, the pinned public source provenance, and ordinary hardware.  The
review does not independently reconstruct the older height-2509/2557
exceptional-core/profile chain or prove that either exact aggregate witness
lifts to individual graph edges.  Those are explicit imported boundaries.
