# Decoders: Beyond Likelihood

Last updated: 2026-10-16

## Overview

A **decoder** reads the syndrome—the pattern of check outcomes—and supplies a correction or a change to the interpreted logical result. It uses a noise model to infer which errors could explain those outcomes. Several errors can produce the same syndrome, so recovering the logical information does not require identifying a unique physical error.

There are several ways to make this inference:

| Method | Principle |
| --- | --- |
| **Minimum weight** | Choose a compatible explanation with the smallest total cost. With equal costs, this means the fewest errors. |
| **Maximum likelihood** | Choose the most probable compatible explanation under the noise model. |
| **Minimum-weight perfect matching (MWPM)** | Solve the minimum-cost problem on a graph whose edges describe fault effects. |
| **Correlated matching** | Use relationships between graph edges to revise matching weights. |
| **Belief propagation (BP)** | Update estimates of fault probabilities using the observed check constraints. |
| **BeliefMatching** | Use BP over whole faults, with matching as a fallback when needed. |

Minimum weight and maximum likelihood describe selection criteria. Matching and BP describe ways to perform the inference. They can overlap: for independent graph-edge events, assigning weight $w=\ln[(1-p)/p]$ makes minimum-weight matching select the most likely edge combination. [PyMatching](https://github.com/oscarhiggott/PyMatching)

In quantum codes, several error combinations can have the same logical effect. **Maximum-likelihood logical decoding** adds their probabilities before choosing a logical class. This can differ from choosing the single most likely error combination. [Decoding objectives](https://arxiv.org/html/2203.04948v4)

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

In a matching graph, the shared event $F$ can be represented by two edges: one joining the first two checks and one joining the last two. Ordinary matching treats them independently. A **detector error model (DEM)** can retain the fact that they came from one event, giving a correlation-aware decoder more information.

PyMatching's **two-pass correlated matching** first runs ordinary matching, then uses the selected edges to adjust the costs of correlated edges and runs matching again. This can improve inference without a full search over shared-event combinations. It remains a heuristic: in the five-qubit example, the tested PyMatching 2.4.0 implementation also selects **10101**, rather than the exact model's preferred **01010**. [Correlated matching](https://github.com/oscarhiggott/PyMatching#correlated-matching)

## BeliefMatching: infer whole faults before matching

**BeliefMatching** first uses **belief propagation (BP)** to estimate whole fault mechanisms from the observed syndrome. A shared event such as $F$ remains one variable, even though it affects several detectors.

The [reference implementation](https://github.com/oscarhiggott/BeliefMatching/blob/main/src/beliefmatching/belief_matching.py) then takes one of two paths:

- If BP finds a syndrome-consistent event assignment, return its predicted logical effect.
- Otherwise, use BP's probability estimates to construct shot-dependent graph weights and run matching.

The matching stage can therefore use evidence from this particular run, rather than only fixed prior edge probabilities. Matching is a fallback in this implementation; it need not run after successful BP. [BeliefMatching paper](https://arxiv.org/abs/2203.04948)

BeliefMatching retains whole-fault relationships while keeping inference practical. Its estimates and final decisions remain approximate; they do not guarantee maximum-likelihood logical decoding.

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

For syndrome 1111, the methods use different criteria or approximations:

| Method | Result or inference in this example |
| --- | --- |
| Fewest physical bit flips | Chooses **01010**: two flipped qubits rather than three. This count ignores event probabilities. |
| Exact maximum likelihood with the shared event | Chooses **01010**, with conditional probability **93.7%**. |
| Ordinary MWPM with independent graph edges | Chooses **10101**, because the graph charges separately for both parts of $F$. |
| Two-pass correlated matching | Also chooses **10101** in the tested implementation; reweighting does not guarantee exact joint inference. |
| BP | The first check alone gives **15.5%** for $F$. Full-graph BP is approximate and was not run here. |
| BeliefMatching | Retains $F$ as a whole-fault variable and can use BP-informed matching. Its output was not tested here. |

The minimum-flip and exact-likelihood choices agree here, but can differ when error probabilities differ. Correlation-aware heuristics do not guarantee exact joint inference.

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

The [verification script](verify_example.py) checks the probabilities by exhaustive enumeration and reports ordinary and correlated matching results using Stim 1.16.0 and PyMatching 2.4.0. Run `uv run python qec_knowledge_base/decoders/verify_example.py --with-stim` from the repository root. BP and BeliefMatching were not executed for this example.
