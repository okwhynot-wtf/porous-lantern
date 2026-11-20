# Related work

Search updated **20 November 2026**.

Porous Lantern uses established ideas: contracting similarities, polygonal symmetry, and endpoint matching. The closest identified construction is a planar eight-gasket studied by Kevin G. Hare. It has the same contraction ratio, and the Lantern's zero-roll control reduces to it. The fixed **30-degree spatial Lantern** is a different, nonplanar attractor. The sources examined did not identify that exact spatial recipe; this is a bounded search result, not a claim of historical originality.

## A known planar parent

Hare's *More Variations on the Sierpiński Sieve* studies overlapping regular-polygon gaskets, including an order-one eight-gasket with contraction ratio

\[
\lambda=\frac{1}{1+\sqrt2}=\sqrt2-1.
\]

Its adjacent pieces have additional overlaps, which the paper analyses using smaller copies. This is a much closer precedent than a general resemblance to a sponge. See the construction in Section 2, especially equation (2.1), Figures 3 and 7, and the eight-gasket discussion in Section 4.2. [Hare (2010), paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3B573F6E4F1B54E1E112C8B4BAC5E43E/S0008414X00005277a.pdf/more_variations_on_the_sierpinski_sieve.pdf), [DOI](https://doi.org/10.4153/CJM-2010-036-3).

The following comparison is a deduction from our [definition](definition.md), rather than a claim made in Hare's paper. Temporarily set the roll to zero while retaining the unit octagon and the chord rule. With \(G=R_z(\pi/4)\), the matrices become

\[
Q_i=G^{-1},\qquad
t_i=G^it_0,\qquad
t_0=(1/\sqrt2,\ 1-1/\sqrt2,\ 0).
\]

The resulting planar attractor \(K_0\) is invariant under \(G\). Consequently

\[
K_0=\bigcup_{i=0}^{7}(rG^{-1}K_0+t_i)
   =\bigcup_{i=0}^{7}(rK_0+t_i).
\]

The translations form a regular octagon, so rotation and uniform scaling identify this with Hare's order-one eight-gasket. Thus the planar endpoint construction and its ratio are already represented in the literature. The released object keeps the 30-degree roll: its rotations leave the plane, and the planar dimension and overlap results do not transfer to it. This comparison does not change the released recipe.

## Other mathematical precedents

| Source | Relation to Porous Lantern | Scope of the comparison |
| --- | --- | --- |
| John E. Hutchinson, *Fractals and Self Similarity* (1981), Indiana University Mathematics Journal 30, 713–747. [Author's text](https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf), [DOI](https://doi.org/10.1512/iumj.1981.30.30055). | The contraction-IFS framework supplies the unique compact attractor and convergence of finite approximations. Section 3.5 treats endpoint-coupled parametrised curves. | These foundations are established mathematics. A rendered finite approximation is distinct from the infinite attractor. |
| Christoph Bandt and Nguyen Viet Hung, *Fractal n-gons and their Mandelbrot sets* (2008), Nonlinearity 21, 2653–2670. [Paper](https://citeseerx.ist.psu.edu/document?doi=6dfa144d60e222dc88aa39515b735d00efb3c882&repid=rep1&type=pdf), [DOI](https://doi.org/10.1088/0951-7715/21/11/009). | Studies planar self-similar sets whose pieces are permuted cyclically by rotation. This is a direct precedent for constructing and exploring fractals by polygonal symmetry. | The Lantern uses spatial rotations; it is outside the paper's planar family. |
| V. V. Aseev, A. V. Tetenov and A. S. Kravchenko, *On Selfsimilar Jordan Curves on the Plane* (2003), Siberian Mathematical Journal 44, 379–386. [Publisher and DOI](https://doi.org/10.1023/A:1023848327898). | The endpoint-coupling method is known as a self-similar zipper. The Lantern's auxiliary path construction uses this kind of matching rule. | Endpoint matching alone does not establish that the resulting path is a Jordan arc. We make no such claim for the Lantern. |
| Fan Wen, *Fractal necklaces with no cut points* (2021 preprint; 2022 journal article), Fractals 30, 2250091. [Author's preprint](https://arxiv.org/abs/2105.00407), [definition in full text](https://arxiv.org/html/2105.00407), [DOI](https://doi.org/10.1142/S0218348X22500918). | Studies cyclic arrangements of connected fractal pieces and their topology. | Definition 1 requires each neighbouring pair to meet in exactly one point. Our verified extra contacts violate that condition for the displayed eight-map IFS. Its necklace theorems therefore do not establish the Lantern's topology. |

“Necklace” is useful informal language for the Lantern's cycle of eight pieces. It should not be read as membership in Wen's narrower class for this IFS. Neither the cycle graph nor a pleasingly continuous rendering determines the full intersection sets. See [results and limits](results.md).

## Solid appearance and physical approximations

Donald Plante's *3D Printable Golden Sponges* explores spatial IFS constructions in which suitable overlap makes finite approximations printable. It provides relevant context for treating an IFS as a sculpture, although it does not identify the Lantern's maps. [Bridges 2017 proceedings, pp. 451–454](https://archive.bridgesmathart.org/2017/bridges2017-451.html).

For Porous Lantern, the infinite attractor has zero three-dimensional volume. The metallic surface in the gallery is a finite rendering envelope. A pleasant solid appearance, a watertight printable approximation, and a positive-volume mathematical solid are separate properties; this release establishes the first and documents the exact zero-volume set.

## What this search establishes

The search covered mathematical IFS literature and selected computational-art sources using combinations of *octagonal*, *eightfold*, *gasket*, *necklace*, *zipper*, *spatial*, *twist*, *chord*, and the ratio \(\sqrt2-1\). It followed promising results to papers or author/publisher records. The [search ledger](../research/prior-art-search.json) records queries, sources, and exclusions.

No inspected source supplied the full combination of the eight conjugate spatial maps, the skip-three-to-next-vertex chord rule, and a 30-degree roll. This leaves the exact recipe's historical status unresolved. Unindexed artwork, differently normalised IFS descriptions, and unpublished experiments remain outside the search. A convincing match would require comparing transformations or attractors up to similarity and internal symmetry, rather than comparing names or pictures alone.

The appropriate description is **a documented spatial fractal study with a known planar relative**, accompanied by reproducible definitions and evidence. “First”, “unique”, and “new mathematical family” are not claims of this release.
