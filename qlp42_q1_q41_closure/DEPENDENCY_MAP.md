# Proof dependency map

Arrows below mean “uses as a mathematical dependency.” They are not claims
that every corresponding graph edge already existed at the initial audit.

```text
QLP-42 canonical norm-32 shell
  |
  +-- six-orbit half-compression reduction
  |     |
  |     +-- mod-4 defect count q = 1 (mod 4)
  |     +-- exact 16-state coupled S/H transform
  |            |
  |            +-- q=1 reflection
  |            |     |
  |            |     +-- complete q=1 third-order b partition
  |            |            |
  |            |            +-- b=20 obstruction
  |            |            +-- b=18 obstruction
  |            |            +-- b=16 obstruction
  |            |            +-- b=14 obstruction
  |            |            +-- b=12 obstruction
  |            |            +-- b=10 obstruction
  |            |            +-- b=8 obstruction
  |            |            +-- b=6 obstruction
  |            |            +-- b=4 obstruction
  |            |                    |
  |            |                    +-- q=1 branch closure
  |            |
  |            +-- q=41 axis reflection
  |                  |
  |                  +-- complete q=41 third-order weight partition
  |                         |
  |                         +-- exact-sum/sign-support layers
  |                         +-- exact all-weight H/S sweep
  |                                  |
  |                                  +-- q=41 branch closure
  |
  +-- q=1 closure + q=41 closure
         |
         +-- extreme-branch corollary: q not in {1,41}
```

## Exhaustive partitions

The q=1 proof uses the disjoint set

```text
{4,6,8,10,12,14,16,18,20}.
```

The q=41 proof uses the disjoint set

```text
{0,4,8,12,16,20}.
```

The package verifier checks both lists exactly and verifies the published
q=41 labeled-word and orbit totals. The q=1 third-order mask counts add to
480, the classifier’s full surviving total.

## Dependency minimality

For the combined corollary, the two branch-closure theorems are sufficient.
For independent auditability, `SOURCE_PINS.json` expands each branch theorem
to the classifiers and row-level certificates on which it actually rests.
Reviews and reproductions are valuable evidence but are not substituted for
the mathematical lemmas themselves.
