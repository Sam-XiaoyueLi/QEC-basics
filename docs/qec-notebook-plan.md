# Companion notebook plan: Quantum Error Correction

Status: plan only. The notebook is not implemented yet.

## Purpose and audience

Turn the second tutorial's repetition-code circuits into experiments a reader can run and modify. Assume the first tutorial and basic Python/linear algebra. Introduce circuit notation and each library operation as it becomes necessary. Each activity should follow **predict → run → explain → change one thing**.

Use `02_quantum_error_correction.ipynb` as the eventual filename. The essay explains the concepts and derivations; the notebook lets readers inspect states, inject errors, collect syndrome records, and measure performance. Keep introductory prose short and refer back to the relevant essay section instead of reproducing it.

## Proposed tools

- NumPy for transparent state-vector and operator calculations, and the small classical hidden-state model used for repeated-round decoding.
- Matplotlib for circuit-independent state, syndrome-history, and failure-probability plots.
- Qiskit and a local simulator for circuit drawings and measured circuit experiments, after checking the current APIs at implementation time.
- No hardware account should be needed for the core notebook. Hardware execution and specialized stabilizer simulators are later extensions.

Record tested package versions and the random seed. Save representative outputs so the published notebook is readable without executing it. Define a consistent convention: write basis strings as q1 q2 q3, and explicitly translate any simulator's displayed bit order. Name syndrome bits s1 for Z1Z2 and s2 for Z2Z3; never infer ordering from a raw result string.

## Learning sequence

### 1. A short classical warm-up — essay Sections 1 and 4

Encode 0 as 000 and 1 as 111. Inject each possible single flip, compute the two XOR checks, and apply majority decoding. Compare single-bit error probability p with the exact repetition failure probability 3p²−2p³. Show one two-flip counterexample so that readers see why the decoder needs assumptions.

Prediction: which checks change for a middle-bit flip? What if two bits flip?

Output: a syndrome table and a compact exact-probability plot. Do not call the crossing at p=1/2 a general QEC threshold.

### 2. Encode an arbitrary qubit — essay Section 8

Prepare cos(theta/2)|0> + exp(i phi)sin(theta/2)|1>, append two zeros, and apply CNOT 1→2 and 1→3. Compare the resulting vector with alpha|000>+beta|111>. Use a nontrivial relative phase so a check based only on populations cannot accidentally pass.

Prediction: does this produce three copies of the original qubit?

Output: an encoding circuit and an amplitude comparison, with global-phase-insensitive state fidelity. Explicitly compare with the different state |psi> tensor |psi> tensor |psi>.

### 3. Build and understand one ZZ check — essay Section 9

Add a fourth qubit as an ancilla. Apply data-to-ancilla CNOTs, then inspect the joint state before measurement. Compute each measurement branch using projectors and compare with sampled circuit outcomes. Use both even-parity superpositions and inputs spanning even and odd parity sectors.

Verify the identity U† Z_a U = Z1 Z2 Z_a numerically. Explain that the ancilla's initial +1 Z eigenvalue is what removes Z_a from the effective data observable.

Prediction: will the ancilla distinguish |00> from |11>? What is destroyed by measuring the data individually instead?

Output: a parity circuit, branch probabilities, and conditional data-state fidelity. Do not use a mixed-state purity assumption after discarding an ancilla or measurement record.

### 4. Extract the full repetition syndrome and recover — essay Sections 4 and 9

Use three data qubits and two measurement ancillas for clarity. Inject I, X1, X2, X3 before a complete check round. Display syndrome bits in the established order. Apply the corresponding correction in simulation and compare the recovered data state to the encoded input.

Prediction: what happens for X2X3, which has the same syndrome as X1?

Output: circuit, syndrome table, recovery fidelities, and a logical-failure counterexample. Use several arbitrary encoded states, not only |0_L>.

### 5. Continuous errors and the code's limitation — essay Sections 2 and 7

Inject R_X1(epsilon). Calculate conditional syndrome probabilities and compare them with cos²(epsilon/2) and sin²(epsilon/2). Recover each nonzero-probability branch and verify the logical state. Separately inject R_Z1(epsilon) and show that the checks stay green while logical coherence changes.

Compare logical X expectation or phase-sensitive fidelity, rather than only computational-basis populations, to expose the undetected phase error.

Output: syndrome probability versus epsilon and a phase-sensitive logical observable. State explicitly that this is not a model in which every coherent rotation is assumed to be a stochastic Pauli error.

### 6. Initialization and terminal logical measurement — essay Sections 8 and 11

