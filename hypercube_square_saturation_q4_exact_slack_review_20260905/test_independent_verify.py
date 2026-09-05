import unittest

import independent_verify as audit


class IndependentSlackAuditTests(unittest.TestCase):
    def test_cube_face_incidence(self) -> None:
        for dimension in (3, 4):
            edges = audit.cube_edges(dimension)
            index = {edge: position for position, edge in enumerate(edges)}
            faces = audit.square_masks(dimension, index)
            self.assertEqual(len(edges), dimension * 2 ** (dimension - 1))
            self.assertEqual(len(faces), dimension * (dimension - 1) * 2 ** (dimension - 3))
            incidence = [sum(mask >> edge & 1 for mask in faces) for edge in range(len(edges))]
            self.assertEqual(set(incidence), {dimension - 1})

    def test_local_equality_classification(self) -> None:
        square_free, equality, profiles = audit.q3_equality_patterns()
        self.assertEqual(len(square_free), 2902)
        self.assertEqual(len(equality), 49)
        self.assertEqual(
            profiles,
            {(0, 0, 0, 0): 1, (7, 4, 0, 2): 48},
        )

    def test_global_facet_gluing(self) -> None:
        _, equality, _ = audit.q3_equality_patterns()
        facets = audit.embedded_facet_patterns(equality)
        compatible, _ = audit.glue_zero_slack_facets(facets)
        self.assertEqual(compatible, (0,))

    def test_capacity_cases_used_by_hand_proof(self) -> None:
        _, equality, _ = audit.q3_equality_patterns()
        capacities = audit.facet_capacity_audit(audit.embedded_facet_patterns(equality))
        self.assertEqual(capacities[3], 1)
        self.assertEqual(capacities[6], 12)

    def test_exact_q4_positive_slack_minimum(self) -> None:
        facets = audit.embedded_priced_facets(audit.q3_priced_patterns(6))
        patterns, _ = audit.glue_with_slack_budget(facets, 6)
        nonempty = [(selected, cost) for selected, cost in patterns if selected]
        self.assertEqual(len(nonempty), 64)
        self.assertEqual({cost for _, cost in nonempty}, {6})
        self.assertEqual({selected.bit_count() for selected, _ in nonempty}, {17})
        self.assertEqual(audit.hypercube_orbit(nonempty[0][0]), {p for p, _ in nonempty})


if __name__ == "__main__":
    unittest.main()
