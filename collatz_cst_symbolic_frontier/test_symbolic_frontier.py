import unittest

from verify_mechanical_first_crossing import CylinderState, audit


def direct_cylinder(word: tuple[int, ...]) -> tuple[int, int]:
    for start in range(1 << len(word)):
        value = start
        observed = []
        for _ in word:
            observed.append(value & 1)
            value = (3 * value + 1) // 2 if value & 1 else value // 2
        if tuple(observed) == word:
            return start, value
    raise AssertionError(word)


class SymbolicFrontierTests(unittest.TestCase):
    def test_cylinder_extension_exhaustively(self) -> None:
        states = [((), CylinderState.empty())]
        for _ in range(10):
            next_states = []
            for word, state in states:
                for bit in (0, 1):
                    extension = word + (bit,)
                    extended_state = state.extend(bit)
                    self.assertEqual(
                        direct_cylinder(extension),
                        (extended_state.residue, extended_state.endpoint),
                    )
                    next_states.append((extension, extended_state))
            states = next_states

    def test_small_audit(self) -> None:
        report = audit(100, 100)
        self.assertEqual(report["first_crossing_cases"], 64)
        self.assertEqual(report["nontrivial_cases"], 62)
        self.assertEqual(report["trivial_equalities"], 2)
        self.assertEqual(report["nontrivial_failures"], 0)
        self.assertEqual(report["last_crossing_length"], 100)
        self.assertEqual(report["last_crossing_odd_count"], 63)
        self.assertEqual(
            report["full_sha256"],
            "5d41f60fa951a4ea7027b1c7683739661dc629543c7abe90d0418ec531617ca9",
        )


if __name__ == "__main__":
    unittest.main()
