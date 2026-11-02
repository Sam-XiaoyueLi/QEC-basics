# Lifted-product codes

Last updated: 2026-11-02

A **lifted-product (LP) construction** produces physical data qubits and their $X/Z$ check memberships from small templates containing connection instructions. A template label expands into several indexed labels, and each connection instruction specifies which copies connect. Combining the templates in a compatible way makes the resulting quantum checks commute.

## What does a lift do to a connection?

Take one design connection between a check label $c$ and a bit label $a$. Make three copies of each label. An unshifted connection would produce $c_0$–$a_0$, $c_1$–$a_1$, and $c_2$–$a_2$. A one-step cyclic shift instead produces:

$$
c_0\longleftrightarrow a_1,\qquad
c_1\longleftrightarrow a_2,\qquad
c_2\longleftrightarrow a_0.
$$

Each check copy still gets one connection from this template edge. The instruction changes its endpoint. This is a **permutation matching**: every copy on one side is matched to exactly one on the other. Erasing the copy indices recovers the original edge.

The copied objects are labels in a design. Once the full quantum construction is expanded, distinct data-qubit labels correspond to distinct physical qubits. Lifting does not copy an unknown quantum state.

## What makes it a lifted product?

An ordinary [hypergraph product](../hypergraph-product-codes/README.md) makes physical-qubit addresses from pairs of seed labels. If both seeds have already been expanded with $L$ copies, their ordinary product carries two independent copy indices and can grow as $L^2$.

A cyclic lifted product works with the compact templates first. Its entries say “no connection,” “connect with this cyclic shift,” or a sum of such shifts. The product combines these entries while retaining **one shared lift index**. Expanding that index gives the actual data qubits and check connections. For fixed template dimensions, the block size then grows as $L$.

That comparison concerns the number of design labels. Whether the smaller construction retains useful logical qubits and distance depends on the templates and shifts. It is not a way to compress an arbitrary existing quantum state.

The compatibility is essential. In a cyclic construction, composing a shift by $s$ with a shift by $t$ has the same result in either order: a shift by $s+t$ modulo $L$. The product recipe uses this agreement to cancel the two contributions to every $X$–$Z$ overlap, together with the appropriate transposes/reversed connections. Arbitrary permutation matrices need not commute. More general nonabelian LP constructions use compatible left and right actions rather than assuming every permutation commutes. [Lifted-product construction](https://arxiv.org/html/2012.04068)

## Why is this useful?

Lifts offer ways to connect repeated templates without paying the full size of an ordinary product of expanded seeds. The choices can change short logical operators and the relationship between rate and distance. Panteleev and Kalachev proved that suitable nonabelian lifted-product families are **asymptotically good**: both the logical count $k$ and distance $d$ grow proportionally to the number $n$ of data qubits. [Good qLDPC construction](https://arxiv.org/abs/2111.03654)

This result does not apply to every small cyclic template. A poor choice may give disconnected components or short logical operators. Even a successful asymptotic construction must be assessed at feasible sizes: check weights have constant factors, the requested connections can be nonlocal, and decoding and fault-tolerant logical gates need their own protocols.

## How does this relate to balanced products and bicycle codes?

[Balanced products](../balanced-product-codes/README.md) describe a related idea through a symmetry of the product labels. For suitable free abelian actions—nonidentity symmetries fix no labels, and the symmetry actions commute with one another—the two descriptions coincide. LP emphasizes compact connection matrices; balanced product emphasizes which product addresses represent the same final role. [Precise relationship](https://arxiv.org/html/2012.09271v3#S4.SS4.SSS3)

[Generalized bicycle codes](../bicycle-codes/README.md) are a particularly compact part of the product landscape, using two equal-sized data blocks and two commuting connection recipes. They provide a concrete entry point into shift-based check design without requiring a full general LP construction.
