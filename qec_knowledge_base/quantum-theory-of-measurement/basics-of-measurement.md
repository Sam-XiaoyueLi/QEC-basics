# Chapter 1. Basics of measurement

**How does a quantum state become a classical measurement record, and what happens to the quantum system along the way?**

[Quantum theory of measurement](README.md) · Source: *Quantum theory of measurement*, Chapter 1, pp. 7–47 (corrected lecture notes, 15 November 2024).

## 1. Preparations, events, and probabilities

A probabilistic theory connects two laboratory procedures: preparing a system and testing whether an event occurs. An event is a yes-or-no question, such as “did the detector report 0?” The theory assigns a probability to each preparation–event pair.

Different procedures can give identical statistics. Two preparations belong to the same **equivalence class** if every event has the same probability for both. We call that class a **state**. Two events belong to the same class if they have the same probability for every preparation. We call that class an **effect**.

Thus a state retains the information needed to predict measurements. An effect retains the information needed to describe one event. Neither specifies every detail of the laboratory procedure.

Let $`\mathcal S`$ be the state set and $`\mathcal E`$ the effect set. Their **statistical duality** $\langle S, E\rangle=p$ is the rule that pairs a state with an effect to give a probability. Each state assigns probabilities to effects, each effect assigns probabilities to states. 

### Convexity

Suppose a preparation randomly chooses state $`\rho_1`$ with probability $`t`$ and state $`\rho_2`$ with probability $`1-t`$, where $`0\leq t\leq1`$. Its effective state is the mixture $`t\rho_1+(1-t)\rho_2`$. For any effect $`E`$,

```math
p(E\mid t\rho_1+(1-t)\rho_2)
=t\,p(E\mid\rho_1)+(1-t)\,p(E\mid\rho_2).
```

The state set is **convex** because it contains these mixtures. Randomly choosing between two yes-or-no tests similarly gives a mixture of their effects, so the effect set is convex too.

This structure applies to probabilistic theories in general. Quantum theory makes a specific choice for the mathematical objects representing states and effects: operators on a complex Hilbert space.

## 2. States and effects on Hilbert space

### What makes a space Hilbert?

A **Hilbert space** is a vector space with an inner product, **complete in the norm defined by that inner product**.

Completeness ensures that taking a convergent limit does not leave the space. Every finite-dimensional inner-product space is already complete. Infinite-dimensional spaces require more care.

For two vectors $`\ket{\phi},\ket{\psi}`$ with components $`\phi_j,\psi_j`$ in an orthonormal basis, the inner product is

```math
\braket{\phi|\psi}=\sum_j\overline{\phi_j}\psi_j.
```

The overline denotes complex conjugation. This inner product is linear in the second vector, conjugate-linear in the first, and conjugate symmetric. It is positive definite: $`\braket{\psi|\psi}\geq0`$, with equality only for the zero vector. The norm is $`\|\psi\|=\sqrt{\braket{\psi|\psi}}`$; distance is the norm of a difference.

For normalized vectors, $`|\braket{\phi|\psi}|^2`$ is the probability that a projection onto $`\ket{\phi}`$ succeeds on input $`\ket{\psi}`$. Orthogonal vectors have zero overlap and can be distinguished perfectly by a suitable measurement.

### From vectors to operators

An **operator** is a linear map acting on vectors. In finite dimensions, it is a matrix. An inner product gives a scalar, whereas the outer product $`\ket{\psi}\bra{\psi}`$ gives an operator.

A normalized vector represents a **pure state** through its density operator:

```math
\rho=\ket{\psi}\bra{\psi}.
```

Multiplying the vector by a global phase leaves this operator unchanged. A random preparation also has a density operator. If choice $`j`$ prepares normalized vector $`\ket{\psi_j}`$ with probability $`p_j`$, then

```math
\rho=\sum_j p_j\ket{\psi_j}\bra{\psi_j},
\qquad p_j\geq0,\qquad \sum_jp_j=1.
```

Different random preparations can give the same density operator. They then predict the same probabilities for every measurement.

