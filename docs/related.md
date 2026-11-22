# Related work

Porous Lantern combines established ideas: contracting similarities, polygonal symmetry, spatial chord alignment and selection by mirror half-spaces. The displayed set D uses a recursively generated motif K. Published results about a generating system do not automatically describe the topology or replacement rules of D.

The literature review below was carried out on **20 November 2026**. It establishes useful precedents, not historical priority for this artwork.

## The planar eight-gasket relative

Kevin G. Hare's *More Variations on the Sierpiński Sieve* studies overlapping regular-polygon gaskets, including an order-one eight-gasket with contraction ratio

\[
\lambda=\frac{1}{1+\sqrt2}=\sqrt2-1.
\]

Its construction is a close mathematical relative of the generating motif. See Section 2, equation (2.1), and the eight-gasket discussion in Section 4.2. [Hare (2010), paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3B573F6E4F1B54E1E112C8B4BAC5E43E/S0008414X00005277a.pdf/more_variations_on_the_sierpinski_sieve.pdf), [DOI](https://doi.org/10.4153/CJM-2010-036-3).

The following relation is a deduction from this project's equations, rather than a result claimed in Hare's paper. Setting the generating roll parameter to zero gives

\[
Q_i=G^{-1},\qquad t_i=G^it_0,\qquad
t_0=(1/\sqrt2,1-1/\sqrt2,0).
\]

Rotation invariance of that planar generating set reduces its equation to eight homotheties, \(x\mapsto rx+t_i\). The translations form a regular octagon, so uniform scaling and rotation identify it with the order-one eight-gasket.

Porous Lantern's definition uses a 30-degree spatial roll in the generating similarities and then the two mirror half-spaces defining D. It is not specified by folding a planar drawing. The planar gasket's dimension and overlap results therefore cannot simply be assigned to the displayed set. Its exact relation to K is the inclusion and dimension argument in [results](results.md).

## Iterated-function-system foundations

John E. Hutchinson's *Fractals and Self Similarity* supplies the existence, uniqueness and convergence framework for the auxiliary contracting IFS. Its separated-similarity dimension theorem also supports the four-map lower bound used here. [Hutchinson (1981), author's text](https://maths-people.anu.edu.au/~john/Assets/Research%20Papers/fractals_self-similarity.pdf), [DOI](https://doi.org/10.1512/iumj.1981.30.30055).

Those results establish the generating motif and the contained copies used in D. They do not, without further work, provide a finite IFS whose attractor is the complete displayed pair.

Christoph Bandt and Nguyen Viet Hung's *Fractal n-gons and their Mandelbrot sets* studies planar self-similar systems with cyclic rotational symmetry. It is relevant precedent for organizing generating maps by polygonal symmetry, while the present construction uses spatial rotations and explicit half-space selection. [Bandt and Hung (2008), DOI](https://doi.org/10.1088/0951-7715/21/11/009).

## Sculpture and finite approximations

Donald Plante's *3D Printable Golden Sponges* explores spatial IFS constructions and finite approximations for sculpture. It provides context for the distinction between a mathematical set and an object with physical thickness. [Bridges 2017 proceedings](https://archive.bridgesmathart.org/2017/bridges2017-451.html).

For Porous Lantern, the exact set has zero volume. Its metallic envelope, the topology of the exact set and the requirements of a printable solid are different questions. The images establish an appearance; the mathematical evidence supports only the properties listed in [results](results.md).

## Scope of the review

The review covered selected mathematical IFS literature and computational-art sources, following promising references to papers and author or publisher records. It was not an exhaustive search of unpublished experiments, unindexed artwork or differently normalized map descriptions.

The appropriate description is a documented spatial fractal artwork with a known planar generating relative and reproducible mathematical evidence. No claim of being the first such object or of establishing a new mathematical family is made. Comparisons capable of settling priority would need to examine the exact maps and retained sets, not only their names or images.
