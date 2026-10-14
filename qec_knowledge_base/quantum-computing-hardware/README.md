# Quantum computing hardware

Last updated: 2026-10-14

## Quantum two-level systems

A classical bit stores $0$ or $1$. A qubit can occupy $|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$, where $\alpha,\beta$ are complex amplitudes and $|\alpha|^2+|\beta|^2=1$. **Superposition is a property of quantum states; it is not created by small size or low temperature.** Natural systems such as atomic internal states and electron spins support it, and engineered circuits can support it too. A coherent drive couples the chosen states and sets their amplitudes and relative phase. Keeping that phase predictable allows later operations to produce interference.

The challenge is to select, prepare, control, and read two states while limiting uncontrolled interactions with the environment. The device can have other levels; unwanted occupation outside the computational pair is **leakage**. Uncontrolled interactions that reveal the qubit state to the environment cause decoherence. Entanglement additionally requires an interaction or a measurement-assisted mechanism that couples the qubits.

**Must it be small?** Individual atoms are convenient because they have reproducible, discrete levels. Small size alone does not protect coherence: atomic qubits still need isolation and careful control. Superconducting qubits instead use collective electrical degrees of freedom in fabricated circuits much larger than an atom.

**Must it be cold?** That depends on the platform. Cooling suppresses thermal excitation and can reduce motion and noise; it does not switch quantum mechanics on. Superconducting circuits need cryogenic operation. Ion and neutral-atom systems cool the particles' motion with lasers, while the surrounding apparatus can operate near room temperature. All three require shielding and control of unwanted interactions. [Circuit review](https://arxiv.org/abs/2006.10433), [ion review](https://www.nature.com/articles/npjqi201634), [atom review](https://www.nature.com/articles/s41567-021-01357-2)

Two coherence measures are useful before comparing devices:

| Quantity | Meaning | Consequence for a circuit |
| --- | --- | --- |
| $T_1$ | Time scale for energy relaxation, usually $\lvert1\rangle\to\lvert0\rangle$. | Stored populations can change during gates and idle periods. |
| $T_2$ | Time scale for loss of coherence between $\lvert0\rangle$ and $\lvert1\rangle$. | Relative phase becomes unreliable, degrading interference. |

