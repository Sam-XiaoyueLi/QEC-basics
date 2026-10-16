# Decoders: from check outcomes to likely faults

Status: Study reference |
Last updated: 2026-10-16

## One physical error can change two checks

Take three data qubits with repetition-code checks

$$
S_1=Z_1Z_2,\qquad S_2=Z_2Z_3.
$$

An encoded state starts in the $+1$ eigenspace of both checks. An unwanted $X_2$ error anticommutes with the $Z_2$ in each check, so both signs change to $-1$. The **fault** is the unwanted physical event. Its **effects** include these changed check results and any change to a tracked logical observable.

Write check sign $+1$ as bit 0 and $-1$ as bit 1. With perfect measurements, the possible single bit flips give:

| Physical error | Check bits $(s_1,s_2)$ |
| --- | --- |
| $X_1$ | 10 |
| $X_2$ | 11 |
| $X_3$ | 01 |

The check bits together form the **syndrome**. A decoder receives this syndrome and a noise model, then infers a correction or a change to the interpreted logical result. It cannot directly observe the underlying error.

In this example, each check has a known initial sign and is measured perfectly. In a repeated experiment, a **detector** is a specified parity of measurement reports that is predictable without faults. It often compares the same check across consecutive rounds. A negative check that remains negative can therefore produce a detection event when it first changes, but no event on the next unchanged round. Preparation, surgery, and readout can use other parity relations. The [decoding notebook](../../decoder.ipynb) develops these distinctions for a noisy logical CNOT. [Stim detector error model specification](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md)

These repetition codes protect against bit flips. They do not provide full protection against arbitrary Pauli errors.

## What weighted matching infers

A matching graph represents detectors as nodes. A fault affecting two detectors gives an edge between them. A fault affecting one detector gives an edge to a boundary. Thus the single $X_2$ fault above is already one ordinary graph edge: its two changed checks do not require two independent faults.

For independent graph-edge events with probabilities $p_e$, a candidate set $E$ has probability

$$
P(E)=\prod_{e\in E}p_e\prod_{e\notin E}(1-p_e).
$$

Factor out $P(\varnothing)=\prod_e(1-p_e)$, which is common to every candidate. Maximizing the remaining product is equivalent to minimizing

$$
W(E)=\sum_{e\in E}w_e,\qquad
w_e=\ln\frac{1-p_e}{p_e}.
$$

An unlikely edge has a higher cost. **Minimum-weight perfect matching (MWPM)** finds a minimum-cost explanation compatible with the observed detector pattern: a fired detector has an odd number of selected incident edges, and an unfired detector has an even number. The optimization considers the whole pattern, including paths and boundaries. The selected edges' logical labels determine the predicted logical flip. [PyMatching documentation](https://pymatching.readthedocs.io/en/stable/)

This calculation depends on which events the model treats as independent. A single shared disturbance can produce several graph components that should remain linked.

## Five qubits: losing a shared-event relationship reverses the answer

Use five data qubits with checks

$$
S_i=Z_iZ_{i+1},\qquad i=1,2,3,4.
$$

The encoded space is spanned by $|00000\rangle$ and $|11111\rangle$, and a logical bit flip is

$$
\bar X=X_1X_2X_3X_4X_5.
$$

Assume perfect check measurements and the following illustrative noise model. These probabilities describe a toy model, not measured hardware.

| Event | Physical effect | Probability | Syndrome if it occurs alone |
| --- | --- | --- | --- |
| $A$ | $X_1$ | 0.10 | 1000 |
| $B$ | $X_3$ | 0.10 | 0110 |
| $C$ | $X_5$ | 0.10 | 0001 |
| $F$ | $X_2X_4$ together | 0.02 | 1111 |

The four events are independent of each other. The two flips **within $F$ always occur together**. There are no independent $X_2$ or $X_4$ events in this model.

Let $a,b,c,f$ be bits indicating whether each event occurred. The resulting physical error pattern and syndrome are

$$
\boldsymbol{x}=(a,f,b,f,c),\qquad
\boldsymbol{s}=(a\oplus f,\ f\oplus b,\ b\oplus f,\ f\oplus c),
$$

where $\oplus$ means addition modulo two. Two flips affecting the same check cancel.

### Evaluate the two explanations of syndrome 1111

Suppose every check returns $-1$. Then $a\ne f$, $b\ne f$, and $c\ne f$. There are exactly two allowed explanations:

| Explanation | Physical error pattern | Probability, including events that did not occur |
| --- | --- | --- |
| $F$ alone | 01010 | $0.02(0.9)^3=0.01458$ |
| $A+B+C$, without $F$ | 10101 | $0.98(0.1)^3=0.00098$ |

