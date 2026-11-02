# Quantum Tanner codes

Last updated: 2026-11-02

A **quantum Tanner code** assigns physical data qubits to the squares of a specially connected network. At each vertex, small classical codes specify which nearby-in-the-network data qubits belong to an $X$ or $Z$ check. The network and local patterns are chosen together so that the checks commute and errors must spread over many qubits to become logical operators.

## Where are the physical qubits?

Think of a collection of square address labels, with **one data qubit per square**. A square has four corner vertices. At a vertex, collect the data qubits belonging to all squares meeting there; that collection is the vertex's local view.

The network used in the construction is called a **left-right Cayley complex**. Its squares arise because a left move and a right move reach the same endpoint in either order. The resulting network has two classes of vertices, with opposite corners of each square in the same class. One class hosts $X$-check patterns and the other hosts $Z$-check patterns.

A square here labels a single data qubit, not four qubits at its corners. A vertex labels a place to specify checks, not automatically one physical measurement ancilla. The network may have many squares at a vertex and generally cannot be laid out as an ordinary planar square lattice with all connections short.

## How does a vertex select a check?

At each vertex, the adjacent square labels can be indexed as a small array: one index for a left move and one for a right move. A binary **mask** selects entries in that array. A one means “include this physical qubit”; a zero means “leave it out.” At an $X$ vertex, the selected qubits receive $X$ operators; at a $Z$ vertex, they receive $Z$ operators.

The recipe chooses two short classical codes, $C_A$ and $C_B$, to specify allowed patterns in the two array directions. At $X$ vertices, use masks from their tensor code: columns follow $C_A$ and rows follow $C_B$. At $Z$ vertices, use the corresponding dual-code masks, with columns in $C_A^\perp$ and rows in $C_B^\perp$. A **dual code** contains masks having even overlap with every mask in the original code. Choosing bases for these local mask spaces supplies a bounded set of generating checks at each vertex.

Why does this produce commuting measurements? When an $X$ and a $Z$ neighborhood meet, their shared squares lie along a common row or column of their local arrays. The two masks restricted to that overlap belong to a classical code and its dual. They therefore share an even number of selected qubits, exactly the commutation rule needed for CSS checks. The geometry and masks work together. [Construction and commutation argument](https://arxiv.org/html/2202.13641v3#S2)

## What makes the long code good?

The number of squares meeting a vertex stays bounded as the overall network grows. The local arrays and selected generating masks stay bounded too. This keeps both check weight and the number of checks touching a data qubit bounded, satisfying the [qLDPC definition](../qldpc-codes/README.md#what-makes-a-code-qldpc).

A network is an **expander** when small regions have many connections out to the rest even though each vertex has only a fixed number of neighbors. Expansion prevents the construction from breaking into weakly connected pieces. The local codes also need distance and robustness properties: roughly, local row and column constraints must control errors consistently rather than letting their violations cancel in a misleading way.

With suitable expansion and robust local codes, quantum Tanner families have both $k$ and $d$ proportional to the number $n$ of data qubits. Sequential and parallel decoders have been proved to correct a linear number of arbitrary data errors in linear time and logarithmic parallel time, respectively, under the stated construction assumptions. These are mathematical decoding guarantees; noisy syndrome extraction and hardware timing require further analysis. [Decoding theorem](https://arxiv.org/abs/2208.05537)

The constant check weights can be substantially larger than familiar weight-four or weight-six checks. The construction's asymptotic parameters do not determine useful finite block sizes, a chip layout, or the overhead of logical gates. These are reasons to compare a specific implementation, rather than the family name alone.

## Is any Tanner graph a quantum Tanner code?

A **Tanner graph** is a drawing of check membership: one kind of node for data variables, another for checks, and an edge for each membership. Surface codes, bicycle codes, and HGP codes can all be drawn this way.

A **classical Tanner-code construction** builds a large code by enforcing small classical codes around vertices of a graph. The **quantum Tanner construction** uses two compatible versions of that idea on the square network described above. It is this recipe, including the compatibility and quality conditions, that gives the family its meaning. [Definitions](https://arxiv.org/abs/2202.13641)

The square networks are related to [balanced products](../balanced-product-codes/README.md), and the construction shares ingredients with good [lifted-product codes](../lifted-product-codes/README.md). These connections explain why the families overlap in the [qLDPC comparison](../qldpc-codes/README.md#how-do-the-main-recipes-compare).
