# Independent review request

Please audit the frozen proof candidate in [`AUDIT.md`](AUDIT.md). Re-running
the Lean or Python checks is useful but is not, by itself, an independent
mathematical review.

## Required checks

1. Verify the exact hypotheses and conclusions of Labbé--Nevo Lemmas 2.1,
   2.2, 2.3, 3.2, 3.4 and Corollary 4.3 under the package's face-number and
   gamma conventions.
2. Verify the `pi=1,2,4,5,6` exclusions, including every dimension shift.
3. Verify that a homology sphere over an arbitrary field, in the adopted
   all-links sense, is a rational homology sphere by the stated rank/Euler
   characteristic argument.
4. Verify that Davis--Okun Theorem 11.2.1 and Gal Corollaries 2.2.2--2.2.3
   imply `gamma_2>=0` for every relevant 4-dimensional vertex link, with
   `h(-1)=16 kappa=gamma_2` in the 3-dimensional input.
5. Derive the vertex-link identity (I1), missing-edge identity (I3), and
   complement triple identity (I4) from the definitions.
6. Check the equality cases in the rigid-profile squeeze.
7. Check that flagness identifies `link_Delta(r)` with the clique complex of
   `G[B]`, and independently recount the 14 complement edges and 52 link
   edges.
8. Check that the Lean theorem hypotheses match, rather than silently assert,
   every unformalized mathematical bridge.

## Requested disposition

Please record exactly one of:

- **accepted**, with reviewer identity, date, source revision, and the scope of
  the checked theorem;
- **accepted conditionally**, naming every unchecked dependency; or
- **objected**, with the first invalid or insufficiently justified bridge and
  a reproducible counterexample when applicable.

Until such a disposition exists, the Discovery Net result remains a
`proof_attempt`. Any objection should be repaired before outward expansion.
