# 5. Multiple measurements: compatibility and disturbance

A measurement can change what a later measurement sees. We can now calculate that change because an instrument supplies both an outcome and a remaining state. This also lets us distinguish sequential measurements from joint measurements of the original observables.

[Learning path](README.md) · Previous: [Instruments and apparatus](instruments-and-apparatus.md) · Course: §§2.1–2.3, pp. 53–83.

## Calculate a sequence using the unnormalized branch

Apply instrument $\mathcal I_s$ first, then measure a POVM $F_t$. The joint probability is

$$
p(s,t)=\operatorname{tr}[\mathcal I_s(\rho)F_t].
$$

This already includes the probability of the first outcome. Dividing by $p(s)$ would give $p(t\mid s)$ instead. Using the dual map from page 3, the whole sequence has effects

$$
G_{s,t}=\mathcal I_s^*(F_t).
$$

A marginal sums over the outcome you ignore. The first marginal is the original $E_s$, but its second marginal is

$$
\sum_sG_{s,t}=\Phi^*(F_t),\qquad \Phi=\sum_s\mathcal I_s.
$$

The first measurement is nondisturbing for $F$ precisely when $\Phi^*(F_t)=F_t$ for every outcome $t$. This is a statement for every input state, not merely a coincidence of probabilities on one chosen input.

## Running example: unsharp Z followed by sharp X

Use the Lüders instrument from page 4, with $c=\sqrt{1-\eta^2}$, and then $F_t=(I+tX)/2$. Direct multiplication gives

$$
G_{s,t}=K_s^\dagger F_tK_s
=\frac14(I+s\eta Z+tcX),
$$

so for input Bloch vector $\mathbf r$,

$$
p(s,t)=\frac14(1+s\eta r_z+tc r_x).
$$

The first marginal is the intended unsharp $Z$. The second is $(I+tcX)/2$: an unsharp $X$ observable on the original input. On $|+\rangle$, the final $X=+1$ probability is $(1+c)/2$. It is $0.9$ at $\eta=0.6$, and $0.5$ at $\eta=1$, rather than the probability one obtained by measuring $X$ directly.

A later $Z$ measurement, by contrast, is undisturbed by this instrument: $\Phi^*(Z)=Z$. Disturbance depends on the observable whose statistics you want to preserve.

## Repeatability is a property of the instrument

Repeatability means that immediately repeating the same measurement returns the same result with probability one, assuming no intervening evolution. A sharp Lüders instrument has this property: after outcome $s$, its state lies in the range of $P_s$, so $P_tP_s=0$ for $t\ne s$ excludes a different result.

A sharp POVM alone does not guarantee repeatability. Measuring $Z$ and then flipping the qubit has the same first-outcome POVM as ordinary $Z$ measurement, but the next $Z$ outcome is opposite. Nor does preserving $Z$ populations make the unsharp instrument repeatable: for $0<\eta<1$, either reported sign remains possible even on a $Z$ eigenstate. For repeated syndrome checks, separate intrinsic randomness, physical changes, and readout faults before interpreting differing records.

## Joint measurability means preserving both requested marginals

POVMs $E_s$ and $F_t$ are jointly measurable if there is a POVM $G_{s,t}$ such that

$$
\sum_tG_{s,t}=E_s,\qquad\sum_sG_{s,t}=F_t.
$$

One parent measurement then produces data for both target observables by classical processing. Two sharp PVMs are jointly measurable exactly when their projections commute. Commutation is sufficient for general POVMs too, but it is not necessary.

For a concrete noncommuting example, consider unsharp $Z$ with strength $a$ and unsharp $X$ with strength $b$, both between zero and one. The effects

$$
G_{s,t}=\frac14(I+saZ+tbX)
$$

sum to $I$ and have the desired marginals. Their eigenvalues are $(1\pm\sqrt{a^2+b^2})/4$, so this construction works when $a^2+b^2\leq1$. For these unbiased orthogonal qubit observables, this is also the necessary condition; see [Busch and Heinosaari, Approximate joint measurements of qubit observables](https://arxiv.org/abs/0706.1415).

The running sequential construction has $a=\eta$ and $b=\sqrt{1-\eta^2}$, exactly on the boundary. Sharp $Z$ and sharp $X$ would require $a=b=1$, which is impossible. The ability to perform two operations in sequence does not make their original sharp observables jointly measurable.

Compatibility guarantees that some joint implementation exists. It does not mean that any chosen instrument for the first POVM preserves the second. Even a sharp measurement can be followed by an extra unitary that disturbs otherwise commuting observables.

## Three different meanings of uncertainty

| Concept | What varies or is compared? | Engineering question |
| --- | --- | --- |
| Preparation uncertainty | Distributions of sharp observables in one prepared state | How predictable are ideal outcomes on this state? |
| Measurement imprecision | Actual measurement statistics versus a target observable | How accurately does the detector implement its specification? |
| Disturbance | Later statistics with versus without an earlier process | What has the earlier measurement changed? |

For Hermitian $A,B$, the Robertson preparation relation is

$$
\Delta_\rho A\,\Delta_\rho B\geq\frac12|\operatorname{tr}(\rho[A,B])|,
$$

where $[A,B]=AB-BA$ and $\Delta_\rho A$ is the standard deviation of ideal $A$ outcomes. For Pauli $X,Z$ this lower bound is $|r_y|$. It can vanish even though $X$ and $Z$ are incompatible; a zero bound is not a compatibility test. This inequality does not directly describe detector error or measurement backaction.

A measurement-uncertainty relation must specify how approximation error is measured. The course uses Wasserstein distances: the minimum transport cost of turning one outcome distribution into another, respecting numerical distances between outcomes, then compares observables across input states. The qubit strengths above provide a simpler concrete trade-off: improving one marginal restricts the other. Avoid applying a universal “error times disturbance” formula without identifying its error definitions and assumptions.

## Where continuous position and momentum fit

Sections 2.1.1 and 2.2.1 extend these ideas to phase space. A phase-space POVM reports approximate position and momentum together. Its marginals are smeared versions of the sharp position and momentum observables; an auxiliary quantum state constrains the possible smearing distributions. A sequential position measurement can likewise broaden later momentum statistics through its interaction with the probe.

This is the same chain of reasoning as for the qubit: specify a joint measurement or an instrument, calculate its marginals, and compare them with the target observables. The detailed continuous-variable bounds require integral measures and operator-domain care. Master the qubit calculation first; return to these sections for bosonic or continuous-variable work.

## Check your understanding

1. For $|+\rangle$ and $\eta=0.6$, calculate all four probabilities $p(s,t)$.
2. Can unbiased unsharp $Z$ and $X$, both with strength $0.8$, be jointly measured?
3. If sharp $Z$ happens not to change $X$ statistics on $I/2$, does that establish nondisturbance?

<details>
<summary>Worked answers</summary>

1. With $c=0.8$, each $s$ has $p(s,+)=0.45$ and $p(s,-)=0.05$. The second marginal is $(0.9,0.1)$.
2. No: $0.8^2+0.8^2=1.28>1$. Equal strengths must be at most $1/\sqrt2$.
3. No. Nondisturbance requires preservation for every input. The input $|+\rangle$ provides a counterexample: sharp $Z$ changes subsequent $X$ probabilities from $(1,0)$ to $(1/2,1/2)$.

</details>

Next: [Tomography](tomography.md) asks whether these measurement records contain enough information to identify the original state.

Last updated: 2026-11-09
