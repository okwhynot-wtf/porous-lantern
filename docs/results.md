# Results and evidence

The fixed Porous Lantern is connected, genuinely spatial and exactly self-similar. It has eightfold rotational symmetry and eight vertical mirror planes. Its eight first-generation pieces meet in a cycle, with additional contacts beyond the designed joining vertices. The central passage and several specified smaller passages are clear of the whole infinite attractor.

These conclusions combine analytic arguments with finite outward-interval checks. The checked premises are recorded in [verification.json](../math/data/verification.json) and can be rebuilt with [verify.py](../math/verify.py). This is a reproducible mathematical investigation, not independent peer review or proof-assistant formalization.

## What is established

| Statement | Evidence and scope |
| --- | --- |
| Exact self-similarity | The fixed eight-map equation; every word image is a similarity copy of the whole. |
| Connected and nonplanar | Retained endpoint joins, nested connected approximations, and an explicit point outside the octagon plane. |
| Eightfold rotation and eight vertical mirrors | Analytic symmetry identities. These give a dihedral subgroup of order 16; the complete isometry group is not classified here. |
| First-level contact graph is exactly an eight-cycle | Neighbours share retained vertices; complete ball covers separate all twenty non-neighbouring pairs by more than 0.01. |
| Adjacent intersections contain more than the planned vertex | A connected subcopy crosses the appropriate mirror plane more than 0.18 from the planned join. |
| Seven representative straight tubes are clear | Each has a complete finite cover certifying clearance from all of \(K\); rotations give further copies. |
| Noncontractible loops surround those axes | A continuous closed path in \(K\) has winding number one; apply the relevant similarity to obtain the smaller loops. |
| Zero ordinary volume | \(8r^3<1\), so volumes of finite enclosing covers tend to zero. |
| Dimension bounds | \(1\leq\dim_H K\leq\log(8)/\log(1+\sqrt2)\approx2.35932\). Equality at the upper bound is not established. |

All lengths below use the unit-octagon coordinates in [the definition](definition.md), before display normalization.

## Connectedness and spatial extent

The interval computation proves that the closed ball \(B=B(0,27/20)\) is invariant:

\[
|t_i|+r(27/20)<27/20\qquad (0\leq i<8).
\]

It contains the octagon vertices. Starting with \(C_0=B\), let \(C_{n+1}=\bigcup_i f_i(C_n)\). The sets are nested and compact. Each contains every \(v_i\), since \(f_i(v_i)=v_i\). If \(C_n\) is connected, its eight images are connected and consecutive images both contain \(v_{i+1}\). Therefore \(C_{n+1}\) is connected. Their intersection is \(K\), so \(K\) is connected and contains every retained vertex.

The retained octagon already contains three noncollinear points in \(z=0\). The actual attractor point \(f_0(v_1)\) has \(z<-1/100\), verified by intervals. Thus the affine span of \(K\) is all of \(\mathbb R^3\).

## Rotations and mirrors

Conjugation by \(G\) permutes the eight maps. Uniqueness of the compact attractor gives \(G(K)=K\).

Let \(H\) reflect in the vertical plane with horizontal angle \(\pi/8\), and let \(H_{\rm in}=G^2H\), the corresponding bisector reflection for the input chord. In the respective chord frames, both reflections have matrix \(\operatorname{diag}(-1,1,1)\). This commutes with the roll about the chord axis. The chord midpoints are fixed, giving

\[
HQ_0=Q_0H_{\rm in},\qquad Ht_0=t_0.
\]

Using \(HG^i=G^{-i}H\),

\[
Hf_i=f_{-i}G^{2i+2}H.
\]

The set \(H(K)\) is \(G\)-invariant, so this identity makes it an attractor for the original eight maps. Uniqueness gives \(H(K)=K\). The generated dihedral group supplies eight vertical reflection planes, spaced by \(\pi/8\).

In particular \(S=GH\) is reflection in \(x=y\), and

\[
S(f_i(K))=f_{1-i}(K).
\]

The numerical verifier checks interval residuals for these identities as an implementation check. An interval containing zero alone would not prove an identity; the frame argument above does that work.

## Which pieces meet

Each consecutive pair \(f_i(K),f_{i+1}(K)\) contains the common vertex \(v_{i+1}\). To exclude other contacts, every word image is enclosed by

\[
f_w(K)\subset B(t_w,r^{|w|}(27/20)).
\]

Rotation reduces all non-neighbouring pairs to separations 2, 3 and 4. For separation 2, the certificate tests every pair of second-level enclosing balls, 64 pairs in total. For separations 3 and 4, first-level balls suffice. In every case it proves

\[
|t_a-t_b|^2>
\left((r^{|a|}+r^{|b|})(27/20)+1/100\right)^2.
\]

The lists are checked as complete prefix covers of the paired address space. The result includes all descendants, rather than only a sampled point cloud. Thus the first-level contact graph has exactly eight edges and is an eight-cycle.

### More than a single joining point

Consider the connected subcopy \(E=f_{04}(K)\subset f_0(K)\) and signed distance \(\ell(x)=(x-y)/\sqrt2\). Two actual points satisfy