The first explanation is about $14.88$ times as likely. Conditioning on the observed syndrome gives

$$
P(F\mid\boldsymbol{s}=1111)
=\frac{0.01458}{0.01458+0.00098}
\approx0.937018.
$$

The posterior is about **93.7%**, although $F$ occurs in only 2% of all runs. The syndrome is much more compatible with $F$ alone than with the competing three-event explanation.

### Replace the shared event with independent graph edges

Now approximate $F$ by two independent events: $X_2$ with probability 0.02 and $X_4$ with probability 0.02. Keep independent $X_1,X_3,X_5$ events at 0.10 each. This preserves the two individual marginal flip rates, but changes their joint probability.

The same observed syndrome still permits physical patterns 01010 and 10101. Their probabilities under the approximation are:

| Explanation | Approximate probability | Matching cost |
| --- | --- | --- |
| 01010 | $(0.02)^2(0.9)^3=0.0002916$ | $2\ln49\approx7.7836$ |
| 10101 | $(0.98)^2(0.1)^3=0.0009604$ | $3\ln9\approx6.5917$ |

The approximation now prefers **10101**, reversing the original answer. It charges twice for the two parts of one shared disturbance.

If the actual error was $X_2X_4$ and the correction is $X_1X_3X_5$, their product is

$$
(X_1X_3X_5)(X_2X_4)=\bar X.
$$

Every check passes afterward, but the logical state has flipped. Likelihood inference can give the right answer for the supplied model while the supplied model misrepresents the physical noise.

### Express the shared event in a detector error model

Label the four check detectors `D0` through `D3`. Track final $Z_1$ as logical observable `L0`. An $X_1$ flips this readout; $X_2X_4$ does not. The model can be written as

```text
error(0.1) D0 L0
error(0.1) D1 D2
error(0.1) D3
error(0.02) D0 D1 ^ D2 D3
```

