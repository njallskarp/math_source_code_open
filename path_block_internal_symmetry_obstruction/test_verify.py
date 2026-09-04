import unittest

import verify


class InternalSymmetryTests(unittest.TestCase):
    def test_direct_counts(self):
        self.assertEqual(
            [verify.fixed_count_direct(q) for q in range(5)],
            [1, 5, 21, 57, 138],
        )

    def test_closed_series(self):
        report = verify.verify()
        self.assertEqual(report["numerator"], [1, 2, 6, 2, 1])
        self.assertEqual(report["numerator_at_minus_one"], 4)

    def test_hstar_is_not_polynomial(self):
        report = verify.verify()
        self.assertEqual(report["hstar_prefix"][:6], [1, 0, 5, -8, 12, -16])

    def test_two_block_minimality(self):
        self.assertEqual(verify.verify_two_block_simplex(max_width=4), 38)


if __name__ == "__main__":
    unittest.main()