A **density operator** satisfies $`\rho\geq0`$ and $`\mathrm{tr}\rho=1`$. Positivity means that it is Hermitian with nonnegative eigenvalues. Hermitian means equal to its conjugate transpose. In finite dimensions, the trace is the sum of diagonal entries.

An **effect** is an operator $`E`$ satisfying $`0\leq E\leq I`$, where $`I`$ is the identity. Both $`E`$ and $`I-E`$ must be positive. Quantum statistical duality is the Born rule:

```math
p(E\mid\rho)=\mathrm{tr}(\rho E).
```

These conditions keep the probability between zero and one. States and effects therefore act on the same Hilbert space, but have different normalization conditions and physical roles. In infinite dimensions, density operators are positive trace-class operators; effects are bounded operators.

### A superposition is not a mixture

Prepare the same superposition $`\ket{+}`$ on every run. Its vector and density matrix are

```math
\ket{+}=\frac{\ket{0}+\ket{1}}{\sqrt2},\qquad
\rho_+=\ket{+}\bra{+}=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}.
```

Alternatively, prepare $`\ket{0}`$ or $`\ket{1}`$ with equal probability and forget the choice. Denote this mixture by $`\rho_{\mathrm{mix}}`$:

```math
\rho_{\mathrm{mix}}=\frac12\ket{0}\bra{0}+\frac12\ket{1}\bra{1}
=\frac12\begin{pmatrix}1&0\\0&1\end{pmatrix}.
```

Both give equal probabilities for 0 and 1 in the computational basis. To distinguish their statistics, use a basis containing $`\ket{+}`$. Its other vector is $`\ket{-}=(\ket{0}-\ket{1})/\sqrt2`$, orthogonal to $`\ket{+}`$.

In this basis, $`\rho_+`$ always gives plus. The mixture gives either sign with probability one half. The off-diagonal entries encode **coherence relative to the chosen basis**. They affect probabilities in other bases. Coherence is basis-dependent; purity, $`\mathrm{tr}(\rho^2)`$, is not. Purity is one for a pure state and below one for a mixed state.

The Pauli matrices name these measurement directions:

```math
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
```

Here $`i`$ is the imaginary unit. The computational basis is the eigenbasis of $`Z`$; the plus/minus basis is the eigenbasis of $`X`$. Both have eigenvalues $`+1,-1`$.

Every qubit density matrix has the **Bloch representation**

```math
\rho=\frac12(I+r_xX+r_yY+r_zZ),\qquad
r_x=\mathrm{tr}(\rho X),\quad r_y=\mathrm{tr}(\rho Y),\quad r_z=\mathrm{tr}(\rho Z).
```

The real vector $`\mathbf r=(r_x,r_y,r_z)`$ has length at most one. The states $`\rho_+`$ and $`\rho_{\mathrm{mix}}`$ have vectors $`(1,0,0)`$ and $`(0,0,0)`$. Their equal $`r_z`$ explains their identical computational-basis statistics.

### Adding and discarding a system

To include a probe or another qubit, combine system spaces by a **tensor product**, $`\mathcal H_A\otimes\mathcal H_B`$. Independent preparations have joint state $`\rho_A\otimes\rho_B`$. A state is separable if it is a mixture of product states; otherwise it is entangled.

If the joint state is $`\rho_{AB}`$ and we retain only system $`A`$, its state is the **partial trace**:

```math
\rho_A=\mathrm{tr}_B(\rho_{AB}).
```

This reduced state preserves every measurement probability available on $`A`$ alone. For the Bell vector $`\ket{\Phi^+}=(\ket{00}+\ket{11})/\sqrt2`$, the joint state is pure but either reduced state is $`I/2`$. A mixed local state need not come from a classical random preparation of the joint system.

A tensor product combines subsystems and multiplies dimensions. A **direct sum** combines orthogonal sectors and adds dimensions. Orthogonal outcome sectors are useful in dilation constructions. A continuous pointer instead uses $`L^2(\mathbb R)`$, the Hilbert space of square-integrable wavefunctions.

We now have states and individual events. A full detector must account for all possible outcomes together.

## 3. Observables and measurement outcomes

A classical outcome is a label, such as a bit or detector number. An effect is the operator used to calculate the probability of that label.

