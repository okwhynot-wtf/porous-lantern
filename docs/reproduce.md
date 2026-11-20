# Reproduce the mathematics

The mathematical package is standalone and uses the fixed original L3-30 recipe. All required source and certificate data are included in this repository.

From the repository root, using Python 3.12 or later:

```sh
python -m pip install -r requirements.txt
python math/verify.py
python math/generate.py --depth 5 --output .build/lantern.csv
```

Alternatively, with `uv` installed:

```sh
uv run --isolated --python 3.12 --with-requirements requirements.txt python math/verify.py
uv run --isolated --python 3.12 --with-requirements requirements.txt python math/generate.py --depth 5 --output .build/lantern.csv
```

See [media and TouchDesigner](media.md) for rendering dependencies, project controls and film export.

## What the verifier checks

[exact.py](../math/exact.py) reconstructs the eight maps from rational constants, \(\sqrt2\), \(\sqrt3\), and the exact chord-frame formula. It uses outward interval arithmetic at 60 decimal digits, independently of the decimal rendering matrices.

[verify.py](../math/verify.py) then checks:

- Strict contraction, the invariant ball, a nonplanarity witness, and \(8r^3<1\).
- Agreement of the frozen rendering export with the independently reconstructed formula to better than \(10^{-13}\).
- The seven required whole-attractor tube clearances and all three non-neighbour separation classes.
- Prefix-free, complete address covers for every separation claim.
- Opposite signs across a mirror plane and distance from the prescribed join for the additional-contact argument.
- Four explicit attractor points inside specified nominal descendant tubes.
- Endpoint, orthogonality and mirror-identity residuals as implementation checks supporting the analytic derivations.

The certificate inputs in [covers.json](../math/data/covers.json) are finite word lists, not point-cloud approximations. The verifier checks their completeness and recomputes every relevant centre and radius. A point search may nominate a useful cover; the finite complete cover and strict inequalities establish the final bound for the infinite set.

The output [verification.json](../math/data/verification.json) records the precision, environment, numerical diagnostics and SHA-256 hashes of its source and input files. To preserve the distributed receipt when rerunning:

```sh
python math/verify.py --receipt .build/verification.json
```

Rounded diagnostic numbers in that JSON are for readability; they are not certified decimal interval endpoints. Pass/fail decisions use interval comparisons internally. The analytic implications—connectedness, symmetry, the mirror-plane contact argument, and winding—are given in [results](results.md).

## Exporting a finite point set

[generate.py](../math/generate.py) exports a deterministic CSV of \(8^n\) points at depth \(n\). It starts at the retained vertex \(v_0\), rather than at an arbitrary seed, so each exact point is in the attractor. Floating-point arithmetic approximates its coordinates.

For the exact finite set, the Hausdorff error is at most

\[
(27/20+1)r^n.
\]

Every level-\(n\) copy has a point of the export in it, and its other points are within this bound because the original set lies in the radius-\(27/20\) ball and \(|v_0|=1\). Numerical coordinate error is additional to this geometric bound.

Depth 5 gives 32,768 points; depth 7 gives 2,097,152. The default coordinates use the unit octagon. Add `--display-units` to apply the frozen uniform scale used by the renderer. A point set is useful for inspection and import into other tools; it does not replace the interval certificates.

## Scope of verification

The release audit reran the interval checks and exported a depth-five CSV in a separate temporary copy of the mathematical package. The successful receipt was produced with Python 3.14, mpmath 1.3.0 and NumPy 2.3.5. The definitions and proof arguments were reviewed alongside those calculations.

This workflow does not compute the exact Hausdorff dimension, classify every contact, or certify pixels of the finite rendered surface. It verifies the specific mathematical statements enumerated above. See [related work](related.md) for the literature context and the limits of the originality claim.
