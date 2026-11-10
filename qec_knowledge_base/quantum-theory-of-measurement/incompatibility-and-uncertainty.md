# Chapter 2. Incompatibility and uncertainty

**Which measurements can we combine, what do they disturb, and how much can their records tell us?**

[Quantum theory of measurement](README.md) · Previous: [Basics of measurement](basics-of-measurement.md) · Source: *Quantum theory of measurement*, Chapter 2, §§2.1–2.4, pp. 53–90 (corrected lecture notes, 15 November 2024).

Chapter 1 connected a measurement result to the state left behind. A second measurement acts on that remaining state. We can therefore collect two results, but they need not have the statistics of the two measurements performed separately on the original input.

This distinction leads to **compatibility**: can one apparatus reproduce both target distributions for every input state? We first ask whether such an apparatus exists, then examine what happens when we implement measurements in sequence.

## 1. Joint measurability: one record, several target distributions

Let $`E=\{E_s\}`$ and $`F=\{F_t\}`$ be two POVMs on the same input space. Their outcome labels are $`s`$ and $`t`$. They are **jointly measurable**, or compatible, if a parent POVM $`G=\{G_{s,t}\}`$ satisfies

```math
\sum_tG_{s,t}=E_s,\qquad \sum_sG_{s,t}=F_t.
```

The sums are **marginals**: keep one label and forget the other. Measuring $`G`$ once produces a pair of classical labels. Across repeated preparations of any state $`\rho`$, the first-label probabilities reproduce $`\mathrm{tr}(\rho E_s)`$ and the second-label probabilities reproduce $`\mathrm{tr}(\rho F_t)`$.

> [!IMPORTANT]
> Compatibility concerns **distributions for every input**. It does not say that each result is predictable, or that the system had two definite values before measurement.

A mother POVM can supply a raw record from which both target distributions follow by classical post-processing. For finite outcomes, this is equivalent to the paired-outcome definition above. A classical label can include extra randomness; it need not literally contain the pair at the detector.

### When does commutation decide compatibility?

If one target is a PVM with projectors $`P_s`$, it is compatible with $`F`$ exactly when every $`P_s`$ commutes with every $`F_t`$. In that case, the joint effects are uniquely

```math
G_{s,t}=P_sF_t=F_tP_s.
```

Thus sharp Pauli $`Z`$ and sharp Pauli $`X`$ are incompatible. Their projectors do not commute. Commutation also suffices for general POVMs, but is not necessary: unsharp effects can be compatible without commuting.

For a binary measurement, the plus effect determines the minus effect. Let $`A`$ and $`B`$ be the plus effects of two binary POVMs, and let $`I`$ be the identity on their input space. Choosing the joint plus-plus effect $`D`$ fixes every other joint effect:

```math
G_{++}=D,\quad G_{+-}=A-D,\quad
G_{-+}=B-D,\quad G_{--}=I-A-B+D.
```

The POVMs are compatible exactly when some $`D`$ makes all four operators positive. Their sum and marginals are already correct. Compatibility thus becomes a matrix feasibility problem: find one positive operator satisfying the remaining positivity constraints.

The tunable qubit detector from Chapter 1 gives a concrete example of this test.

### How much unsharpness allows a joint measurement?

Sharp $`Z`$ and sharp $`X`$ cannot be measured jointly on one qubit. **How much must we weaken them before a joint measurement becomes possible?**

Let $`X,Y,Z`$ be the Pauli matrices and $`I`$ the qubit identity. The two approximate measurements have effects

```math
E_s=\frac12(I+saZ),\qquad
F_t=\frac12(I+tbX),\qquad s,t\in\{+1,-1\}.
```

The parameters $`a,b\in[0,1]`$ describe their strengths:

- **Strength one:** the corresponding sharp measurement.
- **Strength zero:** a fair random sign, with no information about the input.
- **Between zero and one:** the result contains partial information.

For example, on a $`Z`$-plus eigenstate, the first detector reports plus with probability $`(1+a)/2`$. Lowering $`a`$ makes its result less reliable. These POVMs are called **unbiased** because each gives equal outcome probabilities on the maximally mixed state $`I/2`$.

**Try to build one detector that reports both signs.** Consider four candidate parent effects:

```math
G_{s,t}=\frac14(I+saZ+tbX).
```