For finitely many outcomes $`x`$, a **POVM** (positive-operator-valued measure) assigns effects $`E_x`$ such that

```math
E_x\geq0,\qquad \sum_xE_x=I,\qquad
p(x\mid\rho)=\mathrm{tr}(\rho E_x).
```

The sum condition makes the total probability one. Include “no click” as an outcome if it can occur. For continuous outcomes, assign an effect $`E(B)`$ to each measurable set of readings $`B`$. Sums become integrals where a density exists.

A **PVM** (projection-valued measure) is a POVM whose effects are orthogonal projectors $`P_x`$: they satisfy $`P_x^2=P_x`$ and $`P_xP_y=0`$ for different outcomes $`x,y`$. This is a projective, or sharp, measurement.

### A Z measurement with adjustable resolution

Sharp $`Z`$ measurement reports $`s=+1`$ for $`\ket{0}`$ and $`s=-1`$ for $`\ket{1}`$. Its projectors are $`P_s=(I+sZ)/2`$.

A more general detector retains these labels but has strength $`0\leq\eta\leq1`$:

```math
E_s=\frac12(I+s\eta Z),\qquad
p(s\mid\rho)=\frac{1+s\eta r_z}{2}.
```

At $`\eta=1`$, it distinguishes the two basis states perfectly. At $`\eta=0`$, it gives a fair random sign for every input. Intermediate strengths give partial information. This is a **tunable measurement of a qubit**: the parameter changes how much information the result gives.

For example, at $`\eta=0.6`$, the probability of plus is $`0.8`$ on $`\ket{0}`$ and $`0.2`$ on $`\ket{1}`$. The effects specify these statistics, but do not yet specify the interaction or the output state.

### Numerical outcomes and their moments

A detector's complete probability distribution contains more information than its mean. Give each outcome $`x`$ a real value $`a_x`$. Define its first and second moment operators by

```math
A_1=\sum_x a_xE_x,\qquad A_2=\sum_x a_x^2E_x.
```

The mean and variance of the reported value $`a`$ are

```math
\mathbb E[a]=\mathrm{tr}(\rho A_1),\qquad
\mathrm{Var}(a)=\mathrm{tr}(\rho A_2)-[\mathrm{tr}(\rho A_1)]^2.
```

For a PVM, $`A_2=A_1^2`$. This need not hold for a POVM. Our tunable detector reports $`\pm1`$, so $`A_1=\eta Z`$ and $`A_2=I`$. A sharp measurement of the operator $`\eta Z`$ instead reports $`\pm\eta`$. It has the same mean, but generally a different variance.

General effects are not necessarily projectors. The next question is whether projective readout can still realize their probabilities.

## 4. Naimark dilation

> [!IMPORTANT]
> **Every POVM can be represented as a projective measurement on a larger Hilbert space.** This is Naimark dilation, also spelled Neumark dilation.

Let $`J`$ embed the input space $`\mathcal H`$ into a dilation space $`\mathcal M`$. It is an isometry: $`J^\dagger J=I`$, so it preserves lengths and inner products. Let $`P_x`$ be a PVM on $`\mathcal M`$. The dilation must satisfy

```math
E_x=J^\dagger P_xJ,\qquad
\|P_xJ\ket{\psi}\|^2=\bra{\psi}E_x\ket{\psi}
```

for every normalized input vector $`\ket{\psi}`$. Read the first equation from right to left: embed, project, and map back. A projector on the larger space can compress to a non-projective effect on the input.

### A simple construction

Add a register with orthonormal vectors $`\ket{x}`$, one per outcome. Define

```math
J\ket{\psi}=\sum_x\sqrt{E_x}\ket{\psi}\otimes\ket{x},\qquad
P_x=I\otimes\ket{x}\bra{x}.
```

The positive square root $`\sqrt{E_x}`$ is obtained by taking square roots of the eigenvalues. Since the effects sum to the identity, $`J`$ preserves normalization. Reading the register gives the desired POVM statistics.

