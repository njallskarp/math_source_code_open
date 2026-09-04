import unittest

import independent_check as check


class IndependentCheckTests(unittest.TestCase):
    def test_vertex_options(self) -> None:
        self.assertIn((3, 1, 1), check.vertex_options(7, 2))
        self.assertIn((6, 2, 2), check.vertex_options(7, 2))
        self.assertNotIn((8, 3, 2), check.vertex_options(7, 2))

    def test_gale_ryser_accepts_and_rejects(self) -> None:
        self.assertTrue(check.gale_ryser([2, 2, 1], [2, 2, 1]))
        self.assertFalse(check.gale_ryser([3, 3, 0], [3, 2, 1]))

    def test_independent_noncyclic_witness(self) -> None:
        parts = check.independent_partition(5, 7, 3)
        self.assertIsNotNone(parts)
        assert parts is not None
        check.validate_partition(5, 7, 3, parts)
        self.assertEqual(len(parts), 11)
        self.assertEqual(sum(len(part[2]) == 4 for part in parts), 2)

    def test_boundary_square(self) -> None:
        parts = check.independent_partition(2, 2, 2)
        self.assertIsNotNone(parts)
        assert parts is not None
        check.validate_partition(2, 2, 2, parts)

    def test_family_base_case(self) -> None:
        count, _ = check.audit_family(2)
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