Compare these times with **gate, measurement, reset, and idle durations**. A longer coherence time is useful only alongside sufficiently accurate operations. Echo and other refocusing sequences can extend measured coherence, so the measurement protocol matters. [Circuit review](https://arxiv.org/abs/2006.10433)

## Requirements for gate-based quantum computing

The five **DiVincenzo criteria** specify the essential capabilities. [Original paper](https://arxiv.org/abs/quant-ph/0002077)

| Requirement | What the hardware must provide |
| --- | --- |
| Scalable, well-characterized qubits | Known computational states and interactions, with a route to larger systems. |
| Initialization | Reliable preparation of a known state. |
| Long enough coherence | Preserve quantum information over the required operations. |
| Universal gate control | Combine available operations to approximate arbitrary quantum circuits. |
| Qubit-specific measurement | Read the required qubit outcomes reliably. |

For fault-tolerant computation, these capabilities must also support repeated error checks, reset, decoding, and any required feedback. The central tradeoff is **isolation for storage versus controlled coupling for operations**. There is no single coherence time or gate fidelity that guarantees fault tolerance for every code and noise model.

## Superconducting qubits

**Picture a patterned metal circuit on a chip at the bottom of a dilution refrigerator.** A common qubit is the **transmon**: a Josephson junction connected across a capacitor. A typical tunnel junction has two superconductors separated by a thin insulating barrier, often aluminium–oxide–aluminium. Cooper pairs tunnel through the barrier; this differs from a silicon p–n junction. The qubit is a state of the whole circuit. [Junction physics](https://www.nature.com/articles/s41567-024-02400-8)

The capacitor and junction form a quantum oscillator. An ordinary linear oscillator has equally spaced levels, making it difficult to address just one transition. The junction supplies **nonlinearity**, so the $|0\rangle\leftrightarrow|1\rangle$ and $|1\rangle\leftrightarrow|2\rangle$ transitions have different frequencies. We use the lowest two levels and shape pulses to limit leakage into higher ones.

**Control:** a resonant microwave pulse rotates the qubit. Its amplitude and duration set the rotation angle; its phase sets the rotation axis in the equatorial plane. A virtual $Z$ rotation updates the phase reference for subsequent controls. Engineered couplings enable entangling gates. For $CZ$, calibrated controls make $|11\rangle$ acquire an extra phase of $\pi$ relative to the other computational states, after compensating single-qubit phases; the pulse mechanism depends on the device. A readout resonator responds differently to the two qubit states, converting that difference into a measured microwave signal. [Transmon and control review](https://www.nature.com/articles/s41534-016-0004-0)

**Environment:** operation at roughly tens of millikelvin keeps the material superconducting and suppresses thermal occupation of microwave-frequency levels. Cold operation, filtered lines, and shielding work together to reduce noise. [Experimental device](https://www.nature.com/articles/s41467-021-22030-5)

![Superconducting circuits, a Josephson junction cross-section, and unequal circuit energy levels](assets/superconducting.png)

## Trapped ions

**Picture charged atoms suspended in vacuum above or between electrodes, addressed by laser beams.** A common trap uses oscillating radiofrequency fields plus static fields to confine the ions. Their mutual electric repulsion helps organize them into a chain. Two selected internal levels—often hyperfine levels—store each qubit; the ion's position does not encode the bit.

**Control:** a resonant drive, often a two-laser Raman process, coherently couples the internal states. Pulse duration and strength set the rotation angle; drive phase sets the axis. For an entangling gate, state-dependent forces couple the internal states to shared vibrational motion. A carefully timed sequence disentangles that motion at the end while leaving a joint phase on the internal states. State-dependent fluorescence provides readout: one state scatters photons while the other is dark. [Ion architecture review](https://www.nature.com/articles/npjqi201634)

**Connectivity:** ions sharing suitable motional modes can interact without a permanent wire between each pair. In a **QCCD** (quantum charge-coupled device), electrode voltages shuttle ions between storage and gate zones, extending pair access. Transport and the number of zones constrain scheduling. [Helios architecture](https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/helios.html)

**Environment:** high vacuum suppresses collisions; laser cooling prepares suitable motional states. The chamber can be near room temperature, although some traps use cryogenic operation to improve vacuum or reduce noise. [Ion-trap materials review](https://www.nature.com/articles/s41578-021-00292-1)

![Ions suspended above electrodes, shared motion, and transport from storage to a gate zone](assets/trapped-ions.png)

## Neutral atoms

**Picture an array of individual uncharged atoms, each held at the focus of a laser beam in vacuum.** These **optical tweezers** confine atoms through the interaction of the light field with their induced electric dipoles. Two internal states, often hyperfine states, store the qubit. Steering the tweezers rearranges the atoms. [Optical-tweezer review](https://www.nature.com/articles/s41567-021-01357-2)

**Control:** microwave or Raman drives rotate the stored qubit states. To entangle atoms, lasers temporarily couple a computational state to a highly excited **Rydberg state**. Two nearby Rydberg excitations interact strongly. Under **Rydberg blockade**, exciting one atom shifts the joint energy enough to suppress resonant excitation of the other. Suitable pulse sequences exploit that conditional response to produce a gate such as $CZ$, returning the atoms to their storage states. Fluorescence and state-selective procedures provide readout; whether an atom survives measurement depends on the implementation. [Rydberg gate experiment](https://www.nature.com/articles/s41586-023-06481-y)

**Connectivity:** gate access depends on distance and laser addressing. Moving selected atoms into an entangling region enables flexible pair access and parallel operations. **Environment:** the atoms' motion is laser-cooled, with high vacuum suppressing collisions; the apparatus need not be at millikelvin temperatures. Atom loss and replacement are part of the operational design. [Reconfigurable processor](https://www.nature.com/articles/s41586-025-09848-5)

![Neutral atoms in optical tweezers, movement into a gate configuration, and Rydberg excitation](assets/neutral-atoms.png)

## How physical structure affects gates and connectivity

A **native gate** is directly supported by calibrated controls; a compiler builds other gates from these operations. **Connectivity** determines pair access. Any-pair access does not imply unlimited simultaneous gates.

| Platform | Typical native gates | Pair access | Main circuit costs |
| --- | --- | --- | --- |
| Superconducting | Rotations; $CZ$ on current IBM Heron/Nighthawk. Other designs use ECR or exchange gates. [Instructions](https://quantum.cloud.ibm.com/docs/en/guides/qpu-information) | Engineered coupling graph. | Routing, decoherence, crosstalk. |
| Trapped ions | Rotations; motion-mediated entanglers, e.g. Helios $R_{ZZ}(\theta)$. [Gates](https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/helios.html) | Shared motion or transport to gate zones. | Gate time, transport, limited parallelism. |
| Neutral atoms | Rotations; Rydberg controlled-phase gates, e.g. $CZ$. [Experiment](https://www.nature.com/articles/s41586-023-06481-y) | Nearby atoms; rearrangement enables new pairs. | Movement, atom loss, readout/reset. |

For software, inspect the device's **gate set, coupling map, operation durations, error data, and measurement/reset support**. These determine compilation and scheduling costs. For example, native $CZ$ plus Hadamards on the target implements CNOT. Moving an atom changes its location; a SWAP gate exchanges quantum states. Both can enable routing, with different costs.

## Demonstrated capabilities

Selected milestones checked **2026-10-14**. Physical-qubit counts, array sizes, and logical-memory results measure different capabilities.

| Platform | Demonstrated or available capability | What it tells us |
| --- | --- | --- |
| Superconducting | Google's 105-qubit Willow demonstrated logical error suppression as surface-code distance increased, including distance 7. *Nature* (2025). [Paper](https://www.nature.com/articles/s41586-024-08449-y) | Larger codes can improve logical memory under the tested conditions. |
| Superconducting | IBM documents 156-qubit Heron and 120-programmable-qubit Nighthawk; r2 adds high-speed reset (September 2026). [Devices](https://quantum.cloud.ibm.com/docs/en/guides/processor-types) | Available gate-based hardware with differing connectivity and reset features; these are not logical-qubit counts. |
| Trapped ions | Helios: 98 qubits, transport-enabled all-to-all access, average two-qubit infidelity $7.9(2)\times10^{-4}$ across operation zones. November 2025 preprint. [Paper](https://arxiv.org/abs/2511.05465) | Precise gates and flexible routing at system scale; gate fidelity alone does not predict algorithm success. |
| Neutral atoms | A reconfigurable processor with up to 448 atoms demonstrated repeated QEC, logical operations, and qubit reuse. *Nature* (2026; online 2025). [Paper](https://www.nature.com/articles/s41586-025-09848-5) | Integration of key fault-tolerant mechanisms; performance depends on protocol, decoding, and acceptance conditions. |
| Neutral atoms | A separate experiment trapped over 6,100 atoms and measured 12.6(1) s coherence with XY16 dynamical decoupling (a refocusing pulse sequence). *Nature* (2025). [Paper](https://www.nature.com/articles/s41586-025-09641-4) | Large coherent arrays, not a demonstrated 6,100-qubit universal entangling processor. |

These three platforms are useful starting points for gate-based hardware: fast engineered circuits, precise motion-mediated ion gates, and large rearrangeable atom arrays. Semiconductor spins and photonics are also active approaches. [Silicon experiment](https://www.nature.com/articles/s41586-025-09531-9), [photonic experiment](https://www.nature.com/articles/s41586-024-08406-9)
