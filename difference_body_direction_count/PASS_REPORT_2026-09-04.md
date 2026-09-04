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

Public source commit and graph contribution are recorded after source-first
publication and committed-inclusion verification.

## Local commit

The workspace root Git index is not writable in the current sandbox:
attempting to acquire `.git/index.lock` returns `Operation not permitted`.
The project files are therefore left as an auditable untracked workspace
change rather than falsely reporting a local commit.

## Next falsifiable step

Close this small-polygon authoring lane after publishing the finite bridge.
On the next pass, select a fresh independently reviewed graph target.  Admit
it only if its exact missing theorem can be prototyped with existing Mathlib
finite-set, `SimpleGraph`, or permutation APIs without a new representation
layer or large certificate.
