#!/usr/bin/env python3

import json
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
