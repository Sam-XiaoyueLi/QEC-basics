# Quantum computing hardware

Last updated: 2026-10-14

## Overview

A qubit can be in a superposition

$$
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle,
\qquad \alpha,\beta\in\mathbb C,
\qquad |\alpha|^2+|\beta|^2=1.
$$

The amplitudes set the measurement probabilities, $P(0)=|\alpha|^2$ and $P(1)=|\beta|^2$. Their **relative phase**, $\arg\beta-\arg\alpha$, determines how the two components interfere during later gates.

**Atoms, ions, and electron spins provide natural two-level systems.** Neutral atoms and ions have discrete internal energy levels. For two chosen levels with energies $E_0$ and $E_1$, a superposition evolves as

$$
\begin{aligned}
|\psi(t)\rangle
&=\alpha e^{-iE_0t/\hbar}|0\rangle
+\beta e^{-iE_1t/\hbar}|1\rangle\\
&=e^{-iE_0t/\hbar}
\left(\alpha|0\rangle+\beta e^{-i\Delta E\,t/\hbar}|1\rangle\right),
\qquad \Delta E=E_1-E_0.
\end{aligned}
$$

Here $\hbar=h/(2\pi)$, with $h$ Planck's constant. The common factor $e^{-iE_0t/\hbar}$ is a **global phase** and does not affect measurement probabilities. The energy difference determines the evolving relative phase:

$$
\varphi(t)=\varphi(0)-\frac{\Delta E\,t}{\hbar}.
$$

A resonant electromagnetic drive couples the levels and prepares a chosen superposition. Electron spins follow the same description when a magnetic field separates the energies of spin up and spin down.

**Using these states as qubits requires protecting them from their surroundings.** Collisions with air, fluctuating fields, and coupling to uncontrolled motion can exchange energy or disturb the relative phase. When the environment acquires information that distinguishes the components of a superposition, their observable interference is lost. This is **decoherence**. Cooling reduces thermal excitation and unwanted motion. Vacuum, shielding, and controlled fields reduce other disturbances.

**The essence of quantum computing hardware is to select two addressable states, suppress unwanted interactions, and provide controlled coupling for gates and readout.** A gate-based computer needs scalable, well-characterized qubits that can be initialized in known states, controlled with universal gates, and measured individually. Their populations and phase information must survive long enough to perform the required operations. These are the five **DiVincenzo criteria**.

### Relaxation and phase stability

Two time scales quantify this survival: **$T_1$ measures population relaxation**, and **$T_2$ measures the decay of phase coherence**, which reduces interference. Both can be visualized on the Bloch sphere.

On the Bloch sphere introduced in Tutorial 0, the north pole is $|0\rangle$ and the south pole is $|1\rangle$. The height encodes the population difference, and the angle around the vertical axis encodes the relative phase. Noise can shorten the Bloch vector, moving its tip inside the sphere.

| Time scale | Physical change | Bloch-sphere picture |
| --- | --- | --- |
| $T_1$: population relaxation | Population imbalance relaxes toward equilibrium. | For relaxation to the ground state, the vector approaches the north pole. |
| $T_2$: loss of phase coherence | Phase fluctuations wash out interference across repeated runs. Energy relaxation also contributes. | The component in the equatorial plane shrinks. Pure phase noise leaves the height unchanged. |

For hyperfine ground-state encodings, population relaxation can approach a mixture of zero and one. For relaxation toward $|0\rangle$ and simple exponential decay,

$$
p_1(t)=p_1(0)e^{-t/T_1},
\qquad
r_\perp(t)=r_\perp(0)e^{-t/T_2},
$$

where $r_\perp$ is the length of the Bloch vector's projection onto the equatorial plane. The figure starts both examples at $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$, with equal populations and relative phase zero. The vectors show the state averaged over repeated runs, with predictable phase rotation omitted. Compare $T_1$ and $T_2$ with gate and idle durations to judge how much information is lost during a computation.

