# Exact definition

Porous Lantern is a mirror-symmetric pair of spatial fractal pieces meeting on one plane. Its mathematical set is D, defined below. The solid appearance in the images comes from a finite rendering envelope; the exact set has zero three-dimensional volume.

## The displayed set

Let K be the auxiliary generating motif defined by the eight similarities in the next section. Write

\[
P=\{x=y\},\qquad
\ell(x,y,z)=\frac{x-y}{\sqrt2},\qquad
H_+=\{\ell\geq0\},\quad H_-=\{\ell\leq0\}.
\]

The two retained pieces and their union are

\[
D_+=f_0(K)\cap H_+,\qquad
D_-=f_1(K)\cap H_-,\qquad
\boxed{D=D_+\cup D_-}.
\]

**D is the artwork shown in the gallery and film.** K supplies its repeated detail and is a mathematical ingredient in this definition. The equation for K should not be read as a whole-object replacement rule for D.

Reflection \(S(x,y,z)=(y,x,z)\) exchanges the two retained pieces. Their traces on P match exactly, and they meet only on that plane. The [interface account](joins.md) explains this construction visually; [results](results.md) distinguish the proved properties from open questions.

## The generating similarities

Use a unit regular octagon in the horizontal plane:

\[
v_i=(\cos(i\pi/4),\sin(i\pi/4),0),\qquad G=R_z(\pi/4).
\]

Indices are modulo eight. Set

\[
a=v_0,\quad b=v_3,\quad u=v_0,\quad v=v_1,
\qquad r=\frac{|v-u|}{|b-a|}=\sqrt2-1.
\]

For a vector d with nonzero horizontal projection, define a right-handed orthonormal frame

\[
e_1=\frac{d}{|d|},\qquad
e_2=\frac{e_z\times e_1}{|e_z\times e_1|},\qquad
F(d)=[\,e_1\;e_2\;e_1\times e_2\,].
\]

With the standard right-handed rotation \(R_x\), put

\[
Q_0=F(v-u)R_x(\pi/6)F(b-a)^T,
\qquad
t_0=\frac{u+v}{2}-rQ_0\frac{a+b}{2}.
\]

The maps are

\[
f_0(x)=rQ_0x+t_0,\qquad
f_i=G^if_0G^{-i},\qquad 0\leq i<8.
\]

The 30-degree roll is about the reference chord direction before alignment. It is not a turn about the global vertical axis. The maps align the retained vertices:

\[
f_i(v_i)=v_i,\qquad f_i(v_{i+3})=v_{i+1}.
\]

There is a unique nonempty compact generating set

\[
K=\bigcup_{i=0}^{7}f_i(K).
\]

Existence and uniqueness follow from the contraction-IFS theorem. The construction uses the fixed L3-30 parameter values throughout: chord span three, 30-degree roll and ratio \(r=\sqrt2-1\). See [related work](related.md) for the mathematical context.

## Addresses and retained detail

Words are read from the outside inward: \(f_{04}=f_0\circ f_4\). A word w of length n gives

\[
f_w(x)=t_w+r^nQ_wx.
\]

The complete motif \(f_{00}(K)\) lies inside D, strictly on the positive side of the interface. All its descendants \(f_{00w}(K)\) lie in D too. Thus the visible detail has exact recursive structure at arbitrarily small scales.

One generation scales lengths by approximately 0.414214; the corresponding magnification is \(1+\sqrt2\approx2.414214\). These statements concern the retained generating motifs. A finite set of similarities which reconstructs the complete D from copies of D has not been established.

## Coordinates and numerical export

Mathematical distances use the unit octagon above. The renderer may apply the uniform display factor

\[
\lambda\approx1.7579924420999498.
\]

Uniform scaling preserves the clipping plane, reflection symmetry and topology. The authoritative definition is the exact formula for D and its generating maps. [reference.json](../math/data/reference.json) stores a numerical export of the maps; [exact.py](../math/exact.py) reconstructs them independently from rational constants and radicals.
