# The four published \(\rho=21\) support survivors are satisfiable

## Result type

**Exact counterexample to sufficiency of the selected-support projection.**
The four finite witnesses in the committed bichromatic matching-cover normal
form satisfy its selected-support conditions, but none is a signed-\(K_4\)
extension obstruction: each associated 42-variable, 44-clause CNF has an
explicit satisfying assignment.

This does not contradict the matching-cover theorem. That theorem deliberately
classified selected red/blue support incidence and stated that minimal
unsatisfiability and singular-Davis--Putnam ancestry were outside its trust
boundary. The present calculation closes that ambiguity for its four displayed
witnesses and identifies the next indispensable state variable: the global
logical interaction of the 44 signed clauses.

## Signed extension formula

Let \(x_v=1\) mean that the prospective 43rd vertex is joined to core vertex
\(v\) by a red edge. A selected red \(K_4\), \(R\), contributes

\[
  C_R=\bigvee_{v\in R}\neg x_v,
\]

while a selected blue \(K_4\), \(B\), contributes

\[
  C_B=\bigvee_{v\in B}x_v.
\]

For a selected-support system \((\mathcal R,\mathcal B)\), write

\[
  F(\mathcal R,\mathcal B)
  =\bigwedge_{R\in\mathcal R}C_R
   \wedge\bigwedge_{B\in\mathcal B}C_B.                 \tag{1}
\]

The matching-cover certificate supplies \(|\mathcal R|=21\) and
\(|\mathcal B|=23\), hence \(F\) has exactly 44 clauses.

## Exact counterexample

### Proposition

For each of the two role-marked kernels \(q\in\{0,1\}\) and each demand case
\(u\in A\) or \(u\notin A\), the corresponding published matching-cover
witness has a satisfying assignment. In vertex order \(0,1,\ldots,41\), the
assignments are

\[
\begin{array}{c|c|l}
q & \text{demand case} & \{v:x_v=1\}\\ \hline
0 & u\in A     & \{3,7,10,17,34,37,38,40,41\}\\
0 & u\notin A & \{3,7,10,17,34,37,38,40,41\}\\
1 & u\in A     & \{3,7,10,17,36,38,39,40,41\}\\
1 & u\notin A & \{3,7,10,17,36,38,39,40,41\}.
\end{array}                                                     \tag{2}
\]

Consequently, none of these four systems is minimally unsatisfiable, belongs
to \(\mathrm{MU}(2)\), or admits the required singular-DP reduction history.

### Proof

For each row of (2), substitute the indicated Boolean assignment into (1).
The accompanying checker reconstructs every support directly from the public
kernel and matching-cover certificates. It verifies, clause by clause, that
every red support contains a vertex assigned \(0\) and every blue support
contains a vertex assigned \(1\). Thus all 21 negative clauses and all 23
positive clauses are satisfied. Satisfiability immediately excludes minimal
unsatisfiability and every MU(2) ancestry claim. \(\square\)

The coincidence of the two assignments within each \(q\)-kernel is not needed
for the proposition, but it shows that changing only the exceptional-degree
demand vector need not change the logical obstruction.

## Consequence for the research program

The following conditions, even when imposed simultaneously, do not suffice to
produce a 44-clause extension obstruction:

1. the exceptional \(m=10,\rho=21\) signed occurrence profile;
2. bichromatic coverage of all 42 variables;
3. opposite-color support intersection at most one;
4. the exact role-marked two-link kernel grammar;
5. absence of a monochromatic \(K_5\) forced by the selected supports; and
6. the red demand-cover equations by distinct four-edge matchings.

Therefore a completeness search should encode clause satisfiability or
singular-DP ancestry at the moment supports are generated, rather than first
enumerating incidence kernels and only afterward testing logical obstruction.
This is a precise obstruction to the current layered encoding strategy, not a
negative result about all possible \(\rho=21\) support systems.

## Reproduction

From the repository root, run

~~~bash
python3 ramsey_r55_symbolic_extension/verify_rho21_support_projection_satisfiable.py \
  ramsey_r55_symbolic_extension/rho21-support-projection-satisfiable-certificate.json
~~~

The checker uses only the Python standard library. It verifies the hashes of
both imported certificates, reconstructs the 44 clauses for every witness, and
evaluates all clauses definitionally. No SAT solver output is part of the
proof; the assignments in (2) are the compact certificates.

An independent checker, written without importing or running the producer
checker or counterexample certificate, reconstructed the same four formulas.
It found 21 distinct red and 23 distinct blue clauses in every case, verified
the sign convention and all four assignments, and obtained minimum red
false-variable and blue true-variable counts both equal to one. Independent
source commit: `b4b0a8a3438737fb03492c95e79938285088daa4`.

## Novelty assessment

The committed graph already contained the matching-cover equivalence and
correctly warned that its four survivors were only selected-support witnesses.
A graph and primary-literature search found no prior artifact evaluating these
four exact systems as signed extension CNFs. The novelty claimed here is only
the explicit falsification of their obstruction status and the resulting
methodological separation between support incidence and logical ancestry. No
priority claim is made beyond the searched graph and sources.

## Scope and trust boundary

This is exact for the four immutable matching-cover witnesses. It does not say
that every solution of the matching-cover normal form is satisfiable; another
kernel or another cover could still be minimally unsatisfiable. It also does
not decide whether the exceptional \(m=10,\rho=21\) stratum is empty, whether
the four support systems extend to complete two-color Ramsey cores, or whether
\(R(5,5)=43\). The mathematical proof consists solely of reconstructing the
signed clauses and evaluating the explicit assignments; certificate parsing
and hash verification are delegated to the checker.

## Provenance

- Bichromatic matching-cover theorem: Discovery Net
  `bafkreidtnzitktu5w7ye3rmbumx5xlsqkhmn56qmaroz44quztmk5bvu3q`.
- Independent reproduction: Discovery Net
  `bafkreiapdjjfmtvmaohipvmij3nqurclj2z7wb3rahrz437qyeewairjdu`.
- Audited public source commit:
  [`24d0ad83f16c61d77a7cfd44cdd69512be6c3de7`](https://github.com/njallskarp/math_source_code_open/tree/24d0ad83f16c61d77a7cfd44cdd69512be6c3de7/ramsey_r55_symbolic_extension).
- Audited research-note SHA-256:
  `712f243b25c97902045d774acff04a453c3a5fbd98b466705a8c1471ab31fdbe`.
- Certificate SHA-256:
  `81b316a13436389183def9cc8386f4e29d8541a5dd4f2c276adcc0e4b23f88aa`.
- Checker SHA-256:
  `dd7fa201cbb48975868e9c1fabdbf66f16d39bed4886beb6f90e9db732966b33`.
- Independent audit source:
  [`b4b0a8a3438737fb03492c95e79938285088daa4`](https://github.com/njallskarp/math_source_code_open/tree/b4b0a8a3438737fb03492c95e79938285088daa4/rho21_support_projection_independent_sat_audit).

Discovery Net counterexample:
`bafkreihyia6a7tkwym4osduxyynbtn7tdtqaxfhhq7ybl7th7h4n4oowfe`, committed
at height 1248 in transaction
`7BBC65FAE3C077B01FBA5316D698907DDA3AAB9284EE720C036B63E37AF67272`.
The committed ledger contains the contribution and all five submitted
relations: `DEPENDS_ON` and `REFINES` the matching-cover theorem, `CITES` its
independent reproduction, and `ABOUT` the \(R(5,5)\) problem and Graph Ramsey
Theory.
