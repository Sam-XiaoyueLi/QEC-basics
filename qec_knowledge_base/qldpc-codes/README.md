# qLDPC codes

Last updated: 2026-11-03

## What makes a code qLDPC?

A quantum low-density parity-check (qLDPC) family has a set of stabilizer checks in which:

- Each check touches a bounded number of data qubits.
- Each data qubit belongs to a bounded number of checks.
- Both bounds stay fixed as the code grows.

The families use different **recipes for generating check patterns**.

## Families are recipes for the check pattern

Start with physical data qubits. A recipe specifies which qubits each check measures.

For a CSS code, it gives two lists: $X$ checks and $Z$ checks. Each $X$ check must overlap each $Z$ check on an **even number of qubits**, so they commute.

The recipe also determines allowed qubit counts and connections. Implementing those connections on hardware is a separate task.

## How do the main recipes compare?

We write a code as $[[n,k,d]]$:

- **$n$:** number of data qubits.
- **$k$:** number of logical qubits stored. For a stabilizer code, **$k=n-r$**, where $r$ is the number of independent stabilizer generators. The encoding rate is $k/n$.
- **$d$:** smallest number of qubits an undetectable logical Pauli error can affect.

For example, four data qubits with two independent checks, $XXXX$ and $ZZZZ$, encode $4-2=2$ logical qubits. Their product $YYYY$ adds no independent constraint. The distance is 2, giving a $[[4,2,2]]$ code.

| Family | Basic idea | Advantage | Main drawback |
| --- | --- | --- | --- |
| **Geometric** — [surface](../../surface_code.ipynb), toric, [color](../color-codes/README.md) | Arrange checks using a geometric lattice. | Nearby connections simplify hardware. | Usual 2D patches use more data qubits per logical qubit as distance grows. |
| **Hypergraph product (HGP)** | Combine two classical check patterns, creating two sets of data qubits. Checks use both sets so every X–Z overlap is even. | Suitable seeds give constant encoding rate and $d\propto\sqrt n$. | Distance grows relatively slowly; connections can be long. |
| **Lifted product (LP)** | Use small check templates with permutation instructions in the address book, then combine them to generate commuting checks. | Some constructions achieve constant rate and $d\propto n$. | Choosing useful permutations and implementing the connections can be difficult. |
| **Balanced product** | Use symmetry to identify equivalent positions in a product construction. | Reduces the number of qubit positions in the product. | The reduction also changes the code's rate and distance. |
| **Quantum Tanner** | Use small classical codes to define checks on a specially connected network. | Suitable constructions achieve constant rate and $d\propto n$, with efficient decoders. | Checks can involve many qubits and require long connections. |
| **Bicycle** | Use two equal-sized groups of data qubits and repeating connection rules. The rules tell each check which qubits to measure. | Compact recipes give useful small codes, such as the $[[144,12,12]]$ Gross code. | Performance depends on the shifts chosen; long connections remain a challenge. |

These families overlap. For example, some balanced-product constructions are also lifted products. The scaling results above require suitable ingredients; they do not hold for every code made with the recipe.

**Bivariate** and **trivariate bicycle** use two and three shift variables, respectively.

## Why use qLDPC codes?

The attraction of **high-rate qLDPC codes** is storing many logical qubits with fewer data qubits per logical qubit.

For example, the [Gross code](../gross-code/README.md) stores **12 logical qubits in 144 data qubits**. Its original memory protocol adds 144 measurement helpers, bringing the total to **288 physical qubits**. That protocol was studied through simulation. [Original study](https://www.nature.com/articles/s41586-024-07107-7)

The practical saving depends on the whole system: helper qubits, connections, check measurements, decoding, and logical gates. A compact memory does not automatically make a compact computer.

## How do other code types fit in?

Code names can describe different things: a check recipe, an encoding method, or the hardware that stores information.

| Type | Basic idea |
| --- | --- |
| **Small block codes** — Shor, Steane, five-qubit | Encode information in a small fixed block of qubits. |
| **Concatenated codes** | Encode each qubit of one code using another code. |
| **Subsystem codes** — Bacon–Shor | Measure simpler checks while allowing some unneeded degrees of freedom to change. |
| **Bosonic codes** — cat, binomial, GKP | Encode information in the states of an oscillator. |

These approaches can be combined. For example, an outer repetition code can protect a group of bosonic cat qubits, as in [AWS's Ocelot](https://www.amazon.science/blog/amazon-announces-ocelot-quantum-chip).

## What major companies are doing

Selected examples, as of November 3, 2026. Companies may use different codes for different jobs.

| Company | Codes | Work demonstrated or proposed |
| --- | --- | --- |
| **Google** | Surface and color | Demonstrated surface-code error correction and [color-to-surface transfer of magic states](https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/) used for computation. |
| **IBM** | Bivariate bicycle | Proposed a [modular architecture](https://research.ibm.com/publications/tour-de-gross-a-modular-quantum-computer-based-on-bivariate-bicycle-codes--2) with logical operations and simulated error rates. |
| **AWS** | Cat qubits + repetition code | [Demonstrated Ocelot](https://www.amazon.science/blog/amazon-announces-ocelot-quantum-chip): cat encoding suppresses bit flips; repetition checks correct phase flips. |
| **Quantinuum** | Helix and other codes | [Reported demonstrations](https://www.quantinuum.com/blog/helix-a-new-architecture-for-enterprise-scale-fault-tolerant-quantum-computing) of logical memory, computation, and connections between different codes on Helios. |
| **Microsoft, with partners** | Carbon and tesseract color codes | [Demonstrated error correction and logical operations](https://quantum.microsoft.com/en-us/insights/blogs/from-research-to-product-engineering-logical-qubit-demonstrations-shaping-microsoft-utility-scale-quantum-software-platform) on Quantinuum hardware. |
| **IonQ** | qLDPC | [Studying code and operation choices](https://www.ionq.com/blog/how-qldpc-with-scheduled-error-correction-unlocks-faster-fault-tolerant-quantum-computers) for its proposed trapped-ion architecture. |
