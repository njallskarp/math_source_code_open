import unittest

import independent_check as audit


class IndependentInternalSymmetryTests(unittest.TestCase):
    def test_full_coordinates_match_block_sums(self):
        for q in range(4):
            self.assertEqual(
                audit.full_tuple_count(q, False), audit.block_sum_count(q, False)
            )
            self.assertEqual(
                audit.full_tuple_count(q, True), audit.block_sum_count(q, True)
            )

    def test_explicit_permutation_determinant(self):
        mapping = (1, 0, 2, 3, 4, 5, 6)
        self.assertEqual(
            audit.determinant_i_minus_t_permutation(mapping),
            audit.poly_mul([1, 0, -1], audit.poly_pow([1, -1], 5)),
        )

    def test_exact_numerators(self):
        report = audit.verify()
        self.assertEqual(report["ordinary_hstar"], [1, 4, 1])
        self.assertEqual(report["fixed_ehrhart_numerator"], [1, 2, 6, 2, 1])

    def test_character_tail(self):
        report = audit.verify()
        self.assertEqual(report["swap_hstar_prefix"][:6], [1, 0, 5, -8, 12, -16])
        self.assertEqual(report["c2_trivial_prefix"][:6], [1, 2, 3, -4, 6, -8])
        self.assertEqual(report["c2_sign_prefix"][:6], [0, 2, -2, 4, -6, 8])

    def test_two_block_boundary(self):
        self.assertEqual(audit.verify_simplex_boundary(max_width=2, dilations=7), 5)


if __name__ == "__main__":
    unittest.main()
