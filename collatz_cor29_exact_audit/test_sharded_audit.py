#!/usr/bin/env python3

import unittest

from run_sharded_audit import aggregate


class ShardedAuditAggregationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frontier_hash = "a" * 64
        self.binary_hash = "b" * 64
        self.frontier = {
            "split_depth": "4",
            "c": "1536",
            "states": "2",
            "root_generated": "7",
            "root_pruned_exact": "1",
            "root_decision_disagreements": "0",
            "root_corrected_multiplier_disagreements": "2",
            "root_float_multiplier_below_exact": "1",
            "root_float_multiplier_above_exact": "1",
            "root_maximum_multiplier_error": "9",
            "root_second_branch_disagreements": "0",
            "root_minimum_scaled_margin": "3/10",
        }

    def shard(self, index: int, margin: str) -> dict[str, str]:
        return {
            "frontier_sha256": self.frontier_hash,
            "binary_sha256": self.binary_hash,
            "mode": "shard",
            "split_depth": "4",
            "target_depth": "6",
            "c": "1536",
            "frontier_states": "2",
            "shard_index": str(index),
            "shard_count": "2",
            "selected_states": "1",
            "generated": str(10 + index),
            "pruned_exact": "2",
            "frontier": str(3 + index),
            "decision_disagreements": "0",
            "corrected_multiplier_disagreements": "1",
            "float_multiplier_below_exact": str(index),
            "float_multiplier_above_exact": str(1 - index),
            "maximum_multiplier_error": str(4 + index),
            "second_branch_disagreements": "0",
            "minimum_scaled_margin": margin,
        }

    def test_exact_aggregation(self) -> None:
        result = aggregate(
            self.frontier,
            [self.shard(0, "1/4"), self.shard(1, "2/7")],
            frontier_hash=self.frontier_hash,
            binary_hash=self.binary_hash,
            target_depth=6,
        )
        self.assertIn("generated=28\n", result)
        self.assertIn("pruned_exact=5\n", result)
        self.assertIn("frontier=7\n", result)
        self.assertIn("corrected_multiplier_disagreements=4\n", result)
        self.assertIn("maximum_multiplier_error=9\n", result)
        self.assertIn("minimum_scaled_margin=1/4\n", result)

    def test_rejects_incomplete_partition(self) -> None:
        bad = self.shard(1, "2/7")
        bad["selected_states"] = "0"
        with self.assertRaisesRegex(ValueError, "shards cover 1 states"):
            aggregate(
                self.frontier,
                [self.shard(0, "1/4"), bad],
                frontier_hash=self.frontier_hash,
                binary_hash=self.binary_hash,
                target_depth=6,
            )


if __name__ == "__main__":
    unittest.main()
