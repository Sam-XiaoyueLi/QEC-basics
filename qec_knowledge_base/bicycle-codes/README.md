# Bicycle codes: two-block recipes, bivariate and multivariate variants

Last updated: 2026-11-02

Bicycle constructions specify checks on **two equal-sized blocks of physical data qubits**. Two connection recipes determine one check type; exchanging the recipes and reversing their connections gives the other type. Suitable compatible recipes make the $X$ and $Z$ checks commute. Bivariate and multivariate bicycle codes use shifts of periodic addresses to describe those recipes compactly.

## Start with the two data blocks

Call the blocks $L$ and $R$. Give each block the same address set with $M$ addresses, so there are $n=2M$ data qubits. At every address, define an $X$ check that selects qubits in $L$ using recipe $A$ and in $R$ using recipe $B$.

To define a $Z$ check, use the reversed recipe $B$ in $L$ and reversed recipe $A$ in $R$. If the recipes are periodic shifts, a connection “three steps forward” becomes “three steps backward.” In binary matrix notation, where rows are checks and columns are data qubits,

$$
H_X=[A\mid B],\qquad H_Z=[B^T\mid A^T].
$$

Here $A,B$ are $M\times M$ connection matrices; a one denotes membership. The transpose $T$ reverses which endpoints play the check and data roles. If $AB=BA$, then

$$
H_XH_Z^T=AB+BA=0
$$

over binary arithmetic, where two identical contributions cancel. This proves all $X/Z$ overlaps are even. Sparse $A,B$ keep the resulting checks sparse. This is the generalized bicycle form; cyclic shifts supply a convenient way to make the recipes commute. [Generalized bicycle construction](https://arxiv.org/html/2012.04068#S3.SS1)

## What do bivariate and multivariate mean?

“Bivariate” means two shift variables. Label an address by $(i,j)$ with periodic ranges. Let $x$ advance the first coordinate and $y$ advance the second. A polynomial such as $x^3+y+y^2$ is a short list of connections: three steps in the first direction, one in the second, and two in the second. The addition is binary, so coincident repeated terms cancel.

The original bivariate bicycle (BB) construction chooses three shift terms in each of $A$ and $B$, giving weight-six checks when the terms remain distinct. The [Gross code](../gross-code/README.md#check-pattern-recipes) uses

$$
A=x^3+y+y^2,\qquad B=y^3+x+x^2,
$$

with $12\times6$ addresses in each data block. The resulting $[[144,12,12]]$ code has 144 data qubits; its original memory circuit adds 144 measurement ancillas. The Gross page develops the actual supports, rank count, logical operators, preparation, and gates. [Original BB study](https://www.nature.com/articles/s41586-024-07107-7)

**Multivariate bicycle (MB)** extends the shift-variable description. **Trivariate bicycle (TB)** uses three variables while retaining the two-block $[A\mid B]$ construction. Three variables need not mean three independent address directions: Voss and colleagues' concrete encoding uses $z=xy$. The variables describe algebraic connection rules and do not specify the spatial dimension of a chip.

That study includes a weight-five $[[30,4,5]]$ TB example: **30 data qubits plus 30 measurement helpers**, for 60 physical qubits in its protocol. Its performance was evaluated with circuit-noise simulations. This is a finite code example, not a universal parameter formula for TB codes. [Multivariate bicycle paper, version 4](https://arxiv.org/html/2406.19151v4)

## Why are these recipes attractive?

Short shift lists make it practical to search for useful blocks and to describe their repeated check patterns. Some instances combine a useful rate with moderate distance and small check weights. Symmetries can also support particular logical operations, although being able to store many logical qubits does not automatically make each one easy to address.

The choices of shifts and periodic sizes determine check dependencies and short logical operators. Commutation alone does not establish $k$ or $d$, and the bicycle name does not imply linear distance. Larger or more flexible polynomials can also increase check weight. The original BB result is a memory protocol assessed by simulation; its thresholds depend on the extraction circuit, noise model, and decoder. [BB protocol and analysis](https://arxiv.org/html/2308.07915v2)

Periodic address drawings can hide long physical connections. A real layout must implement those interactions, and the cost of routing, helpers, decoding, and logical operations belongs in the comparison. The generalized bicycle form also lies within the broader [lifted-product framework](../lifted-product-codes/README.md), so these labels need not identify separate kinds of code.

## How is trivariate tricycle different?

**Trivariate tricycle (TT)** is a different construction studied by Jacob, McLauchlan, and Browne. It uses three polynomials and a longer sequence of compatible maps, formally a length-three chain complex. That extra structure includes relations among checks that are useful for handling measurement errors. The 3D toric code is one instance.

The work studies **partial single-shot decoding**: exploiting check redundancy to handle measurement errors with a single syndrome round in the protected sector, without assuming every error type has identical protection. It also constructs transversal Clifford operations and, for selected subfamilies, constant-depth logical $CCZ$ gates. These claims come from theory and numerical simulations, with conditions specific to the construction. [Tricycle paper, version 3, October 2, 2026](https://arxiv.org/abs/2508.08191v3)

| Name | What changes in the recipe? |
| --- | --- |
| Bivariate bicycle | Two shift variables specify the two-block bicycle checks. |
| Trivariate bicycle | Three variables specify recipes within that same two-block framework; variables can be dependent. |
| Trivariate tricycle | Three polynomials enter a longer construction with additional check relations and different gate/decoding properties. |

The [qLDPC family table](../qldpc-codes/README.md#how-do-the-main-recipes-compare) places these alongside the other construction methods.
