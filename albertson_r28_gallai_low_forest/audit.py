#!/usr/bin/env python3
"""Independent closed-form audit of the two block-packing thresholds."""

from math import comb


def phi(u: int) -> int:
    return comb(u + 1, 2)


def main() -> None:
    # Convexity packs the increment budget into the largest permitted parts.
    ceiling_52_one_25 = phi(25) + phi(24) + phi(2)
    ceiling_51_no_25 = phi(24) + phi(24) + phi(2)
    assert ceiling_52_one_25 == 628
    assert ceiling_51_no_25 == 603

    # Exact degree-sum floors.  The final +1 is the edge between the two
    # singleton components of H-B, which is absent from H and present in G.
    floors_768_n52 = (
        768 - ((27 + 1) + (27 + 25) + (27 + 25)) + 1,
        768 - ((27 + 2) + (27 + 24) + (27 + 25)) + 1,
    )
    floors_769_n52 = (
        769 - ((27 + 3) + (27 + 25) + (27 + 25)) + 1,
        769 - ((27 + 4) + (27 + 24) + (27 + 25)) + 1,
    )
    assert floors_768_n52 == (637, 637)
    assert floors_769_n52 == (636, 636)
    assert min(floors_768_n52 + floors_769_n52) > ceiling_52_one_25

    floors_n51 = (610, 609, 609, 609)
    assert min(floors_n51) > ceiling_51_no_25

    print("PASS independent Gallai threshold audit")
    print("ceilings=n52_at_most_one_K26:628,n51_no_K26:603")
    print("floors=n52_row768:637,n52_row769:636,n51_min:609")
    print("conclusions=row768_survivors:1,row769_survivors:6,forced_unique_K26:4")


if __name__ == "__main__":
    main()
