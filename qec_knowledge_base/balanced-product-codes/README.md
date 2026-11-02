# Balanced-product codes

Last updated: 2026-11-02

A **balanced product** uses a shared symmetry to decide which product addresses represent one physical data-qubit role. It applies the same rule to check labels and their connections. This can produce a smaller code than an ordinary product, while retaining a structured way to make commuting checks.

## Start with the addresses of the data qubits

In an ordinary product, pairing a label from one ingredient with a label from another creates a new address. If each ingredient has three indexed copies, one part of the product has nine possible addresses $(i,j)$, with $i,j\in\{0,1,2\}$.

Suppose the ingredients have a compatible cyclic symmetry. Consider the rule “increase the first index by one and decrease the second by one,” wrapping modulo three:

$$
(i,j)\longmapsto(i+1,j-1).
$$

Repeatedly applying this rule sorts the nine addresses into three groups:

| Group of product addresses | One final data-qubit role |
| --- | --- |
| $(0,0),(1,2),(2,1)$ | $Q_0$ |
| $(0,1),(1,0),(2,2)$ | $Q_1$ |
| $(0,2),(1,1),(2,0)$ | $Q_2$ |

Each group is an **orbit**: all the addresses reachable from one another by the symmetry. The final design assigns one physical qubit to the orbit. Here the invariant label is $i+j$ modulo three, which distinguishes the three rows of the table.

This happens while designing the code. We allocate three qubits for these three roles. There is no operation that merges nine already-encoded unknown qubits into three. This address example describes one component of a construction; it is not by itself a complete three-qubit quantum code.

## What happens to the checks?

A code is a list of checks and their data-qubit memberships. Grouping data addresses is only useful if the checks can be grouped consistently too.

The shared symmetry must preserve each ingredient's incidence pattern: whenever a bit belongs to a check, moving both labels by the symmetry must give another valid membership. In the product, it then moves an entire check and all its connections together. Check labels are collected into orbits just like data labels. A connection between the resulting check and data roles is computed from the original memberships, using parity if several contributions reach the same role.

This is why a symmetry of the checking structure matters. Choosing groups that merely look similar in a drawing does not provide the required compatibility. The balanced-product construction carries the commuting-check relation through this identification. Its formal description is a **quotient of a product**, meaning that symmetry-related labels are treated as one label. [Definition and check construction](https://arxiv.org/html/2012.09271v3#S4)

The word “balanced” refers to transferring a symmetry action between the two factors. In the cyclic example,

$$
(i+1,j)\sim(i,j+1),
$$

where $\sim$ means “the same final role.” Advancing the first factor or advancing the second gives equivalent addresses. This is the same identification as the opposite-shift rule used in the table.

## What is gained, and what must still be proved?

An ordinary product keeps both indices independently. A balanced product retains their relationship after the symmetry identification, which can substantially reduce the number of roles. It also changes the logical operators and constraints. The number of logical qubits and distance must therefore be established for the resulting code.

Breuckmann and Eberhardt's explicit construction achieves a logical count of order $n^{4/5}$ and distance at least of order $n^{3/5}$, where $n$ is the number of data qubits. The distance exponent exceeds the square-root behavior of standard good-seed HGP codes, but the rate $k/n$ of that construction decreases with size. Those exponents describe a particular proven family, not the definition of balanced product. [Explicit family and bounds](https://arxiv.org/abs/2012.09271v3)

The design needs ingredients with the required symmetry and expansion properties. Suitable block sizes can be restricted, connectivity need not be planar, and useful finite-size decoding and logical operations do not follow from taking the quotient.

## Why does lifted product sound similar?

For suitable free abelian symmetry actions, balanced and [lifted products](../lifted-product-codes/README.md) give the same construction. “Free” means a nonidentity symmetry does not leave a label fixed; “abelian” means the symmetry actions commute. The orbit description and the compact shift-matrix description then express the same connections. [Relationship](https://arxiv.org/html/2012.09271v3#S4.SS4.SSS3)

[Quantum Tanner codes](../quantum-tanner-codes/README.md) also use closely related square networks, but add a specific prescription for local check masks. The [family comparison](../qldpc-codes/README.md#how-do-the-main-recipes-compare) is therefore a map of related recipes, not a partition into unrelated code types.
