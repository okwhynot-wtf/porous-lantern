# Results and evidence

These results concern the displayed Porous Lantern set

\[
D=(f_0(K)\cap\{x\geq y\})\cup(f_1(K)\cap\{y\geq x\}).
\]

K is the auxiliary generating motif from the [definition](definition.md). Properties of K are used below only when an explicit argument transfers them to D.

## What is established

| Property of D | Evidence and scope |
| --- | --- |
| Mirror symmetry | Reflection \(S(x,y,z)=(y,x,z)\) exchanges the two retained halves. |
| An exact shared interface | The halves meet precisely on their identical traces in \(x=y\). |
| Actual seam contacts | The trace contains the retained vertex \(v_1\) and at least one additional contact more than 0.18 units away. |
| Exact recursive detail | The complete motif \(f_{00}(K)\), and every descendant within it, is contained in D. |
| Genuinely spatial geometry | That retained motif has three-dimensional affine span. |
| Hausdorff dimension | \(\dim_H D=\dim_H K\); the numerical value remains unresolved. |
| Zero ordinary volume | D is a subset of K, and \(8r^3<1\) forces K to have zero three-dimensional volume. |

Connectivity of D, the full structure of its interface and a finite whole-object IFS description are **not established**. A continuous-looking metallic surface does not settle those questions.

The evidence combines analytic arguments with finite outward-interval checks. It is reproducible mathematical research, not proof-assistant formalization or independent peer review. All distances below use the unit-octagon coordinates.

## Why the traces match

Conjugation by \(G=R_z(\pi/4)\) permutes the generating maps, so uniqueness gives \(G(K)=K\). Let H reflect in the vertical plane at angle \(\pi/8\). The chord-frame construction gives

\[
HQ_0=Q_0G^2H,\qquad Ht_0=t_0.
\]

These identities imply

\[
Hf_i=f_{-i}G^{2i+2}H.
\]

Using rotation invariance and uniqueness again gives \(H(K)=K\). Therefore \(S=GH\), the reflection in \(x=y\), satisfies

\[
S(f_i(K))=f_{1-i}(K).
\]

In particular S exchanges the two generating pieces used in D and swaps the retained half-spaces. Hence \(S(D)=D\), and

\[
(f_0(K)\cap H_+)\cap(f_1(K)\cap H_-)=f_0(K)\cap P=f_1(K)\cap P.
\]

The algebra proves the identity. Numerical residual intervals containing zero are consistency checks, not substitutes for that argument. No larger symmetry group is claimed for D.

## The seam contains more than a prescribed vertex

The generating motif K is connected. One way to see this is to iterate its map union on the invariant ball of radius \(27/20\): each stage is connected, the images retain their cyclic endpoint contacts, and the nested compact stages converge to K.

Consequently \(E=f_{04}(K)\) is connected. Two retained points have signed distances to P satisfying

\[
\ell(f_{04}(v_5))<-0.14,\qquad
\ell(f_{04}(v_1))>0.18.
\]

E therefore crosses P. Each crossing is fixed by S and belongs to both generating pieces, so it survives in the displayed interface. A separate enclosing-ball inequality places all of E more than 0.18 from \(v_1\), establishing an additional contact.

This argument proves that the common trace is nontrivial. It does not prove that either retained half, or their union D, is connected. Different components could carry different contacts.

## A complete motif survives the half-space selection

Every word image has the certified enclosure

\[
f_w(K)\subset B(t_w,r^{|w|}(27/20)).
\]

For the address 00, the entire enclosing ball has \(\ell>0.36\). Thus

\[
f_{00}(K)\subset D\subset K.
\]

All \(f_{00w}(K)\) are present as well. The maps of K are genuine spatial similarities: retained vertices give three noncollinear points in a plane, and a certified additional point lies outside it. The retained copy therefore gives D three-dimensional affine span too.

Similarity invariance and monotonicity of Hausdorff dimension now yield

\[
\dim_H K=\dim_H f_{00}(K)\leq\dim_H D\leq\dim_H K.
\]

This proves equality without knowing its exact numerical value.

## Dimension and volume

The four generating images with indices 0, 2, 4 and 6 are pairwise separated by more than 0.01. Their four-map subsystem lies inside K and satisfies strong separation, giving the lower bound

\[
\frac{\log4}{\log(1+\sqrt2)}
\leq\dim_H D
\leq\frac{\log8}{\log(1+\sqrt2)},
\qquad
1.5728794\lesssim\dim_H D\lesssim2.3593191.
\]

The upper bound comes from the eight-map similarity cover. The lower-bound subsystem uses the same non-neighbour separation certificates checked by the verifier. The separated-IFS dimension formula is standard; see [Hutchinson (1981), Section 5.3](https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf). Equality at the upper bound is not established.

At depth n, the eight-map cover consists of \(8^n\) balls with radii proportional to \(r^n\). Their total volume tends to zero because \(8r^3<1\). Hence K, and therefore D, has zero three-dimensional Lebesgue measure and empty interior. The rendered surface has finite thickness and is a separate display approximation.

## A selected clear axis

The line \(L_{00}=f_{00}(\{(0,0,z):z\in\mathbb R\})\) has an entire cylindrical neighbourhood of radius

\[
\delta_{00}=\frac{11}{50}r^2\approx0.037746
\]

which misses K, and therefore misses D. The interval check covers the whole infinite generating set. This is a certified clearance associated with the retained motif; it is not a measurement of the visible edge in a render or a claim about every apparent opening.

## Verification and open questions

The generating-map verifier reconstructs the exact radicals, checks the invariant ball and complete separation covers, and supplies the ingredients used above. The interface verifier checks the retained-copy enclosure and seam-crossing inequalities. See [reproduction](reproduce.md) for commands and evidence files.

A finite collection of similarities generating all of D has not been established. The complete seam topology, connectedness of D, exact dimension, full symmetry group, and smoothness or manufacturability of a thickened approximation remain open. Historical priority is addressed separately in [related work](related.md).
