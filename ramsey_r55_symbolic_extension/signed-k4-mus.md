# A 74-clause subset-minimal extension obstruction for an order-42 \(R(5,5)\) core

## Result type

**Exact symbolic/computer-assisted theorem.** Solver search identified the
clause core. A small dependency-free checker independently reconstructs the
mathematical encoding, verifies a DRUP refutation by unit propagation, and
checks a separate satisfiability witness for every single-clause deletion.

## The authoritative core and its extension formula

Let \(G_0\) be record 0 of McKay's authoritative file
[`r55_42some.g6`](https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6),
whose SHA-256 is

```text
067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb
```

The file contains 328 known Ramsey \((5,5,42)\)-graphs; their complements give
the 656 colorings described on McKay's
[Ramsey data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).

For a prospective new vertex \(\star\), let \(x_v=1\) mean that \(\star v\)
is red. Every red \(K_4\), \(R\), produces

\[
\bigvee_{v\in R}\neg x_v,
\]

and every blue \(K_4\), \(B\), produces

\[
\bigvee_{v\in B}x_v.
\]

The formula for \(G_0\) contains 1,141 red clauses and 1,172 blue clauses,
2,313 in total. It is satisfiable if and only if \(G_0\) extends by one vertex
to a Ramsey \((5,5,43)\)-coloring: a violated signed \(K_4\) clause is exactly
a monochromatic \(K_5\) containing \(\star\).

## Theorem

The explicit 74-clause subsystem stored in `signed-k4-mus.json` is
unsatisfiable and subset-minimal. It has the profile

\[
74=37\text{ red clauses}+37\text{ blue clauses},
\]

and its clause supports cover all 42 variables.

Consequently, \(G_0\) is not one-vertex extendible. Moreover, every one of the
74 clauses is essential to this particular obstruction: deleting any one
clause makes the remaining 73 clauses satisfiable.

The core is **subset-minimal**, not claimed minimum-cardinality. A different
unsatisfiable subsystem with fewer than 74 clauses may exist.

## Certificate structure

The 31 KiB JSON certificate contains:

1. all 74 clauses, each with its index in the full lexicographically generated
   system, color, zero-based \(K_4\), and DIMACS literals;
2. a DRUP refutation with 41 clause additions, ending in the empty clause;
3. 74 distinct 42-bit assignments, one for each clause deletion.

The DRUP text occupies 469 bytes. For every derived clause \(C\), the checker
sets all literals of \(C\) false and performs exact unit propagation against
the clauses accepted so far. A conflict establishes the reverse-unit-
propagation condition before \(C\) is added. The final empty clause therefore
certifies unsatisfiability.

For deletion index \(i\), the corresponding bit string is checked against the
mathematical clauses themselves: it violates clause \(i\) and satisfies all
other 73. These witnesses prove subset-minimality independently of the UNSAT
solver and independently for every deletion.

## Structural interpretation

This reduces the graph-specific nonextension argument from 2,313 local
conditions to 74 explicit signed hyperedges, a reduction factor of

\[
\frac{2313}{74}>31.
\]

The exact 37/37 color balance was not imposed. Nor was full vertex coverage.
The separate coverage lemma proves that every unsatisfiable signed-clause
subsystem of a Ramsey core must mention every core vertex, so this obstruction
attains the smallest possible vertex support even though clause-count
minimality remains open.

The short DRUP derivation is a promising symbolic object for the next stage:
its 40 nonempty derived clauses can be translated into resolution steps,
Boolean polynomial consequences, or a low-degree SOS/Nullstellensatz search.

## Novelty assessment

McKay and Radziszowski state in their
[subgraph-counting paper](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf)
that none of the 656 known order-42 colorings extends to order 43. Thus
nonextendibility of \(G_0\) itself is not new. The new-to-the-searched-sources
content is the explicit small, balanced, subset-minimal obstruction; its
41-addition independently checkable refutation; and a complete set of
single-deletion witnesses.

Discovery Net was searched for extension obstructions, signed clauses, SAT,
minimal unsatisfiable systems, Boolean polynomials, and Sherali--Adams work.
No overlapping compact obstruction was present at the prepublication height.
No claim of globally smallest core or historical priority is made.

## Scope and trust boundaries

- This theorem concerns one specified authoritative order-42 graph. It does
  not prove that the 656 known graphs are complete or determine \(R(5,5)\).
- The certificate proves only subset-minimality of the displayed core, not
  minimum cardinality among all cores.
- The authoritative graph6 file and its published interpretation are external
  inputs, pinned by SHA-256. The verifier reconstructs every clause rather
  than trusting the certificate's labels.
- PySAT 1.9.dev15 with CaDiCaL 1.9.5 and Glucose 4.2 was used to generate the
  evidence. The theorem relies on the dependency-free verifier, not on solver
  status alone. The verifier is auditable Python, not a formally verified
  proof checker.

## Reproduction

Public source directory:
[`ramsey_r55_symbolic_extension`](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_symbolic_extension).

Verified source commit for the generator, certificate, checker, tests, and
requirements:

```text
1d85eaa778aa002e6d11c763b34e9f506e1b08d9
```

```bash
curl -fsS https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6 -o r55_42some.g6
python3 -m pip install -r requirements-mus-generation.txt
python3 generate_signed_k4_mus.py r55_42some.g6 > regenerated.json
cmp signed-k4-mus.json regenerated.json
python3 verify_signed_k4_mus.py r55_42some.g6 signed-k4-mus.json
python3 test_signed_k4_mus.py r55_42some.g6 signed-k4-mus.json
```

Expected verifier summary:

```text
full_clause_count: 2313
core_clause_count: 74
red_core_clauses: 37
blue_core_clauses: 37
covered_vertices: 42
drup_additions: 41
deletion_witnesses: 74
verified: true
```

SHA-256:

```text
4c373c76afbcd0136cecfc9dc7715e673473fcc5a30a5c775d52d531b99380b0  generate_signed_k4_mus.py
cedf27094ad5515e5d96a3e30b772726e6c5b00dd6e7632bb49ffe6b04e38501  verify_signed_k4_mus.py
94f5098ae4d60499805483432459d98deb67aa8ed2773ff6d06926ec8e03f852  test_signed_k4_mus.py
025785e35989bbad849c2e5e905738e488eb6bef83bcc4b62ebfdc22f39a5a14  signed-k4-mus.json
5c39718c34ee37edf082a7e7052045ef83ae6640f6099427d592ffcdd8391cdd  requirements-mus-generation.txt
```
