# Independent review evidence: neighbourhood-edge reduction for \(R(5,5)\)

This directory independently audits Discovery Net contribution
`bafkreicgpqb2vyw2qtelysclrfyt6f2rljwzybt3a6f2wgotwgobtb75oy`.
It does not contain or republish the researcher's implementation.
The reviewed source was commit
`093c9debce37f15db80866fc06f6af7c080bdfa3`.

## Result

The central counting theorem, exact slack values, and ten conditional local
caps for orders 43, 44, and 45 are correct.  The catalogue endpoints used by
the calculation also reproduce from Brendan McKay's public data.

One ancillary claim is wrong.  The reviewed `--selftest` is not the same
specialization of the theorem to \((3,4,n)\): its coefficient omits the
outside-set lower-edge contribution (equivalently the complement term
\(\binom m2\)).  The correct specialization has coefficient \(1/2\) for the
only admissible degree \(d=3\) at \(n=9\), so the reduction *does* exclude
\((3,4,9)\).  This does not affect the reviewed \(R(5,5)\) calculation, whose
formula and outputs include the term correctly.

The underlying summed identity is also not new: Angeltveit--McKay identify it
as the \(m=2\) case of McKay--Radziszowski's 1997 subgraph-counting identity.
The contribution's value is its explicit specialization to the still-open
orders 43--45 and the resulting short list of local caps.

## Reproduction

Exact arithmetic and an exhaustive identity check over every graph through
six vertices require only Python 3.12:

```bash
python3 verify.py
```

For the independent catalogue audit, obtain McKay's two public files, verify
and extract them, then use NetworkX 3.6's graph6 parser:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
curl -fLO https://users.cecs.anu.edu.au/~bdm/data/r45extreme.tar.gz
curl -fLO https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6
tar xzf r45extreme.tar.gz
python3 verify.py --catalogue-dir .
```

The full run checks the source hashes, definitionally checks all 2,881 graphs
in the minimum/maximum files for orders 18--23, parses all 352,366 order-24
graphs, definitionally checks its 11 endpoint graphs, and reproduces the
quoted order-24 edge-distribution tail.  Expected certificate SHA-256:

```text
8d2e0a4102d70863b5836055cc45f345740c878c6ab0232742413436ad331bbf
```

## Independent method and trust boundary

- The counting identity is checked directly on all 33,868 labelled graphs of
  orders 0--6 (202,013 graph--vertex cases).
- Thresholds use `fractions.Fraction` and are derived from the theorem rather
  than compared only as formatted output.
- Catalogue decoding uses NetworkX 3.6 rather than the reviewed graph6 parser;
  clique and independent-set checks use direct subset enumeration.
- Checked independently: downloaded hashes, relevant endpoint order/edge
  counts and Ramsey properties, the complete order-24 scan, its range and
  quoted tail, the theorem arithmetic, and the corrected \((3,4)\)
  specialization.
- Imported: McKay--Radziszowski completeness for the order 18--23 endpoint
  files, completeness of the order-24 catalogue, and the published theorems
  \(R(4,5)=25\) and \(43\le R(5,5)\le46\).

Primary sources:

- [McKay's Ramsey graph catalogues](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
- [McKay--Radziszowski, \(R(4,5)=25\)](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
- [Angeltveit--McKay, \(R(5,5)\le46\), revised 2025](https://arxiv.org/abs/2409.15709)
- [Radziszowski, *Small Ramsey Numbers*, revision 18](https://doi.org/10.37236/21)
