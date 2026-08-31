#!/usr/bin/env python3

import unittest

from verify_cycle_lower_bound import verify


class CycleLowerBoundTest(unittest.TestCase):
    def test_exact_certificate(self) -> None:
        result = verify()
        self.assertEqual(result["odd_entries_min"], 137_500_000_001)
        self.assertEqual(result["shortcut_entries_min"], 217_932_330_829)
        self.assertEqual(result["classical_entries_min"], 355_432_330_830)
        self.assertTrue(result["barina_implies_hercher_hypothesis"])
        self.assertTrue(result["three_pow_665_exceeds_two_pow_1054"])


if __name__ == "__main__":
    unittest.main()
