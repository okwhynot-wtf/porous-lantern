# One Lantern join: matching seam, genuine interleaving

The two pieces are mirror partners and their traces on the mirror plane match **exactly**. Cutting each piece back to its own side gives a single shared interface. However, this removes some genuine Lantern geometry; it does more than delete duplicate points. The cut version still contains complete, exact copies of the original Lantern at every smaller scale. What it loses is the original eight-map equation for its **whole shape**, not all fractal structure.

This study changes no original recipe or reference asset. All lengths below use the unit-radius retained octagon, before display normalization. The calculations use the original L3-30 construction, with ratio `r = sqrt(2) - 1`.

## The proposed interface

Let `K` be the unchanged infinite Lantern, `A = f_0(K)` and `B = f_1(K)`. Set

```text
P = {(x,y,z): x=y}
ell(x,y,z) = (x-y)/sqrt(2)
H+ = {ell >= 0}; H- = {ell <= 0}
A+ = A intersect H+; B- = B intersect H-
D = A+ union B-
C = D union f_2(K) union ... union f_7(K)
```

`D` is the edited pair. `C` replaces just that pair in the original Lantern and leaves the other six pieces unchanged. This is a local experiment: it does not restore all eightfold symmetries or classify every other join.

Reflection `S(x,y,z) = (y,x,z)` exchanges `A` and `B`. Since it fixes every point of `P`,

```text
A intersect P = B intersect P
A+ intersect B- = A intersect P
```

The clipped pieces are therefore disjoint away from the plane and have precisely the same boundary trace on it. This is an exact matching **set** on a plane. It does not establish a smooth surface, matching tangents, a continuous seam curve, connected clipped pieces, or a manufacturable solid. The infinite Lantern itself has zero ordinary three-dimensional volume; a rendered solid is an envelope of it at a specified resolution and thickness. Adding a filled cap to a rendered cut is another geometric operation and is not part of this definition.

The mirror identity comes from the unchanged recipe's chord-frame construction. If `G` rotates by pi/4 and `H` reflects about the vertical plane at pi/8, the chord frames give `H Q_0 = Q_0 G^2 H` and `H t_0 = t_0`. Conjugating the maps gives `H f_i = f_(-i) G^(2i+2) H`. Rotation invariance and uniqueness of the compact IFS attractor give `H(K)=K`, hence `S=GH` sends `f_i(K)` to `f_(1-i)(K)`. The script checks residual intervals as a consistency check; residuals containing zero alone are not the proof of an exact identity.

## A piece which really does extend under the other side

Consider the exact attractor point `p = f_04(v_5)`. The retained vertex `v_5` lies in `K`, so this is a genuine point of `A`, not a mesh vertex invented by rendering. Its approximate coordinates are

```text
p = (0.33734511, 0.54442520, 0.17956530)
ell(p) = -0.1464277379
```

The outward-interval certificate establishes two strict bounds:

* `ell(p) < -0.14`: the point lies on the side discarded from `A`.
* `distance(p, f_j(K)) > 0.06` for **every** `j=1,...,7`: no other original piece supplies the same point, including the mirrored partner `B`.

Consequently `p` belongs to `K` and does not belong to `C`. It is distinct geometry, not an exactly duplicated layer. Reflection gives the corresponding distinct point in `B` on the side discarded from `B`.

The result is stronger than one missing point. Because `f_5(v_5)=v_5`, the whole miniature Lantern `f_04555(K)` lies within

```text
(27/20 + 1) r^5 < 0.03
```

of `p`. Every point of that miniature lies below `ell=-0.11` and more than `0.03` from every other first-generation piece. Thus **an entire exact miniature Lantern is removed** by this cut.

There are also genuine contacts which the cut retains. The connected subcopy `f_04(K)` contains points with `ell < -0.14` and `ell > 0.18`, so it crosses `P`. Every such crossing is shared by `A` and `B`. A separate interval bound places this entire subcopy more than `0.18` from the prescribed join vertex `v_1`. The seam therefore includes more than the original planned vertex. The full intersection set remains unclassified; this study does not establish that every shared point lies on `P`.

