#!/usr/bin/env python3
"""Compare the target and reviewer histograms kernel by kernel.

Run this from the public review directory, next to the target directory
``line_graph_signature_c3_core``.  This comparison deliberately imports both
implementations; independence is supplied by ``independent_check.py`` itself.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import networkx as nx


EXPECTED = "636d19d7c03daf340c08069493998239ef871e4f1b1236640dc28822b26ff72f"
TARGET_COMMIT = "8e5e99d2f6a0c027497a4c65061c8603fc8d7377"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    here = Path(__file__).resolve().parent
    review = load("review_check", here / "independent_check.py")
    target = load(
        "target_check",
        here.parent / "line_graph_signature_c3_core" / "verify_c3_core.py",
    )

    per_kernel = {}
    for kernel in target.enumerate_c3_kernels():
        graph = nx.MultiGraph()
        graph.add_nodes_from(range(kernel[0]))
        for u, v, multiplicity in kernel[1]:
            for _ in range(multiplicity):
                graph.add_edge(u, v)
        fingerprint = ",".join(map(str, review.kernel_fingerprint(graph)))

        counts = Counter()
        edges = target.kernel_edge_instances(kernel)
        for residues in product(range(1, 5), repeat=len(edges)):
            lengths = target.canonical_residue_lengths(edges, residues)
            adjacency = target.expand_kernel(kernel, lengths)
            positive, nullity, negative = target.inertia(
                target.shifted_signless(adjacency)
            )
            counts[(positive - negative - 2, nullity)] += 1
        per_kernel[fingerprint] = {
            f"s={signature},z={nullity}": count
            for (signature, nullity), count in sorted(counts.items())
        }

    canonical_histograms = json.dumps(
        {fingerprint: per_kernel[fingerprint] for fingerprint in sorted(per_kernel)},
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(canonical_histograms.encode()).hexdigest()
    assert digest == EXPECTED

    result = {
        "per_kernel_histogram_sha256": digest,
        "status": "MATCH",
        "target_source_commit": TARGET_COMMIT,
    }
    canonical_result = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(canonical_result)
    print("RESULT_SHA256=" + hashlib.sha256(canonical_result.encode()).hexdigest())


if __name__ == "__main__":
    main()
