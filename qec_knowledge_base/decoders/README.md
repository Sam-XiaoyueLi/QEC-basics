# Decoders: Beyond Likelihood

Last updated: 2026-10-16

## Overview

A **decoder** reads the syndrome, which is the pattern of check outcomes, and supplies a correction. To choose that correction, it infers which faults could explain the syndrome. Different faults can require different corrections, but some errors produce the same syndrome and can be corrected in the same way. The decoder therefore does not need to identify the exact physical origin of every error.

This inference uses an **error model** that describes possible faults, their probabilities, and their effects on the checks. The model can treat faults as independent or include shared events that affect several qubits together.

The decoder seeks a likely explanation of the measured syndrome. For independent graph-edge events, maximizing an explanation's probability can be expressed as minimizing its total **weight**. Each edge receives a numerical penalty $w=\ln[(1-p)/p]$ based on its probability $p$: less likely edges receive larger penalties. Choosing the compatible combination with the smallest sum of weights therefore selects the most probable edge combination under that model. This probability-based weight differs from simply counting affected qubits. [PyMatching](https://github.com/oscarhiggott/PyMatching)

**Minimum-weight matching** carries out this search on a graph. **BeliefMatching** and **correlated matching** add inference steps that use the observed syndrome to revise the weights:

| Decoder | How it uses probabilities and weights |
| --- | --- |
| **Minimum-weight perfect matching (MWPM)** | Finds a compatible explanation with the smallest total graph weight, using weights computed from the error model. |
| **BeliefMatching** | Uses **belief propagation (BP)** to estimate whole-fault probabilities conditioned on the syndrome, with BP-informed matching as a fallback. [Implementation](https://github.com/oscarhiggott/BeliefMatching/blob/main/src/beliefmatching/belief_matching.py) |
| **Correlated matching** | Runs matching, uses inferred edges and modeled correlations to revise other edge weights, then matches again. [Two-pass method](https://github.com/oscarhiggott/PyMatching#correlated-matching) |

Stim can express fault probabilities and detector effects in a **detector error model (DEM)**, which PyMatching converts into a weighted graph. Splitting a shared fault into independent graph edges can lose information. The five-qubit example below shows how this changes the preferred correction. We use the same faults to examine correlated matching and BeliefMatching, then turn to advanced decoders.

## Five qubits: when the graph loses a correlation

Take a five-qubit bit-flip repetition code with four checks:

$$
Z_1Z_2,\quad Z_2Z_3,\quad Z_3Z_4,\quad Z_4Z_5.
$$

Assume perfect check measurements, initially all $+1$. This repetition code protects against bit flips only.

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

## Correlated matching: revise the graph weights

In a matching graph, the shared event $F$ can be represented by two edges: one joining the first two checks and one joining the last two. Matching on the independent-edge graph treats them independently, while the DEM retains their shared origin.

PyMatching's **two-pass correlated matching** uses a first matching result to reweight correlated edges for a second pass. It remains a heuristic: in the five-qubit example, the tested PyMatching 2.4.0 implementation also selects **10101**, rather than the exact model's preferred **01010**. [Correlated matching](https://github.com/oscarhiggott/PyMatching#correlated-matching)

## BeliefMatching: infer whole faults before matching

**BeliefMatching** first uses **belief propagation (BP)** to estimate whole fault mechanisms from the observed syndrome. The shared event $F$ remains one variable, even though it affects all four detectors. [BeliefMatching paper](https://arxiv.org/abs/2203.04948)

The [reference implementation](https://github.com/oscarhiggott/BeliefMatching/blob/main/src/beliefmatching/belief_matching.py) then takes one of two paths:

- If BP finds a syndrome-consistent event assignment, return its predicted logical effect.
- Otherwise, use BP's probability estimates to construct shot-dependent graph weights and run matching.

Keeping $F$ intact preserves the relationship lost by the independent-edge approximation, although BP and BeliefMatching remain approximate.

## How belief propagation updates a probability

With perfect checks and known initial signs, each changed check is a detector event. Only $A$ and $F$ affect the first detector. If it fired, exactly one occurred:

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

The event occurs in 2% of all runs, but this measurement raises its probability **in this run** to 15.5%. The model's event rate remains unchanged.

This calculation is a local BP message. If $F$ happened, the fired detector requires $A$ to be absent, with probability 0.9. If $F$ did not happen, it requires $A$ to be present, with probability 0.1. The check therefore supplies a likelihood ratio of **9** in favor of $F$.

Across a larger graph, event variables combine their prior probabilities with evidence from neighboring checks. Checks use the observed parity to constrain neighboring events. Messages exclude the receiving check's own previous contribution to avoid immediately counting it twice, and repeated classical updates carry information through the graph. [BP documentation](https://software.roffe.eu/ldpc/bp_decoding_example.html)

Loops can return information by other routes, making BP approximate or causing oscillations. In this toy, the middle two checks impose the same condition on $B$ and $F$, so multiplying all check evidence as if independent would double-count a constraint. The **93.7%** result above is exact enumeration, not a guaranteed BP output.

BP needs the relevant faults in its model; iterating cannot discover an omitted mechanism. It receives measurements, not hidden error labels.

## Comparing the same example

For syndrome 1111, the exact shared-event model prefers **01010** with probability **93.7%**:

| Decoder | Result for this example |
| --- | --- |
| **MWPM** | **10101** in the independent-edge model. |
| **Two-pass correlated matching** | **10101** in the tested implementation. |
| **BeliefMatching** | Not executed here. The BP calculation above illustrates how syndrome evidence updates the estimate for $F$. |

## Advanced decoding methods

**BP+OSD** uses BP's reliability estimates to guide ordered statistics decoding: binary linear algebra finds a syndrome-consistent solution, with additional candidate searches available. This helps when BP's hard decisions fail to satisfy all checks. **BP+LSD** localizes the algebra to error clusters, reducing the size of the solves. These are BP-based decoders, rather than variants of BeliefMatching. [OSD and LSD documentation](https://software.roffe.eu/ldpc/quantum_decoder.html)

For [qLDPC codes](../qldpc-codes/README.md), including the [Gross code](../gross-code/README.md), other approaches change BP's updates, explore several hypotheses, or use a different representation altogether:

| Team | Approach and mechanism | Scope of public results |
| --- | --- | --- |
| **IBM** | **Relay-BP** varies memory strengths in BP updates to reduce oscillations, break symmetries, and explore valid corrections. | An FPGA prototype targets Gross-code memory under a circuit-noise model. This is classical decoder hardware, not an integrated physical Gross-code memory. [Algorithm](https://arxiv.org/abs/2506.01779), [FPGA study](https://arxiv.org/abs/2510.21600) |
| **IonQ** | **BP-guided beam search** retains several promising hypotheses. Wider beams explore more alternatives. A later stack separates longer-window error tracking from shorter-window logical-outcome decoding. | CPU benchmarks include simulated workloads up to 408 logical qubits with assumed 1–5 ms extraction cycles. [Beam search](https://arxiv.org/abs/2512.07057), [decoding stack](https://arxiv.org/abs/2608.25027) |
| **Riverlane** | **Local Clustering Decoder** grows and merges detection-event clusters using a Union-Find-based method. FPGA parallelism speeds processing, and signals such as heralded leakage can adapt the graph. | Classical hardware timing and simulated quantum resource savings are distinct results. [LCD paper](https://www.nature.com/articles/s41467-025-66773-x) |
| **Google / DeepMind** | **Tesseract** uses A* search with pruning over fault subsets. **AlphaQubit 2** learns logical predictions from measurement records. | AlphaQubit 2 is evaluated on simulated circuits and recorded Willow data. Fast TPU processing per cycle is distinct from final-decision latency and live communication delays. [Tesseract](https://arxiv.org/abs/2503.10988), [AlphaQubit 2](https://arxiv.org/abs/2512.07737) |

Compare logical error rates under the same code and noise assumptions, then ask whether throughput keeps up with measurements and whether difficult cases meet feedback deadlines. A CPU, FPGA, or TPU names execution hardware, not a decoding algorithm.

The [verification script](verify_example.py) checks the probabilities by exhaustive enumeration and reports MWPM and correlated matching results using Stim 1.16.0 and PyMatching 2.4.0. Run `uv run python qec_knowledge_base/decoders/verify_example.py --with-stim` from the repository root. BP and BeliefMatching were not executed for this example.