They already have the correct marginals. Summing over the second sign cancels the $`X`$ terms:

```math
G_{s,+}+G_{s,-}
=\frac14(I+saZ+bX)+\frac14(I+saZ-bX)
=\frac12(I+saZ)=E_s.
```

Likewise, summing over the first sign gives $`F_t`$. All four effects sum to $`I`$. So **the remaining question is whether every parent effect is positive**. Otherwise, some input would receive a negative “probability.”

Each $`G_{s,t}`$ has eigenvalues

```math
\frac{1+\sqrt{a^2+b^2}}4,\qquad
\frac{1-\sqrt{a^2+b^2}}4.
```

The smaller eigenvalue is nonnegative exactly when

```math
a^2+b^2\leq1.
```

Geometrically, $`X`$ and $`Z`$ are perpendicular Bloch-sphere directions. Their contributions combine with length $`\sqrt{a^2+b^2}`$. If that length exceeds one, the candidate effect is no longer positive.

For this pair of unbiased measurements, the bound is also **necessary**: no other parent can evade it. The positivity calculation above proves that this parent works within the bound; necessity is a further result, included in the general criterion below.

| $`Z`$ strength $`a`$ | Largest allowed $`X`$ strength $`b`$ | Meaning |
| --- | --- | --- |
| $`1`$ | $`0`$ | Sharp $`Z`$; the other sign carries no $`X`$ information. |
| $`0.6`$ | $`0.8`$ | Partial information about both. |
| $`1/\sqrt2`$ | $`1/\sqrt2`$ | Strongest equal-strength joint readout. |
| $`0`$ | $`1`$ | Sharp $`X`$; the other sign carries no $`Z`$ information. |

**Unsharpness makes the requested statistics less demanding.** The parent reproduces the two weakened distributions for every input. It does not perform a joint measurement of sharp $`X`$ and sharp $`Z`$.

This tradeoff also appears in a measurement sequence. An unsharp Lüders $`Z`$ measurement of strength $`a`$, followed by sharp $`X`$, gives an effective $`X`$ strength $`b=\sqrt{1-a^2}`$. The sequence reaches the boundary: increasing the information obtained about $`Z`$ reduces the $`X`$ information available afterward. The sequential-measurement section derives this state change.

#### Extending the test to other directions

The bound above uses perpendicular directions. For arbitrary directions, let $`\mathbf e,\mathbf f`$ be Bloch vectors of length at most one. Write $`\boldsymbol\sigma=(X,Y,Z)`$, with $`\mathbf e\cdot\boldsymbol\sigma=e_xX+e_yY+e_zZ`$. Unbiased plus effects $`(I+\mathbf e\cdot\boldsymbol\sigma)/2`$ and $`(I+\mathbf f\cdot\boldsymbol\sigma)/2`$ are compatible exactly when

```math
\|\mathbf e+\mathbf f\|+\|\mathbf e-\mathbf f\|\leq2.
```

For the orthogonal vectors $`\mathbf e=(0,0,a)`$ and $`\mathbf f=(b,0,0)`$, both norms equal $`\sqrt{a^2+b^2}`$. This gives the necessary and sufficient condition $`a^2+b^2\leq1`$ used above.

#### Adding a third measurement direction

We can also ask one detector to report unsharp $`X,Y,Z`$ statistics. For strengths $`\lambda_x,\lambda_y,\lambda_z\in[0,1]`$, joint measurability requires and is guaranteed by

```math
\lambda_x^2+\lambda_y^2+\lambda_z^2\leq1.
```

A useful parent needs only four outcomes. Label them $`k=0,1,2,3`$ and assign sign vectors

```math
\mathbf v_0=(1,1,1),\quad \mathbf v_1=(1,-1,-1),\quad
\mathbf v_2=(-1,1,-1),\quad \mathbf v_3=(-1,-1,1).
```

Let $`v_{k,j}`$ be component $`j\in\{x,y,z\}`$ of vector $`\mathbf v_k`$. Define

```math
G_k=\frac14\left(I+\lambda_xv_{k,x}X+
\lambda_yv_{k,y}Y+\lambda_zv_{k,z}Z\right).
```

For direction $`j`$, report the sign $`v_{k,j}`$. Grouping the four outcomes by this sign gives the desired unsharp Pauli measurement. We will return to this same four-outcome detector for tomography.

### Position and momentum: the continuous version

