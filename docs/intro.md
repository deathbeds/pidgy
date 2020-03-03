[Fernando Perez], creator of [`IPython`], wrote an essay titled ["Literate computing" and computational reproducibility]. He defines the [Literate Computing] workflow as weaving narrative directly into live computation. Meanwhile, [Literate Programming] refers to complete programs that to double as literate about computational thinking. This work explores the overlapping features of [Literate Computing] and [Literate Programming] that allow for the co-development of interactive computational thought to implicitly mature to readable, reusable, and reproducible literature.

![](literate_computing_venn.jpeg)

[Literate Programming] and [Literate Computing] shine light on perspectives on computational thinking as documentation tools for the program and computation, respectively. From [Literate Programming], we focus combining narrative and code to communicate human and machine logic. [Literate Computing] considers introduces informal rich display, derived from live computation, that can enrich as computational narrative.

![](tangle_weave_diagram.svg)

`pidgy` is consistent with [Literate Programming] by defining tangle and weave steps, and it goes further to formalize testing while interactively developing computational literature. The original 1979 `"WEB"` implementation chose Tex and PASCAL, and this `pidgy` implementation chooses [Markdown] and [Python].

![](pidgy_literate_computing.jpeg)

Throughout this work we'll design a purpose built interactive literate computing interface. This work is interested in designing an interactive experience that results in multi-objective computational documents that are readable, reusable, and reproducible over longer timelines than single use notebooks and programs.

["literate computing" and computational reproducibility]: http://blog.fperez.org/2013/04/literate-computing-and-computational.html
[tools for the life cycle of a computational idea]: https://sinews.siam.org/Details-Page/jupyter-tools-for-the-life-cycle-of-a-computational-idea
