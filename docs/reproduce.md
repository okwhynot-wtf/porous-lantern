# Reproduce the geometry

The displayed geometry is the two-piece set D in the [definition](definition.md). Its construction has two stages: generate the recursive motif K, then retain the prescribed half-space of each placed piece. Rendering adds a finite surface envelope after that geometric definition.

## Run the mathematical checks

From the repository root, with the project's Python requirements installed:

```sh
python -m pip install -r requirements.txt
python math/verify.py --receipt .build/verification.json
python research/join-study/source/certify_interface.py
```

[exact.py](../math/exact.py) reconstructs the generating similarities from rational constants and radicals using 60-decimal-digit outward interval arithmetic. The generating-map checks establish contraction, the invariant ball, spatial extent, mirror identities, complete separation covers and selected clear axes.

The interface check establishes the premises used specifically for D: generating coordinates, a connected motif crossing the shared plane, and a complete word-00 motif whose enclosing ball lies strictly inside the retained half-space. The [results](results.md) give the analytic arguments and identify which conclusions concern the displayed set.

The source inputs include [the numerical reference](../math/data/reference.json) and [finite certificate covers](../math/data/covers.json). Prefix-free, complete covers bound every address of the infinite generating set. They are not nearest-neighbour tests on sampled points.

The checks emit receipts with source/input hashes, arithmetic precision and numerical diagnostics. The readable decimal diagnostics are not certified interval endpoints; the internal outward interval comparisons carry the strict inequalities. Some identities require the analytic chord-frame argument: an interval which merely contains zero is not a proof of exact equality.

## A numerical point sample of D

This Python example uses the included mathematical package. It samples K, places the positive-side piece, applies its half-space condition and reflects the retained sample to produce the other half:

```python
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, "math")
from model import R, Q, T, points

motif = points(5)
placed = R * motif @ Q[0].T + T[0]
positive = placed[placed[:, 0] >= placed[:, 1]]
negative = positive[:, [1, 0, 2]]
lantern = np.concatenate([positive, negative])

Path(".build").mkdir(exist_ok=True)
np.savetxt(".build/porous-lantern.csv", lantern,
           delimiter=",", header="x,y,z", comments="")
```

Coordinates use the unit octagon. Floating arithmetic approximates the exact points and plane test. This sample is useful for inspection and import into other programs; it does not certify the seam or connectivity.

For the complete depth-n generating sample, the geometric Hausdorff bound is \((27/20+1)r^n\). That bound **does not automatically transfer through the half-space filtering**: samples close to the clipping boundary can be discarded even when nearby points of the exact retained set remain. Coverage of the displayed sample needs its own analysis.

## Render and record

The [media page](media.md) describes the current stills, film and TouchDesigner project. Rendering evaluates the same retained pieces; shading and envelope thickness affect their appearance without changing the defining half-spaces.

The film pipeline records a fixed sequence of cooked TouchDesigner TOP frames. Its media receipt records the export settings and output metadata. Mathematical certification is independent of the raster output: neither successful movie encoding nor a continuous-looking surface establishes topology.

## Build the website

The website is generated from these documents and the current media manifest:

```sh
python -m pip install -r site-requirements.txt
python scripts/build_site.py
```

The build checks local pages, image paths and internal links. [Provenance](provenance.md) records authorship, assistance and reuse terms.
