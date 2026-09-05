#!/usr/bin/env python3
"""Print the compact exact initial-order and final-row certificate."""

from verify import (
    CANDIDATE_ORDERS,
    R,
    build_base_tables,
    build_recursive_tables,
    critical_edge_floor,
    critical_sources,
    direct_best,
)


def main() -> None:
    base_tables, base_hulls = build_base_tables(max(CANDIDATE_ORDERS))
    recursive, _ = build_recursive_tables(59)
    print("n\tcritical_m\tcritical_support\tdirect_sample\tdirect_ceiling\tstatus")
    for n in CANDIDATE_ORDERS:
        m = critical_edge_floor(R, n)
        value, witnesses = direct_best(n, m, base_tables, base_hulls)
        witness = ";".join(
            f"s{w.sample_order}[{w.left_q},{w.right_q}]@{w.mean_q}"
            f"*{w.multiplier}={w.unrounded}"
            for w in witnesses
        )
        if n <= 59:
            recursive_value = recursive[n][m]
            status = "recursive-open" if recursive_value < 8281 else "closed"
            if n == 56 and recursive_value < 8281:
                status = "closed-by-disconnected-complement"
        else:
            status = "closed-direct"
        print(
            f"{n}\t{m}\t{','.join(critical_sources(R, n))}\t{witness}"
            f"\t{-((-value.numerator) // value.denominator)}\t{status}"
        )
    print()
    print("n\tm\trecursive_cr_lower\tdegree_excess\tforced_degree28_min")
    for n, lo, hi in ((57, 824, 828), (58, 838, 840)):
        for m in range(lo, hi + 1):
            excess = 2 * m - 28 * n
            print(f"{n}\t{m}\t{recursive[n][m]}\t{excess}\t{max(0, n-excess)}")


if __name__ == "__main__":
    main()
