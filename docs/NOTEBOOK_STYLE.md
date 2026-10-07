# Notebook style guide

Use this guide when drafting or editing this tutorial series. It distills the effective teaching style of `shor_tutorial.ipynb` and its continuation, `surface_code.ipynb`. It describes a voice and a working pattern, not a mandatory section template. Preserve the author's learner notes, inline TODOs, and completed work.

## The central pattern

**Explain the question → define the objects → run a small example → interpret the result.**

Start with a physical question: “How can we protect a qubit using checks that involve only nearby qubits?” State the notebook's concrete task and assumed knowledge in a few sentences. Give readers enough context to understand each cell without the original conversation.

Develop one example through the notebook. In Shor, the same encoder and eight checks lead into decoding and a memory experiment. In the surface code, the written tutorial's numbered patches lead into states, scheduled ancilla measurements, errors, and lattice surgery. Introduce a new tool or representation only when it solves the next problem.

## Prose and notation

- Write direct, short paragraphs. State the point before its derivation. Prefer “An X error flips these Z-check signs” to abstract descriptions of what the next section will explore.
- Explain the concept before the code. After a table or plot, explain the observation that matters.
- Define every new symbol, register label, bit convention, and index at first use. For measurement bits, explicitly give `0 ↔ +1` and `1 ↔ −1`.
- Distinguish physical Paulis from logical Paulis. State the qubit numbering and logical-operator convention before printing strings.
- Keep one convention throughout an example. If a library uses different coordinates or representatives, give the mapping or explicitly introduce the new convention.
- Use equations for the actual rule being implemented, followed by one concrete instance. Avoid algebra that does not help interpret the experiment.
- Introduce technical words when needed, alongside their meaning. “We track a correction in a Pauli frame” needs an explanation of how it changes a later readout.
- Match the approachable voice of Shor without copying its accidental numbering, unchecked promises, or imprecise sentences. An intro must promise only what the notebook actually demonstrates.

## Code cells

- Prefer visible physics over general software architecture. Use descriptive names such as `logical_z`, `syndrome_of`, `check_round`, and `run_memory`.
- Keep cells focused. Separate defining a circuit, running it, and plotting results when each needs its own explanation.
- Use a short helper for a repeated operation; introduce what it does before its first use. Avoid a large hidden helper module that contains the experiment itself.
- Explain non-obvious library conventions in nearby comments: identity symbols, measurement record order, simulator qubit IDs, and logical-outcome ordering.
- Put meaningful checks next to the claim: compare ancilla syndromes with commutation, test corrections on single-qubit errors, or check every branch of a small operator identity.
- A circuit diagram is usually clearer than a gate-order table. Tables suit error/syndrome/correction comparisons and numerical outcomes.
- Provide small default runs with fixed seeds. Keep optional larger runs explicit, and show sample counts and parameter definitions.
- Save useful, verified outputs for readers browsing on GitHub. Do not churn outputs or cell IDs unrelated to an edit.

## Plots and interpretation

Use readable static plots for the published notebook. Label axes with the measured quantity, noise convention, and duration where relevant. Use consistent X/Z colors and mark qubit/check labels clearly. Prefer a few interpretable panels to a wall of diagrams.

For sampled failure rates, show counts or uncertainty intervals. Explain what a zero count means. Keep logical-X errors distinct from failures of a logical-X readout. Compare distances at a stated duration and never infer an asymptotic threshold from a small sweep.

## Scope and correctness

- Separate ideal state preparation, ideal Pauli-product measurement, scheduled ancilla circuits, and noisy circuit experiments. State where assumptions change.
- A joint logical parity must not be described as separate measurements of its factors. Show what information is retained.
- Clearing a syndrome is not the same as restoring the logical state. Include an explicit logical-error counterexample when teaching recovery.
- Basis-state tests do not establish arbitrary quantum-state action. Use complementary-basis tests and, when practical, a complete operator identity.
- Claims of noisy fault tolerance require appropriate circuit checks and decoding; successful noiseless tests alone are not enough.
- Cite primary software documentation near the relevant API or in a short reference list. Validate the installed version instead of copying an API from an older notebook untested.

## What not to add automatically

Do not impose reading assignments, quizzes, a closing exercise section, or blank answer cells. Inline questions can help, but they are not required. Do not add distance-enumeration code merely because distance is mentioned. Do not let a tutorial turn into a long API reference, performance benchmark, or summary of the authoring process.

## Before delivery

Execute from a fresh kernel, inspect the saved diagrams and plots, verify the stated invariants, and check that each promised topic is actually covered. Record limitations truthfully: execution is not a full mathematical or pedagogical review. Keep maintenance guides and validation records on development branches; publish reader-facing notebooks and necessary runtime files to `main` only when authorized.

## Companions to a written tutorial

Use the current written source as the reference for qubit numbering, orientation, colors, check supports, gate orders, logical representatives, and outcome conventions. Identify the companion tutorial by title. Match its section progression; use code to demonstrate the claims rather than replacing it with a separate library-generated example. Explain an intentional change of scale, such as distance five for the schedule and distance three for the seam.

For the surface-code companion, use Loom for quantum operators, circuits, and simulation, including its bundled Clifford simulator. NumPy may verify small linear-algebra identities; Matplotlib may draw diagrams. Do not introduce a second quantum SDK or an external simulator interface. Distinguish selected preparation branches from deterministic encoders, and ideal sequential seam measurements from scheduled noisy surgery.

When explaining gate order, show the actual circuit and separate three questions: does the layer avoid collisions, does interleaving preserve the intended measurements, and how does an ancilla fault spread? Include a collision-free counterexample with inconsistent shared-qubit ordering. Plot from the circuit data so the figure and executed order agree. Keep physical-qubit simulations separate from logical-qubit operator proofs, and state what each verifies.