For the fair-coin POVM $`E_0=E_1=I/2`$ on a qubit, this becomes $`J\ket{\psi}=\ket{\psi}\otimes\ket{+}`$. Measuring the added qubit gives 0 or 1 with equal probability, whatever the input.

### What makes a dilation minimal?

A dilation is minimal when the vectors $`P_xJ\ket{\psi}`$, over all inputs and outcomes, span the whole dilation space. In infinite dimensions, include limits of their linear combinations. There are no unused directions.

This condition concerns outcome branches, not just the embedded inputs. In the fair-coin example, the two branches are $`\ket{\psi}\otimes\ket{0}/\sqrt2`$ and $`\ket{\psi}\otimes\ket{1}/\sqrt2`$. Together they span the full four-dimensional space, so this dilation is minimal. An extra untouched ancilla would introduce unused directions.

Every dilation contains an isometric copy of a minimal dilation. To state this precisely, let $`(\mathcal M_0,P_0,J_0)`$ be minimal and $`(\mathcal M,P,J)`$ any dilation of the same POVM. An isometry $`W:\mathcal M_0\to\mathcal M`$ satisfies

```math
WJ_0=J,\qquad P_xW=WP_{0,x}.
```

The first equation preserves how inputs enter. The second preserves how each outcome branch is selected. Every dilation therefore contains a copy of the minimal one. If both are minimal, $`W`$ is onto and hence unitary: they differ only in coordinates.

Naimark dilation fixes probabilities. It does not determine the remaining system state. Before addressing that state, we must distinguish the raw detector outcome from the result we choose to report.

## 5. Post-processing and coarse graining

**Post-processing changes the classical record after the quantum measurement.** Suppose raw outcome $`x`$ is reported as $`y`$ with conditional probability $`q(y\mid x)`$. The effects for the reported measurement are

```math
F_y=\sum_xq(y\mid x)E_x,\qquad
q(y\mid x)\geq0,\qquad \sum_yq(y\mid x)=1.
```

This sum accounts for every raw outcome that can produce the reported label. It describes relabeling, randomized reporting, and readout errors.

For example, first measure sharp $`Z`$, then flip the recorded sign with probability $`\epsilon`$, where $`0\leq\epsilon\leq1/2`$. The reported effects are

```math
F_s=(1-\epsilon)P_s+\epsilon P_{-s}
=\frac12[I+s(1-2\epsilon)Z].
```

These are the tunable effects with $`\eta=1-2\epsilon`$. The same POVM can therefore describe an unsharp interaction or a sharp measurement followed by reporting errors.

**Coarse graining** merges several outcomes into one. If two measured bits have effects $`E_{00},E_{01},E_{10},E_{11}`$, retaining only their parity gives

```math
F_{\mathrm{even}}=E_{00}+E_{11},\qquad
F_{\mathrm{odd}}=E_{01}+E_{10}.
```

This is useful when the task needs parity rather than both individual bits. But deleting detail from a classical record does not undo the physical measurement. Measuring both data qubits and forgetting their individual values can destroy coherence that a direct parity measurement preserves.

To describe that difference, probabilities are no longer enough. We need the state transformation caused by the measurement.

## 6. Operations and channels

A **quantum operation** is a **linear, completely positive, trace-nonincreasing map** $`\Phi`$ from input operators to output operators.

Linearity makes the map respect preparation mixtures. Positivity keeps positive inputs positive. **Complete positivity** requires this **even when the input is part of an entangled system**. For a reference system $`R`$ left untouched, $`\Phi\otimes\mathrm{id}_R`$ must preserve positivity for every finite reference dimension.

This is essential for operations on qubits inside a register. Transposition preserves positivity on an isolated system, but transposing one half of the Bell-state density matrix gives an eigenvalue of $`-1/2`$. The transpose map is therefore positive but not completely positive. It cannot be a universal physical operation on a subsystem.

An operation can describe a selected measurement outcome. Let $`p`$ be its probability and $`\rho'`$ its conditional output state. For normalized input $`\rho`$,

```math
p=\mathrm{tr}[\Phi(\rho)],\qquad
\rho'=\frac{\Phi(\rho)}{p}\quad\text{when }p>0.
```

