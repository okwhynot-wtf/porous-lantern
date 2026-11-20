# Numerical anatomy of the original 0/1 join

The two neighboring miniature Lanterns are mirror partners, but the material
that extends across their shared mirror plane is **not simply an identical
duplicate layer**. In particular, the retained vertex `f04(v5)` belongs to
piece A, crosses into B's nominal half-space, and remains separated from B.
The [companion interval certificate](data/interface-certificate.json) proves the needed separation; the numerical
screen here independently locates it and shows convergence.

The original recipe is unchanged. All coordinates below use the unit-octagon
normalization, not the display export's scale.

## Sets and rendering

- A = `f0(K)` and B = `f1(K)`.
- The mirror is `S(x,y,z)=(y,x,z)`; it exchanges A and B.
- The proposed dividing plane is `P: x=y`.
- Signed distance to P is `w=(x-y)/sqrt(2)`. A's nominal side is `w>=0`.

For exact sets, A and B have identical traces on P: every point of A on P
is fixed by S and therefore belongs to B. This identity does not imply that
all geometry on either side of P coincides. It also does not classify their
entire intersection, which may include points away from P.

K has zero three-dimensional volume. Its solid-looking surface is a finite
approximation with thickness. Any displayed volume of interpenetration belongs
to that envelope. A translucent or colored overlap image can reveal how the
envelopes interpenetrate but cannot, by itself, prove the extent of the exact
fractal intersection.

## A useful close-up

Use the symmetric focus
`(0.4565945963, 0.4565945963, 0.2228825445)` with roughly a 0.35–0.40 radius.
This surrounds the smaller Lantern E = `f04(K)`, whose center is
`(0.4693887547, 0.4438004380, 0.2228825445)` and whose conservative bounding-ball
radius is `1.35*r^2 = 0.2316233816`.

E contains vertices on both sides of P. Because E is connected, it contains
an actual point on P, hence an actual point shared by A and B. The existing
crossing certificate places this contact away from the intended octagonal
vertex join. This is a genuine meeting of the infinite sets, not only a
renderer effect. The argument does not identify the full contact trace or
prove an overlap region of positive area or volume.

The especially informative wrong-side vertex is

```
p = f04(v5) = (0.3373451064, 0.5444251993, 0.1795652974)
w(p)       = -0.1464277379
```

Its mirror gives the corresponding wrong-side vertex of B. Coloring these
two points makes the distinction between mirror correspondence and geometric
coincidence visible. Their projections in one camera can coincide while their
three-dimensional positions differ.

## Convergence screen

The finite clouds start from retained vertex v0, so every sample is an actual
attractor point up to floating arithmetic. For a complete depth-n cloud inside
A or B, the Hausdorff sampling error is at most `(1.35+1)*r^n`.

| Total word depth | Samples per piece | Hausdorff error | Sample distance from p to B | Distance lower screen |
|---|---:|---:|---:|---:|
| 5 | 4,096 | 0.0286543 | 0.0771997 | 0.0485455 |
| 6 | 32,768 | 0.0118690 | 0.0681392 | 0.0562703 |
| 7 | 262,144 | 0.0049163 | 0.0668091 | 0.0618928 |
| 8 | 2,097,152 | 0.0020364 | 0.0668091 | 0.0647727 |

The last column subtracts the sampling error from the sample distance. It is a
floating-point screen, not an independently rounded interval proof. The gap
is large enough to be a useful robust nomination for the separate certificate.

The fraction of this deterministic cloud on A's wrong side converges toward
about 12.7%. This is a fraction of sampled addresses, **not a volume fraction,
surface-area fraction, or proved exact invariant-measure value**. The image
should not describe it as a percentage of material.

## Reproducing the numerical screen

From the repository root, run:

```sh
python research/join-study/source/analyze_overlap.py
```

The script uses the unchanged [`math/model.py`](../../math/model.py) and writes
[`data/overlap-screen.json`](data/overlap-screen.json): coordinates, the depth
comparison, the reference hash and conservative bounding-ball contact screens.
It needs NumPy and SciPy, listed in this study's [requirements file](requirements.txt). The
largest depth uses 2,097,152 points per piece, so allow several hundred MB of
working memory. This publication version writes no large clouds or rendering
arrays. The independent exact proof is reproduced by
[`source/certify_interface.py`](source/certify_interface.py), which is much
lighter and needs only mpmath.

The [public visual study](../../docs/joins.md) includes a horizontal section
through the witness height `z=0.1795652974`. Its horizontal coordinate is
`u=(x+y)/sqrt(2)` and its normal coordinate is `w=(x-y)/sqrt(2)`. The shaded
regions are finite-thickness envelopes built from depth-eight samples, with
sampling error at most `e=0.0020364` in the unit-octagon coordinates.

If `d` is distance to the sample cloud, true set distance lies between
`max(0,d-e)` and `d`, apart from floating arithmetic. Therefore `d<=tau` is
inside the tau-thickened exact set, while `d>tau+e` is outside it. The band
between these bounds is unresolved by the samples. A close approach in the
section is not proof of exact contact at a specified grid coordinate.

The contact-ball screen remains as far as approximately 0.1163 from P at depth
eight. This is only an upper bound on where intersection might occur, and it
does not establish that any off-plane intersection actually occurs. Conversely,
it does not justify saying the entire exact intersection lies on P.

## What a clean interface would mean

A lossless ownership split takes the already combined exact set and assigns
each side to one owner. Its union remains K, including K's exact self-similarity.
The owned halves generally stop being full original miniature Lanterns. This
removes duplicate ownership without changing the external shape.

A geometric trim retains `A∩{w>=0}` and `B∩{w<=0}`. Their traces on P agree,
but this trim removes the distinct wrong-side geometry exemplified by p. It is
not merely deleting a duplicate. The companion certificate also excludes p
from the other six first-level pieces, so they cannot restore it. This changes
the original attractor and cannot remain the attractor of the same eight maps.

That does **not** mean all fractal character disappears. Uncut smaller copies
of K remain. It also does not rule out designing a different self-similar or
graph-directed construction. Matching on P alone does not prove a smooth
surface, a connected trimmed object, or a manufacturable solid interface.
