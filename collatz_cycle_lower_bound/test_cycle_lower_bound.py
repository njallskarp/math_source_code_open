#!/usr/bin/env python3

import unittest

from verify_cycle_lower_bound import verify


class CycleLowerBoundTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify()
        self.assertEqual(result["odd_entries_min"], 137_500_000_001)
        self.assertEqual(result["shortcut_entries_min"], 217_932_343_851)
        self.assertEqual(result["classical_entries_min"], 355_432_343_852)
        self.assertTrue(result["barina_implies_hercher_hypothesis"])
        self.assertTrue(result["exact_log_product_floor_certified"])


if __name__ == "__main__":
    unittest.main()