Trace-nonincreasing means $`0\leq p\leq1`$ for a normalized positive input. The trace is the branch probability; $`\rho'`$ is the conditional output state. Keep the unnormalized branch until its probability has been extracted. Normalization generally makes the conditional update nonlinear.

A **channel** is a quantum operation that **preserves trace for every input**. It describes a process without outcome selection, such as a gate, noise, reset, or a measurement whose result is ignored.

These conditions define allowed transformations. Dilations and matrix representations explain how to realize and calculate them.

## 7. Stinespring, Kraus, and Choi

### Stinespring: include the ancilla, then discard it

Let $`\mathcal H`$ be the input space, $`\mathcal K`$ the output space, and $`\mathcal M`$ an ancilla space. A **Stinespring dilation** uses a map $`V:\mathcal H\to\mathcal K\otimes\mathcal M`$ such that

```math
\Phi(\rho)=\mathrm{tr}_{\mathcal M}(V\rho V^\dagger).
```

For a channel, $`V^\dagger V=I`$. It is an isometry and can be realized by adding a prepared ancilla and applying a suitable larger unitary.

The system can lose coherence because information becomes stored in correlations with the ancilla. For example, prepare an ancilla in $`\ket{0}`$ and apply a controlled-NOT (CNOT) gate. It flips the ancilla when the system is in $`\ket{1}`$:

```math
(\alpha\ket{0}+\beta\ket{1})\otimes\ket{0}
\longmapsto\alpha\ket{00}+\beta\ket{11}.
```

Discarding the ancilla leaves $`|\alpha|^2\ket{0}\bra{0}+|\beta|^2\ket{1}\bra{1}`$. The joint evolution was reversible, but the reduced state has lost its computational-basis coherence.

For an operation, $`V^\dagger V\leq I`$ is sufficient. Realizing a trace-decreasing operation physically also requires outcome selection. Unitary evolution followed only by discarding an ancilla always preserves trace.

### Kraus: calculate without retaining the ancilla

Choose an orthonormal ancilla basis $`\{\ket{\ell}\}`$. The operators $`K_\ell`$ map input vectors to output vectors. They are the components of the same joint map:

```math
V\ket{\psi}=\sum_\ell K_\ell\ket{\psi}\otimes\ket{\ell}.
```

The partial trace removes cross terms between different ancilla basis vectors, giving the **Kraus representation**:

```math
\Phi(\rho)=\sum_\ell K_\ell\rho K_\ell^\dagger,\qquad
V^\dagger V=\sum_\ell K_\ell^\dagger K_\ell.
```

A Kraus sum is completely positive. It defines an operation when the last sum is at most $`I`$, and a channel when it equals $`I`$. Kraus matrices can be rectangular if input and output dimensions differ.

Different Kraus sets can describe the same map. Their labels need not be observed outcomes. For example, complete dephasing has Kraus sets $`\{\ket{0}\bra{0},\ket{1}\bra{1}\}`$ and $`\{I/\sqrt2,Z/\sqrt2\}`$. One suggests measurement branches; the other suggests random phase flips. They give the same channel when those labels are not retained.

### Choi: store the entire operation in one matrix

Complete positivity appears to require testing all entangled inputs. In finite dimensions, one maximally entangled input is sufficient. Let the input dimension be $`d`$, with orthonormal basis $`\{\ket{i}\}_{i=1}^d`$. Introduce a reference of the same dimension. Define a normalized maximally entangled vector and the Choi operator of the map by

```math
\ket{\Omega}=\frac1{\sqrt d}\sum_{i=1}^d\ket{i}_R\otimes\ket{i}_{\mathrm{in}},\qquad
C_\Phi=(\mathrm{id}_R\otimes\Phi)(\ket{\Omega}\bra{\Omega}).
```

This **Choi operator** acts on reference–output space. Expanding it shows why it determines the whole map:

```math
C_\Phi=\frac1d\sum_{i,j}\ket{i}\bra{j}\otimes\Phi(\ket{i}\bra{j}).
```

Each block records the action on one basis operator, including off-diagonal operators that carry coherence. Every input matrix is a linear combination of these basis operators.

