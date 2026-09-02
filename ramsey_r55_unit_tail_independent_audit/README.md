# Independent audit of potential-matched unit-tail ancestries

This directory independently checks the all-parameter construction claiming
that scalar singular-DP excess data cannot by itself force repeated
nonpivot-literal overlap.  The target mathematical source is
`ramsey_r55_symbolic_extension/potential-matched-unit-ancestry-counterexample.md`
at commit `af024dbb91e92a7c21bf6459874b05ad57ff34c8`.

The checker does not import or run the producer checker or certificate.  It
uses a different filler history: at every filler step it selects the last
available clauses in canonical order, whereas the producer selects the
first.  For every `3 <= p <= 33`, it independently:

- constructs the terminal formula and explicit deletion witnesses;
- transports deletion witnesses through inverse unit extensions and the
  final binary split;
- verifies every reverse Davis--Putnam identity;
- checks all variable, clause, deficiency, charge, overlap, and potential
  totals;
- exhibits a variable-complementation map making the first forward fan a
  pure opposite-sign disjoint `3+3` pair; and
- checks the complete 31-parameter, 744-step range.

Run with CPython 3.11 or later and no third-party packages:

```bash
python3 ramsey_r55_unit_tail_independent_audit/independent_unit_tail_audit.py
```

The final line must be:

```text
independent_unit_tail_audit=PASS
```

## Trust boundary

The finite checker verifies an independently selected history for each
integer parameter.  The universal mathematical content is the symbolic
proof that inverse unit extension and the disjoint binary split preserve
minimal unsatisfiability, together with the elementary schedule bounds.  The
construction is abstract `MU(2)`: it does not make all 44 initial clauses
pure signed four-clauses and therefore does not construct or refute a Ramsey
extension obstruction.
