#!/usr/bin/env python3

import unittest

import verify


class HallCompressionTests(unittest.TestCase):
    def test_single_cluster_terminal_only(self) -> None:
        out = verify.tournament(0, 1)
        rows = verify.blowup(out, (4,))
        self.assertEqual(verify.direct_strong_vertices(rows), (3,))
        self.assertEqual(verify.compressed_strong_clusters(out, (4,)), (0,))

    def test_transitive_quotient_fixture(self) -> None:
        out = verify.tournament((1 << 6) - 1, 4)
        sizes = (1, 2, 3, 2)
        rows = verify.blowup(out, sizes)
        terminals = verify.terminal_vertices(sizes)
        compressed = tuple(terminals[index] for index in verify.compressed_strong_clusters(out, sizes))
        self.assertEqual(verify.direct_strong_vertices(rows), compressed)

    def test_published_margin_one_certificate(self) -> None:
        certificate = verify.published_certificate()
        self.assertEqual([row["defect"] for row in certificate], [1] * 6)
        self.assertEqual(verify.compressed_strong_clusters(verify.PUBLISHED_OUT, verify.PUBLISHED_SIZES), ())

    def test_invalid_cluster_size(self) -> None:
        with self.assertRaises(ValueError):
            verify.blowup(verify.tournament(0, 2), (1, 0))

    def test_invalid_quotient(self) -> None:
        with self.assertRaises(ValueError):
            verify.validate_quotient((frozenset(), frozenset()))


if __name__ == "__main__":
    unittest.main()
