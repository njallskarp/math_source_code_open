# A 7/4 lower bound for square saturation in the hypercube

Let `Q_d` be the `d`-dimensional hypercube and let
`sat(Q_d,Q_2)` denote the minimum number of edges in a square-free spanning
subgraph which becomes non-square-free whenever any omitted cube edge is
added.  The main result in this directory is

```text
sat(Q_d,Q_2) >= 7 d 2^(d-1) / (2d+5),     d >= 3.
```

Consequently

```text
liminf_{d -> infinity} sat(Q_d,Q_2) / 2^d >= 7/4.
```

The proof is in [PROOF.md](PROOF.md).  Its new ingredient is a local slack
inequality on the six square faces of a 3-cube.  The face-adjacency graph is
`K_{2,2,2}`; a boundary count in this graph turns either an inactive incidence
or a repeated witness into enough slack to strengthen the standard
three-edge-face count.

## Reproduction

Requires Python 3.11 or later and only the standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_local_slack.py
diff -u EXPECTED_OUTPUT.txt <(PYTHONDONTWRITEBYTECODE=1 python3 verify_local_slack.py)
shasum -a 256 EXPECTED_OUTPUT.txt
```

The expected-output SHA-256 is
`5f59ff07706ae03570bc36897b6b8e375c4cc74507b940f338e643fb2add79b7`
and is recorded in `SHA256SUMS`.  The checker:

- reconstructs the 12 edges and six faces of `Q_3` from definitions;
- exhausts all `2^12` edge patterns and checks the local slack inequality for
  every square-free pattern;
- independently enumerates all square-saturated patterns in `Q_2` and `Q_3`;
- evaluates the exact integer lower bound for dimensions 3 through 10.

The exhaustive check is corroboration, not the proof of the general theorem.
The universal argument is the face-boundary proof in `PROOF.md`.

## Literature and scope

Johnson and Pinto proved the semisaturation lower bound
`(3/2-o(1)) 2^d` and explicitly noted that obtaining a stronger lower bound
for square-free saturated graphs seemed difficult:

- J. R. Johnson and T. Pinto, *Saturated Subgraphs of the Hypercube*,
  [arXiv:1406.1766](https://arxiv.org/abs/1406.1766).

Morrison, Noel, and Scott proved `sat(Q_d,Q_m)=Theta(2^d)` for every fixed
`m` and determined the weak-saturation number:

- N. Morrison, J. A. Noel, and A. Scott, *Saturation in the Hypercube and
  Bootstrap Percolation*,
  [arXiv:1408.5488](https://arxiv.org/abs/1408.5488).

A focused primary-source and exact-formula search on 2026-09-04 found no
published `7/4` lower bound or the local 3-cube slack inequality.  This is a
search-relative novelty statement, not a priority claim.

## Trust boundary

The mathematical claim rests on the displayed combinatorial proof, elementary
double counting, and integer arithmetic.  The checker uses CPython and an
exhaustive `4096`-pattern loop only to audit the local lemma and small cases.
There is no floating point, randomness, solver, external data, generated
certificate, or private state.
