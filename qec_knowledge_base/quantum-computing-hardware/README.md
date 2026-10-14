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

Qubits can be encoded in superconducting circuit levels, atomic states, semiconductor spins, or photons. Each platform supplies different controls, interactions, and noise sources. [Semiconductor example](https://www.nature.com/articles/s41586-025-09531-9), [photonic example](https://www.nature.com/articles/s41586-024-08406-9)

Superconducting qubits, trapped ions, and neutral atoms are prominent gate-based platforms with demonstrated multi-qubit control and error-correction experiments. They illustrate three useful hardware choices: fast electrical control on a chip, precise atomic control through shared ion motion, and large rearrangeable atom arrays. Their different interactions determine native gates and connectivity.

## Superconducting qubits

### What are zero and one?

A **Josephson junction** has two superconductors separated by a thin insulating barrier. Coherent Cooper-pair tunnelling makes it a **nonlinear inductor**. In parallel with a large capacitor, it forms a transmon's **anharmonic oscillator**. Its quantum wavefunctions have discrete energies. We use the ground level as $|0\rangle$ and the first excited level as $|1\rangle$.

The junction's nonlinearity makes successive gaps unequal:

$$
E_1-E_0\ne E_2-E_1.
$$

A selective pulse can therefore control the lowest pair while avoiding $|2\rangle$. The pair supports $\alpha|0\rangle+\beta|1\rangle$. Occupying higher levels is **leakage**. [Transmon paper](https://arxiv.org/abs/cond-mat/0703002)

### Protection and coherence

Millikelvin cooling suppresses thermal excitation. Low-loss materials, shielding, and filtered control lines reduce unwanted energy exchange and phase noise. Defects, stray radiation, and crosstalk remain limitations. Willow reports mean $T_1=68\,\mu\mathrm{s}$ and $T_{2,\mathrm{CPMG}}=89\,\mu\mathrm{s}$ with refocusing pulses. These are device measurements, not fixed properties of all transmons. [Experiment](https://www.nature.com/articles/s41586-024-08449-y)

### Preparation, single-qubit gates, and readout

**Prepare zero:** allow relaxation toward the ground state, or measure and apply $X$ when the result is one. [Reset protocols](https://www.nature.com/articles/s41467-021-26205-y)

**Drive:** the resonant frequency is $f_{01}=(E_1-E_0)/h$, typically a few gigahertz. This energy gap calls for microwaves. An optical laser's carrier is far above the transition. In the frame rotating at $f_{01}$, pulse phase selects an axis in the $X$–$Y$ plane. Strength and duration set the angle. [Control review](https://www.nature.com/articles/s41534-016-0004-0)

- **$X$:** choose the $X$-axis phase and a calibrated $\pi$ pulse. It swaps zero and one, up to global phase.
- **$Y$:** use the same rotation angle with drive phase shifted by $\pi/2$.
- **$Z$:** update the tracked phase frame by $\pi$ and adjust subsequent controls. This **virtual $Z$** implements $\alpha|0\rangle+\beta|1\rangle\to\alpha|0\rangle-\beta|1\rangle$ without a separate physical pulse. [Virtual Z gates](https://arxiv.org/abs/1612.00858)
- **Readout:** probe a coupled resonator whose microwave response depends on the qubit state. The calibrated response is classified as zero or one. [Readout](https://www.nature.com/articles/s41534-016-0004-0)

### Interactions and native gates

Capacitive or inductive couplings connect selected circuits, often through tunable couplers. They exchange excitations or shift joint-state energies. A conditional phase of $\pi$ on $|11\rangle$, after compensating single-qubit phases, gives **$CZ$**. One implementation exploits coupling to the nearby $|02\rangle$ level. Other designs favour exchange or ECR gates. Native single-qubit operations include rotations and virtual $Z$. Fixed connectivity creates routing costs for distant qubits. [Coupled-circuit example](https://www.nature.com/articles/ncomms11059)

![A capacitor and Josephson junction in parallel, junction materials, and unequal circuit energy levels](assets/superconducting.png)

## Trapped ions

### What are zero and one?

An **ion is an atom with a net electric charge**. Oscillating and static electric fields confine ions in vacuum. Each ion carries one qubit in two selected internal states.

For a common $^{171}\mathrm{Yb}^{+}$ encoding,

$$
|0\rangle=|F=0,m_F=0\rangle,
\qquad
|1\rangle=|F=1,m_F=0\rangle.
$$

$F$ labels the total angular momentum formed by coupling electron and nuclear angular momenta. $m_F$ labels its projection along the chosen field axis. Both qubit states lie in the electronic ground manifold, with different hyperfine energies. [State encoding](https://www.nature.com/articles/s41467-020-20330-w)

### Protection and coherence

High vacuum suppresses collisions. Laser cooling controls motion, while stable fields, magnetic shielding, and stable drive references protect phase. A second ion species can cool shared motion without resonantly exciting the stored qubits. Ground-state hyperfine relaxation is weak, giving long population lifetimes. Unwanted light and microwave leakage can still change populations. A single-ion memory study measured Ramsey coherence of $1.6\,\mathrm{s}$ and, with dynamical decoupling, fitted a coherence time near $5500\,\mathrm{s}$ from measurements through $960\,\mathrm{s}$. [Memory experiment](https://www.nature.com/articles/s41467-020-20330-w)

### Preparation, single-qubit gates, and readout

**Prepare zero:** optical pumping repeatedly excites unwanted states and lets them decay. Population accumulates in the chosen zero state, which stops absorbing the pumping light.

**Address one ion:** focus a laser beam onto it, steer the beam to another ion, or shuttle the chosen ion into a control zone. A **Raman drive** uses two laser frequencies whose difference matches the qubit splitting. Their relative phase selects the $X$–$Y$ axis, and pulse strength and duration set the angle. [Individual addressing](https://www.nature.com/articles/s41467-024-53405-z)

- **$X$:** apply an addressed Raman $\pi$ pulse with the phase defining the $X$ axis.
- **$Z$:** update the tracked phase frame, or use light to shift the two energies differently and accumulate a relative phase of $\pi$.
- **Readout:** a state-selective optical transition scatters photons for a bright state and few photons for a dark state. Photon counts identify the outcome. [Ion controls](https://www.nature.com/articles/npjqi201634)

### Interactions and native gates

Electric repulsion couples the ions' motion into shared vibrational modes. State-dependent laser forces couple selected qubits to those modes. A timed sequence closes the motional trajectory while leaving an entangling operation on the internal states. This naturally produces **$XX$ or $ZZ$ interactions**, with the chosen spin axis set by controls or basis rotations. A $ZZ$ interaction produces $R_{ZZ}(\theta)=e^{-i\theta Z\otimes Z/2}$. [Motion-mediated gates](https://www.nature.com/articles/s41534-021-00489-w)

Shared modes or ion transport provide flexible pair access. Gate time, motional heating, transport, and the number of gate zones limit throughput and parallelism. Helios exposes native phase-controlled rotations, virtual $R_z$, and $R_{ZZ}$. [Hardware instructions](https://docs.quantinuum.com/systems/user_guide/hardware_user_guide/helios.html)

![Trapped ions, their internal qubit levels, and shared motion used for entangling gates](assets/trapped-ions.png)

## Neutral atoms

### What are zero and one?

A **neutral atom has no net electric charge**. It is also held in vacuum, but its confinement comes from an **optical tweezer**: a laser beam focused into a tiny spot. The light's electric field displaces the electron cloud slightly relative to the nucleus, inducing an electric dipole. For a typical red-detuned trapping laser, whose frequency lies below an atomic resonance, the atom's energy is lower near the bright focus. Moving away raises its energy, creating a restoring force that holds it near the focus. An array of spots holds an array of atoms. [Optical trapping](https://arxiv.org/abs/physics/9902072)

For example, choose two ground-state hyperfine levels of $^{87}\mathrm{Rb}$:

$$
|0\rangle=|F=1,m_F=0\rangle,
\qquad
|1\rangle=|F=2,m_F=0\rangle.
$$

The same electron and nuclear angular momenta combine into different total-angular-momentum states. An atom in the first state represents zero, and an atom in the second represents one. Both occupy the same trap and electronic ground manifold. A drive prepares superpositions of these two internal configurations. $F$ and $m_F$ have the meanings defined for ions. [Rubidium encoding](https://www.nature.com/articles/s41586-025-09848-5)

### Protection and coherence

Vacuum suppresses collisions. Laser cooling reduces motion, and stable fields and trapping light limit phase noise. Trap-light scattering can change internal states, intensity variations shift their energies, and atoms can be lost. These are major control and scaling constraints. A separate caesium-array experiment reports population-depolarization $T_1=119\,\mathrm{s}$, ensemble Ramsey $T_2^*=14\,\mathrm{ms}$ without refocusing, and $T_2=12.6\,\mathrm{s}$ with XY16 pulses. Long population lifetime therefore does not guarantee long unrefocused phase coherence. [Array experiment](https://www.nature.com/articles/s41586-025-09641-4)

### Preparation, single-qubit gates, and readout

**Prepare zero:** optical pumping transfers population into the selected internal state. Focused Raman beams address individual atoms. Other implementations combine global microwave rotations with local light-induced energy shifts. Steering tweezers rearranges the atoms.

- **$X$:** drive the storage-state transition with a resonant $\pi$ pulse and the $X$-axis phase.
- **$Z$:** shift the two energies differently with focused light to accumulate a relative phase of $\pi$. Compatible control systems can also track phase-frame updates.
- **Readout:** state-dependent fluorescence or mapping the internal state to position or atom loss distinguishes zero and one. Retaining the atom depends on the method. [Control](https://www.nature.com/articles/s41586-023-06481-y), [Readout and reuse](https://www.nature.com/articles/s41586-025-09848-5)

### Interactions and native gates

Ground-state atoms interact weakly at typical tweezer separations. A laser temporarily couples a storage state to a highly excited **Rydberg state**, denoted $|r\rangle$. Its large electronic extent enables strong interactions between atoms. The doubly excited state's energy shifts, making excitation of one atom change the response of its neighbour. Under **Rydberg blockade**, that shift suppresses resonant excitation of the second atom.

A laser sequence converts this conditional response into a phase, producing **$CZ$** while returning population to the storage states. Moving atoms into range selects interacting pairs. Native operations include storage-state rotations and Rydberg controlled-phase gates. Optical addressing, movement, loss, and reset determine scheduling costs. [Gate experiment](https://www.nature.com/articles/s41586-023-06481-y)

![Optical tweezer confinement, rubidium zero and one states, and Rydberg blockade](assets/neutral-atoms.png)

## Comparison

| Platform | Qubit and confinement | Control and readout | Interaction and native gates | Advantages | Limitations |
| --- | --- | --- | --- | --- | --- |
| Superconducting | Lowest circuit levels on a cryogenic chip. | Microwave rotations, virtual $Z$, resonator readout. | Engineered coupling graph. $CZ$, ECR, or exchange gates depending on design. | Fast gates and integrated electrical control. | Decoherence, leakage, crosstalk, cryogenic wiring, and routing. |
| Trapped ions | Hyperfine states of charged atoms in electric traps and vacuum. | Focused Raman or selected microwave drives, phase control, fluorescence. | Shared motion or transport to gate zones. $XX$/$ZZ$ entanglers. | Precise operations, long-lived states, flexible pair access. | Slower gates, motional heating, transport, and limited gate-zone parallelism. |
| Neutral atoms | Hyperfine states of uncharged atoms in laser traps and vacuum. | Raman/microwave drives, local light shifts, state-selective imaging. | Rydberg interactions and movable arrays. Controlled-phase gates such as $CZ$. | Large arrays and rearrangeable geometry. | Atom loss, trap-light noise, optical crosstalk, movement, and measurement/reset costs. |

## Demonstrated capabilities

As of the sources checked on **2026-10-14**, the three platforms show complementary progress. Superconducting Willow demonstrated logical-memory error suppression as surface-code distance increased, while IBM supplies programmable Heron and Nighthawk processors. [Willow](https://www.nature.com/articles/s41586-024-08449-y), [IBM](https://quantum.cloud.ibm.com/docs/en/guides/processor-types) Trapped-ion Helios combines 98 qubits with transport-enabled all-to-all access and average two-qubit infidelity $7.9\times10^{-4}$. [Helios](https://arxiv.org/abs/2511.05465) Neutral-atom experiments have integrated repeated QEC, logical operations, and reuse in a processor of up to 448 atoms, and separately demonstrated coherent arrays exceeding 6,100 atoms. [Logical processing](https://www.nature.com/articles/s41586-025-09848-5), [Array scale](https://www.nature.com/articles/s41586-025-09641-4) These results establish useful ingredients for larger fault-tolerant computers. Physical-qubit counts, stored coherence, and reliable logical operations measure different capabilities.

## Conclusions

- **A hardware qubit** is a chosen pair of physical states whose populations and relative phase can be prepared, preserved, controlled, and measured.
- **A single-qubit gate** changes their amplitudes or relative phase. Calibrated pulse strength, duration, frequency, and phase implement the required rotation. Some operations are tracked through phase-frame updates.
- **Readout** couples the state to a classical signal, such as microwave response or photon counts. Calibration converts that signal into a bit. Readout can change the quantum state, and reset prepares it for reuse.
- **A two-qubit gate** uses a controlled interaction so joint evolution cannot be reduced to independent single-qubit operations. The coupling graph, motion, or atom positions determine pair access. Compilers build requested gates from the native set.
- **Protection** combines isolation, cooling, shielding, stable controls, and refocusing. QEC adds redundant encoding and repeated checks for reliable logical computation. Compare operation times and errors alongside $T_1/T_2$.
- **Other platforms** include semiconductor electron or hole spins in quantum dots, nuclear and defect-centre spins, and photonic encodings. They use different confinement, control, and interconnect mechanisms. [Semiconductor example](https://www.nature.com/articles/s41586-025-09531-9), [Photonic example](https://www.nature.com/articles/s41586-024-08406-9), [Defect spins](https://arxiv.org/abs/1302.3288)
