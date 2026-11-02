# Erasure conversion: knowing where the damage is

Last updated: 2026-11-02

## What is an erasure?

Imagine ten data qubits carrying encoded information. An unknown error leaves the decoder asking both *where* the damage is and *what* correction it needs. An erasure flag supplies an extra fact: **qubit 7 is unreliable**.

The flag identifies the location, even if the damage itself is unknown. The qubit need not disappear. An atom leaving its trap, an excitation being lost, or a device leaving its two valid qubit states can all supply an erasure when detected. A check usually locates the damage within the interval since the previous check, rather than reporting its exact time. [Quantum erasure channel](https://arxiv.org/html/quant-ph/9610042v2), [erasure checks in circuits](https://arxiv.org/abs/2408.00829)

The extra information is not the lost quantum state. It is a warning attached to a particular unit of the code.

## Doesn't the syndrome already tell us where an error happened?

Sometimes it does, under a restricted noise assumption. But several errors can give the same syndrome.

Take the three-qubit bit-flip repetition code. Its checks are $Z_1Z_2$ and $Z_2Z_3$. A positive sign means that neighboring bits agree; a negative sign means they differ. Both $X_3$ and $X_1X_2$ produce the signs $(+,-)$:

- $X_3$ leaves qubits 1 and 2 agreeing, while qubits 2 and 3 differ.
- $X_1X_2$ also leaves qubits 1 and 2 agreeing, while qubits 2 and 3 differ.

Without more information, a decoder usually favors the single flip $X_3$. If $X_1X_2$ actually occurred, that choice leaves a logical bit flip.

Now suppose reliable flags say **only qubits 1 and 2 may be damaged; qubit 3 is unaffected**. For possible bit flips on those two locations, the checks distinguish every case:

| Possible error on the flagged locations | $Z_1Z_2$ | $Z_2Z_3$ |
| --- | --- | --- |
| No flip | $+$ | $+$ |
| $X_1$ | $-$ | $+$ |
| $X_2$ | $-$ | $-$ |
| $X_1X_2$ | $+$ | $-$ |

The syndrome has not gained more bits. The flags have narrowed the set of explanations, so $(+,-)$ now identifies $X_1X_2$. This is the extra information an erasure-aware [decoder](../decoders/README.md) can use.

This example protects **bit flips only**. For a full quantum code of distance $d$, the ideal guarantee is correction of up to $\lfloor(d-1)/2\rfloor$ unknown arbitrary errors, or up to $d-1$ known-location erasures. A mixture of $t$ unknown errors and $s$ erasures is correctable when

$$
2t+s<d.
$$

Thus an ideal distance-three quantum code can correct one unknown arbitrary error or two erasures. These are code-level guarantees with ideal recovery, not performance claims for noisy measurement circuits. [Erasure-code theory](https://arxiv.org/html/quant-ph/9610042v2)

## What does “conversion” mean physically?

The hardware encoding is chosen **before the error happens**, so a common physical fault takes the device outside its valid encoding. A measurement can then flag which device left that space. Conversion makes the fault recognizable; it does not repair the information.

One implementation uses three energy levels of a **fluxonium**, a [superconducting electrical circuit](../quantum-computing-hardware/README.md#superconducting-qubits). Instead of using adjacent levels as the qubit, it skips the middle one:

| Energy level | Role |
| --- | --- |
| Highest of the three: $|f\rangle$ | Computational 1 |
| Middle: $|e\rangle$ | Erasure state |
| Lowest: $|g\rangle$ | Computational 0 |

An encoded superposition occupies $|g\rangle$ and $|f\rangle$. The unused middle level provides somewhere detectable for relaxation to go. [Single-fluxonium experiment](https://arxiv.org/html/2601.11086v1)

In integer fluxonium at zero flux, a parity selection rule suppresses the direct one-photon $|f\rangle\to|g\rangle$ transition. Relaxation $|f\rangle\to|e\rangle$ instead leaves the encoding and can be flagged. Having three levels alone is insufficient: the transition strengths must favor this behavior. [Integer-fluxonium experiment](https://arxiv.org/html/2607.27123v1)

A phase error can still occur within the valid $g/f$ space without producing an erasure. The hardware redirects a useful class of faults, not every possible fault.

## How do we check the middle level without reading the qubit?

Couple the fluxonium to a microwave resonator. Choose circuit parameters so the resonator responds almost identically to $|g\rangle$ and $|f\rangle$, but differently to $|e\rangle$. Send a microwave probe and classify the returned signal. The intended distinction is **inside or outside the encoding**, without resolving computational 0 versus 1. Imperfect matching of the responses can disturb the qubit, and missed flags remain possible. [Resonator readout](https://arxiv.org/html/2607.27123v1#S2.SS3)

Even an ideal check does not guarantee that every unflagged superposition stays unchanged. If one computational state decays faster, surviving without a flag favors the longer-lived component and can change their relative amplitudes. Readout backaction and this conditional evolution are separate effects. [Fluxonium discussion](https://arxiv.org/html/2607.27123v1#S2.SS2)

## Does it have to be a three-level device?

Another route is **dual rail**: encode one qubit using one excitation shared across two modes. A simple basis is

$$
|0\rangle_{\mathrm{enc}}=|10\rangle,\qquad
|1\rangle_{\mathrm{enc}}=|01\rangle.
$$

A superposition $\alpha|10\rangle+\beta|01\rangle$ has exactly one excitation. Losing it produces $|00\rangle$, outside the encoding. An occupancy check can flag the loss.

The check must distinguish **one excitation from zero**, without learning which rail contains it. Measuring the rails separately would reveal the encoded basis value and destroy the superposition. With equal decay rates, loss can act as a state-independent erasure; unequal rates can distort the relative amplitudes in the surviving state. Actual devices may use superpositions of these basis states, but the same one-excitation subspace supports the encoding. [Dual-rail erasure-qubit proposal](https://arxiv.org/html/2208.05461v1)

The common idea is to make a likely fault move the state outside the space reserved for valid information, then detect that departure.

## If the state is damaged, how can we recover it?

The small hardware encoding supplies the warning. An **outer error-correcting code** distributes logical information across several such units. Its decoder combines the location flags with syndrome measurements to choose a recovery, using the quantum information that remains encoded across the other units.

The flag contains no amplitudes and makes no copy of the original state. Resetting a flagged device makes it available again, but reset alone does not restore its share of the logical information. Recovery is a collective code operation, subject to the code's erasure-correction capacity.

This gives three distinct experimental outcomes:

| Operation | What it establishes |
| --- | --- |
| Detect an erasure | Identify a unit that left its encoding. |
| Discard flagged runs: **postselection** | Improve results for the retained subset, with fewer runs surviving. |
| Use flags in code recovery | Recover or decode logical information using the known locations, without necessarily discarding the run. |

An improvement after postselection is useful evidence about the hardware, but it is not by itself a demonstration of correcting erasures and continuing a fault-tolerant computation.

## What has been demonstrated?

Selected results, checked **2 November 2026**. The rows measure different things and should not be read as a platform ranking.

| System | Experimental result | What to keep separate |
| --- | --- | --- |
| **Integer fluxonium**, July 2026 preprint | Resonator-based erasure detection and lower gate error after discarding flags. [Paper](https://arxiv.org/html/2607.27123v1) | Postselected improvement, not outer-code recovery. |
| **Metastable ytterbium atoms**, Nature Physics 2026 | A four-data-qubit $[[4,2,2]]$ code uses mid-circuit erasure information to improve decoded logical-state preparation from 0.874(4) to 0.902(3), **without postselection**. [Paper](https://arxiv.org/html/2506.13724v2) | A small-code decoding demonstration, not large-distance scaling. |
| **Superconducting cavity dual rail**, 2025 preprint | An error-detectable entangling gate with about 0.5% erasure per gate and residual postselected errors dominated by dephasing. [Paper](https://arxiv.org/html/2503.10935v2) | A hardware gate result; code-performance projections are simulations. |
| **Transmon qutrits**, April 2026 preprint | An ancilla-assisted erasure check and lifetime above $500\,\mu\mathrm{s}$ under repeated checks with postselection. [Paper](https://arxiv.org/abs/2604.08672) | Lifetime of retained runs, not unconditional tenfold improvement or a completed outer-code protocol. |

## What can reduce the advantage?

Some errors remain inside the encoding and are never flagged. A check can miss a real erasure, raise a false flag, or itself introduce noise. Between checks, a damaged unit can interact with others and spread faults, so flag timing and gate propagation matter alongside location.

Checks and resets also cost hardware operations and time. Checking more frequently catches damage sooner but adds more opportunities for disturbance; the best cadence depends on the device and code. The useful outcome is a lower logical failure rate after accounting for residual errors, detection imperfections, and those additional operations. [Protocol trade-offs](https://arxiv.org/abs/2408.00829)
