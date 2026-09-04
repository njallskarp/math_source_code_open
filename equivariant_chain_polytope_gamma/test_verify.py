import unittest

import verify


class EquivariantTransferTests(unittest.TestCase):
    def test_edge_sum_criterion(self):
        scan = verify.structural_scan()
        self.assertGreater(scan["structural_cases"], scan["graded_cases"])
        self.assertGreater(scan["nonuniform_graded_cases"], 0)

    def test_comparability_identification(self):
        for case in verify.named_cases():
            self.assertEqual(verify.comparability_edges(case), verify.blowup_edges(case))

    def test_named_cases(self):
        for case in verify.named_cases():
            report = verify.verify_case(case)
            self.assertGreater(report["transfer_equivariance_checks"], 0)

    def test_nonuniform_degree(self):
        case = next(c for c in verify.named_cases() if c.name == "k22_nonuniform_1_2")
        report = verify.verify_case(case)
        self.assertEqual(report["degree"], sum(case.sizes) - 3)
        self.assertEqual(report["group_order"], 4)


if __name__ == "__main__":
    unittest.main()