![Bloch-sphere views of energy relaxation toward the ground state and loss of phase coherence at fixed populations](assets/bloch-coherence.png)

## Hardware platforms

Qubits can be encoded in superconducting circuit levels, atomic states, semiconductor spins, or photons. Each platform supplies different controls, interactions, and noise sources.

Superconducting qubits, trapped ions, and neutral atoms are prominent gate-based platforms with demonstrated multi-qubit control and error-correction experiments. They illustrate three useful hardware choices: fast electrical control on a chip, precise atomic control through shared ion motion, and large rearrangeable atom arrays. Their different interactions determine native gates and connectivity.

## Superconducting qubits

A **Josephson junction** has two superconductors separated by a thin insulating barrier. Coherent Cooper-pair tunnelling makes it a **nonlinear inductor**. In parallel with a large capacitor, it forms a transmon's **anharmonic oscillator**. Its quantum wavefunctions have discrete energies. We use the ground level as $|0\rangle$ and the first excited level as $|1\rangle$.

The junction's nonlinearity makes successive gaps unequal:

$$
E_1-E_0\ne E_2-E_1.
$$

A selective pulse can therefore control the lowest pair while avoiding $|2\rangle$. Unwanted population in higher levels is **leakage**.

When we think about superconducting qubits, we can picture a chip with transmons, readout resonators, couplers, and control lines patterned on its surface, mounted at the coldest stage of a dilution refrigerator. Cooling to tens of millikelvin suppresses thermal excitation. Low-loss materials, shielding, and filtered control lines help preserve the qubits’ states, while material defects, stray radiation, and crosstalk can still cause errors.

A **readout resonator** is often a winding transmission line that supports a microwave electromagnetic mode. Its response shifts depending on whether the coupled transmon is in zero or one. A **3D cavity** supports a similar mode inside a metal enclosure. **Control lines** carry gate pulses to the qubits, and **readout lines** carry probe and measurement signals.

![Two transmons connected by a coupler, with separate readout resonators and control lines](assets/chip-layout.png)

The resonant frequency is $f_{01}=(E_1-E_0)/h$, typically **a few gigahertz**. This energy gap calls for **microwaves**. In the frame rotating at $f_{01}$, pulse phase selects an axis in the $X$–$Y$ plane. Strength and duration set the angle.

- **$X$:** choose the $X$-axis phase and a calibrated $\pi$ pulse. It swaps zero and one, up to global phase.
- **$Y$:** use the same rotation angle with drive phase shifted by $\pi/2$.
- **$Z$:** update the tracked phase frame by $\pi$ and adjust subsequent controls. This **virtual $Z$** implements $\alpha|0\rangle+\beta|1\rangle\to\alpha|0\rangle-\beta|1\rangle$ without a separate physical pulse.
- **Readout:** send a microwave probe through the readout resonator and classify the returning response as zero or one.

A **coupler** sets the interaction between qubits. It can be a capacitive or inductive connection, a coupling resonator, or a tunable circuit containing additional Josephson junctions. Adjusting the interaction exchanges excitations or shifts joint-state energies. A conditional phase of $\pi$ on $|11\rangle$, after compensating single-qubit phases, gives **$CZ$**. One implementation exploits coupling to the nearby $|02\rangle$ level. Other designs favour exchange or ECR gates. Native single-qubit operations include rotations and virtual $Z$. Fixed connectivity creates routing costs for distant qubits.

![A capacitor and Josephson junction in parallel, junction materials, and unequal circuit energy levels](assets/superconducting.png)

## Trapped ions

An **ion is an atom with a net electric charge**. Oscillating and static electric fields confine ions in vacuum. Each ion carries one qubit in two selected internal states. For a common $^{171}\mathrm{Yb}^{+}$ encoding,

