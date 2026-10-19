# Decoders: Beyond Likelihood

Last updated: 2026-10-16

## From syndrome to correction

A **decoder** reads the syndrome—the pattern of check outcomes—and supplies a correction. It infers plausible faults from their measured effects. Several faults can produce the same syndrome, and different physical errors can have the same effect on the encoded information. Successful decoding therefore does not require identifying a unique physical origin.

The inference starts with a **noise model**: which faults can occur, how probable they are, and which checks they affect. Probabilities can be converted into numerical **costs**, also called weights. For an independent event of probability $p$, the cost

$$
w=\ln\frac{1-p}{p}
$$

lets us compare compatible explanations by adding costs instead of multiplying probabilities. Minimizing the sum selects the most probable event combination under that model. This statistical weight differs from **physical error weight**, which counts affected qubits.

Decoders process this information differently. **Minimum-weight perfect matching (MWPM)** searches a weighted graph. **Correlated matching** uses an initial matching result to revise correlated edge weights. **BeliefMatching** first estimates fault probabilities using belief propagation, then uses matching when needed. Their representations and approximations matter as much as the instruction to choose a likely explanation.

## What MWPM matches

A **detector** is a parity of measurement outcomes whose value is predictable without faults. A departure from that value is a detection event. With repeated noisy measurements, a detector often compares checks across time; with perfect measurements and known initial check signs, it can simply report a changed check.