The last line is **one event with probability 0.02**. Its `^` marker suggests two graph components; it does not declare their independence. Ordinary matching can use these as separate edges and lose the shared-event relationship. [Stim component-separator semantics](https://github.com/quantumlib/Stim/blob/main/doc/file_format_dem_detector_error_model.md#separator-target)

The [CNOT notebook](../../decoder.ipynb) requests `decompose_errors=True` and calls `Matching.from_detector_error_model(dem)` without enabling correlations. It also implements a small lookup decoder that compares one or two **whole DEM mechanisms** using products of odds. These are different searches over different representations: the lookup model retains a shared mechanism but limits the number of mechanisms considered.

PyMatching also supports correlated matching, enabled when constructing and decoding with `enable_correlations=True`. This is a separate decoding procedure, not a change to what `^` means. Correlation-aware heuristics are not guaranteed to reproduce exact inference on every model. [PyMatching implementation and API documentation](https://github.com/oscarhiggott/PyMatching/blob/master/src/pymatching/matching.py)

## Belief propagation: updating this run's probabilities

**Belief propagation (BP)** approximately infers which modeled events occurred, conditioned on this run's syndrome. Its calculations use the existing measurements. They do not require another physical run or a change to the underlying event rates.

Start with just the first detector in the five-qubit example. Only $A$ and $F$ affect it. If it fired, then $a\oplus f=1$:

| Compatible possibility | Prior probability |
| --- | --- |
| $F$ happened and $A$ did not | $0.02\times0.9=0.018$ |
| $F$ did not happen and $A$ did | $0.98\times0.1=0.098$ |

The unobserved $B$ and $C$ events sum out. Therefore

$$
P(F\mid s_1=1)
=\frac{0.018}{0.018+0.098}
\approx0.155172.
$$

This one fired detector raises the probability that $F$ occurred **in this run** from 2% to about **15.5%**. The population rate $P(F)=0.02$ remains unchanged.

### What a check message contains

Assume $F$ happened. To explain the fired detector, $A$ must be absent, which has probability 0.9. Assume $F$ did not happen. Then $A$ must be present, which has probability 0.1. The detector supplies a likelihood ratio of $0.9/0.1=9$ in favor of $F$.

Multiplying the prior odds by that evidence gives

$$
\underbrace{\frac{0.02}{0.98}}_{\text{prior odds}}
\times
\underbrace{\frac{0.9}{0.1}}_{\text{check evidence}}
=\frac{9}{49}.
$$

Convert odds $r$ to probability by $r/(1+r)$, giving $9/58\approx0.155172$. This is the arithmetic behind a local check-to-event message.

In a larger problem, a **factor graph** connects event variables to the detector constraints they affect. Event-to-check messages combine the prior with evidence from other checks. Check-to-event messages weigh the assignments of neighboring events that satisfy the observed parity. When sending a message back toward a check, BP excludes that check's own incoming contribution to avoid immediately counting it twice. Iterating lets information travel through the graph. [BP decoding documentation](https://software.roffe.eu/ldpc/bp_decoding_example.html)

On a tree, sum-product BP can calculate exact marginal probabilities. Loops allow information to return by other routes, so the estimates can become approximate or oscillate. Quantum-code graphs often contain short loops and several equivalent explanations.

In this toy, the second and third detector equations are both $b\oplus f=1$. They are redundant. Treating all four checks as independent pieces of evidence would count the same constraint more than once. The **93.7% all-syndrome result above comes from exact enumeration**, not from multiplying four independent check messages or from an executed BP decoder.

Three operations should stay distinct:

| Operation | What changes? |
| --- | --- |
| Noise calibration | Estimates event rates from many measurements or experiments. |
| Per-shot inference | Estimates this run's events using its syndrome and an existing model. |
| Online model adaptation | Changes model parameters or structure using additional information, such as a leakage flag. |

Standard BP cannot recover a shared-event mechanism that was omitted from its supplied model merely by iterating longer.

## BeliefMatching: BP over faults, with matching when needed

BeliefMatching runs BP on the whole fault mechanisms, including mechanisms that affect more than two detectors. This retains a variable for a shared event such as $F$, rather than beginning with two independent copies of it.

In the [reference implementation](https://github.com/oscarhiggott/BeliefMatching/blob/main/src/beliefmatching/belief_matching.py), the next step depends on the BP result:

1. If BP finds a syndrome-consistent event assignment, return the logical-flip prediction from that assignment.
2. Otherwise, convert BP's event estimates into graph-edge estimates and use them to set shot-dependent matching weights. Matching then supplies a syndrome-consistent prediction.

Thus matching is a fallback after unsuccessful BP in this implementation. It does not necessarily run after every BP pass. The fallback uses its own posterior-derived cost construction; it is not simply the original fixed-prior matching graph. [BeliefMatching paper](https://arxiv.org/abs/2203.04948)

Neither branch guarantees exact maximum-likelihood **logical** decoding. Finding the single most probable event combination differs from summing the probabilities of all combinations with the same logical effect. In a stabilizer code, errors differing by a stabilizer act equivalently on encoded information. A logical-class decoder compares those combined probabilities. The two objectives coincide in the tiny example because each of its two explanations has a different logical effect, but they need not coincide in larger codes.

The decoder also does not receive simulator truth. The CNOT notebook keeps `observable_flips` separate and uses them to evaluate predictions. Live decoding of unknown quantum data has no such truth label.

## Other ways to finish or improve the inference

### BP with algebraic post-processing: OSD and LSD

BP can produce useful probabilities without producing a final hard decision that satisfies every detector equation. **Ordered statistics decoding (OSD)** uses the reliability ordering to choose variables for binary linear algebra, solves the syndrome equation, and can search additional candidates by varying selected bits. The post-processor enforces syndrome consistency; it does not certify the true physical error or optimal logical class.

**Localized statistics decoding (LSD)** performs the algebra within growing error clusters, merging them when needed, rather than solving across the entire matrix at once. BP supplies guidance, while local solves reduce the size of the algebraic tasks. These are BP+OSD and BP+LSD, respectively. [LDPC decoder documentation](https://software.roffe.eu/ldpc/quantum_decoder.html)

### Relay-BP: change the iteration dynamics

BP can repeatedly switch between competing hypotheses. Relay-BP introduces varied memory strengths into the updates, changing how previous beliefs affect new ones. Different strengths help suppress oscillations and break symmetries. Relay stages adjust these strengths and can encounter several valid corrections. The mechanism is an altered BP search, rather than an OSD linear-algebra fallback. [Relay-BP paper](https://arxiv.org/abs/2506.01779)

This matters for [qLDPC codes](../qldpc-codes/README.md), including the [Gross code](../gross-code/README.md): their sparse checks support message passing, but their graphs and equivalent error patterns can make plain BP difficult.

### Beam search: retain several hypotheses

A beam search keeps several promising partial explanations instead of committing immediately to one. It expands candidates, uses BP to guide which branches look plausible, and retains a bounded number for further exploration. A wider beam usually costs more computation and can improve accuracy. This creates a controllable search budget rather than an exhaustive search of every fault combination. [BP-guided beam-search paper](https://arxiv.org/abs/2512.07057)

### Clustering and learned decoding

**Union-Find-style clustering** grows regions around detection events and merges connected regions until their parity can be resolved, including through boundaries. A correction can then be extracted within those regions. Local structure and parallel processing make this attractive for hardware implementations. Riverlane's Local Clustering Decoder is an adaptive FPGA implementation of this approach. [LCD paper](https://www.nature.com/articles/s41467-025-66773-x)

A **neural decoder** learns a mapping from measurement records to logical predictions from training examples. Training changes network parameters; inference applies the trained network to a new record. This is distinct from BP's per-shot inference with explicitly supplied event priors. AlphaQubit 2 is one example. [AlphaQubit 2 paper](https://arxiv.org/abs/2512.07737)

## Public company work and what its benchmarks establish

The examples below describe public research as of 16 October 2026. A company can investigate several algorithms, and a CPU, FPGA, GPU, or TPU names the execution hardware rather than the decoding algorithm.

| Team | Publicly described approach | Evidence and scope |
| --- | --- | --- |
| **IBM** | Relay-BP; FPGA implementation targeting Gross-code memory. | The prototype reports 24 ns BP iterations and average decoding below $1\,\mu\mathrm{s}$ per cycle under specified circuit-noise probabilities below $3\times10^{-3}$. These are classical prototype results against a noise model, not a demonstrated integrated physical Gross-code memory. [FPGA study](https://arxiv.org/abs/2510.21600) |
| **IonQ** | BP-guided beam search; a longer-window error decoder tracks the Pauli frame while a shorter-window outcome decoder answers time-critical logical measurements. | CPU benchmarks include simulated workloads up to 408 logical qubits, with assumed 1–5 ms syndrome-extraction cycles. This is a tested classical stack for modeled workloads, not a 408-logical-qubit quantum experiment. [Dual-decoder study](https://arxiv.org/abs/2608.25027) |
| **Riverlane** | Local Clustering Decoder, with FPGA parallelism and graph adaptations triggered by signals such as heralded leakage. | The work combines classical hardware performance with simulated quantum-error performance. Its projected resource savings depend on the leakage model and comparison decoder. [LCD study](https://www.nature.com/articles/s41467-025-66773-x) |
| **Google / Google DeepMind** | Matching and correlated matching, Tesseract search, and AlphaQubit 2 neural decoding appear in public research. | Tesseract uses A* search with pruning over fault subsets. AlphaQubit 2 is evaluated on simulated circuits and recorded Willow data. Its real-time variant achieves sub-microsecond average processing per cycle on TPUs in specified settings; final-decision latency and live measurement/communication delays are separate quantities. [Tesseract](https://arxiv.org/abs/2503.10988), [AlphaQubit 2](https://arxiv.org/abs/2512.07737) |
| **Quantinuum** | Helios includes a real-time control stack supporting GPU-accelerated classical computation. | The company account establishes a control/compute capability, not one universal decoder algorithm for every experiment or code. [Helios account](https://www.quantinuum.com/blog/introducing-helios-the-most-accurate-quantum-computer-in-the-world) |

Google's **Tesseract decoder** is an algorithm. The **tesseract code** mentioned in other companies' logical-qubit demonstrations is a quantum code; sharing a name does not make them the same object.

To compare decoders, keep the following quantities separate:

| Quantity | Question it answers |
| --- | --- |
| Logical error rate | How often is the logical prediction wrong under this code, circuit, and noise model? |
| Throughput | Can the decoder process measurements as fast as they arrive? |
| Decision latency | How long after the needed measurements is a particular logical answer ready? |
| Runtime tail | How often do difficult shots or windows exceed the time budget? |
| Execution assumptions | Which code, noise model, processor, precision, core count, and parallelism were used? |

A decoder may keep up on average while occasionally delaying a conditional logical gate. A throughput number alone does not establish a feedback deadline. Results using different code families, noise models, and execution hardware do not provide a universal ranking.

## Reproduce the small example

[verify_example.py](verify_example.py) exhaustively checks all 16 event combinations in the shared-event model and all 32 physical patterns in the independent approximation. It verifies the conditional probabilities, matching costs, and logical difference. With `--with-stim`, it also compares the DEM with a Stim circuit and checks ordinary PyMatching's prediction:

```bash
# From the repository root; exact arithmetic needs only Python's standard library.
python qec_knowledge_base/decoders/verify_example.py

# Uses the repository's Stim and PyMatching environment.
uv run python qec_knowledge_base/decoders/verify_example.py --with-stim
```

The checks were run with Stim 1.16.0 and PyMatching 2.4.0. They confirm that ordinary matching selects 10101 for syndrome 1111. BP, BeliefMatching, and the other decoder families were not executed for this page; the 93.7% value is the exact posterior for the specified toy model.
