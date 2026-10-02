# The (6,7) sphere-braid derivation

The [walkthrough](braid-six-seven-proof.html) reduces the supplied 178-letter
word to `(σ4 σ5)^3 (σ1 σ2)^-3` through 2,486 elementary rewrites, including
19 sphere-relator substitutions. The two triple twists cancel as mapping
classes of the six-punctured sphere. The product remains the nontrivial
central full twist in the spherical braid group; these are distinct claims.

The [JSON certificate](braid-six-seven-proof.json) records every move, and
the [complete move table](braid-six-seven-proof.md) is readable without
running code. To verify each algebraic step and regenerate the page:

```sh
python render_braid_proof.py
```

If you have the original `BraidSixSeven.svg`, also verify that the 178 letters
were transcribed from that exact file:

```sh
python render_braid_proof.py --source-svg path/to/BraidSixSeven.svg
```

The source check compares both the parsed letters and the recorded SHA-256.
Without `--source-svg`, the verifier checks the certificate from its recorded
input word but does not check a separate SVG transcription.