The same question applies to a particle's position and momentum, or to two quadratures of an oscillator. For one canonical degree of freedom, work on $`L^2(\mathbb R)`$; $`I`$ now denotes its identity. Let $`Q`$ and $`P`$ be the canonical position and momentum operators, with $`[Q,P]=iI`$ in units where $`\hbar=1`$. Their sharp PVMs are incompatible.

An approximate joint measurement can instead report a pair of real numbers $`(q,p)`$. A **phase-space POVM** describes these readings. A standard family is built from a density operator $`\sigma`$, called the seed state, and displacement operators

```math
W(q,p)=e^{i(pQ-qP)}.
```

For a measurable region $`B`$ in the position–momentum plane, its effect is

```math
G_\sigma(B)=\frac1{2\pi}\int_B
W(q,p)\sigma W(q,p)^\dagger\,dq\,dp.
```

This family is **covariant**: displacing the input shifts the reported distribution by the same amount. The seed specifies the detector's resolution, not the input state being measured.

Its position marginal is the ideal position distribution blurred by a noise distribution. Its momentum marginal has the corresponding momentum noise. These two noise distributions come from the position and momentum distributions of one reflected seed state. Reflection reverses the signs of both coordinates; it does not change their widths.

The shared seed matters. We cannot choose arbitrarily narrow position noise and momentum noise independently. Their widths must satisfy a quantum state's preparation-uncertainty constraint. Section 3 will connect this to a measurement-error bound.

Compatibility tells us what a joint detector can achieve. An instrument is needed to determine what a particular sequence actually achieves.

## 2. Sequential measurements: the first operation changes the second input

Let the first measurement have instrument $`\{\mathcal I_s\}`$ and effects $`E_s`$. Let the second measurement have effects $`F_t`$ on the first instrument's output space. For initial state $`\rho`$, the joint probability is

```math
p(s,t)=\mathrm{tr}[\mathcal I_s(\rho)F_t].
```

The branch $`\mathcal I_s(\rho)`$ is unnormalized, so this expression already includes the probability of the first result. Dividing by $`p(s)=\mathrm{tr}[\mathcal I_s(\rho)]`$ instead gives $`p(t\mid s)`$ when $`p(s)>0`$.

Using the dual operation defined in Chapter 1, the sequence is a POVM on the original input:

```math
G_{s,t}=\mathcal I_s^*(F_t).
```

Let $`\Phi=\sum_s\mathcal I_s`$ be the first instrument's channel when its record is ignored. The marginals are

```math
\sum_tG_{s,t}=E_s,\qquad
\sum_sG_{s,t}=\Phi^*(F_t).
```

The first marginal remains the intended measurement. The second becomes the later measurement pulled back through the earlier state change. Producing two labels does not establish joint measurability of the original targets $`E`$ and $`F`$.

### Nondisturbance refers to a specified later measurement

When input and output spaces agree, the first instrument is **nondisturbing for** $`F`$ if

```math
\Phi^*(F_t)=F_t\quad\text{for every }t.
```

This **preserves the later distribution for every input state**. Agreement on a single state is insufficient. It also does not mean that every conditional branch leaves the state unchanged.

Nondisturbance implies that the sequence is a joint measurement of the original targets. Conversely, a compatible pair has some sequential realization, but it can require a larger intermediate space and a different second detector. Compatibility does not guarantee that an arbitrarily chosen first instrument preserves the original second detector.

Naimark dilation provides such a sequential realization: embed the input, select a projective outcome in the larger space, and measure a commuting POVM there. The dilation retains the information needed for the second marginal.

### Running example: unsharp Z, then sharp X

Use the Chapter 1 Lüders instrument with strength $`\eta\in[0,1]`$:

```math
E_s=\frac12(I+s\eta Z),\qquad
K_s=\sqrt{E_s},\qquad \mathcal I_s(\rho)=K_s\rho K_s^\dagger.
```

Let $`c=\sqrt{1-\eta^2}`$. The ignored-result channel preserves computational-basis populations and multiplies coherence by $`c`$. Follow it with sharp $`X`$, whose effects are $`F_t=(I+tX)/2`$.

For $`s,t=\pm1`$, the sequence has effects

```math
G_{s,t}=K_s^\dagger F_tK_s
=\frac14(I+s\eta Z+tcX).
```

