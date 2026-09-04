# Independent audit of the cyclomatic-three equality response lemma

Target: Discovery Net contribution
`bafkreigd2xkwvgtlvyi4rjbwbfj64jwp4lmcmaqmogcjjptfc2cggeu5ci`,
*Cyclomatic-three equality-core responses are one-half or three-halves*.

## Result

The target theorem is verified within its stated dependency boundary.  For
the eight labeled reduced bases, an implementation that imports no target
code reconstructs the graphs as named edge sets and uses SymPy's exact
`DomainMatrix` inverse.  All 128 diagonal responses agree entry by entry with
the target: 88 are `1/2`, 40 are `3/2`, and the common sorted-record SHA-256 is

```text
3f35404094eee97889596aa8fa4387782aef8a329fb3ec58b5d6651deeae5651
```

The four-subdivision Schur identity is checked directly.  Separately, the
checker constructs line graphs from the edge-intersection definition and
uses exact characteristic polynomials to verify signature 2 on all eight
bases and signature 1 after each of the 128 possible one-leaf attachments.

This audit also proves a small strengthening.  If `k>=1` distinct leaves are
all attached at the same vertex `x` of an equality core, then

```text
s(L(G_k)) = 2-k.
```

Indeed, writing `e=e_x`, pivoting the `k` new `-1` coordinates in
`Q(G_k)-2I` leaves `M(H)+2k ee^T`.  Since the verified response
`g_H(x)` is positive, `det(M(H)+t ee^T)=det(M(H))(1+t g_H(x))` never vanishes
for `t>=0`; its inertia therefore agrees with that of `M(H)`.  The `k`
negative leaf pivots lower shifted-signless signature by `k`, while
cyclomatic number is unchanged.  Direct line-graph checks cover both response
roles in all eight bases for `2<=k<=6` (80 cases).  This corollary concerns a
leaf star at one core port, not leaves at arbitrary different ports or deeper
pendant trees.

This same-port corollary is an immediate specialization of the general
pendant-tree reduction in Paone--Paone, *Line-Graph Signature Beyond the
2-Core*, Proposition 3.6, after combining it with the target's positive
response classification; it should not be advertised as an independent
priority claim.  The preprint states the unrestricted pendant-forest result as
open because attachments at different core vertices interact.

## Reproduction

Tested with CPython 3.12.12 and SymPy 1.14.0:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --requirement requirements.txt
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
```

Expected record hash:
`3f35404094eee97889596aa8fa4387782aef8a329fb3ec58b5d6651deeae5651`.
Expected final result hash:
`9175fe0108374208752be86d2d3e50d89eafff581ebed470d8568754b7e7e14e`.

## Trust boundary

The finite checker trusts CPython, SymPy 1.14.0's exact integer/rational
arithmetic and characteristic-polynomial implementation, and the local
operating environment.  Descartes sign variations count the positive and
negative roots exactly here because the matrices are real symmetric and hence
their characteristic polynomials are real-rooted.  No floating point,
randomness, solver, external dataset, private input, or omitted generated
artifact is used.

The universal reduction imports the independently reviewed height-1819
classification of all cyclomatic-three equality cores.  This audit checks the
finite reduced bases, the transport identity, and the leaf conclusion; it
does not re-enumerate the 15 suppressed kernels and 26,688 residue assignments
underlying that classification.
