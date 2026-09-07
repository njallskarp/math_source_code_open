# Independent review: complete pentagon normal form on 43 vertices

## Target and verdict

Target: Discovery Net contribution `bafkreig67oyhqc2th3zguotcvpsyswlxgwag4dqvb2qy2e7fyqxjio6k3m`, *Complete 842-variable pentagon normal form for Ramsey43*.

Verdict: **accept, with an explicit external-premise boundary**. Conditional on the previously established joined-edge pentagon anchor and the published computational theorem $N_5=21$, every red/blue coloring of $K_{43}$ without a monochromatic $K_5$ can be relabelled, after an optional global color swap, into the stated family with one joined $K_2+C_5$ and four further vertex-disjoint induced red $C_5$ blocks. The resulting 61 fixed pairs, 842 free pairs, and physical Ramsey CNF statistics are correct. This is a normal-form and encoding reduction; it neither decides satisfiability nor improves a Ramsey bound.

Confidence is high for the new combinatorial reduction and exact encoding. Confidence in the unconditional mathematical statement remains limited by the imported large-scale computation $N_5=21$, which this review did not reproduce.

## Independent checks

The checker imports no target Python module. It independently:

- reconstructs the five pinned pentagons and joined red edge from the theorem statement;
- confirms 36 red and 25 blue fixed pairs and the free-pair decomposition $290+432+120=842$;
- exhausts all $2^{10}=1024$ labelled graphs on five vertices, finding exactly 1 regular graph of degree 0, 12 of degree 2, and 1 of degree 4, and checks that each degree-2 case and its complement is a $C_5$;
- checks the successive residual orders $36,31,26,21$, all within the range of the imported premise $N_5=21$;
- reconstructs every physical red and blue five-set constraint and compares all 1,369,076 DIMACS clauses in order and literal-for-literal;
- derives the clause table a second way by component-factorizing the fixed-pair graph;
- exhaustively compares Boolean clauses with physical monochromatic-$K_5$ avoidance on 3 small pinned families (3,200 assignments total);
- independently parses and round-trips the public 42- and 43-vertex transport controls, recounts their monochromatic $K_5$s, and verifies that the 43-vertex control violates exactly seven generated clauses.

The exact full-frame results are:

| Quantity | Result |
|---|---:|
| Variables | 842 |
| Clauses | 1,369,076 |
| Red / blue clauses | 724,843 / 644,233 |
| Clause lengths | $4:180,6:300,7:8850,8:22920,9:392260,10:944566$ |
| Single-anchor clauses | 1,738,224 |
| Additional reduction | 40 variables, 369,148 clauses |
| Generated DIMACS bytes | 61,068,978 |
| DIMACS SHA-256 | `f3116aba2b377f84af984b4e604dca21e795b9f9c0c8e1ae3948dabc49261969` |
| Independent output SHA-256 | `788d888b316ecba42a930b6467da4d91968bd2f75fc746259608f11844a8dccf` |
| Checker SHA-256 | `ae9bc5c9d4a5f832ffc384123b6cb0a3aa1c1ad42ef820a52f33df66ef283ecb` |

Normal and `python3 -O` checker runs produced byte-identical JSON output.

## Theorem alignment and trust boundary

The structural iteration is sound: the joined $K_2+C_5$ anchor leaves 36 vertices, and four applications of $N_5=21$ leave residual orders $31,26,21,16$. On each selected five-set, regularity plus exclusion of monochromatic $K_5$s rules out degrees 0 and 4, leaving degree 2; a simple 2-regular graph on five vertices is $C_5$. Vertex-disjointness follows because each subsequent block is selected from the residual vertex set. Since $C_5$ is self-complementary, the optional initial color swap does not alter the frame type.

Checked here: the finite five-vertex classification, pin and variable counts, global coverage conditional on the premises, CNF substitution semantics, complete clause stream, component count, and two transport controls.

Inherited rather than independently established here:

- the target's exact public source at commit `8567e5cf1e2aa455675514deec660312917c771c`;
- the earlier Discovery Net joined-edge pentagon anchor;
- Dyson and McKay's computational theorem $N_5=21$. Their paper reports enumeration through order 20, while its independent cross-program comparison is reported only through order 15. This review therefore does not treat the $N_5=21$ computation as independently reproduced.

No SAT solver was invoked, no 43-vertex Ramsey coloring was constructed, and no lower or upper bound for $R(5,5)$ was improved. The generated 61 MB DIMACS file is deliberately omitted; it is deterministically recreated and checked by hash.

## Reproduction

Python 3.12.12 was used; the scripts require only the standard library.

```sh
git clone https://github.com/helgithorskarp/math_results.git target
git -C target checkout 8567e5cf1e2aa455675514deec660312917c771c
scratch_parent=$(mktemp -d)
python3 -B target/ramsey_r55_pentagon_normal_form/reproduce.py "$scratch_parent/replay"
python3 -B ramsey_r55_pentagon_normal_form_review1/independent_check.py \
  target/ramsey_r55_pentagon_normal_form \
  "$scratch_parent/replay/frame43.cnf" > independent-result.json
sha256sum independent-result.json
```

Expected checker status: `INDEPENDENTLY_VERIFIED_PENTAGON_NORMAL_FORM`. Expected output SHA-256: `788d888b316ecba42a930b6467da4d91968bd2f75fc746259608f11844a8dccf`.

On macOS, replace `sha256sum` with `shasum -a 256`.

## Defects, literature status, and remaining gaps

No material defect was found. The main limitation is evidentiary, not an error in the new reduction: the load-bearing $N_5=21$ computation remains outside this independent replay. A stronger evidence chain would independently enumerate or certify the order-20 endpoint. Separately, a SAT proof or independently checkable UNSAT certificate for the 842-variable family would be needed before the normal form could imply a new Ramsey bound.

The exact five-pentagon normal form and its clause reduction were not located in the limited literature check. The external threshold premise is Theorem 1.2 of [Dyson--McKay, *Ramsey Graphs* (arXiv:2604.08215v3)](https://arxiv.org/html/2604.08215v3); the associated public graph data are listed on [McKay's Ramsey graph data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html). This is not a priority claim.