For a linear map in finite dimensions, complete positivity is equivalent to $`C_\Phi\geq0`$. A channel additionally satisfies $`\mathrm{tr}_{\mathrm{out}}C_\Phi=I_R/d`$; an operation satisfies the corresponding inequality. Here $`I_R`$ is the reference identity.

Some software uses the unnormalized vector $`\sum_i\ket{i}\otimes\ket{i}`$. Its Choi matrix is $`dC_\Phi`$, and its channel partial trace is $`I_R`$. Check normalization and tensor order before comparing implementations.

Kraus operators calculate the output; the Choi operator stores the map in one positive matrix. For a qubit-to-qubit operation, Kraus matrices are $`2\times2`$, while the Choi matrix is $`4\times4`$. Once the basis and convention are fixed, the Choi matrix is unique, but the Kraus set is not.

### Minimality connects the three descriptions

An eigendecomposition of the Choi matrix gives a Kraus representation. For a nonzero operation in finite dimensions,

```math
\begin{aligned}
\mathrm{rank}(C_\Phi)&=\text{minimum number of Kraus operators}\\
&=\text{minimum Stinespring ancilla dimension}.
\end{aligned}
```

A Kraus set is minimal when its operators are linearly independent. A minimal Stinespring dilation has no redundant ancilla dimensions. Let $`A`$ range over output operators and $`I_{\mathcal M}`$ denote the ancilla identity. The vectors $`(A\otimes I_{\mathcal M})V\ket{\psi}`$ then span the full output–ancilla space as $`A`$ and the input vary. In infinite dimensions, take the closure of that span.

As with Naimark dilation, any dilation contains a minimal one. Here the identifying isometry acts on the ancilla alone. If $`V_0`$ is minimal, another dilation has $`V=(I_{\mathcal K}\otimes W)V_0`$ for an ancilla isometry $`W`$. If both are minimal, $`W`$ is unitary. Minimal dimension does not imply minimum gate count.

### The dual map predicts output measurements from the input

For an output observable $`A`$, define the dual map $`\Phi^*`$ by

```math
\mathrm{tr}[\Phi(\rho)A]=\mathrm{tr}[\rho\Phi^*(A)],\qquad
\Phi^*(A)=\sum_\ell K_\ell^\dagger A K_\ell.
```

We can evolve the state forward or pull the observable back; both give the same prediction. Trace preservation becomes $`\Phi^*(I)=I`$. This will let us extract effects from measurement operations and calculate sequences of measurements.

Stinespring describes what remains after discarding an ancilla. To obtain a classical record as well, we must first read the ancilla as a probe.

## 8. Quantum measurement models

A **measurement model** specifies a probe space $`\mathcal K`$, its initial state $`\sigma`$, a joint unitary $`U`$, and pointer projectors $`Q_x`$. The system starts in $`\rho`$, independently of the probe.

**Prepare the probe → interact → read the pointer → discard the probe.**

The operation for pointer result $`x`$ is

```math
\mathcal I_x(\rho)=\mathrm{tr}_{\mathcal K}\left[
(I\otimes Q_x)U(\rho\otimes\sigma)U^\dagger(I\otimes Q_x)
\right].
```

Its trace is the probability of $`x`$. Dividing by that trace gives the conditional system state. This model describes the statistics and state changes; it does not resolve why one individual outcome occurs.

### The tunable Z measurement: statistics and disturbance together

An optical implementation adjusts a wave-plate parameter $`\gamma`$. Restrict it here to $`0\leq\gamma\leq\pi/4`$, over which measurement strength increases. Its outcome operators are

```math
K_\pm=\frac1{\sqrt2}(\cos\gamma\,I\pm\sin\gamma\,Z),\qquad
\mathcal I_\pm(\rho)=K_\pm\rho K_\pm^\dagger.
```

Computing their effects recovers our earlier detector:

```math
E_\pm=K_\pm^\dagger K_\pm
=\frac12[I\pm\sin(2\gamma)Z],\qquad \eta=\sin(2\gamma).
```

The same interaction also determines the state when the outcome is ignored:

