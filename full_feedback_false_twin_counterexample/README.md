# False-twin counterexample for full-feedback localization

A connected cubic graph \(G\) of order 12 has
\(\zeta_d^*(G)=1\), but duplicating its vertex 5 as a nonadjacent
false twin gives a 13-vertex graph with parameter 2. More generally,
replacing vertex 5 by \(m\) independent twins gives parameter 2 for
every \(m\ge2\). The other quotient vertices remain singletons.

This refutes adaptive one-probe preservation under arbitrary independent
substitution. It shows that the factor-two general substitution bound
is sharp even when just one independent module has size two. It neither
settles uniform independent substitution nor produces parameter above two.

Read [THEOREM.md](THEOREM.md) for the graph, complete certificate rules,
finite tables, the replication lemma for an existing twin class of size
at least two, and the specific recontamination obstruction.

## Reproduce

Python standard library only; checked with CPython 3.12.12. From this
directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 solve.py
shasum -a 256 -c SHA256SUMS
```

The verifier's final lines must be:

```text
result_sha256=2cdd339096858154c5cd9a2c723b969857bbd71cc074acddaa53a935410f3352
VERIFIED
```

The independent regeneration's final lines must be:

```text
certificate_sha256=14116980ee0b70f06b8ea951fc73c397973511f1ca39635a8aca0e9d663f037c
REGENERATED
```

`EXPECTED_OUTPUT.txt` contains both complete outputs. `certificate.json`
is the compact finite input: explicit graph edges, an 11-state winning
strategy, an 18-state evasion family, and the resolving pair. A territory
mask is \(\sum_{v\in B}2^v\), with labels starting at zero. Its initial
one-probe winning rank is 10. All 16 unresolved strategy branches and
all 234 evasion obligations are checked directly.

`verify.py` computes distances by breadth-first search and works with
vertex sets. It rejects three corrupted certificates and audits the
replication response rule on 166 small graph instances and the stated
family through order 19. Those finite audits are not the proof for
unbounded module size.

`solve.py` computes distances by Floyd--Warshall and uses integer masks.
It runs a synchronous least fixed point over all 4,096 and 8,192 beliefs,
then compares the regenerated certificate with the supplied one. Normal
and Python optimized-mode outputs agree. The optional `--write` flag
regenerates `certificate.json`; ordinary reproduction changes no source.

Both programs finish in under one second on the campaign machine;
performance is not a mathematical claim. No packages, network requests,
external solver, graph catalogue, or large generated artifact are needed.

## Status and trust

Exact computer-assisted finite counterexample, followed by a written
universal replication argument. The compact verifier is sufficient to
check the finite theorem without trusting the discovery search or the
complete-game solver. The two programs share only the explicit input
and mathematical game definition, not distance or fixed-point code.

The remaining trust is the mathematical certificate interpretation,
the replication proof, the verifier, Python, and hardware. There is no
formal proof-assistant verification or independent peer review. Novelty
is relative to the graph and primary sources searched on 2026-09-09;
historical priority and counterexample minimality are not asserted.