The first marginal is unsharp $`Z`$ with strength $`\eta`$. The second is unsharp $`X`$ with strength $`c`$, even though the second detector is sharp. This sequence reaches the compatibility boundary $`\eta^2+c^2=1`$ derived above.

For input $`\ket{+}=(\ket{0}+\ket{1})/\sqrt2`$ and $`\eta=0.6`$, we have $`c=0.8`$. Each first result has probability $`1/2`$. The joint probabilities are

```math
p(s,+)=0.45,\qquad p(s,-)=0.05\qquad(s=\pm1).
```

The final plus probability is $`0.9`$. Measuring $`X`$ directly would give one. At $`\eta=1`$, the first measurement removes all computational-basis coherence, and the final $`X`$ result is a fair random sign.

A later sharp $`Z`$ measurement is undisturbed by this instrument because its populations are preserved. Thus disturbance depends on which later measurement we care about.

### Repeatability is a different requirement

An instrument is **repeatable** if an immediate repetition **returns the same result with probability one**, with no intervening evolution.

A sharp Lüders measurement with projectors $`P_s`$ is repeatable: after result $`s`$, the state lies in the range of $`P_s`$. But a device can measure sharp $`Z`$ and then flip the qubit. Its POVM is unchanged, while repetition returns the opposite result.

The unsharp Lüders instrument above preserves $`Z`$ populations but is not repeatable for $`0<\eta<1`$. Even a $`Z`$ eigenstate can yield either sign on each run. Repeated syndrome records can therefore differ because of readout randomness, system evolution, or faults. Their causes require different models.

### How much freedom does a fixed POVM leave?

For every instrument with effects $`E_s`$, there are outcome-dependent channels $`\Lambda_s`$ such that

```math
\mathcal I_s(\rho)=\Lambda_s\left(\sqrt{E_s}\rho\sqrt{E_s}\right),
```

Start with the Lüders branch, then apply an outcome-dependent state transformation. This explains why effects alone cannot specify disturbance. It does not establish that one instrument minimizes every possible measure of disturbance.

For a rank-one POVM, each nonzero effect has a one-dimensional range. The Lüders branch then has a fixed normalized output for that outcome. For each instrument, there are output density matrices $`\sigma_s`$, independent of the input state, such that

```math
\mathcal I_s(\rho)=\mathrm{tr}(\rho E_s)\sigma_s,
```

Once $`s`$ is known, the output contains no additional information about the input. Any later measurement only produces a classical post-processing of $`s`$. This is why a fully resolved basis measurement cannot preserve an unknown superposition for later use.

### Why extracting information cannot leave every state unchanged

There is a complementary way to use Stinespring dilation. Fix an ignored-result channel $`\Phi`$ with minimal dilation $`V`$ and environment $`\mathcal M`$. Every instrument whose branches sum to $`\Phi`$ can be obtained by measuring a POVM $`\{D_s\}`$ on that environment. For any output operator $`A`$,

```math
\mathcal I_s^*(A)=V^\dagger(A\otimes D_s)V,
```

Different environment readouts produce different records without changing the average channel.

For the identity channel, the minimal environment is one-dimensional. Its effects are just numbers $`p_s`$, independent of the input, so

```math
\mathcal I_s(\rho)=p_s\rho,\qquad E_s=p_sI.
```

An instrument that leaves every state unchanged therefore cannot reveal information about an arbitrary input state. This does not forbid preserving selected states or selected observables. An ideal QEC check can reveal a syndrome while preserving information within a code subspace.

### Sequential position and momentum

The continuous example follows the same mechanism. First use the von Neumann probe to measure position approximately, then measure momentum sharply on the remaining system.

Let $`\psi(x)`$ be the input wavefunction, $`\phi(q)`$ the initial probe wavefunction, and $`g>0`$ the coupling strength. For pointer result $`q`$, the unnormalized conditional system wavefunction is proportional to $`\phi(q-gx)\psi(x)`$. The first measurement multiplies the input by a shifted probe wavefunction. Fourier transformation converts this multiplication into convolution. The first measurement therefore changes the later momentum statistics.

After calibrating the pointer scale by dividing its reading by $`g`$, the combined readout is a covariant phase-space POVM. The probe state fixes both the position resolution and the momentum disturbance. A sharper second detector does not recover the momentum distribution that existed before the first interaction.