$$
|0\rangle=|F=0,m_F=0\rangle,
\qquad
|1\rangle=|F=1,m_F=0\rangle.
$$

$F$ labels the total angular momentum formed by coupling electron and nuclear angular momenta. $m_F$ labels its projection along the chosen field axis. Both states lie in the electronic ground manifold, with different hyperfine energies, so their populations can be long-lived.

Preserving these states also requires protection from the surroundings. Vacuum suppresses collisions, laser cooling controls motion, and stable fields and drive references protect phase. A second ion species can cool shared motion without resonantly exciting the stored qubit. Unwanted light, microwave leakage, and motional heating remain error sources.

Optical pumping prepares zero by repeatedly exciting other states and allowing them to decay until population accumulates in the chosen state. Focused beams then address individual ions, or electrodes shuttle selected ions into a control zone. A **Raman drive** uses two laser frequencies whose difference matches the qubit splitting. Their relative phase selects the $X$–$Y$ axis, and pulse strength and duration set the rotation angle.

- **$X$:** apply an addressed Raman $\pi$ pulse with the phase defining the $X$ axis.
- **$Z$:** update the tracked phase frame, or shift the two levels differently with light to accumulate a relative phase of $\pi$.
- **Readout:** illuminate a state-selective optical transition and use photon counts to distinguish bright and dark states.

Electric repulsion couples the ions' motion into shared vibrational modes. State-dependent laser forces couple selected qubits to those modes. A timed sequence closes the motional trajectory while leaving an entangling operation on the internal states. This produces **$XX$ or $ZZ$ interactions**, with the spin axis set by controls or basis rotations. A $ZZ$ interaction gives $R_{ZZ}(\theta)=e^{-i\theta Z\otimes Z/2}$.

Shared modes or transport provide flexible pair access. Gate time, motional heating, transport, and the number of gate zones limit throughput and parallelism. Native controls include phase-controlled rotations, virtual $R_z$, and $R_{ZZ}$.

![Trapped ions, their internal qubit levels, and shared motion used for entangling gates](assets/trapped-ions.png)

## Neutral atoms

A **neutral atom has no net electric charge**. It is also held in vacuum, but an **optical tweezer** provides the confinement: a laser beam focused into a tiny spot. The light's electric field slightly displaces the electron cloud relative to the nucleus, inducing an electric dipole. With a suitable laser frequency, the atom's energy is lower near the bright focus. Moving away raises its energy, creating a restoring force. An array of spots therefore holds an array of atoms.

For example, two ground-state hyperfine levels of $^{87}\mathrm{Rb}$ can encode

$$
|0\rangle=|F=1,m_F=0\rangle,
\qquad
|1\rangle=|F=2,m_F=0\rangle.
$$

These are different combinations of electron and nuclear angular momenta. An atom in the first state represents zero, and in the second represents one. Both occupy the same trap and electronic ground manifold. A drive prepares superpositions of these internal configurations.

Vacuum suppresses collisions, laser cooling reduces motion, and stable fields and trapping light limit phase noise. Trap-light scattering can change populations, intensity variations shift the levels, and atoms can be lost.

Optical pumping prepares zero. Focused Raman beams address selected atoms, while other implementations combine global microwave rotations with local light-induced energy shifts. Pulse strength and duration set the rotation angle, and drive phase selects the $X$–$Y$ axis. Steering the tweezers rearranges the atoms.

- **$X$:** drive the storage-state transition with a resonant $\pi$ pulse and the $X$-axis phase.
- **$Z$:** shift the two levels differently with focused light to accumulate a relative phase of $\pi$. Compatible controllers can also track phase-frame updates.
- **Readout:** use state-dependent fluorescence, or map the internal state to position or atom loss before imaging. Atom retention depends on the method.

Ground-state atoms interact weakly at typical tweezer separations. A laser temporarily couples a storage state to a highly excited **Rydberg state**, $|r\rangle$, whose large electronic extent enables strong interactions. Exciting one atom shifts the energy required to excite its neighbour. Under **Rydberg blockade**, that shift suppresses resonant excitation of the second atom.