The decoding graph has detector nodes. An edge models an effect on two detectors, or on one detector and a boundary. MWPM connects the observed detection events through paths, allowing paths to end at boundaries, and minimizes the total edge cost. The selected edges explain the observed parity at every detector. [PyMatching documentation](https://github.com/oscarhiggott/PyMatching)

This graph works naturally for independent faults with one- or two-detector effects. A shared disturbance affecting four detectors needs additional treatment. **Splitting its effects into graph edges is useful for matching, but scoring those edges independently can discard their shared origin.**

## Issue with MWPM: independent edge scores

Consider five qubits encoding $|00000\rangle$ and $|11111\rangle$, with checks

$$
Z_1Z_2,\quad Z_2Z_3,\quad Z_3Z_4,\quad Z_4Z_5.
$$

Measurements are perfect and the initial signs are $+1$. Label the four detectors $D_0,D_1,D_2,D_3$. This repetition code protects against bit flips. Its illustrative noise model has four independent events:

| Event | Physical effect | Probability | Detectors flipped |
| --- | --- | --- | --- |
| $A$ | $X_1$ | 0.10 | $D_0$ |
| $B$ | $X_3$ | 0.10 | $D_1,D_2$ |
| $C$ | $X_5$ | 0.10 | $D_3$ |
| $F$ | One shared $X_2X_4$ disturbance | 0.02 | All four |

The two flips inside $F$ always occur together. There are no separate physical $X_2$ or $X_4$ mechanisms.

Suppose all four detectors fire: syndrome **1111**. Exactly two event combinations explain it. Writing a 1 at each flipped qubit gives:

| Explanation | Pattern | Probability, including absent events |
| --- | --- | --- |
| $F$ alone | 01010 | $0.02(0.9)^3=0.01458$ |
| $A+B+C$, without $F$ | 10101 | $0.98(0.1)^3=0.00098$ |

Exact inference therefore prefers $F$, with conditional probability

$$
P(F\mid1111)=\frac{0.01458}{0.01458+0.00098}\approx93.7\%.
$$

Now give this **same physical model** to a matching decoder. Stim's **detector error model (DEM)** records each mechanism's probability and detector effects. Our supplied DEM describes $F$ as

```text
error(0.02) D0 D1 ^ D2 D3
```

The separator `^` suggests two graph components: $D_0$ – $D_1$ and $D_2$ – $D_3$. Both remain parts of **one** probability-0.02 mechanism in the DEM. [Stim format](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md)

When PyMatching builds the graph for MWPM, each component receives probability 0.02 and weight $\ln49$. Matching scores their selection independently. Thus exact inference and MWPM start from the same supplied DEM, but use different scoring rules. The resulting independent-edge scores are:

| Candidate correction | Graph score, including unselected edges | Selected-edge cost |
| --- | --- | --- |
| 01010 | $(0.02)^2(0.9)^3=0.0002916$ | $2\ln49\approx7.78364$ |
| 10101 | $(0.98)^2(0.1)^3=0.0009604$ | $3\ln9\approx6.59167$ |

These scores are **not the physical pattern probabilities** in the previous table. The physical experiment has not changed. The graph approximation charges twice for the components of $F$, so MWPM chooses **10101**.

If the actual error was $X_2X_4$, that correction leaves

$$
(X_1X_3X_5)(X_2X_4)=X_1X_2X_3X_4X_5=\bar X.
$$

Every check passes, but the logical state flips. Retaining the joint mechanism would have favored the other correction. More generally, the most probable individual explanation can also differ from the most probable **logical class**, which sums probabilities over errors requiring equivalent recovery.

## Correlated matching: let one edge suggest another

PyMatching's **two-pass correlated matching** first runs MWPM, then treats its selected edges as evidence when reweighting correlated edges. A second matching uses those revised weights. For example, selecting one component of $F$ can make its partner more plausible. [Two-pass algorithm](https://github.com/oscarhiggott/PyMatching#correlated-matching)

In this example, however, the first pass selects $A+B+C$. Neither component of $F$ is selected to seed that reweighting. This explains why the tested PyMatching 2.4.0 implementation still chooses **10101**. Correlated matching uses more of the model than independent-edge matching, but its first-pass-guided heuristic does not guarantee exact joint inference.

## BeliefMatching: infer whole faults first

**Belief propagation (BP)** performs approximate Bayesian inference on a graph connecting fault variables to the detector constraints they affect. Here $F$ remains one variable connected to all four detectors. Variables exchange probability information with checks, allowing evidence from the measured syndrome to revise estimates for whole mechanisms. [BeliefMatching paper](https://arxiv.org/abs/2203.04948)

The first detector illustrates the calculation. Only $A$ and $F$ affect it, so a detection event requires exactly one of them:

$$
P(F=1,A=0)=0.02\times0.9=0.018,
$$

$$
P(F=0,A=1)=0.98\times0.1=0.098.
$$

Consequently,

$$
P(F\mid D_0\text{ fired})=\frac{0.018}{0.018+0.098}\approx15.5\%.
$$

The check supplies a **9:1 likelihood ratio** favoring $F$: if $F$ occurred, $A$ must be absent, with probability 0.9; otherwise $A$ must be present, with probability 0.1. Combining that check-to-event message with $F$'s prior odds $0.02/0.98$ produces the 15.5% posterior.

Across the graph, variables combine their priors with incoming messages, while checks enforce the observed parity. Each outgoing message excludes the recipient's previous contribution. Repeated updates spread information using classical computation on this shot's measurements; they require no new experiment or recalibration. [BP documentation](https://software.roffe.eu/ldpc/bp_decoding_example.html)

Loops can bring evidence back through other routes, making BP approximate or causing oscillations. Here the middle two checks both constrain $B\oplus F$, so their information is redundant. Multiplying four check contributions as independent evidence would overcount it.

**BeliefMatching** uses these whole-fault estimates in one of two ways. If BP finds a syndrome-consistent assignment, the reference implementation returns its predicted logical effect directly. Otherwise, it constructs graph weights from BP's estimated probabilities and runs matching. This preserves the shared mechanism during BP while retaining matching as a fallback. [Implementation](https://github.com/oscarhiggott/BeliefMatching/blob/main/src/beliefmatching/belief_matching.py)

The [verification script](verify_example.py) checks exact enumeration and the graph conversion, and reports **10101** for both MWPM and correlated matching with Stim 1.16.0 and PyMatching 2.4.0. BP and BeliefMatching were not executed; **93.7% is the exact posterior, not a claimed BP result**.

## Beyond matching, and what companies build

**BP+OSD** uses BP's reliability estimates to guide ordered statistics decoding: binary linear algebra and candidate searches produce a syndrome-consistent correction. **BP+LSD** localizes these algebraic solves to error clusters. Both offer ways to recover when BP alone fails. [OSD and LSD documentation](https://software.roffe.eu/ldpc/quantum_decoder.html)

Industrial work spans [qLDPC codes](../qldpc-codes/README.md), including the [Gross code](../gross-code/README.md), and topological codes such as surface and color codes. The approaches address different combinations of accuracy and processing deadlines:

| Team | Mechanism and demonstrated scope |
| --- | --- |
| **IBM** | **Relay-BP** varies memory strengths in BP updates to damp oscillations and explore different corrections. Its FPGA prototype decodes Gross-code memory under simulated circuit noise; it is not an integrated physical Gross-code memory. [Algorithm](https://arxiv.org/abs/2506.01779), [FPGA study](https://arxiv.org/abs/2510.21600) |
| **IonQ** | **BP-guided beam search** retains a bounded set of promising candidates. A later stack separates longer-window error tracking from shorter-window logical-outcome decoding. CPU benchmarks cover simulated workloads up to 408 logical qubits with assumed 1–5 ms extraction cycles. [Beam search](https://arxiv.org/abs/2512.07057), [decoding stack](https://arxiv.org/abs/2608.25027) |
| **Riverlane** | Its Union-Find-based **Local Clustering Decoder** grows and merges detection-event clusters on FPGAs, with graph adaptations for information such as heralded leakage. Reported hardware timing and simulated quantum resource savings are distinct results. [LCD paper](https://www.nature.com/articles/s41467-025-66773-x) |
| **Google / DeepMind** | **Tesseract** uses A* search with pruning over fault subsets. **AlphaQubit 2** is a trained neural decoder evaluated on simulated circuits and recorded Willow data. [Tesseract](https://arxiv.org/abs/2503.10988), [AlphaQubit 2](https://arxiv.org/abs/2512.07737) |

Compare logical error rates under the same code and noise model, then distinguish **throughput**, which determines whether processing keeps up with incoming measurements, from **feedback latency**, the time until a required decision arrives. Average speed can hide slow difficult cases, so latency tails matter too. Fast processing per cycle alone does not establish the final feedback deadline, including communication and control.
