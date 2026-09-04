import unittest

import verify


class VerifyTests(unittest.TestCase):
    def test_startup(self):
        for dims in ((3, 3, 3), (3, 4, 5), (6, 3, 4)):
            states = verify.startup(*dims)
            for before, after in zip(states, states[1:], strict=False):
                self.assertEqual(verify.delta_types(before, *dims), after)

    def test_layer_recurrence(self):
        for dims in ((3, 3, 3), (3, 4, 5), (5, 3, 4)):
            total = sum(dims)
            self.assertEqual(
                verify.delta_types(verify.startup(*dims)[-1], *dims),
                verify.layer(total - 2, *dims),
            )
            for s in range(total - 2, 2, -1):
                self.assertEqual(
                    verify.delta_types(verify.layer(s, *dims), *dims),
                    verify.layer(s - 1, *dims),
                )

    def test_endpoint(self):
        for dims in ((3, 3, 3), (3, 4, 5), (5, 3, 4)):
            self.assertEqual(
                verify.delta_types(verify.layer(2, *dims), *dims),
                verify.initial(*dims),
            )

    def test_kappa_strict(self):
        self.assertGreater(verify.verify_kappa_covers(3, 4, 5), 0)

    def test_rank_filling(self):
        self.assertGreater(verify.verify_rank_filling(3, 4, 5), 0)


if __name__ == "__main__":
    unittest.main()