\[
\ell(f_{04}(v_5))<-0.14,\qquad
\ell(f_{04}(v_1))>0.18.
\]

Connectedness forces \(E\) to meet \(x=y\). Reflection \(S\) fixes any crossing point and exchanges \(f_0(K)\) with \(f_1(K)\); consequently that point belongs to both pieces. The additional inequality

\[
|t_{04}-v_1|>r^2(27/20)+0.18
\]

places the whole subcopy, and hence the crossing, more than 0.18 from the planned join \(v_1\). Rotation gives the same conclusion for every adjacent pair. The full intersection sets, their dimensions and their numbers of components remain unclassified.

## Clear passages

Let \(L\) be the entire vertical axis and \(L_w=f_w(L)\). Define the conservative radius

\[
\delta_w=(11/50)r^{|w|}.
\]

Each infinite cylinder of radius \(\delta_w\) around the following axes is disjoint from the entire \(K\):

| Word | Radius, approximately | Cover leaves | Deepest leaf |
| --- | ---: | ---: | ---: |
| root | 0.220000 | 8 | 1 |
| 0 | 0.091127 | 29 | 2 |
| 00 | 0.037746 | 50 | 3 |
| 01 | 0.037746 | 36 | 3 |
| 02 | 0.037746 | 50 | 3 |
| 05 | 0.037746 | 50 | 3 |
| 000 | 0.015635 | 148 | 6 |

Rotating by \(G^i\) adds \(i\) to every address digit, modulo eight. All such rotated counterparts are also certified. This covers all eight first-generation axes and selected deeper ones; it is not an all-generations theorem.

For an axis origin \(o\) and exact unit direction \(d\), every accepted word ball satisfies

\[
|(t_a-o)\times d|^2>
\left(r^{|a|}(27/20)+\delta_w\right)^2.
\]

The accepted words are prefix-free and form a complete address cover. They therefore bound every point of the infinite object. These radii are conservative guaranteed clearances, not measurements of the visible boundaries in a render.

### Why these axes pass through holes

Write \(h_i=f_iG^i=G^if_0\). Each \(h_i\) maps the same endpoints \(A=v_0,B=v_3\) to \(v_i,v_{i+1}\), and \(h_i(K)=f_i(K)\).

On the complete space of continuous paths from \(A\) to \(B\), concatenate \(h_0(\gamma),h_1(\gamma),h_2(\gamma)\), giving each one-third of the parameter interval. Endpoint matching makes this a continuous path operator with contraction factor \(r\) in the uniform metric. Its unique fixed path lies in \(K\): start with the straight segment in the invariant ball, and every successive iterate lies in the corresponding iterated full IFS cover, whose limit is \(K\).

Concatenate \(h_i(\gamma)\) for all eight indices to obtain a closed path through the octagon vertices. Each arc and its polygon edge lie in the same convex first-level enclosing ball. These balls avoid the central axis by the root certificate. Linear homotopy within the balls deforms the closed path to the regular octagon without crossing the axis, so its winding number is one. It cannot contract to a point inside \(K\).

For a certified word \(w\), its similarity image winds once around \(L_w\). Because the whole \(K\) avoids that axis, the smaller loop is also noncontractible in the whole object. Independence of these loop classes and the full homology of \(K\) have not been established.

### A copied hole need not retain its full clearance

At the same scaled radius \(\delta_w\), four other second-generation tubes contain explicit points of other first-level pieces:

| Axis | Point in \(K\) | Distance to axis, approximately |
| --- | --- | ---: |
| 03 | \(f_{10523}(v_5)\) | 0.035958 |
| 04 | \(f_{171670}(v_2)\) | 0.035477 |
| 06 | \(f_{733012}(v_3)\) | 0.035477 |
| 07 | \(f_{72745}(v_6)\) | 0.035958 |

All are strictly inside the nominal radius 0.037746. This proves intrusion into those particular tubes. It does not prove that the axis itself is blocked, that every narrower tube is obstructed, or that a curved route is impossible.

## Volume, dimension and the rendered surface

The \(8^n\) level-\(n\) enclosing balls have total volume proportional to \((8r^3)^n\), which tends to zero. Hence \(K\) has zero three-dimensional Lebesgue measure and empty interior. A metallic image is a finite-resolution visualization of this set, with a positive surface envelope.

The same cover gives

\[
\dim_H K\leq\frac{\log8}{\log(1/r)}
=\frac{\log8}{\log(1+\sqrt2)}\approx2.35932.
\]

Connectedness and the retained vertices make the projection of \(K\) onto the \(x\)-axis contain \([-1,1]\). A Lipschitz projection cannot increase Hausdorff dimension, so \(\dim_H K\geq1\). No separation condition sufficient to turn the similarity exponent into an equality has been proved here.

## Remaining questions

The exact Hausdorff dimension, complete adjacent intersection structure, full symmetry group, complete topology and a general rule for surviving descendant passages remain open in this investigation. Historical originality also remains open. None of these is needed to define the object, reproduce the images, or establish the specific geometric statements above.