## Precisely which self-similarity survives

The edited set is a nonempty compact proper subset `C` of `K`. The original eight contracting similarities have only one nonempty compact fixed set, `K`. Therefore

```text
C != union_i f_i(C)
```

for those original maps. The uniqueness theorem is [Hutchinson (1981), Section 3.1(3)](https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf). Reapplying the unchanged recipe to the edited whole cannot reconstruct that same edited whole.

Nevertheless, the entire copy `f_00(K)` survives: its enclosing ball is strictly inside `A`'s retained halfspace, with `ell > 0.36`. Every descendant `f_00w(K)` survives too. An arbitrarily deep zoom into this surviving copy therefore encounters the original exact Lantern structure. This is a statement about contained copies, not a promise that every camera crop is an isolated copy without neighbouring geometry.

This also gives an exact dimension result, even though the numerical value of the original Hausdorff dimension remains unknown:

```text
f_00(K) subset D subset C subset K
dim_H(D) = dim_H(C) = dim_H(K)
```

Similarity preserves Hausdorff dimension, and inclusion is monotone for that dimension. The removed set also has the same dimension, since it contains `f_04555(K)` and is a subset of `K`. Equal dimension does not mean equal appearance, equal connectivity, or the same global replacement rule.

So the accurate distinction is: **the proposed seam keeps fractal copies and the original fractal dimension, while changing the whole object's original self-similarity equation.** It has not been proved impossible for the edited object to have some different exact IFS.

## The lossless alternative

There is a different way to make each point belong to one side without changing the Lantern at all:

```text
J = A union B
J+ = J intersect H+; J- = J intersect H-
J = J+ union J-
```

This simply reassigns ownership. The portion of `A` under the plane becomes part of `J-`, instead of being deleted. The whole Lantern remains `K` and keeps its exact original eight-map self-similarity. The two newly assigned parts are no longer the original `A` and `B`. Since the occupied geometry has not changed, this operation alone cannot smooth away a visible ledge or recess in that geometry.

Likewise, counting an exactly shared point once instead of twice changes no union geometry. A set union already counts it only once.

## Could a new construction repeat the clean join at every scale?

That remains a reasonable design direction, but this local cut does not supply such a construction. A one-time planar crop introduces a boundary condition that descendants encounter at different positions and orientations. Repeating a clipping instruction is not, by itself, a proof of an ordinary self-similar IFS.

A finite graph-directed construction would need a finite collection of boundary types and exact replacement rules showing that their transformed boundaries close among those types. No such finite closure is established here. The next design step would be to formulate those seam-compatible building blocks explicitly, then test and prove their recursion. This study neither proves nor rules out that possibility.

## Reproduction and scope of the certificate

Run from the repository root (the script also works with an absolute path from any directory):

```powershell
python research/join-study/source/certify_interface.py
```

The script reads [`math/exact.py`](../../math/exact.py), reconstructing the maps from rational constants and radicals with 60-digit outward interval arithmetic. It rechecks the invariant ball of radius `27/20`. Every word image is contained in a ball of radius `(27/20) r^length(word)` around its translation.

For each other first-generation piece, the script adaptively subdivides its entire address space until every enclosing ball satisfies

```text
|p-c_word|^2 > ((27/20) r^length(word) + 3/50)^2.
```

The accepted leaves are checked to form a complete prefix cover. Thus the clearance statement concerns the whole infinite piece, not a finite point cloud. Piece `B` requires 78 leaves, with maximum word length 5; each of the other six pieces is excluded by its first-level enclosing ball.

The receipt is [data/interface-certificate.json](data/interface-certificate.json). It records every cover leaf, rational bounds, readable numerical diagnostics, input hashes and the verifier hash. The original input hashes are checked again before writing. Binary-float diagnostics are not certified decimal bounds; the rational inequalities and interval checks carry the certificate. The analysis combines these finite inequalities with the analytic arguments above; it is not independent peer review or proof-assistant formalization.
