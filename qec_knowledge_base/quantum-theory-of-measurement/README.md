# Quantum theory of measurement

**How does a quantum state become a classical measurement record, and what happens to the quantum system along the way?**

## Learning path

| Chapter | Leading question | Important concepts |
| --- | --- | --- |
| [1. Basics of measurement](basics-of-measurement.md) | How do preparations, measurement records, and state changes fit together? | Statistical duality, Hilbert spaces, density operators, effects, POVMs, operations, dilations, Kraus and Choi representations, probes, instruments. |
| [2. Incompatibility and uncertainty](incompatibility-and-uncertainty.md) | Which measurements can be combined, and what can their records tell us? | Joint measurability, sequential measurements, uncertainty, informational completeness, reconstruction, calibration. |

## Conclusion

A POVM specifies the probabilities of a classical record. An instrument also specifies the quantum state left after each result. A probe model explains how an interaction produces both.

Combining measurements requires more than collecting several labels: their distributions must match the intended observables. The instrument determines disturbance, while compatibility limits which target statistics one apparatus can reproduce. Unsharp measurements can still reveal a complete state across repeated preparations, provided the detector is calibrated and the data contain independent information.

For quantum software, specify both what the record must reveal and what quantum information must survive. These two requirements connect readout, feedback, tomography, and QEC syndrome extraction.

Last updated: 2026-11-09
