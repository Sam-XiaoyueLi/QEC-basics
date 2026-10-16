# QLDPC codes: definitions, trade-offs, and industry approaches

Status: Study reference | Last updated: 2026-10-16

## What QLDPC means

**QLDPC means “quantum low-density parity-check.”** It describes a broad class of quantum error-correcting codes, including the [Gross code](../gross-code/README.md).

Quantum information is encoded across many physical qubits, and we repeatedly measure **checks**—joint properties of groups of qubits—to detect errors without reading out the logical information. The pattern of check outcomes is called the **syndrome**. A classical **decoder** uses those outcomes to infer a suitable correction.

“Low density” describes the checking structure:

- Each check involves only a small number of qubits.
- Each qubit participates in only a small number of checks.

For a QLDPC code family, both numbers remain bounded as the code grows. In a check matrix, this means bounded row and column weights: each row describes a check, and each column describes a qubit. Most commonly discussed examples are **stabilizer codes**, whose checks are commuting Pauli operators. Many are also **CSS codes**, with separate checks made entirely of $X$ operators or entirely of $Z$ operators. [Definition and examples](https://www.nature.com/articles/s41586-024-07107-7)

## Protection and encoding efficiency

The usual notation is $[[n,k,d]]$:

| Parameter | Meaning |
| --- | --- |
| $n$ | Number of data qubits |
| $k$ | Number of encoded logical qubits |
| $d$ | Minimum number of qubits on which an undetectable, nontrivial logical Pauli error can act |

The **encoding rate** is $k/n$. A higher rate means more logical qubits per data qubit. The distance tells us about protection: with ideal syndrome information and suitable recovery, a distance-$d$ code can correct arbitrary errors on up to $\lfloor(d-1)/2\rfloor$ qubits. Noisy check measurements and gates require a fault-tolerant measurement protocol and decoder; distance alone does not specify the resulting logical error rate.

Some QLDPC families achieve both a rate that stays above zero and a distance proportional to $n$. As the block grows, both its storage capacity and its distance grow proportionally. These are called **asymptotically good codes**. This is a property of particular families, rather than a guarantee of the QLDPC definition. [Panteleev and Kalachev](https://arxiv.org/abs/2111.03654)

The attraction is the possibility of protecting many logical qubits with fewer physical qubits per logical qubit. The Gross code is a concrete example: $[[144,12,12]]$, with six-qubit checks. Its original measurement scheme uses another 144 check ancillas, giving 288 physical qubits in total. This illustrates why the data-qubit count alone does not capture the full hardware cost. [Bivariate bicycle construction](https://www.nature.com/articles/s41586-024-07107-7)

## Practical trade-offs

**Sparse checks do not necessarily mean easy hardware implementation.** A check can involve only six qubits while those qubits are physically far apart. “Few qubits per check” describes connectivity in the code; “nearby qubits” describes geometry in the hardware.

Routing interactions, measuring checks reliably, decoding outcomes quickly, and performing logical gates all affect whether the theoretical savings survive in a real machine. A code that stores information efficiently may still need substantial resources to address individual logical qubits or carry out a computation.

Surface codes themselves satisfy the QLDPC definition. In research conversations, however, “QLDPC” often refers to other constructions aimed at better encoding efficiency, including hypergraph-product, lifted-product, quantum Tanner, and bivariate bicycle codes.

A standard rotated surface-code patch stores one logical qubit using $d^2$ data qubits at distance $d$. Its checks can be measured using nearby interactions on a 2D grid. High-rate QLDPC constructions aim to protect many logical qubits together in a block, often with connections that are harder to implement on that grid. Neither approach wins from its code parameters alone. [Code and hardware comparison](https://www.nature.com/articles/s41586-024-07107-7)

QLDPC codes are a major research direction, with hardware demonstrations already reported, including small bivariate bicycle variants on a 32-qubit processor. These demonstrations are steps toward practical use; they do not yet establish large-scale operation. [Experimental demonstration](https://www.nature.com/articles/s41567-025-03157-4)

## Other kinds of quantum codes

Code names often describe different aspects of a construction, so these categories overlap. QLDPC describes check sparsity; other names describe geometry, the encoding method, or the physical system storing information.

| Approach | Basic idea | How it compares with QLDPC |
| --- | --- | --- |
| **Small block codes**—Shor, Steane, five-qubit code | Encode a few logical qubits into a fixed block of physical qubits. | Useful for learning QEC and as building blocks. A single small code does not establish how check sizes or encoding efficiency scale. |
| **Concatenated codes** | Encode each qubit of a code block into another code block, repeating in layers. | Protection increases through nesting. This supports structured fault-tolerant operations, but the physical-qubit cost can grow substantially with the number of layers. |
| **Topological codes**—surface, toric, color codes | Arrange qubits and checks on a lattice; logical information is associated with extended structures across it. | Many are themselves QLDPC. Geometric locality can simplify hardware, while common 2D constructions have less favorable encoding efficiency than high-rate QLDPC families. |
| **Subsystem codes**—Bacon–Shor | Protect the information of interest while allowing additional “gauge” degrees of freedom to change. | Can replace difficult stabilizer measurements with simpler gauge measurements. Small gauge checks alone do not imply that the stabilizer checks satisfy the usual QLDPC definition. |
| **Bosonic codes**—cat, binomial, GKP | Encode information in the many available states of an oscillator, such as a microwave cavity or optical mode. | Use a different physical encoding resource. They can reduce the number of separate modes needed, but require suitable state preparation, control, and error correction. |

The foundational sources include [stabilizer codes](https://arxiv.org/abs/quant-ph/9705052), [concatenation](https://arxiv.org/abs/quant-ph/9608012), [color codes](https://arxiv.org/abs/quant-ph/0605138), [subsystem codes](https://arxiv.org/abs/quant-ph/0610088), and [GKP oscillator encoding](https://arxiv.org/abs/quant-ph/0008040).

**Stabilizer and CSS are mathematical classifications.** The Steane code, surface code, and Gross code are all CSS stabilizer codes, despite their different structures. The [Shor-code notebook](../../shor_tutorial.ipynb) introduces protection against both bit and phase flips; the [surface-code notebook](../../surface_code.ipynb) develops repeated checks and lattice surgery, and the [decoding notebook](../../decoder.ipynb) shows how noisy measurement records are used to infer corrections.

Approaches can also be combined. A bosonic code can protect each underlying qubit, with an outer qubit code providing another layer of protection. [Example using concatenated cat codes](https://doi.org/10.1103/PRXQuantum.3.010329)

## What major companies are doing

The following is a snapshot of public work **as of October 16, 2026**. “Demonstrated” refers to specific experiments; an architecture or roadmap describes a proposed larger system. These are examples of each company's work, rather than an exclusive choice of one code.

| Company | Codes used or developed | How they are using them |
| --- | --- | --- |
| **Google Quantum AI** | Primarily **surface codes**, with **color codes** for some operations | Demonstrated below-threshold surface-code error correction on Willow: increasing code distance reduced logical errors. Its October 2026 work also demonstrated preparing special resource states in a color code and transferring them into a surface code. [Surface-code results](https://research.google/blog/making-quantum-error-correction-work/), [color-code work](https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/) |
| **IBM** | **Bivariate bicycle QLDPC codes**, including the Gross code | These form the basis of its proposed modular fault-tolerant architecture. IBM is developing the connectivity, check measurements, and logical operations needed to implement it. The full architecture remains a development target. [Architecture research](https://research.ibm.com/publications/tour-de-gross-a-modular-quantum-computer-based-on-bivariate-bicycle-codes--2) |
| **Amazon / AWS** | **Bosonic cat encoding combined with a repetition code** | Demonstrated on Ocelot: cat-qubit stabilization suppresses bit flips, while a repetition code across cat qubits corrects phase flips. This combines two protection mechanisms tailored to the hardware's noise. [Ocelot results](https://www.amazon.science/blog/amazon-announces-ocelot-quantum-chip) |
| **Quantinuum** | Several codes, including its **concatenated Helix code**, plus surface-code interfaces | Demonstrated protected memory and logical operations on its trapped-ion Helios processor. Movable ions provide flexible connectivity, allowing more complex code connections. [Helix demonstration](https://www.quantinuum.com/blog/helix-a-new-architecture-for-enterprise-scale-fault-tolerant-quantum-computing) |
| **Microsoft**, with hardware partners | **Carbon codes** derived from concatenation, **tesseract color codes**, and other geometric constructions | With Quantinuum hardware, demonstrated error correction and logical operations using $[[12,2,4]]$ carbon and $[[16,6,4]]$ tesseract codes. These experiments are distinct from Microsoft's own Majorana hardware programme. [Technical account](https://quantum.microsoft.com/en-us/insights/blogs/from-research-to-product-engineering-logical-qubit-demonstrations-shaping-microsoft-utility-scale-quantum-software-platform) |
| **IonQ** | **QLDPC codes**, alongside specialised error-reduction protocols | Developing trapped-ion architectures, logical-operation protocols, and decoders for QLDPC codes. Recent work evaluates codes within its proposed “Walking Cat” architecture; those architecture results are research toward a future system. [QLDPC research](https://www.ionq.com/blog/how-qldpc-with-scheduled-error-correction-unlocks-faster-fault-tolerant-quantum-computers) |

These choices reflect different engineering priorities. Google's surface-code approach fits nearby interactions on a grid. IBM's high-rate QLDPC approach aims to store multiple logical qubits efficiently within each block. Flexible connectivity in trapped-ion systems gives companies more freedom to explore other check structures. AWS engineers cat qubits so bit flips become rare, then targets the remaining phase errors with an outer code.

A company may also use different codes for memory, logical gates, and preparation of special resource states. Google's color-to-surface-code experiment is a direct example: the resource states, often called **magic states**, enable operations needed for universal quantum computation.

## How to compare candidates

When hearing about a QLDPC code, first ask which family it belongs to and what its $[[n,k,d]]$ parameters are. For a practical comparison, also ask:

- **Total hardware overhead:** how many data qubits, ancillas, and other components are required?
- **Connectivity:** which qubits must interact, and how are those interactions implemented?
- **Logical error rate:** what performance survives when gates, preparation, and check measurements can fail?
- **Decoding:** can the decoder keep up with the measurement stream and the feedback deadlines?
- **Logical operations:** what are the time and hardware costs of preparation, gates, and readout?

The useful comparison is the cost of achieving a specified reliability for the intended computation. No single code property settles all of these questions.
