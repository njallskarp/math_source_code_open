# The missing order-four Latin-cube size is impossible

An exact complete computation proves \(29\notin ML(3,4)\). Together with the established memberships and exclusions,
\[
ML(3,4)=\{28\}\cup\{30,31,\ldots,61\}\cup\{64\}.
\]
See [PROOF.md](PROOF.md) for the complete smallest-layer reduction, orbit coverage, CNF equivalence, dependencies, and trust boundary. This is an exact computer-assisted result; independent peer review is pending.

Every hypothetical 29-entry cube has a globally smallest coordinate slice of size four through seven. There are 431 possible slice orbits. Each exact extension formula has an independently checked UNSAT proof. A separate orbit–stabilizer audit agrees with a direct count of all labeled slice configurations. Known 28- and 30-entry cubes pass the full encoding interfaces.

## Reproduce

Use Python 3.12, a C99 compiler, Python-SAT **1.8.dev24**, and DRAT-trim at commit **`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`**. Validation used CPython 3.12.12, Apple Clang 17.0.0, and the bundled Glucose 4.1 solver. Run from this directory. The example places all dependencies, binaries, and generated proof files outside the source tree:

```sh
python3 -m venv /tmp/mplc29-venv
/tmp/mplc29-venv/bin/python -m pip install python-sat==1.8.dev24
git clone https://github.com/marijnheule/drat-trim.git /tmp/mplc29-drat
git -C /tmp/mplc29-drat checkout --detach 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/mplc29-drat drat-trim
cc -std=c99 -O3 -Wall -Wextra -Wpedantic -Wconversion orbits.c -o /tmp/mplc29-orbits
/tmp/mplc29-orbits > /tmp/mplc29-orbits.json
/tmp/mplc29-venv/bin/python -B run_proofs.py \
  --orbits /tmp/mplc29-orbits.json \
  --drat-trim /tmp/mplc29-drat/drat-trim \
  --work-dir /tmp/mplc29-proofs > /tmp/mplc29-run.jsonl
```

A full invocation performs the independent orbit, counter, binary-interface, and positive-control audits before checking all 431 proof traces. It compares both final results with the committed expected records. It terminates with an error on an unfinished solver call, a rejected proof, a missing case, or a manifest mismatch. The default conflict ceiling is a guard against unfinished reproduction, not a mathematical cutoff; encountering it gives no theorem result. `--start` and `--stop` are local partitioning aids whose restricted runs report only `PARTIAL`.

The final record contains:

```text
status: VERIFIED
claim: 29 is not in ML(3,4)
cases: 431
verified_unsat_cases: 431
instance_manifest_sha256: 4dcb262693cf41194511e287460e3cfe87971127e468c8136e0696018ad6d6f0
```

For a faster standard-library-only audit, after generating the orbit list:

```sh
python3 -B audit.py /tmp/mplc29-orbits.json
python3 -O -B audit.py /tmp/mplc29-orbits.json
shasum -a 256 -c SHA256SUMS
```

Both audit modes match [EXPECTED_AUDIT.json](EXPECTED_AUDIT.json), with audit SHA-256 `cb256cbcdabbd3bc2d70ad019baf1b583e91c2c93486a564fe28d4353e0689cc`. They are an audit of coverage and interfaces, not a substitute for the 431 proof checks. Optional C validation adds `-O1 -g -fsanitize=address,undefined` and compares the entire resulting orbit JSON with the optimized build.

## Evidence and resources

The initial complete proof-generation/checking run took about 259 seconds. It generated about 423 MB of traces cumulatively, with the largest individual trace about 22.2 MB. Only the current formula and trace are retained by the driver; none of these large generated files is published. The source, controls, and expected records are compact. Setup requires network access; the mathematical computation thereafter uses only locally generated instances and the installed tools.

`orbits.c` provides exact representatives. `model.py` supplies the Boolean model and explicit unary counters. `audit.py` checks orbit mass by a separate row-matching dynamic program and verifies the semantic interfaces. `run_proofs.py` generates Glucose proofs and requires DRAT-trim acceptance for each formula. The solver verdict alone is insufficient. Remaining trust is the written proof, source/checkers, DRAT semantics, toolchains, and hardware.

The positive controls are credited in [PROOF.md](PROOF.md). The 28-membership is classical. The new 29-exclusion is new to the inspected graph and primary sources; historical priority is not established.