```math
\Phi(\rho)=\mathcal I_+(\rho)+\mathcal I_-(\rho)
=\cos^2\gamma\,\rho+\sin^2\gamma\,Z\rho Z.
```

The computational-basis diagonal entries stay fixed. The off-diagonal entries are multiplied by $`c=\cos(2\gamma)=\sqrt{1-\eta^2}`$.

| Setting | Outcome information | State change when the outcome is ignored |
| --- | --- | --- |
| $`\gamma=0`$ | A fair random sign, independent of the input | No change |
| $`0<\gamma<\pi/4`$ | Partial information about $`Z`$ | Partial loss of coherence in the computational basis |
| $`\gamma=\pi/4`$ | Sharp $`Z`$ measurement | All computational-basis off-diagonal entries vanish |

The instrument here is the **Lüders instrument** for these effects: $`K_s=\sqrt{E_s}`$. At $`\eta=0.6`$, an input $`\rho_+`$ produces either result with probability one half. The conditional Bloch vectors are $`(0.8,0,0.6)`$ and $`(0.8,0,-0.6)`$. Both states are pure; averaging them gives the mixed state with vector $`(0.8,0,0)`$.

Compare this with sharp $`Z`$ followed by sign-reporting errors. It can have the same effects, but its ignored-result channel removes all computational-basis coherence at every error rate. Thus the information–disturbance relation above belongs to this chosen instrument, not to the POVM alone.

### The von Neumann model: a continuous pointer

Replace the probe qubit by a pointer with position $`q`$, momentum operator $`P`$, and normalized initial wavefunction $`\phi(q)`$. Let $`A`$ be the system observable being measured. With $`\hbar=1`$ and accumulated coupling strength $`g`$, the interaction is

```math
U=e^{-igA\otimes P}.
```

Momentum generates position shifts. If $`\ket{a}`$ is an eigenvector satisfying $`A\ket{a}=a\ket{a}`$, its pointer wavefunction shifts to $`\phi(q-ga)`$. The pointer's position now carries information about the eigenvalue.

For $`A=Z`$, the joint wavefunction changes as

```math
(\alpha\ket{0}+\beta\ket{1})\phi(q)
\longmapsto
\alpha\ket{0}\phi(q-g)+\beta\ket{1}\phi(q+g).
```

If the shifted distributions overlap strongly, one reading gives little information about the qubit's $`Z`$ value. If they are well separated, the reading distinguishes the two values reliably. Resolution depends on the shift relative to the pointer's initial width.

For a discrete observable $`A=\sum_a aP_a`$, where $`P_a`$ projects onto its eigenspace, the pointer probability density is

```math
p(q)=\sum_a\mathrm{tr}(\rho P_a)|\phi(q-ga)|^2.
```

The initial pointer distribution therefore blurs the target measurement. A Gaussian pointer always has some overlap at finite separation and width. Disjoint shifted supports can instead allow exact identification of discrete eigenvalues by grouping readings.

Define $`K(q)=\sum_a\phi(q-ga)P_a`$. For a set of readings $`B`$, the conditional operation is

```math
\mathcal I_B(\rho)=\int_B K(q)\rho K(q)^\dagger\,dq.
```

This is the continuous version of a Kraus sum. An exact reading is described by a density; an interval has a probability. Discarding the pointer multiplies coherence between different eigenvalue sectors by the overlap of their pointer states. Orthogonal pointer states remove that coherence completely.

The apparatus models differ, but both produce a classical record and a remaining quantum state. An instrument captures these two outputs without retaining the apparatus's internal details.

## 9. Instruments and measurement dilation

An **instrument** is a collection of quantum operations $`\{\mathcal I_x\}`$, one per recorded outcome, whose sum is a channel.

> [!IMPORTANT]
> An instrument describes **both a classical result and a remaining quantum state**.

For input $`\rho`$, it gives

```math
p(x)=\mathrm{tr}[\mathcal I_x(\rho)],\qquad
\rho_x=\frac{\mathcal I_x(\rho)}{p(x)}\quad(p(x)>0),\qquad
\Phi(\rho)=\sum_x\mathcal I_x(\rho).
```