A laser sequence turns this conditional response into a phase, producing **$CZ$** while returning population to the storage states. Moving atoms into range selects interacting pairs. Native operations include storage-state rotations and Rydberg controlled-phase gates. Optical addressing, movement, loss, and reset determine scheduling costs.

![Optical tweezer confinement, rubidium zero and one states, and Rydberg blockade](assets/neutral-atoms.png)

## Comparison

| Platform | Qubit and confinement | Control and readout | Interaction and native gates | Advantages | Limitations |
| --- | --- | --- | --- | --- | --- |
| Superconducting | Lowest circuit levels on a cryogenic chip. | Microwave rotations, virtual $Z$, resonator readout. | Engineered coupling graph. $CZ$, ECR, or exchange gates depending on design. | Fast gates and integrated electrical control. | Decoherence, leakage, crosstalk, cryogenic wiring, and routing. |
| Trapped ions | Hyperfine states of charged atoms in electric traps and vacuum. | Focused Raman or selected microwave drives, phase control, fluorescence. | Shared motion or transport to gate zones. $XX$/$ZZ$ entanglers. | Precise operations, long-lived states, flexible pair access. | Slower gates, motional heating, transport, and limited gate-zone parallelism. |
| Neutral atoms | Hyperfine states of uncharged atoms in laser traps and vacuum. | Raman/microwave drives, local light shifts, state-selective imaging. | Rydberg interactions and movable arrays. Controlled-phase gates such as $CZ$. | Large arrays and rearrangeable geometry. | Atom loss, trap-light noise, optical crosstalk, movement, and measurement/reset costs. |

## What current hardware can do

**Universal gate-based devices on all three platforms can express the same quantum algorithms.** Hardware changes how the circuit is compiled: which native gates implement it, which pairs can interact, and how much time is spent on gates, movement, and measurement. Mid-circuit measurement, reset, and feedback depend on the particular processor and its programming interface. Some neutral-atom machines expose analog simulation rather than arbitrary gate circuits.

| Platform | $T_1$: population lifetime | Phase-coherence examples | What a program can request | Main scheduling constraint |
| --- | --- | --- | --- | --- |
| Superconducting | Willow mean: $68\,\mu\mathrm{s}$. | $T_2=89\,\mu\mathrm{s}$ with CPMG refocusing. [Measurement](https://www.nature.com/articles/s41586-024-08449-y) | Single-qubit rotations and entangling gates on connected pairs. | Fast gates, but short memory and extra routing for distant pairs. |
| Trapped ions | Ground-state hyperfine populations can be long-lived. | Single-ion example: Ramsey $1.6\,\mathrm{s}$. Refocusing gives a fitted $5500\,\mathrm{s}$ from data through $960\,\mathrm{s}$. [Measurement](https://www.nature.com/articles/s41467-020-20330-w) | Addressed rotations and entangling gates through shared motion or transport. | Longer memory, but gates, transport, and cooling consume time. |
| Neutral atoms | Caesium-array example: $119\,\mathrm{s}$ for depolarization. | Ensemble Ramsey $T_2^*=14\,\mathrm{ms}$. XY16 refocusing gives $T_2=12.6\,\mathrm{s}$. [Measurement](https://www.nature.com/articles/s41586-025-09641-4) | Addressed rotations and Rydberg gates, with atom rearrangement to select pairs. | Movement, atom loss, and measurement/reset procedures affect the schedule. |

These are measured examples, not platform-wide constants. The coherence measurements and programmable operations can come from different devices within each platform. $T_2^*$ is measured without refocusing pulses. Refocusing extends storage coherence, but those pulses must fit around the computation. Compare coherence with the durations and errors of the actual circuit, rather than treating $T_2$ as an allowed program runtime.
