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

**The essence of quantum computing hardware is to select two addressable states, suppress unwanted interactions, and provide controlled coupling for gates and readout.** A gate-based computer needs scalable, well-characterized qubits that can be initialized in known states, controlled with universal gates, and measured individually. Their populations and phase information must survive long enough to perform the required operations. These are the five **DiVincenzo criteria**. [Original paper](https://arxiv.org/abs/quant-ph/0002077)

### Relaxation and phase stability

Two time scales quantify this survival: **$T_1$ measures energy relaxation**, which changes the populations, and **$T_2$ measures the decay of phase coherence**, which reduces interference. Both can be visualized on the Bloch sphere.

On the Bloch sphere introduced in Tutorial 0, the north pole is $|0\rangle$ and the south pole is $|1\rangle$. The height encodes the population difference, and the angle around the vertical axis encodes the relative phase. Noise can shorten the Bloch vector, moving its tip inside the sphere.

| Time scale | Physical change | Bloch-sphere picture |
| --- | --- | --- |
| $T_1$: energy relaxation | The excited-state population decays as the qubit releases energy. | For relaxation to the ground state, the vector approaches the north pole. |
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

Qubits can be encoded in superconducting circuit levels, atomic states, semiconductor spins, or photons. Each platform supplies different controls, interactions, and noise sources. [Semiconductor example](https://www.nature.com/articles/s41586-025-09531-9), [photonic example](https://www.nature.com/articles/s41586-024-08406-9)

Superconducting qubits, trapped ions, and neutral atoms are prominent gate-based platforms with demonstrated multi-qubit control and error-correction experiments. They illustrate three useful hardware choices: fast electrical control on a chip, precise atomic control through shared ion motion, and large rearrangeable atom arrays. Their different interactions determine native gates and connectivity.

## Superconducting qubits

### Qubit and initialization

A **Josephson junction** consists of two superconductors separated by a thin insulating barrier. Cooper pairs tunnel coherently through the barrier, making the junction act as a **nonlinear inductor**. Connecting it in parallel with a large capacitor forms an **anharmonic oscillator**, commonly implemented as a transmon.

The circuit's charge and superconducting phase are quantum variables. Its wavefunction is confined in a potential well, which admits only certain stationary states with discrete energies. These states form the oscillator's energy levels, labelled $|0\rangle,|1\rangle,|2\rangle,\ldots$.

A harmonic oscillator has equally spaced energy levels. The Josephson junction adds a nonlinear correction, making the gaps different:

$$
E_1-E_0\ne E_2-E_1.
$$

The unequal gaps let a selective pulse address $|0\rangle\leftrightarrow|1\rangle$ without significantly exciting $|2\rangle$. The lowest pair therefore serves as a qubit, supporting superpositions $\alpha|0\rangle+\beta|1\rangle$. Population in higher levels is **leakage**. [Transmon paper](https://arxiv.org/abs/cond-mat/0703002)

**Why microwaves?** For resonant control, the drive frequency matches the energy gap:

$$
f_{01}=\frac{E_1-E_0}{h}.
$$

Typical transmon circuit parameters give transition frequencies of a few gigahertz, in the microwave range. An optical laser's carrier frequency is far above this transition. [Circuit and control review](https://www.nature.com/articles/s41534-016-0004-0)

**Initialize to zero:** cooling favours the ground state. An active-reset option measures the qubit and applies an $X$ pulse if it is in $|1\rangle$, returning it to $|0\rangle$. Each qubit has an individually addressable control channel. [Reset protocols](https://www.nature.com/articles/s41467-021-26205-y)

### Single-qubit control: X, Y, and Z

The energy states $|0\rangle$ and $|1\rangle$ define the computational $Z$ basis, used for readout. In a frame rotating at the qubit frequency, a resonant microwave pulse rotates around an axis in the Bloch sphere's **$X$–$Y$ plane**. Pulse strength and duration set the angle $\theta$. Pulse phase $\phi_d$, measured relative to the controller's reference, sets the axis:

$$
R_{\phi_d}(\theta)
=\exp\!\left[-\frac{i\theta}{2}
\left(\cos\phi_d\,X+\sin\phi_d\,Y\right)\right].
$$

By convention, $\phi_d=0$ gives $R_X(\theta)$ and $\phi_d=\pi/2$ gives $R_Y(\theta)$. For a constant resonant drive, $\theta=\Omega\tau$, where $\Omega$ is the Rabi angular frequency and $\tau$ the pulse duration.

| Gate | How to implement it | Example |
| --- | --- | --- |
| $X$ | Use an $X$-axis pulse calibrated for $\theta=\pi$. It gives $R_X(\pi)=-iX$, equivalent to $X$ up to global phase. | Exchanges $\lvert0\rangle$ and $\lvert1\rangle$. |
| $Z$ | Apply a **virtual $Z$**: update the qubit's tracked phase frame by $\pi$ and adjust subsequent control phases accordingly. | Changes $\alpha\lvert0\rangle+\beta\lvert1\rangle$ to $\alpha\lvert0\rangle-\beta\lvert1\rangle$, so $\lvert+\rangle\to\lvert-\rangle$. |

A virtual $Z$ needs no separate physical pulse. Its logical effect is carried by the updated reference for subsequent gates. Merely choosing pulse phase $\pi$ produces an axis along $-X$, rather than a $Z$ rotation. [Microwave control and virtual Z gates](https://arxiv.org/abs/1612.00858)

A readout resonator converts the qubit state into a measurable microwave response. [Readout](https://www.nature.com/articles/s41534-016-0004-0)

### Interaction and protection

Capacitive or inductive couplings connect selected circuits, often through tunable couplers. They exchange excitations or shift joint-state energies. A calibrated conditional phase gives a gate such as $CZ$. [Coupled-circuit example](https://www.nature.com/articles/ncomms11059)

Low-loss materials, millikelvin cooling, filtered control lines, and shielding suppress unwanted energy exchange and phase noise. Material defects, stray radiation, and frequency fluctuations remain error sources. **Coherence example:** Willow reports mean $T_1=68\,\mu\mathrm{s}$ and $T_{2,\mathrm{CPMG}}=89\,\mu\mathrm{s}$. CPMG is a refocusing pulse sequence, so this $T_2$ includes active suppression of phase noise. [Willow experiment](https://www.nature.com/articles/s41586-024-08449-y)

![A capacitor and Josephson junction in parallel, junction materials, and unequal circuit energy levels](assets/superconducting.png)

## Trapped ions

### Qubit and initialization

Electromagnetic fields hold charged atoms in vacuum. **One ion carries one qubit in two selected internal states.** A common choice is two hyperfine levels in the electronic ground state, distinguished by the coupled electron and nuclear angular momenta. Both levels can therefore be long-lived. [Ion architecture review](https://www.nature.com/articles/npjqi201634)

**Initialize to zero:** optical pumping repeatedly excites unwanted states and lets them decay by emitting photons. The laser frequencies and polarization make the chosen $|0\rangle$ a state that stops absorbing the pumping light, so population accumulates there. This can prepare an entire register in $|00\ldots0\rangle$. [State preparation](https://www.nature.com/articles/s41467-020-20330-w)

### Individual control: X and Z

Ions are separated by micrometres. A tightly focused laser beam addresses one ion, while beam steering selects another. A QCCD (quantum charge-coupled device) can instead shuttle selected ions into gate zones. [Individual addressing experiment](https://www.nature.com/articles/s41467-024-53405-z), [QCCD operation](https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/helios.html)

A **Raman drive** uses two laser frequencies whose difference matches the qubit splitting. It drives the internal transition without storing the qubit in an optically excited state. Pulse strength and duration set the rotation angle, and relative laser phase sets the $X$–$Y$ axis.

| Operation | Representative implementation |
| --- | --- |
| $X$ | Address the ion with an $X$-axis Raman pulse calibrated for a $\pi$ rotation. It exchanges $\lvert0\rangle$ and $\lvert1\rangle$. |
| $Z$ | Update the tracked phase frame by $\pi$. A physical alternative shifts the two levels differently with light, accumulating a calibrated relative phase. |
| Readout | Illuminate a state-dependent optical transition. Photon counts distinguish a bright state from a dark state. |

Microwaves can also drive hyperfine qubits, with additional spatial or frequency selection needed for individual addressing. Helios implements $R_z$ virtually and exposes phase-controlled single-qubit rotations. [Ion controls](https://www.nature.com/articles/npjqi201634), [Native gates](https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/helios.html)

### Interaction and protection

The ions' electric repulsion couples their motion into shared vibrational modes. State-dependent laser forces couple selected qubits to those modes. A timed pulse sequence returns the motion to its initial condition while leaving an entangling operation on the internal states, such as $XX$ or $ZZ$ up to basis rotations. [Motion-mediated gates](https://www.nature.com/articles/s41534-021-00489-w)

High vacuum suppresses collisions. Laser cooling controls motion, while stable fields, magnetic shielding, and stable drive references preserve phase. Cooling ions of another species can remove motional energy without resonantly exciting the stored qubit. **$T_1$:** ground-state hyperfine qubits have weak spontaneous relaxation. Practical population errors often come from unwanted light or microwave driving.

**Coherence example:** a single $^{171}\mathrm{Yb}^{+}$ memory experiment measured unrefocused Ramsey coherence of $1.6\,\mathrm{s}$. With dynamical decoupling, measurements up to $960\,\mathrm{s}$ gave a fitted coherence time near $5500\,\mathrm{s}$. [Memory experiment](https://www.nature.com/articles/s41467-020-20330-w)

![Trapped ions, their internal qubit levels, and shared motion used for entangling gates](assets/trapped-ions.png)

## Neutral atoms

### Qubit and initialization

Focused lasers hold uncharged atoms in **optical tweezers**, through the interaction between the light and the atom's induced electric dipole. **One atom carries a qubit in two internal states**, commonly two ground-state hyperfine levels. Optical pumping prepares the chosen zero state, using repeated excitation and decay to concentrate population there. [Optical-tweezer review](https://www.nature.com/articles/s41567-021-01357-2)

### Individual control: X and Z

Focused Raman beams address selected atoms. Other implementations combine global microwave rotations with local light-induced energy shifts. Steering the tweezers changes the spatial arrangement.

| Operation | Representative implementation |
| --- | --- |
| $X$ | Apply a resonant $\pi$ rotation with the drive phase defining the $X$ axis. Use local addressing to select the atom. |
| $Z$ | Shift the two qubit levels differently with focused light and let them accumulate a relative phase of $\pi$. Phase-frame updates are also possible with compatible control tracking. |
| Readout | State-selective fluorescence or state-to-position/loss mapping distinguishes the internal states. Atom retention depends on the method. |

Pulse strength and duration set the angle, while drive phase selects the $X$–$Y$ axis, as for ions and superconducting qubits. [Single-qubit control](https://www.nature.com/articles/s41586-023-06481-y), [Local addressing and readout](https://www.nature.com/articles/s41586-025-09848-5)

### Interaction and protection

Ground-state atoms interact weakly at typical tweezer separations. Lasers temporarily excite them to a **Rydberg state**, whose large electronic extent enables strong interactions. For identical atoms with single-atom excitation energy $E_r$, the doubly excited pair has energy

$$
E_{rr}=2E_r+V,
$$

where $V$ is the interaction shift. When $|V|\gg\hbar\Omega$, with $\Omega$ the Rabi angular frequency, exciting one atom suppresses resonant excitation of the second. This **Rydberg blockade** makes the response conditional on the neighbouring qubit, enabling a gate such as $CZ$. The sequence returns population to the storage states. Moving atoms into gate range selects interacting pairs. [Rydberg gate experiment](https://www.nature.com/articles/s41586-023-06481-y)

Vacuum suppresses collisions, laser cooling reduces motion, and stable fields and trapping light limit phase noise. Trap-light scattering can change internal states, while intensity variations shift their energies. Atom loss is an additional error, separate from internal-state $T_1/T_2$.

**Coherence example:** a 6,100-atom caesium array reported $T_1=119\,\mathrm{s}$ for hyperfine depolarization, ensemble Ramsey $T_2^*=14\,\mathrm{ms}$, and $T_2=12.6\,\mathrm{s}$ with XY16 refocusing. Here $T_2^*$ is measured without refocusing pulses. The large difference shows how trapping inhomogeneity and active noise suppression affect the reported time. [Array experiment](https://www.nature.com/articles/s41586-025-09641-4)

![An optical tweezer array, Rydberg excitation, and the shifted double-excitation level behind blockade](assets/neutral-atoms.png)

## How physical structure determines native gates

Coupling changes joint-state energies or exchanges excitations. The available interaction and controls determine which entangling operations are convenient. A compiler combines these **native gates** into the requested circuit.

| Platform | Physical origin of a representative native gate | Pair access |
| --- | --- | --- |
| Superconducting | Coupling nonlinear circuit levels can shift the energy of $\lvert11\rangle$. Accumulating a conditional phase of $\pi$ gives $CZ$, after correcting single-qubit phases. One method uses the nearby $\lvert02\rangle$ level. Other designs favour exchange or ECR gates. [Circuit example](https://www.nature.com/articles/ncomms11059) | Engineered coupling graph. Distant states require routing. |
| Trapped ions | Shared motion converts state-dependent forces into an effective spin–spin interaction. A $ZZ$ interaction directly gives $R_{ZZ}(\theta)$. Other force orientations give $XX$ or $YY$, related by single-qubit basis rotations. [Gate mechanism](https://doi.org/10.1146/annurev-conmatphys-032822-045619) | Shared modes or transport to gate zones. Gate zones limit parallelism. |
| Neutral atoms | Rydberg blockade makes excitation depend on the neighbour's state. Laser sequences turn that conditional response into a phase, giving $CZ$ while returning to storage states. [Experiment](https://www.nature.com/articles/s41586-023-06481-y) | Atoms within gate range. Rearrangement enables new pairs. |

For $Z=\operatorname{diag}(1,-1)$ and interaction energy scale $J$,

$$
H_{\mathrm{int}}=J\,Z\otimes Z
\quad\Rightarrow\quad
U(t)=e^{-iJtZ\otimes Z/\hbar}
=R_{ZZ}(2Jt/\hbar).
$$

Here $R_{ZZ}(\theta)=e^{-i\theta Z\otimes Z/2}$. This exposes the hardware-to-gate connection: **an interaction acting for a controlled time produces the gate angle**. Helios exposes $R_{ZZ}$ in its native instruction set. [Hardware gates](https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/helios.html)

For compilation and scheduling, inspect the device's **gate set, coupling map, durations, errors, and measurement/reset support**. Native $CZ$ can implement CNOT using Hadamards on the target. Physical transport and quantum SWAP gates provide different ways to route information.

## Demonstrated capabilities

Selected milestones checked **2026-10-14**. Physical-qubit counts, array sizes, and logical-memory results measure different capabilities.

| Platform | Demonstrated or available capability | What it tells us |
| --- | --- | --- |
| Superconducting | Google's 105-qubit Willow demonstrated logical error suppression as surface-code distance increased, including distance 7. *Nature* (2025). [Paper](https://www.nature.com/articles/s41586-024-08449-y) | Larger codes can improve logical memory under the tested conditions. |
| Superconducting | IBM documents 156-qubit Heron and 120-programmable-qubit Nighthawk. Revision r2 adds high-speed reset (September 2026). [Devices](https://quantum.cloud.ibm.com/docs/en/guides/processor-types) | Available gate-based hardware with differing connectivity and reset features. These are not logical-qubit counts. |
| Trapped ions | Helios: 98 qubits, transport-enabled all-to-all access, average two-qubit infidelity $7.9(2)\times10^{-4}$ across operation zones. November 2025 preprint. [Paper](https://arxiv.org/abs/2511.05465) | Precise gates and flexible routing at system scale. Gate fidelity alone does not predict algorithm success. |
| Neutral atoms | A reconfigurable processor with up to 448 atoms demonstrated repeated QEC, logical operations, and qubit reuse. *Nature* (online 2025, volume 2026). [Paper](https://www.nature.com/articles/s41586-025-09848-5) | Integration of key fault-tolerant mechanisms. Performance depends on protocol, decoding, and acceptance conditions. |
| Neutral atoms | A separate experiment trapped over 6,100 atoms and measured 12.6(1) s coherence with XY16 dynamical decoupling (a refocusing pulse sequence). *Nature* (2025). [Paper](https://www.nature.com/articles/s41586-025-09641-4) | Large coherent arrays, not a demonstrated 6,100-qubit universal entangling processor. |
