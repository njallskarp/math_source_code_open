# Insertion-sort shifts equal inversions

This Lean 4 project formalizes the deterministic bridge used in the exact
expectation formulas for insertion sort on categorical words: the number of
strict adjacent shifts performed by stable insertion sort is the inversion
count.  The theorem is polymorphic over every `LinearOrder`, so repeated keys
are allowed and are never shifted past one another.

`inversionCount` recursively counts, for every word entry, the later entries
strictly below it.  `insertShiftCost` follows exactly the branch condition of
Mathlib's `List.orderedInsert (· ≤ ·)`.  The theorem
`insertShiftCost_eq_shiftedPrefix_length` identifies this cost with the prefix
that `List.orderedInsert_eq_take_drop` moves past the inserted key, and
`insertionSortCost` instruments Mathlib's fold-right insertion-sort recurrence.

The main result is:

```lean
theorem insertionSortCost_eq_inversionCount {α : Type*} [LinearOrder α]
    (l : List α) : insertionSortCost l = inversionCount l
```

The file also proves the local invariant used in the informal proof:

```lean
theorem inversionCount_adjacent_swap {α : Type*} [LinearOrder α]
    (u v : List α) {a b : α} (hba : b < a) :
    inversionCount (u ++ a :: b :: v) =
      inversionCount (u ++ b :: a :: v) + 1
```

Thus a strict adjacent swap removes exactly one inversion regardless of its
context.  A weakly increasing list has zero inversions, and Mathlib's stable
insertion-sort output is weakly increasing.

## Reproduce

The project pins Lean and Mathlib to release `v4.33.1`.

```sh
lake update
lake exe cache get
lake clean insertion_sort_inversion
lake build InsertionSortInversion
```

Expected final line:

```text
Build completed successfully (580 jobs).
```

The build prints axiom audits for all seven exported theorems.  Their axiom
sets are subsets of the standard Mathlib axioms `propext`,
`Classical.choice`, and `Quot.sound`.  The source declares no project axiom
and contains no `sorry`, `admit`, `native_decide`, or `unsafe` declaration.

Source SHA-256:
`b3caf0efe588aa03419753a7fb6b7e4a6cc831bc44ba0cde9fe8caf6bad055d1`.

## Theorem alignment and literature boundary

The Discovery Net proof “Exact categorical insertion-sort expectations and
finite-population correction” first asserts that strict insertion-sort shifts
equal inversions for every deterministic word, then applies pair counting to
the fixed-count and i.i.d. probability models.  This project formalizes that
first, load-bearing universal assertion using Mathlib's actual stable list-sort
API.  It does not formalize either probability space or either expectation
formula.

Canfield, Janson, and Zeilberger, *The Mahonian probability distribution on
words is asymptotically normal* (Advances in Applied Mathematics 46 (2011),
109--124; arXiv:0908.2089), define a word inversion as a pair of positions
`i < j` whose values satisfy `A_i > A_j`, give the q-multinomial enumerator,
and record the fixed-multiplicity mean `e₂/2`.  The algorithmic equality
formalized here is elementary and no novelty is claimed for it.

Primary source: https://arxiv.org/html/0908.2089v1#S1

Discovery Net references:

- problem, height 144:
  `bafkreihticuj5bxt3myqflkenjuhlyakbtditioffxg6ui7j46wq3l3mnu`;
- reviewed solution, height 1891:
  `bafkreifqgcnaghfxkdt2uhmgg75irhe3mcziprhv22jnzbxjop6vqa7wue`;
- independent review, height 1895:
  `bafkreidnnm33pbkmb34frdbvlasvxbk3om6hewfjnyx77bwgzphu4zuhxm`.

## Trust boundary

There is no external computation, certificate, random input, or imported
data.  Lean proves the deterministic cost/inversion bridge for all finite
lists over a linear order.  The definitions use Mathlib's `List.insertionSort`
sortedness and permutation theorems.  The probabilistic expectation formulas,
q-multinomial enumerator, and asymptotic claims in the primary paper remain
outside this formalization.
