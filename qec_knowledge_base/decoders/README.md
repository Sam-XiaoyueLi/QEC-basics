# Decoders: Beyond Likelihood

Last updated: 2026-10-16

## Recap: lookup decoding and matching

In the [decoding notebook](../../decoder.ipynb), we use the measured detector events to infer whether a logical readout needs flipping. Stim generates a **detector error model (DEM)**: possible fault mechanisms, their probabilities, and their detector and logical effects.

We first build a small lookup decoder that tries one or two whole DEM mechanisms and chooses the most likely explanation consistent with the observed events. We then give the DEM to **PyMatching**, which represents detectors as graph nodes and graphlike fault effects as edges. Minimum-weight perfect matching finds a low-cost explanation without the lookup decoder's one-or-two-mechanism limit.

Both use likelihood information. Their answers depend on the noise model and the search they perform. In particular, treating the graph components of one shared fault as independent can change which explanation looks most likely. [Stim DEM specification](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md), [PyMatching](https://github.com/oscarhiggott/PyMatching)

## Five qubits: when the graph loses a correlation

Take a five-qubit bit-flip repetition code with four checks:

$$
Z_1Z_2,\quad Z_2Z_3,\quad Z_3Z_4,\quad Z_4Z_5.
$$

The encoded space is spanned by $|00000\rangle$ and $|11111\rangle$. Assume perfect check measurements, initially all $+1$. This toy protects against bit flips, not arbitrary Pauli noise.

Suppose the noise consists of four independent events:

| Event | Physical effect | Probability |
| --- | --- | --- |
| $A$ | $X_1$ | 0.10 |
| $B$ | $X_3$ | 0.10 |
| $C$ | $X_5$ | 0.10 |
| $F$ | $X_2X_4$ together | 0.02 |

The two flips inside $F$ always occur together. There are no independent $X_2$ or $X_4$ mechanisms. These are illustrative probabilities, not hardware measurements.

Now observe all four check signs as $-1$, written as syndrome **1111**. Exactly two event combinations explain it:

| Explanation | Flipped-qubit pattern | Probability, including absent events |
| --- | --- | --- |
| $F$ alone | 01010 | $0.02(0.9)^3=0.01458$ |
| $A+B+C$, without $F$ | 10101 | $0.98(0.1)^3=0.00098$ |

Each pattern flips exactly one qubit in every adjacent pair, so every check changes sign. The shared event is about **14.88 times more likely**. Conditioned on this syndrome, its probability is

$$
P(F\mid1111)=\frac{0.01458}{0.01458+0.00098}\approx93.7\%.
$$

Now replace $F$ with two **independent** flips, $X_2$ and $X_4$, each with probability 0.02. Their individual rates stay the same, but their joint probability changes:

| Pattern | Probability under the independent approximation |
| --- | --- |
| 01010 | $(0.02)^2(0.9)^3=0.0002916$ |
| 10101 | $(0.98)^2(0.1)^3=0.0009604$ |

The preference reverses: the approximation chooses **10101**. It charges twice for the two parts of one shared disturbance.

If the true error was $X_2X_4$ and we correct with $X_1X_3X_5$, the combined operation is

$$
(X_1X_3X_5)(X_2X_4)=X_1X_2X_3X_4X_5=\bar X.
$$

All checks pass afterward, but the logical state has flipped. The failure comes from discarding a relationship in the noise model. Likelihood inference itself can retain that relationship.

In a DEM, the shared event can appear as

```text
error(0.02) D0 D1 ^ D2 D3
```

This is one event affecting four detectors. The `^` suggests two graph components, without declaring them independent. The notebook uses ordinary matching on such decompositions. PyMatching also offers **correlated matching**, which exploits component relationships through a different decoding procedure. [Stim separator semantics](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md#separator-target), [PyMatching correlated-matching API](https://github.com/oscarhiggott/PyMatching/blob/master/src/pymatching/matching.py)

## BeliefMatching: infer whole faults before matching

**BeliefMatching** first uses **belief propagation (BP)** to estimate whole fault mechanisms from the observed syndrome. A shared event such as $F$ remains one variable, even though it affects several detectors.

The [reference implementation](https://github.com/oscarhiggott/BeliefMatching/blob/main/src/beliefmatching/belief_matching.py) then takes one of two paths:

- If BP finds a syndrome-consistent event assignment, return its predicted logical effect.
- Otherwise, use BP's probability estimates to construct shot-dependent graph weights and run matching.

The matching stage can therefore use evidence from this particular run, rather than only fixed prior edge probabilities. Matching is a fallback in this implementation; it need not run after successful BP. [BeliefMatching paper](https://arxiv.org/abs/2203.04948)

This still uses probabilistic inference. Its advantage is keeping more of the fault structure while making the search practical. It does not guarantee the most likely logical result: the most likely individual fault combination can differ from the logical class with the largest total probability across equivalent combinations.

## How belief propagation updates a probability

Return to the first detector in the five-qubit example. Only $A$ and $F$ affect it. If it fired, exactly one of them occurred:

| Compatible possibility | Probability before conditioning |
| --- | --- |
| $F$ happened, $A$ did not | $0.02\times0.9=0.018$ |
| $F$ did not happen, $A$ did | $0.98\times0.1=0.098$ |

Therefore,

$$
P(F\mid\text{first detector fired})
=\frac{0.018}{0.018+0.098}
\approx15.5\%.
$$

The event occurs in 2% of all runs, but this measurement makes it more plausible **in this run**. No extra physical experiment is needed. The DEM's prior probability can remain 0.02 across shots.

This calculation is a local BP message. If $F$ happened, the fired detector requires $A$ to be absent, with probability 0.9. If $F$ did not happen, it requires $A$ to be present, with probability 0.1. The check therefore supplies a likelihood ratio of **9** in favor of $F$.

Across a larger graph, event variables combine their prior probabilities with evidence from neighboring checks. Checks use the observed parity to constrain neighboring events. Messages exclude the receiving check's own previous contribution to avoid immediately counting it twice, and repeated classical updates carry information through the graph. [BP documentation](https://software.roffe.eu/ldpc/bp_decoding_example.html)

Loops can return information by other routes, making BP approximate or causing oscillations. In this toy, the middle two checks impose the same condition on $B$ and $F$, so multiplying all check evidence as if independent would double-count a constraint. The **93.7%** result above is exact enumeration, not a guaranteed BP output.

BP estimates this shot's faults; calibration estimates noise rates across experiments. Standard BP also needs the relevant mechanisms in its model: it cannot discover an omitted shared disturbance simply by iterating longer. The decoder receives measurements, not the simulator's hidden error labels.

## Other decoding approaches

**BP+OSD** uses BP's reliability estimates to guide ordered statistics decoding: binary linear algebra finds a syndrome-consistent solution, with additional candidate searches available. This helps when BP's hard decisions fail to satisfy all checks. **BP+LSD** localizes the algebra to error clusters, reducing the size of the solves. Neither syndrome consistency nor a high-scoring candidate certifies the true logical answer. [OSD and LSD documentation](https://software.roffe.eu/ldpc/quantum_decoder.html)

For [qLDPC codes](../qldpc-codes/README.md), including the [Gross code](../gross-code/README.md), other approaches change BP's updates, explore several hypotheses, or use a different representation altogether:

| Team | Approach and mechanism | What the public results establish |
| --- | --- | --- |
| **IBM** | **Relay-BP** varies memory strengths in BP updates to reduce oscillations, break symmetries, and explore valid corrections. | An FPGA prototype targets Gross-code memory under a circuit-noise model. Its classical timing results do not establish an integrated physical Gross-code memory. [Algorithm](https://arxiv.org/abs/2506.01779), [FPGA study](https://arxiv.org/abs/2510.21600) |
| **IonQ** | **BP-guided beam search** retains several promising hypotheses. A wider beam spends more computation exploring alternatives. A later stack separates longer-window error tracking from shorter-window logical-outcome decoding. | CPU benchmarks cover simulated workloads up to 408 logical qubits with assumed 1–5 ms extraction cycles, rather than a quantum experiment at that scale. [Beam search](https://arxiv.org/abs/2512.07057), [decoding stack](https://arxiv.org/abs/2608.25027) |
| **Riverlane** | **Local Clustering Decoder** grows and merges detection-event clusters using a Union-Find-based method. FPGA parallelism speeds processing, and signals such as heralded leakage can adapt the graph. | Classical hardware timing and simulated quantum resource savings are distinct results. [LCD paper](https://www.nature.com/articles/s41467-025-66773-x) |
| **Google / DeepMind** | Alongside matching and correlated matching, **Tesseract** uses A* search with pruning over fault subsets. **AlphaQubit 2** learns logical predictions from measurement records. | AlphaQubit 2 is evaluated on simulated circuits and recorded Willow data. Fast TPU processing per cycle is distinct from final-decision latency and live communication delays. [Tesseract](https://arxiv.org/abs/2503.10988), [AlphaQubit 2](https://arxiv.org/abs/2512.07737) |

These methods trade accuracy, computation, and response time differently. Compare logical error rates under the same code and noise assumptions, then ask whether throughput keeps up with incoming measurements and whether difficult cases meet logical-feedback deadlines. A CPU, FPGA, or TPU is the execution hardware; it does not by itself identify the decoding algorithm.

The [verification script](verify_example.py) checks the five-qubit probabilities by exhaustive enumeration and confirms ordinary PyMatching's choice using Stim 1.16.0 and PyMatching 2.4.0. Run `uv run python qec_knowledge_base/decoders/verify_example.py --with-stim` from the repository root. BP and BeliefMatching were not executed for this example.