We can now identify the relevant limits. Some concern the input preparation; others concern the accuracy of a detector or the disturbance caused by a sequence.

## 3. Uncertainty: specify what is uncertain

| Concept | What is compared or varied? | Question |
| --- | --- | --- |
| Preparation uncertainty | Ideal measurement distributions in one state | Can this state give narrow distributions for both observables? |
| Measurement uncertainty | Actual joint-measurement marginals versus target observables | How accurately can one device approximate both targets? |
| Disturbance | Later statistics with and without an earlier measurement | What did the earlier instrument change? |

Compatibility does not make outcomes deterministic. Two compatible measurements can both have broad distributions on a given state.

### Preparation uncertainty

For Hermitian observables $`A,B`$ and input state $`\rho`$, define the standard deviation by

```math
\Delta_\rho A=\sqrt{\mathrm{tr}(\rho A^2)-[\mathrm{tr}(\rho A)]^2}.
```

With commutator $`[A,B]=AB-BA`$, the Robertson relation is

```math
\Delta_\rho A\,\Delta_\rho B
\geq\frac12|\mathrm{tr}(\rho[A,B])|.
```

This compares distributions from ideal measurements on identically prepared copies. It does not assume that one measurement precedes the other.

For position and momentum, $`[Q,P]=iI`$ gives $`\Delta_\rho Q\,\Delta_\rho P\geq1/2`$, for states with the required finite moments and operator domains. Narrowing a Gaussian in position broadens its momentum distribution; suitable Gaussian states attain equality.

For Pauli $`X,Z`$, the lower bound is $`|r_y|`$, where $`r_y=\mathrm{tr}(\rho Y)`$. It can vanish even though sharp $`X`$ and $`Z`$ are incompatible. A state-dependent Robertson bound is therefore not a test of measurement compatibility.

### Measurement uncertainty needs an error definition

To compare an approximate detector with a target, compare their outcome distributions on the same input. **Wasserstein distance** measures this difference through the cost of moving probability between numerical outcomes.

Let $`p(u)`$ and $`q(v)`$ be two finite distributions with numerical labels $`u,v`$. A coupling $`\pi(u,v)`$ is any joint distribution whose marginals are $`p`$ and $`q`$. The order-two distance is

```math
W_2(p,q)^2=\min_\pi\sum_{u,v}(u-v)^2\pi(u,v).
```

For continuous distributions, replace the sum by an integral over joint probability measures and take the infimum over all couplings. The distance can be infinite.

The coupling is a mathematical comparison of distributions. It need not represent a physically available joint quantum measurement.

For POVMs $`E,F`$, let $`p_\rho^E,p_\rho^F`$ be their distributions on state $`\rho`$. Define the worst-case detector distance

```math
d_2(E,F)=\sup_\rho W_2(p_\rho^E,p_\rho^F).
```

Taking the supremum prevents a detector from passing merely because it works on one favorable input.

For labels $`+1,-1`$, let $`p_+`$ and $`q_+`$ be the two plus probabilities. Exactly $`|p_+-q_+|`$ probability must move a distance of two, so

```math
W_2(p,q)^2=4|p_+-q_+|.
```

Return to the compatible unsharp $`Z,X`$ pair with strengths $`a,b`$. Denote the sharp target PVMs by $`P^Z,P^X`$. Their squared worst-case errors are

```math
d_2(P^Z,E)^2=2(1-a),\qquad
d_2(P^X,F)^2=2(1-b).
```

Since $`a^2+b^2\leq1`$ implies $`a+b\leq\sqrt2`$, this family obeys

```math
d_2(P^Z,E)^2+d_2(P^X,F)^2\geq4-2\sqrt2.
```

The equal-strength choice $`a=b=1/\sqrt2`$ attains the bound. It quantifies how much these two sharp targets must be approximated. It says nothing about finite-sample estimation error.

A general binary detector can also have bias. Write plus effects as $`A=(\alpha I+\mathbf e\cdot\boldsymbol\sigma)/2`$ and $`B=(\beta I+\mathbf f\cdot\boldsymbol\sigma)/2`$, with real $`\alpha,\beta`$ chosen so both effects lie between zero and $`I`$. Let $`d_2(A,B)`$ denote the distance between the binary POVMs determined by these plus effects. The same distance calculation gives

