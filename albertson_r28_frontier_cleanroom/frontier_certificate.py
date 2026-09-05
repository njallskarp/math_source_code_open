#!/usr/bin/env python3
"""Emit the sparse 67-row provenance certificate checked by verify.py."""

from verify import (
    N_MIN,
    ORDER_MAX,
    R,
    base_support,
    build_base_tables,
    ceil_fraction,
    critical_edge_candidates,
    critical_edge_floor,
    direct_sample_best,
    z_complete,
)


def main() -> None:
    threshold = z_complete(R)
    base_tables, base_hulls = build_base_tables(ORDER_MAX)
    print("n\tm_floor\tedge_support\taffine_endpoint_support\tsample_support\thull_support\texact_direct_bound\tceiling\tstatus")
    for n in range(N_MIN, ORDER_MAX + 1):
        candidates = critical_edge_candidates(R, n)
        best_twice_edges = max(value for _, value in candidates)
        edge_support = "+".join(name for name, value in candidates if value == best_twice_edges)
        m = critical_edge_floor(R, n)
        bound, witnesses = direct_sample_best(n, m, base_tables, base_hulls)
        affine_support = ";".join(
            f"s{w.sample_order}:L={'+'.join(base_support(w.sample_order, w.left_q))},"
            f"R={'+'.join(base_support(w.sample_order, w.right_q))}"
            for w in witnesses
        )
        samples = tuple(w.sample_order for w in witnesses)
        hull_support = ";".join(f"s{w.sample_order}[{w.left_q},{w.right_q}]" for w in witnesses)
        rounded = ceil_fraction(bound)
        if n == 54:
            status = "closed_by_disconnected_floor_766"
        elif n == 55:
            status = "frontier"
        elif n == 56:
            status = "closed_by_recursive_bound_7115"
        else:
            assert rounded >= threshold
            status = "closed_directly"
        print(
            f"{n}\t{m}\t{edge_support}\t{affine_support}\t{','.join(map(str, samples))}\t"
            f"{hull_support}\t{bound}\t{rounded}\t{status}"
        )


if __name__ == "__main__":
    main()
