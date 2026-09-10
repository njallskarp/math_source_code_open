# Two probes suffice for every substitution over the Tutte 12-cage

For arbitrary nonempty finite internal graphs \(H_v\), the graph \(T[H_v]\), where \(T\) is the Tutte 12-cage, has full-feedback directional localization number at most two. The exhibited strategy uses at most five rounds.

This closes the substitution route even though the quotient admits no winning adjacent-pair strategy. The proof first weakens the quotient's self response to its entire neighborhood, certifies a four-round strategy with probes at distance two, then simulates it in actual modules and adds one finishing round. See [THEOREM.md](THEOREM.md) for the universal argument and its hypotheses.

## Reproduce

From the source repository root, using Python 3.12 and its standard library only:

```sh
python3 -B full_feedback_tutte_substitution/verify.py
python3 -O -B full_feedback_tutte_substitution/verify.py
cd full_feedback_tutte_substitution
shasum -a 256 -c SHA256SUMS
```

Both Python runs must match `EXPECTED_OUTPUT.txt`, ending with:

```text
result_sha256=5745367018f652ac5abccaedf4b37c56692a07e5499832832b481917081471b0
VERIFIED: quotient policy and actual substitution interfaces
```

`policy.json` contains 312 rows `[territory_mask, rank, probe_1, probe_2]`. The root has rank four and probes 0 and 2. All pairs are at distance two. The verifier checks every response branch, with no symmetry reduction: 332 unresolved branches and 2177 singleton branches. It separately compares ordinary and modified partitions for all 378 distance-two actions and rejects three corrupted policies.

`audit_expansion.py` constructs seven actual substituted graphs, of orders 126 through 1008, and checks all histories of the prescribed strategy, including internal responses and the final robber move. Its breadth-first first-step propagation uses the actual full self response, whereas the quotient verifier explicitly uses the weakened auxiliary self response. A second audit covers 172 small expanded graphs for the projection and finishing interfaces.

The universal claim follows from the written proof, supported by these exact finite audits. Internal graphs are not restricted to the audited examples. Five rounds is not asserted to be optimal, and the parameter need not equal two for every substitution.

No NetworkX, `pynauty`, solver, network access, or large generated certificate is needed to reproduce the result. Those graph packages helped discover the policy locally; they are not part of its verification. The remaining trust boundary is the explicit input, unformalized mathematical proof, exact checker, Python, and hardware. Independent peer review of this new result is pending.