```math
d_2(A,B)^2=2\left(|\alpha-\beta|+\|\mathbf e-\mathbf f\|\right).
```

The scalar term detects bias; the vector term detects changes in direction and strength.

For a sequence, the second approximation is the disturbed measurement $`\Phi^*(F)`$. Comparing it with the original $`F`$ turns the same distribution-based framework into a disturbance measure. State the instrument and the distance before interpreting an error–disturbance claim.

### Why pointer noise has a quantum limit

For the covariant position–momentum family, both marginal noise distributions arise from one seed state. With additive convolution noise of finite second moment, the worst-case distance equals the root-mean-square noise displacement. It includes any offset in the mean and equals the standard deviation only for centered noise.

The two distances are therefore at least the seed's respective standard deviations. Their product inherits its preparation-uncertainty bound. Let $`Q_{\mathrm{sharp}},P_{\mathrm{sharp}}`$ be the sharp position and momentum PVMs, and let $`E,F`$ be the joint detector's marginals. Then

```math
d_2(Q_{\mathrm{sharp}},E)\,
 d_2(P_{\mathrm{sharp}},F)\geq\frac12.
```

The distance uses calibrated position and momentum units, with $`\hbar=1`$. Restoring units gives $`\hbar/2`$.

Thus the seed's uncertainty limits the detector's resolution. This is different from uncertainty already present in the input state being measured.

Unsharp joint measurements have limits, but they can also collect several kinds of information at once. We now ask whether their complete records can identify the input state.

## 4. Tomography: reconstruct a state from repeated preparations

A measurement is **informationally complete** if **different input states always produce different outcome distributions**. With enough repeated preparations, its statistics can identify the density matrix. This is the condition that makes state tomography possible.

> [!IMPORTANT]
> The unknown state is reconstructed from **many identically prepared copies**. One measurement result does not determine an arbitrary state.

Nor can we generally measure $`X`$, then $`Y`$, then $`Z`$ on one qubit and treat those results as undisturbed samples of the original state.

In finite Hilbert-space dimension $`d`$, a density matrix has $`d^2-1`$ independent real parameters. Informationally complete POVM effects must span the real vector space of Hermitian operators. A single such POVM needs at least $`d^2`$ outcomes; enough outcomes without independent effects are insufficient.

For $`d>1`$, one PVM is not informationally complete: its probabilities reveal populations in one eigenbasis, not all coherences. Several settings on separate copies, or one suitable non-projective POVM, can supply the missing information.

### Separate Pauli settings

Let $`\mathbf r=(r_x,r_y,r_z)`$ be the unknown qubit state's Bloch vector, with length at most one. Its density matrix is

```math
\rho=\frac12(I+r_xX+r_yY+r_zZ),\qquad |\mathbf r|\leq1,
```

Each Pauli setting gives one component through the mean of its sign outcomes.

Let $`n_{j,+},n_{j,-}`$ be the counts in setting $`j\in\{x,y,z\}`$, and let $`N_j=n_{j,+}+n_{j,-}>0`$. A hat marks an estimate:

```math
\hat r_j=\frac{n_{j,+}-n_{j,-}}{N_j},\qquad
\hat\rho=\frac12(I+\hat r_xX+\hat r_yY+\hat r_zZ).
```

For 1,000 shots per setting, plus counts of 700, 400, and 800 give $`\hat{\mathbf r}=(0.4,-0.2,0.6)`$. The estimate is physical because its length is $`\sqrt{0.56}<1`$.

Three other spin directions also suffice if they are linearly independent. Nearly dependent directions make reconstruction sensitive to small frequency errors.

### The four-outcome joint detector also performs tomography

Return to the parent effects $`G_k`$ from Section 1, with strengths $`\lambda_x,\lambda_y,\lambda_z`$ and sign vectors $`\mathbf v_k`$. Their probabilities are

```math
p_k=\frac14\left(1+\lambda_xv_{k,x}r_x+
\lambda_yv_{k,y}r_y+\lambda_zv_{k,z}r_z\right).
```

For each direction $`j`$, average the reported signs. This gives $`\lambda_jr_j`$. Therefore, if all three strengths are nonzero,

```math
r_j=\frac1{\lambda_j}\sum_{k=0}^3v_{k,j}p_k,
\qquad j\in\{x,y,z\}.
```

This detector is informationally complete exactly when all three strengths are nonzero. At zero strength in one direction, the probabilities contain no information about that component.

