from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import independent_profile_check as checker


class IndependentProfileCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = checker.compute_audit()

    def test_multiset_enumeration_is_complete(self) -> None:
        self.assertEqual(self.result["visited_degree_multisets"], 296010)

    def test_all_split_profile_counts(self) -> None:
        self.assertEqual(self.result["profile_counts"], [1, 5, 17, 40, 69, 95, 122])

    def test_connectivity_and_escape_counts(self) -> None:
        self.assertEqual(self.result["connected_counts"], [1, 5, 16, 37, 63, 85, 107])
        self.assertEqual(self.result["escape_counts"], [0, 0, 1, 3, 6, 10, 15])

    def test_escape_certificate_digest(self) -> None:
        self.assertEqual(
            self.result["escape_data_sha256"], checker.TARGET_ESCAPE_DATA_DIGEST
        )

    def test_diameter_profile_counts(self) -> None:
        self.assertEqual(self.result["diameter_eight_counts"], [0, 2, 11, 30, 52, 70, 88])
        self.assertEqual(self.result["diameter_five_counts"], [0, 0, 5, 16, 28, 37, 49])

    def test_abstract_d26_boundary_witness(self) -> None:
        witness = self.result["boundary_witness"]
        self.assertEqual((witness["red_clique"], witness["blue_clique"]), (4, 4))
        self.assertEqual(witness["blue_components"], [13, 13])

    def test_mutated_target_certificate_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.txt"
            path.write_text(checker.TARGET_ESCAPE_HEADER + "mutated\n", encoding="ascii")
            with self.assertRaises(AssertionError):
                checker.compare_target_certificate(path, "expected\n")


if __name__ == "__main__":
    unittest.main()
