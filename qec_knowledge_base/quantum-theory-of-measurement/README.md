# Quantum theory of measurement

**How do we model quantum measurements so that we can correctly predict their results, simulate their effects, and use their outcomes to control a quantum program?**

A measurement produces a classical result and changes the quantum state. Software must model both when computation continues: outcome probabilities determine which branch runs, and the conditional state determines what happens next. This matters for mid-circuit measurements, reset, feedback, and QEC syndrome extraction. For terminal readout, only the result statistics may matter.

In a QEC cycle, ancilla measurements produce syndrome bits, a decoder uses them to choose corrections or update a Pauli frame, and the data qubits continue computing. A correct model must capture both the reliability of those bits and the measurement's effect on the data.

## Learning path

| Topic | Leading question | Important concepts |
| --- | --- | --- |
| [1. States and subsystems](states-and-subsystems.md) | What information describes the input? | Density matrices, mixtures, superpositions, coherence, entanglement, tensor products, partial trace. |
| [2. Effects and POVMs](effects-and-povms.md) | What results can the detector report? | Effects, Born rule, projective measurements, POVMs, readout errors, post-processing, Naimark dilation. |
| [3. Operations and channels](operations-and-channels.md) | How can the quantum state change? | Kraus maps, complete positivity, quantum channels, reset, Choi matrices, Stinespring dilation. |
| [4. Instruments and apparatus](instruments-and-apparatus.md) | What state accompanies each result? | Instruments, conditional states, measurement backaction, ancillas, feedback, parity measurements. |
| [5. Compatibility and disturbance](compatibility-and-disturbance.md) | What happens when measurements are combined? | Sequential measurements, joint measurability, disturbance, repeatability, preparation and measurement uncertainty. |
| [6. Tomography](tomography.md) | What can the records tell us about the input? | Informational completeness, state reconstruction, finite-shot uncertainty, measurement calibration. |

Last updated: 2026-11-09
