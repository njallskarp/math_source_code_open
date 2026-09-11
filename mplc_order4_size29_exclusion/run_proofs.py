"""Regenerate and independently check every smallest-layer UNSAT proof."""

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

from model import build


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int)
    parser.add_argument("--budget", type=int, default=5000000)
    parser.add_argument("--solver", default="glucose4")
    args = parser.parse_args()
    from pysat.solvers import Solver

    levels = json.loads(args.orbits.read_text())["levels"]
    if [len(x) for x in levels] != [1, 1, 2, 5, 18, 39, 121, 253]:
        raise ValueError("unexpected orbit levels")
    jobs = [(k, i, mask) for k in range(4, 8) for i, mask in enumerate(levels[k])]
    full_run = args.start == 0 and (args.stop is None or args.stop >= len(jobs))
    if full_run:
        from audit import run_audits

        print(json.dumps({"audit": run_audits(levels)}), flush=True)
    args.work_dir.mkdir(parents=True, exist_ok=True)
    cnf_path = args.work_dir / "current.cnf"
    proof_path = args.work_dir / "current.drat"
    records = []
    started = time.monotonic()
    for job, (k, index, mask) in enumerate(jobs):
        if job < args.start or (args.stop is not None and job >= args.stop):
            continue
        cnf, _, meta = build(mask)
        encoded = cnf.dimacs().encode("ascii")
        cnf_path.write_bytes(encoded)
        t = time.monotonic()
        with Solver(name=args.solver, bootstrap_with=cnf.clauses, with_proof=True) as solver:
            solver.conf_budget(args.budget)
            status = solver.solve_limited()
            if status is not False:
                raise RuntimeError(f"case {k}:{index}: status {status}; proof campaign incomplete")
            proof = solver.get_proof()
            stats = solver.accum_stats()
        proof_path.write_text("\n".join(proof) + "\n", encoding="ascii")
        checked = subprocess.run(
            [str(args.drat_trim.resolve()), str(cnf_path.resolve()), str(proof_path.resolve())],
            capture_output=True,
            text=True,
        )
        if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
            (args.work_dir / "failed-check.txt").write_text(checked.stdout + checked.stderr)
            raise RuntimeError(f"proof rejected for {k}:{index}")
        record = {
            "job": job,
            "k": k,
            "index": index,
            "mask": mask,
            "cnf_sha256": hashlib.sha256(encoded).hexdigest(),
            "proof_sha256": hashlib.sha256(proof_path.read_bytes()).hexdigest(),
            "proof_bytes": proof_path.stat().st_size,
            "conflicts": stats["conflicts"],
            "variables": cnf.nvars,
            "clauses": len(cnf.clauses),
            "checked": True,
            "seconds": time.monotonic() - t,
            **meta,
        }
        records.append(record)
        print(json.dumps(record, sort_keys=True), flush=True)
    (args.work_dir / "records.json").write_text(json.dumps(records, indent=2) + "\n")
    if full_run and len(records) == len(jobs):
        canonical = [[r["k"], r["index"], r["mask"], r["cnf_sha256"]] for r in records]
        digest = hashlib.sha256(json.dumps(canonical, separators=(",", ":")).encode()).hexdigest()
        result = {
            "status": "VERIFIED",
            "claim": "29 is not in ML(3,4)",
            "orbit_counts": [len(x) for x in levels],
            "cases": len(records),
            "verified_unsat_cases": len(records),
            "instance_manifest_sha256": digest,
        }
        expected = Path(__file__).with_name("EXPECTED_RESULT.json")
        if not expected.exists() or result != json.loads(expected.read_text()):
            raise ValueError("proof result differs from committed expected result")
        (args.work_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        print(
            json.dumps({"complete_result": result, "elapsed_seconds": time.monotonic() - started}),
            flush=True,
        )
    else:
        print(json.dumps({"status": "PARTIAL", "checked_cases": len(records)}), flush=True)


if __name__ == "__main__":
    main()