The POVM follows by taking traces, or equivalently by applying the dual operations to the output identity:

```math
E_x=\mathcal I_x^*(I),\qquad
p(x)=\mathrm{tr}(\rho E_x).
```

Summing branches gives the channel with the result ignored. Keeping their labels preserves the relation between the classical result and the quantum state.

### Why an instrument is needed

Consider two devices with outcomes $`x=0,1`$. Device A measures the computational basis and leaves the corresponding eigenstate. Device B reports the same result, then resets the qubit to zero:

```math
\mathcal I_x(\rho)=\ket{x}\bra{x}\rho\ket{x}\bra{x},\qquad
\mathcal J_x(\rho)=\mathrm{tr}(\rho\ket{x}\bra{x})\ket{0}\bra{0}.
```

Their POVMs agree. After result 1, however, Device A leaves $`\ket{1}`$ and Device B leaves $`\ket{0}`$. A later gate or measurement distinguishes the devices. Their instruments contain the missing information.

Instruments are therefore needed for mid-circuit measurement, feedback, sequential measurements, and postselection. If result $`x`$ selects a unitary correction $`U_x`$, the average feedback channel is

```math
\Psi(\rho)=\sum_x U_x\mathcal I_x(\rho)U_x^\dagger.
```

A controller must retain the result until it has selected the correction.

### Measurement dilation: build the instrument with a probe

A **measurement dilation** realizes an instrument in a larger system. It must reproduce **both the probabilities and the conditional state changes**.

For example, initialize a probe qubit in $`\ket{0}`$, apply CNOT with the system as control, and read the probe in the computational basis. This realizes Device A above. Following that readout with a conditional reset realizes Device B. The probe construction specifies more than a POVM because it also specifies the remaining state.

More generally, write each outcome operation using Kraus operators $`K_{x\ell}`$:

```math
\mathcal I_x(\rho)=\sum_\ell K_{x\ell}\rho K_{x\ell}^\dagger,
\qquad \sum_{x,\ell}K_{x\ell}^\dagger K_{x\ell}=I.
```

Here $`x`$ is recorded, while $`\ell`$ labels terms that need not be resolved. Use orthonormal probe vectors $`\ket{x,\ell}`$ and define

```math
V\ket{\psi}=\sum_{x,\ell}K_{x\ell}\ket{\psi}\otimes\ket{x,\ell}.
```

The completeness condition makes $`V`$ an isometry. Measuring the probe sectors labeled by $`x`$ and discarding the probe gives exactly $`\mathcal I_x`$. For matching input and output spaces, this isometry extends to a joint unitary with a prepared probe. More general input and output spaces can use additional registers.

| Dilation | What the larger construction reproduces |
| --- | --- |
| Naimark | A POVM's outcome probabilities |
| Stinespring | An operation's state transformation |
| Measurement dilation | An instrument's outcome probabilities and conditional state transformations |

### Why this distinction matters for QEC

An ideal two-qubit parity measurement reports even or odd while preserving coherence within each parity subspace. Its projectors, labeled by $`s=\pm1`$, are

```math
P_s=\frac12(I+sZ\otimes Z),\qquad
\mathcal I_s(\rho)=P_s\rho P_s,
```

where $`I`$ is now the two-qubit identity. Prepare an ancilla in $`\ket{0}`$ and apply a CNOT from each data qubit to that ancilla. Measuring the ancilla gives the parity without distinguishing $`00`$ from $`11`$.

The Bell state $`\ket{\Phi^+}`$ therefore survives the ideal even-parity outcome. Measuring both data bits and retaining only their parity gives the same parity probabilities, but destroys that Bell-state coherence. Correct syndrome statistics alone do not establish that a measurement preserves the encoded information.

This is the reason for collective checks in [Gross-code state preparation](../gross-code/README.md#preparing-all-twelve-logical-qubits-in-zero). Fault tolerance additionally requires analysis of faults in the extraction circuit.

An instrument now lets us predict a full measurement sequence. [Chapter 2: incompatibility and uncertainty](incompatibility-and-uncertainty.md) asks which measurements can be combined and what an earlier measurement changes.

Last updated: 2026-11-10