Prepare |0_L>, |1_L>, and |+_L>. Read logical Z using decoded physical Z results. Read logical X using X measurements on each qubit and the product of their eigenvalues. Demonstrate that these are terminal measurements and are different from nondestructive syndrome extraction.

Output: expected outcome distributions for the three initial states. Show that a single individual X-readout error can reverse the logical X product.

### 7. Fault timing inside an extraction circuit — essay Section 10

Verify the four CNOT Pauli propagation identities. Insert faults at named circuit locations, for example a data X before versus after its CNOT, an ancilla X just before readout, and an ancilla Z between its two CNOTs.

Track both the data error and the reported syndrome. Keep the same explicitly drawn gate schedule as the essay. Show one example in which the record and data are both affected, and one in which only the recorded bit changes.

Output: annotated circuits and a table of predicted versus simulated effects. Do not apply the simple pre-round syndrome table blindly to mid-round faults.

### 8. Repeated checks with reporting noise — essay Section 12

Begin with the explicitly simplified phenomenological model: independent X errors with probability p on each data qubit between rounds, ideal check extraction, and independent syndrome-report flips with probability q. Keep state preparation ideal initially. Model terminal data readout separately, with an explicit error probability.

No physical corrections are applied between rounds. Display raw syndrome bits and detection events d_i(t)=s_i(t) XOR s_i(t−1). Compare a persistent data error with one bad report. Include boundary data faults and wrong final readout to show why some event histories terminate at boundaries.

Output: a space–time grid with raw reports and changed checks distinguished. Explain that circuit-level noise can create correlations absent from this model.

### 9. Decode a small memory experiment — essay Section 13

For three data qubits, use an exact small hidden-state model before introducing a general-purpose matching decoder. Track the eight possible data bit strings, their transition probabilities under p, and the likelihood of the two reported checks under q. Start from a uniform prior over the two legal codewords, not the known prepared answer.

Preserve the initial logical label in the inference (for example, track joint hypotheses for initial logical bit and current three-bit string). Condition on all syndrome reports and the final noisy data readout, then choose the maximum-posterior initial logical bit. The final-state marginal alone is not enough if the goal is to infer the stored initial bit.

The simulator keeps the actual prepared bit only for scoring. Explain the transition and observation probabilities with one short hand-worked example before running the decoder. Benchmark both initial logical values and average fairly.

Compare full-history decoding with final majority voting under the same p, q, number of intervals, and terminal readout model. If a naive per-round correction baseline is included, define it and account for its action when calculating later detection events.

Output: one worked decoded history and Monte Carlo logical failure estimates with binomial confidence intervals. Report number of trials, seed, T, p, q, and final readout noise. Clearly label simulated results.

### 10. Read the performance result honestly

Plot logical failure probability versus storage duration/rounds under a stated time convention. Include an unencoded baseline with the same elapsed storage time and appropriate terminal readout assumptions. Explain that extra physical gates and idle durations require explicit circuit-level modeling before claiming a hardware advantage.

Do not claim a threshold from one three-qubit code. Do not claim protection of arbitrary quantum states from a logical-Z memory benchmark. Revisit the undetected phase example to make the limitation visible.

End with an exercise asking which additional checks would be needed to detect phase errors and why adding arbitrary X checks may conflict with the existing Z checks. This motivates the surface-code tutorial.

## Verification and completion criteria

- Restart and run all cells without credentials or a hardware backend.
- Establish displayed qubit and syndrome ordering with explicit basis-state cases.
- Check recovery on phase-sensitive encoded inputs, including an input entangled with an optional reference qubit for a stronger extension.
- Verify projectors, CNOT propagation, and exact small-rotation formulas independently of sampled counts.
- Validate the tiny decoder against exhaustive enumeration for a few short histories. Test perfect-readout and zero-noise limits; ensure the true prepared logical label is not supplied to the decoder.
- Distinguish exact results, sampled estimates, and assumptions in every plot caption. Include uncertainty for failure estimates and handle zero observed failures with a nonzero upper confidence bound.
- Keep code cells short and explain what the reader should notice before each output.

## Suggested next working session

First build activities 1–4 as one connected experiment and establish conventions. Then add 5–7 to test the physics, followed by the repeated-round model and decoder in 8–10. If the notebook becomes too long, retain one file initially with clear optional sections; split into a circuit lab and a memory/decoding lab only after reviewing the learner flow.

The implementation target is a local simulated experiment, not a hardware demonstration. Hardware execution, surface-code matching, general noise-channel theory, and full fault-tolerant scheduling remain later extensions.
