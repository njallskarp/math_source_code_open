#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

from local_rigidity import complete_graph_edges, direct_count, initial_colors
from solve_cyclic43 import load_certificate, verify_flips


HERE = Path(__file__).resolve().parent


class DirectVerifierTests(unittest.TestCase):
    def test_seed_has_exactly_43_red_cliques(self) -> None:
        result = verify_flips(set())
        self.assertEqual(result["red_k5_count"], 43)
        self.assertEqual(result["blue_k5_count"], 0)

    def test_primary_certificate_has_exactly_two(self) -> None:
        result = verify_flips(load_certificate(HERE / "certificate.json"))
        self.assertEqual(result["monochromatic_k5_count"], 2)
        self.assertEqual(result["red_k5_count"], 2)
        self.assertEqual(result["blue_k5_count"], 0)

    def test_fu_malik_certificate_has_exactly_two(self) -> None:
        result = verify_flips(load_certificate(HERE / "certificate-fm.json"))
        self.assertEqual(result["monochromatic_k5_count"], 2)
        self.assertEqual(result["red_k5_count"], 0)
        self.assertEqual(result["blue_k5_count"], 2)

    def test_certificates_record_exact_optimum(self) -> None:
        for name in ("certificate.json", "certificate-fm.json"):
            payload = json.loads((HERE / name).read_text())
            self.assertEqual(payload["optimum"], 2)

    def test_persisted_local_rigidity_minimizers_recount_to_two(self) -> None:
        cases = (
            ("certificate.json", "local-rigidity-primary.json", "radius_two_minimizer_sample"),
            ("certificate-fm.json", "local-rigidity-fm.json", "radius_two_minimizer_sample"),
            (
                "certificate.json",
                "local-rigidity-radius3-primary.json",
                "radius_three_minimizer_sample",
            ),
            (
                "certificate-fm.json",
                "local-rigidity-radius3-fm.json",
                "radius_three_minimizer_sample",
            ),
        )
        edge_ids, _ = complete_graph_edges()
        for certificate_name, result_name, sample_field in cases:
            colors, _ = initial_colors(load_certificate(HERE / certificate_name))
            payload = json.loads((HERE / result_name).read_text())
            for changed_edge in payload[sample_field]:
                normalized = tuple(changed_edge)
                colors[edge_ids[normalized]] = not colors[edge_ids[normalized]]
            count, _ = direct_count(colors, edge_ids)
            self.assertEqual(count, 2)

    def test_persisted_radius_six_searches_exclude_improvement(self) -> None:
        for name in (
            "local-rigidity-radius6-primary.json",
            "local-rigidity-radius6-fm.json",
        ):
            payload = json.loads((HERE / name).read_text())
            self.assertEqual(payload["radius"], 6)
            self.assertEqual(payload["base_monochromatic_k5_count"], 2)
            self.assertFalse(payload["improvement_found"])
            self.assertEqual(payload["exact_minimum_through_requested_radius"], 2)
            self.assertEqual(len(payload["expanded_by_depth"]), 7)
            self.assertEqual(
                payload["expanded_by_depth"][1:],
                payload["distinct_nonroot_states_by_depth"][1:],
            )


if __name__ == "__main__":
    unittest.main()
