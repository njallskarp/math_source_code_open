# Full-feedback localization: unrestricted pairs versus adjacent pairs

The Tutte 12-cage has full-feedback directional localization number exactly two. A concrete policy wins in at most three rounds with unrestricted pairs, while an explicit invariant lets the robber evade every strategy that probes an edge each round.

This supplies a genuine two-probe quotient outside the adjacent-pair hypothesis used in the earlier substitution obstruction. It does not produce an unrestricted parameter above two or establish such a lower bound for any substitution.

Read [THEOREM.md](THEOREM.md) for the game convention, proof, scope, and prior-work links.

## Reproduce

From the repository root, with Python 3.12 and no third-party dependencies:

```sh
python3 -B full_feedback_adjacent_pair_separation/verify.py
python3 -O -B full_feedback_adjacent_pair_separation/verify.py
cd full_feedback_adjacent_pair_separation
shasum -a 256 -c SHA256SUMS
```

Both Python commands must match `EXPECTED_OUTPUT.txt`, ending with:

```text
result_sha256=07cf64fff5a15817838bec4c4b9b98490c00ea38f1f28c22b865fe52381c7664
VERIFIED: unrestricted two probes win; every adjacent-pair strategy loses
```

The verifier constructs the graph from its 18-entry LCF shift list. It enumerates all 2646 core pairs at distances two through four and all 189 adjacent probe actions, checking 500,094 evasion obligations. It separately checks all actual responses of the 122-node unrestricted winning policy, including 123 unresolved branches and 1011 singleton branches. Three deliberately corrupted policies must be rejected.

`policy.json` contains only the compact winning policy. Each row is `[territory_mask, rank, probe_1, probe_2]`; the root uses rank three and probes 0 and 5. Every unresolved legal child must occur with rank lowered by one. No claim of optimal duration is made.

The losing family is generated from its mathematical formula, so no exhaustive witness dump is needed. The SHA-256 digest printed for the 500,094 witness rows is reproducibility evidence; all obligations are checked afresh.

The earlier exploration used NetworkX and local `pynauty` canonicalization to find a policy. Those tools, their generated state, and their search completeness are outside the proof's trust boundary. The published checker imports neither and consumes no downloaded graph data. The written proof and exact verifier remain unformalized, and independent peer review is pending.

The files are limited to the proof, this guide, the verifier, a compact policy, expected output, and a hash manifest. No build outputs, packages, caches, raw search results, or large generated certificates are required.
