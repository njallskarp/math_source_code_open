# Ramsey R(5,5): a two-anchor binary-interface witness

This package gives an exact limitation witness in the order-43, `d=22`,
deficiency-six branch.  It keeps a `22+20` anchor split, reanchors an eligible
high red partner, constrains all four monochromatic neighborhoods of the two
roots, and satisfies the tight 452-edge degree profile.  No omitted diagonal
edge is forced to both colors by one-edge `K5` defects.  Nevertheless, three
five-set inequalities on eight vertices form a width-two contradiction.

The result therefore refutes the proposed *uniformity* of the particular
one-edge mechanism used at Discovery Net height 2811.  It does not contradict
that height's exact-instance lemma, does not exclude the whole `d=22,t>=108`
family, and is not a Ramsey graph.

## Exact replay

The main checker uses only the Python standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.json -
PYTHONDONTWRITEBYTECODE=1 python3 controls.py | diff -u EXPECTED_CONTROLS.txt -
shasum -a 256 -c SHA256SUMS
```

An algorithmically independent reconstruction uses NetworkX's graph6 decoder,
graph complements and maximal-clique enumeration, and enumerates forcing
configurations edge-first:

```sh
uv run --no-project --cache-dir /tmp/r55-gap-cache \
  --with networkx==3.6.1 --python python3 independent_check.py \
  | diff -u EXPECTED_INDEPENDENT.json -
```

`PROOF.md` states the three-clause argument.  `WITNESS.json` contains the two
small catalog cores, six explicitly deleted red-core edges, the 22 by 20
incidence matrix, and the eight-vertex certificate.  No catalog or solver is
needed for verification.

## Optional discovery replay

`discover.py` is the discovery-only SAT/CEGAR search.  It starts from the exact
two-anchor, degree and edge constraints.  Each found opposite one-edge forcing
pair is converted to a conditional blocking clause; the stored witness appears
after three rounds in the reference run.

```sh
uv run --no-project --cache-dir /tmp/r55-gap-cache \
  --with python-sat==1.9.dev15 --python python3 discover.py --seconds 300
```

The solver output is not proof evidence and need not reproduce the identical
model.  Only a model independently accepted by the exact checkers is relevant.

## Expected invariants

- red edges and degree multiset: `452`, `20^8 21^26 22^9`;
- root profiles: `(22,108,6)`, `(20,100,0)`, `(21,95,12)`, `(21,101,6)`;
- two-anchor cell sizes: `10,11,10,10`; omitted diagonal edges: `210`;
- distinct width-one forces: seven blue and thirteen red, with no conflict;
- exact binary certificate: `x_4_32>=1`, `x_4_35>=1`,
  `x_4_32+x_4_35<=1`;
- red-edge SHA-256:
  `ce0d51d5a9978184161385fb5da8688d5f03e98411d0296353e83521046a9d97`;
- residual-clause SHA-256:
  `3eeda8e69185581e3b86f91041b381a2f5a78761947b74a727bde9bea7520840`.

## Trust boundary

The mathematical certificate is the three displayed inequalities, while the
standard-library verifier reconstructs and exhaustively checks their hypotheses
plus every advertised degree, neighborhood and forcing count.  The independent
checker uses a separate graph implementation and enumeration order.  Trusted
are the short source, CPython/NetworkX semantics, ordinary hardware, and SHA-256
collision resistance.  The discovery solver, its cardinality encoding, and its
SAT verdict are explicitly outside the proof boundary.  The two embedded core
records are verified directly for all properties used here; identifying the
22-vertex parent with McKay's complete catalog additionally trusts that catalog.

