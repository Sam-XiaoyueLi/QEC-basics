# Hypergraph-product codes

Last updated: 2026-11-02

A **hypergraph-product (HGP) code** specifies data qubits and commuting $X/Z$ checks by combining two classical parity-check blueprints. Its useful feature is that it builds commutation into the recipe: wherever an $X$ check and a $Z$ check meet, their shared data qubits come in pairs. It is one construction within the [qLDPC family map](../qldpc-codes/README.md#how-do-the-main-recipes-compare).

## How can five data qubits illustrate the recipe?

Start with four physical data qubits arranged as addresses in a square:

| | First column | Second column |
| --- | --- | --- |
| First row | $q_1$ | $q_2$ |
| Second row | $q_3$ | $q_4$ |

Suppose we want $X$ checks down columns and $Z$ checks across rows. The first column and first row share only $q_1$. Because $X_1Z_1=-Z_1X_1$, those two checks anticommute. They cannot both be stabilizer constraints.

Add a fifth **data qubit**, $q_5$, and include it in all four checks:

| Check | Operator |
| --- | --- |
| First column, $X$ | $X_1X_3X_5$ |
| Second column, $X$ | $X_2X_4X_5$ |
| First row, $Z$ | $Z_1Z_2Z_5$ |
| Second row, $Z$ | $Z_3Z_4Z_5$ |

Now every column–row pair overlaps on its original intersection and on $q_5$. The two minus signs cancel. All checks commute. Measurement ancillas would be additional qubits; $q_5$ is part of the encoded block.

The four checks are independent, so they leave $5-4=1$ logical qubit. The distance is two: for example, $X_1X_2$ commutes with every check but is not a stabilizer. Every single-qubit Pauli is detected. Thus this is a $[[5,1,2]]$ code, which detects a single-qubit error but cannot correct an arbitrary one. The familiar perfect five-qubit code has different checks and distance three.

## Where did those two sets of data qubits come from?

The ingredients here are two classical two-bit repetition blueprints. The first has labels $a_1,a_2$ and a parity rule $c$ saying that the bits agree. The second has $b_1,b_2$ and an agreement rule $d$. A classical blueprint supplies bit labels, check labels, and which bits belong to each check.

HGP assigns one physical data qubit to each bit–bit pair and each check–check pair:

$$
q_1=(a_1,b_1),\quad q_2=(a_1,b_2),\quad
q_3=(a_2,b_1),\quad q_4=(a_2,b_2),\quad q_5=(c,d).
$$

These pairs are addresses for the five physical data qubits. The seed labels are design ingredients, not additional encoded quantum systems.

For larger seeds, let the first have $n_1$ bits and $m_1$ checks, and the second have $n_2$ bits and $m_2$ checks. Allocate data qubits $q_{ij}$ for bit pairs and $r_{cd}$ for check pairs. There are

$$
n=n_1n_2+m_1m_2
$$

data qubits. The connection rule is:

| Quantum check label | Data qubits it touches |
| --- | --- |
| $X$ check $(c,j)$ | All $q_{ij}$ whose first-seed bit $i$ belongs to check $c$, and all $r_{cd}$ whose second-seed check $d$ contains bit $j$. |
| $Z$ check $(i,d)$ | All $q_{ij}$ whose second-seed bit $j$ belongs to check $d$, and all $r_{cd}$ whose first-seed check $c$ contains bit $i$. |

For a given $X$–$Z$ pair, either both seed memberships hold, giving the two shared qubits $q_{ij}$ and $r_{cd}$, or neither shared qubit appears. Sparse seeds keep both the check weights and the checks per qubit bounded. [Original construction](https://arxiv.org/abs/0903.0566)

“Hypergraph” means a relation may involve more than two vertices. A parity rule can be drawn as one hyperedge touching its bits, or as a check node joined to those bits in a Tanner graph. Surface-code checks also involve several qubits. The distinguishing feature of HGP is the product recipe above.

## What does the construction buy?

With suitable comparable-size classical LDPC seeds having constant rate and linear distance, HGP yields quantum codes with $k$ proportional to $n$ and distance proportional to $\sqrt n$. Many logical qubits share one sparse block. Particular repetition-code choices also recover surface and toric constructions. [Rate, distance, and examples](https://arxiv.org/abs/0903.0566)

The general connection pattern need not fit nearby interactions on a planar chip. Check weight depends on the seed degrees, and the seed choice also affects decoding. Expander-based HGP codes admit a proven linear-time decoder for a number of adversarial errors of order $\sqrt n$; an **expander** is a sparse network whose small regions still have many connections to the rest. This theorem has specific expansion assumptions. [Quantum expander decoding](https://arxiv.org/abs/1504.00822)

[Lifted products](../lifted-product-codes/README.md) and [balanced products](../balanced-product-codes/README.md) modify how product labels are combined, opening other rate–distance trade-offs. Their extra structure is part of the code design; shortening an ordinary HGP block arbitrarily does not preserve its protection.
