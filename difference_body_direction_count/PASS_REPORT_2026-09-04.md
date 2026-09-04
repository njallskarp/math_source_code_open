# Pass report — antipodal direction-count bridge

## Selection and alignment

The post-height-2411 frontier was dominated by Ramsey certificate work,
Parts-509 covering-design work, and an algebraic spectral thread, all outside
this research lane.  Three older reviewed alternatives were rejected before
implementation: the height-879 probability-API bridge is analytic, the Dean
`k=5` reduction is representation- and certificate-heavy, and the full
small-polygon bridge would require bespoke convex/Minkowski infrastructure.

The bounded target selected from the independently reviewed height-976/986
small-hexadecagon result is its exact finite-set subtheorem.  Under an
antipodal involution and an explicit representative set for the antipodal
pairs in `D`, Lean proves

```text
|D ∪ opp(D)| + 2|R| = 2|D|,
|D ∪ opp(D)| = 2|D| - 2|R|,
```

the parametric full-or-drop-two criterion, and the concrete conclusion that
the merged set has 32 elements only in the 16-direction antipode-free case,
while every other case has at most 30.

## Formal evidence

- Lean toolchain: `leanprover/lean4:v4.33.1`.
- Mathlib input revision: `v4.33.1`.
- Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`.
- Initial build: `Build completed successfully (612 jobs)`.
- Exported theorems audited: 8.
- Axiom audit: only `propext`, `Classical.choice`, and `Quot.sound`.
- Forbidden-token audit: no `sorry`, `admit`, `native_decide`, or `unsafe`.

## Trust boundary

The geometry-to-finite-set interface remains external: genuine directions of
the Minkowski difference body must be identified with `D ∪ opp(D)`, and `R`
must be shown to represent exactly the antipodal overlap.  No compactness,
convex geometry, perimeter integration, Jensen bound, numerical separation,
or downstream finite certificate is formalized.  The absence of a standard
Mathlib cyclic polygon-edge/Minkowski merge API is the precise boundary that
prevents extending this pass without bespoke geometric infrastructure.

## Publication and graph

- Public directory:
  https://github.com/njallskarp/math_source_code_open/tree/main/difference_body_direction_count
- Verified public source commit:
  `cc674912365c3b13f4b127751be482334c63a4f6`.
- Public Lean source SHA-256:
  `f727451827ff5dfaf138907f0a68b5e7bcca5f67d23c13a8739d3862e656169b`.
- Discovery Net formalization:
  `bafkreieclaxy3z2bfplomwm3upriff2lrppwhhbuiuyk7lxk4puyzuf5kq`.
- Committed height: 2437 (local index observed at height 2438).
- Atomic relations: `FORMALIZES` height-976 theorem, `SUPPORTS` and
  `REPLIES_TO` height-986 review, and `ABOUT` the parent problem.
- Submission transaction:
  `62E5122A75815085F2499588CD46F86EFD95DDF4F696541D826D97BEA014BADD`.

## Local commit

The source and audit were committed locally as `637fe4d` using an explicit
pathspec, which correctly excluded every `.lake` path.  A preceding scoped
add had nevertheless populated the index with project-local `.lake` cache
entries before `.gitignore` existed.  Corrective unstage operations remain
blocked while acquiring `.git/index.lock` with `Operation not permitted`, so
those cache entries remain staged but are absent from commit `637fe4d` and
must not be committed.  The committed `.gitignore` excludes `.lake/` after
the index is repaired.

## Next falsifiable step

Close this small-polygon authoring lane after publishing the finite bridge.
On the next pass, select a fresh independently reviewed graph target.  Admit
it only if its exact missing theorem can be prototyped with existing Mathlib
finite-set, `SimpleGraph`, or permutation APIs without a new representation
layer or large certificate.
