# Exact definition

Porous Lantern is the compact attractor of eight contracting similarities in three-dimensional Euclidean space. This edition fixes the original **L3-30** recipe: a regular octagon, a reference chord spanning three edges, a 30° roll and contraction ratio \(r=\sqrt2-1\). These parameters stay the same at every generation.

The mathematical object has zero ordinary three-dimensional volume. The images give it a finite surface envelope so its folds and passages can be seen. Geometry and display thickness are separate choices.

## The eight maps

Use a unit regular octagon in the horizontal plane:

\[
v_i=(\cos(i\pi/4),\sin(i\pi/4),0),\qquad G=R_z(\pi/4).
\]

Indices are taken modulo eight. Put

\[
A=v_0,\quad B=v_3,\quad U=v_0,\quad V=v_1,
\qquad r=\frac{|V-U|}{|B-A|}=\sqrt2-1.
\]

For a vector \(d\) with nonzero horizontal projection, form the right-handed orthonormal frame

\[
x=\frac{d}{|d|},\qquad
y=\frac{e_z\times x}{|e_z\times x|},\qquad
F(d)=[\,x\;y\;x\times y\,].
\]

With the usual right-handed rotation

\[
R_x(\beta)=
\begin{pmatrix}
1&0&0\\
0&\cos\beta&-\sin\beta\\
0&\sin\beta&\cos\beta
\end{pmatrix},\qquad \beta=\pi/6,
\]

define

\[
Q_0=F(V-U)R_x(\pi/6)F(B-A)^T,
\qquad
t_0=\frac{U+V}{2}-rQ_0\frac{A+B}{2}.
\]

The seed similarity and its seven rotated companions are

\[
f_0(x)=rQ_0x+t_0,\qquad
f_i=G^if_0G^{-i}.
\]

There is a unique nonempty compact set \(K\) satisfying

\[
K=\bigcup_{i=0}^{7}f_i(K).
\]

This is the original Porous Lantern. The general existence and uniqueness statement is the standard contraction-IFS theorem; see [related work](related.md).

Each map is a proper similarity and aligns two retained vertices:

\[
f_i(v_i)=v_i,\qquad f_i(v_{i+3})=v_{i+1}.
\]

The 30° roll is about the reference chord's direction before alignment. It is not a 30° turn about the global vertical axis. This distinction matters when rebuilding the object in another program.

## Addresses and scale

A word is read from the outside inward: \(f_{04}=f_0\circ f_4\). For a word \(w=i_1\cdots i_n\),

\[
f_w(x)=t_w+r^nQ_wx,
\qquad f_w(K)\subseteq K.
\]

Every such subset is an exact scaled and rotated copy of the whole. Overlap with neighbouring copies does not invalidate this identity. It can affect which copied openings remain clear in the entire parent object.

One generation reduces lengths by about 0.414214 and increases the camera magnification needed to recover the parent size by \(1+\sqrt2\approx2.414214\). Three generations correspond to \(7+5\sqrt2\approx14.071068\) times magnification.

The fixed point of \(f_0\) is \(v_0\). A continuous camera that follows its repeated address can use

\[
F_d(x)=v_0+r^dQ_0^d(x-v_0),
\]

where the fractional rotation uses a fixed axis-angle logarithm of \(Q_0\). At integer \(d=n\), this is exactly \(f_0^n\). At intermediate values it is a smooth camera path, not an assertion that the fractal is invariant under every fractional scale.

## Mathematical and display coordinates

All distances in [the results](results.md) refer to the unit octagon above. The frozen rendering export multiplies all coordinates by the positive constant

\[
\lambda\approx1.7579924420999498.
\]

This uniform display normalization changes neither symmetry nor topology. The authoritative definition is the exact formula above; the matrices in [the numerical reference](../math/data/reference.json) are a floating-point export of it. The [verifier](../math/verify.py) reconstructs the maps from rational numbers and radicals independently of that export.

## Relation to the planar construction

As a comparison only, setting the roll to zero gives \(Q_0=G^{-1}\). Rotational invariance then reduces the set equation to eight homotheties \(x\mapsto rx+G^it_0\), with

\[
t_0=(1/\sqrt2,\,1-1/\sqrt2,\,0).
\]

This connects the recipe to the established planar eight-gasket family. The published object here keeps the 30° roll and is nonplanar. See [the prior-art comparison](related.md); no historical priority is claimed.
