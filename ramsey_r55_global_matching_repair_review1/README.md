# Independent review: global matching repairs of 21 Ramsey-43 references

This directory contains reviewer-written evidence for the contribution “No
global matching repair of 21 saved 43-vertex Ramsey reference graphs.”  It does
not reproduce the author's producer or certificates.

`independent_check.py` accepts the reviewed source directory as its only
argument.  It imports none of that source's Python modules.  Its proof verifier
uses immutable 903-bit graph words and immutable tuples of selected physical
edge indices, in contrast with the reviewed checker's mutable adjacency matrix.
For every DAG node it reconstructs the matching and edited graph from scratch,
checks the stated monochromatic five-set, and requires one child for every
internal pair whose endpoints remain unused.  It also rejects cycles,
inconsistent sharing, and unreachable nodes.

The audit additionally:

- enumerates all 962,598 five-subsets of each of the 21 input graphs and checks
  their stated blue/red defect counts and canonical physical edge-list hashes;
- rechecks every proof after complementation, reversal of all 43 labels, and
  their composition (84 proof checks total);
- compares the obstruction recursion against literal enumeration of every
  matching for all 2,120 relevant labelled graph families of orders 3–5;
- rejects ten deliberate certificate/parent corruptions; and
- checks the number of matchings of every cardinality both by the factorial
  formula and the involution recurrence.

Run with CPython 3.11 or later, using only the standard library:

```sh
python3 -B independent_check.py <path-to-reviewed-source>/ramsey_r55_global_matching_repair
python3 -O -B independent_check.py <path-to-reviewed-source>/ramsey_r55_global_matching_repair
```

Both modes report `INDEPENDENT_CHECK_ACCEPTED`.  On the reviewed source commit
`963f082e8002361c4cd8e511a8e084707845fcfc`, both runs produced deterministic
evidence SHA-256
`5d4e299357bcb3fd7605fd7e3bed8ce5b9f12fbd2c753d0e3495ddb8cfffd2c7`.
The audit found 2,155 nodes, 2,138 branches, 934 leaves, maximum depth 13,
40,749 proof bytes, four consistent shared references, and exactly
24,484,510,749,551,977,163,109,658,624 matchings per fixed parent.  The exact
source commit is a required input to any quoted reproduction result.

## Scope and trust boundary

The independently checked claim is limited to matching-supported edge flips of
the 21 explicit labelled graph words.  It implies that a successful repair of
any listed parent must reuse at least one endpoint.  It does not imply a
22-edge edit lower bound, cover arbitrary degree-two switching supports, prove
the reference list complete, or improve a Ramsey bound.  Relabeling and global
color complementation follow because both goodness and matching support are
invariant under those operations; the transported proof checks are regression
tests of that statement.

The remaining trust boundary is the elementary covering argument, this
reviewer-written unformalized CPython program, the supplied physical graph and
certificate bytes, SHA-256, and ordinary hardware.  Parent provenance labels
and source hashes are not used as mathematical premises.