The symmetric choice $`\lambda_x=\lambda_y=\lambda_z=1/\sqrt3`$ gives the tetrahedral POVM. Define unit vectors $`\mathbf n_k=\mathbf v_k/\sqrt3`$ and write $`\boldsymbol\sigma=(X,Y,Z)`$. Then

```math
G_k=\frac14(I+\mathbf n_k\cdot\boldsymbol\sigma),\qquad
\mathbf r=3\sum_{k=0}^3p_k\mathbf n_k.
```

The dot product means the weighted sum of Pauli matrices. One apparatus setting now collects enough information for all three components across repeated preparations. Its marginals are unsharp; this does not implement a joint measurement of the three sharp Pauli PVMs.

### Informational completeness does not guarantee an accurate estimate

The reconstruction formulas use exact probabilities. Real experiments substitute frequencies from a finite number of shots. For independent ideal Pauli shots,

```math
\mathrm{Var}(\hat r_j)=\frac{1-r_j^2}{N_j}.
```

More shots reduce sampling uncertainty. They cannot recover an unmeasured component or correct an unknown detector model.

For an unbiased detector aligned with Pauli direction $`j`$, let $`0<\eta_j\leq1`$ be its known strength and $`\hat m_j`$ its measured sign average. Write $`\sigma_x=X`$, $`\sigma_y=Y`$, and $`\sigma_z=Z`$. The effects are $`(I\pm\eta_j\sigma_j)/2`$. Correcting the scale gives

```math
\hat r_j=\frac{\hat m_j}{\eta_j},\qquad
\mathrm{Var}(\hat r_j)=\frac{1-\eta_j^2r_j^2}{N_j\eta_j^2}.
```

Small strength amplifies sampling noise. If both the strength and the state component are unknown, the data identify only their product. Separate calibration or additional assumptions are required.

Finite sampling can also give $`|\hat{\mathbf r}|>1`$, so direct linear inversion produces a matrix with a negative eigenvalue. A constrained fit can require $`\rho\geq0`$ and $`\mathrm{tr}\rho=1`$, for example by maximizing the likelihood of the observed counts. A physical estimate can still be biased or fit the data poorly; those require separate checks.

These are practical estimation issues beyond the exact reconstruction formulas. Keep **detector error, sampling error, and lack of information separate** when diagnosing a result.

### Continuous-variable tomography and optical readout

The same question applies to an oscillator: do the chosen probability distributions distinguish all possible states?

Position and momentum distributions alone do not. They can agree for different states whose phase information differs. For example, Gaussian wavefunctions with opposite quadratic phases can have identical position and momentum distributions.

Additional **rotated quadratures** provide distributions along other phase-space directions. With the convention $`Q_\theta=Q\cos\theta+P\sin\theta`$, the angle $`\theta`$ selects the direction. Measuring all angles in $`[0,\pi)`$, or a dense set in that interval, on separately prepared copies is informationally complete.

A single covariant phase-space POVM can also be informationally complete. For seed $`\sigma`$, define its characteristic function $`\chi_\sigma(q,p)=\mathrm{tr}[\sigma W(q,p)]`$. The condition is that the closure of the region where $`\chi_\sigma`$ is nonzero is the whole plane. In particular, a Gaussian seed with an everywhere nonzero characteristic function satisfies it. Unsharp marginals can therefore still provide enough joint data to reconstruct the input.

Two optical measurement schemes implement these observables:

- **Balanced homodyne detection** mixes a signal with a strong local oscillator and subtracts two photocounts. The oscillator phase selects a quadrature. Ideal quadrature statistics arise in the strong-oscillator limit; detector inefficiency adds noise.
- **Eight-port homodyne detection** combines two such readouts to obtain a phase-space record. An auxiliary state's preparation controls the effective seed and resolution. Detector losses broaden the ideal statistics.

The apparatus model determines which POVM belongs in the reconstruction. Treating a noisy detector as ideal can turn readout errors into apparent state errors.

Let $`n`$ be the number of qubits. Unrestricted state tomography involves $`4^n-1`$ parameters. Many software tasks need only a few expectations or correlations. QEC needs syndrome information while preserving encoded quantum information. The appropriate measurement is therefore determined by both what the record must reveal and what the system must retain.

Last updated: 2026-11-10
