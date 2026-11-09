"""Small, dense examples for the measurement learning path. Requires NumPy.

Tensor order is system first, ancilla second; outcomes are ordered +1, -1.
These checks illustrate the notes, not a general-purpose simulation library.
"""
import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULIS = (X, Y, Z)
ZERO = np.diag([1, 0]).astype(complex)
PLUS = (I + X) / 2


def state(r):
    """Density matrix from a physical Bloch vector."""
    r = np.asarray(r, dtype=float)
    if r.shape != (3,) or np.linalg.norm(r) > 1 + 1e-12:
        raise ValueError("Expected a Bloch vector of length at most one")
    return (I + sum(v * p for v, p in zip(r, PAULIS))) / 2


def apply_kraus(rho, kraus):
    return sum(k @ rho @ k.conj().T for k in kraus)


def discard_second(rho, d_first=2, d_second=2):
    return np.trace(
        rho.reshape(d_first, d_second, d_first, d_second), axis1=1, axis2=3
    )


def luders_operators(eta):
    if not 0 <= eta <= 1:
        raise ValueError("eta must lie between zero and one")
    a, b = np.sqrt((1 + eta) / 2), np.sqrt((1 - eta) / 2)
    return [np.diag([a, b]), np.diag([b, a])]


def choi(kraus):
    """Unnormalized Choi, reference/input first and output second."""
    d = kraus[0].shape[1]
    units = np.eye(d)
    return sum(
        np.kron(np.outer(units[i], units[j]),
                apply_kraus(np.outer(units[i], units[j]), kraus))
        for i in range(d) for j in range(d)
    )


def check_examples():
    # Reduced state and the failure of complete positivity for transposition.
    bell = np.array([1, 0, 0, 1]) / np.sqrt(2)
    bell_rho = np.outer(bell, bell)
    assert np.allclose(discard_second(bell_rho), I / 2)
    partial_transpose = bell_rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1)
    assert np.allclose(np.linalg.eigvalsh(partial_transpose.reshape(4, 4)),
                       [-0.5, 0.5, 0.5, 0.5])

    rho = state([0.4, -0.2, 0.6])
    for eta in (0.0, 0.3, 0.6, 0.8, 1.0):
        ks = luders_operators(eta)
        assert np.allclose(sum(k.conj().T @ k for k in ks), I)
        branches = [k @ rho @ k.conj().T for k in ks]
        probs = np.array([np.trace(b).real for b in branches])
        assert np.allclose(probs, [(1 + eta * 0.6) / 2, (1 - eta * 0.6) / 2])
        c = np.sqrt(1 - eta**2)
        expected = state([c * 0.4, c * -0.2, 0.6])
        assert np.allclose(sum(branches), expected)
        assert np.allclose(sum(p * b / p for p, b in zip(probs, branches)), expected)

        for s, p, branch in zip((1, -1), probs, branches):
            target = np.array([c * 0.4, c * -0.2, 0.6 + s * eta]) / (1 + s * eta * 0.6)
            assert np.allclose(branch / p, state(target))
            for t in (1, -1):
                f = (I + t * X) / 2
                assert np.isclose(np.trace(branch @ f), (1 + s * eta * 0.6 + t * c * 0.4) / 4)

        j = choi(ks)
        assert np.min(np.linalg.eigvalsh(j)) >= -1e-12
        assert np.allclose(discard_second(j), I)

        # A unitary extension, controlled by the system computational state.
        # U0|0> = (a,b), U1|0> = (b,a).
        a, b = ks[0][0, 0], ks[0][1, 1]
        u0 = np.array([[a, -b], [b, a]])
        u1 = np.array([[b, -a], [a, b]])
        u = np.kron(ZERO, u0) + np.kron(I - ZERO, u1)
        assert np.allclose(u.conj().T @ u, np.eye(4))
        joint = u @ np.kron(rho, ZERO) @ u.conj().T
        assert np.allclose(discard_second(joint), expected)
        for pointer, branch in zip((ZERO, I - ZERO), branches):
            projector = np.kron(I, pointer)
            assert np.allclose(discard_second(projector @ joint @ projector), branch)

        # Same POVM from sharp measurement plus noisy labels; different channel.
        eps = (1 - eta) / 2
        ps = (ZERO, I - ZERO)
        noisy = [(1 - eps) * ps[i] @ PLUS @ ps[i]
                 + eps * ps[1 - i] @ PLUS @ ps[1 - i] for i in (0, 1)]
        assert np.allclose([np.trace(b).real for b in noisy], [0.5, 0.5])
        assert np.allclose(sum(noisy), I / 2)

    # A zero-probability branch is an all-zero operator, not a normalized state.
    impossible = luders_operators(1.0)[1] @ ZERO @ luders_operators(1.0)[1]
    assert np.allclose(impossible, np.zeros((2, 2)))

    # Feedback: sharp Z and conditional X reset any state to zero.
    reset = ZERO @ rho @ ZERO + X @ (I - ZERO) @ rho @ (I - ZERO) @ X
    assert np.allclose(reset, ZERO)

    # Collective parity preserves the Bell coherence; separate Z measurements do not.
    p_even = (np.eye(4) + np.kron(Z, Z)) / 2
    assert np.allclose(p_even @ bell_rho @ p_even, bell_rho)
    separate = apply_kraus(bell_rho, [np.kron(a, b) for a in (ZERO, I - ZERO)
                                    for b in (ZERO, I - ZERO)])
    assert np.allclose(separate, np.diag([0.5, 0, 0, 0.5]))

    # Explicit parity ancilla circuit: basis |data0,data1,ancilla>.
    u_parity = np.zeros((8, 8))
    for a in range(2):
        for b in range(2):
            for anc in range(2):
                u_parity[4*a + 2*b + (anc ^ a ^ b), 4*a + 2*b + anc] = 1
    pair = np.kron(PLUS, PLUS)
    coupled = u_parity @ np.kron(pair, ZERO) @ u_parity.T
    for pointer, p in zip((ZERO, I - ZERO), (p_even, np.eye(4) - p_even)):
        proj = np.kron(np.eye(4), pointer)
        assert np.allclose(discard_second(proj @ coupled @ proj, 4, 2), p @ pair @ p)

    # Tetrahedral tomography and compatibility boundary.
    directions = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
    effects = [(I + sum(v*p for v, p in zip(n, PAULIS))) / 4 for n in directions]
    probs = np.array([np.trace(rho @ e).real for e in effects])
    assert np.allclose(sum(effects), I)
    assert np.allclose(3 * probs @ directions, [0.4, -0.2, 0.6])
    for a, b in ((0.6, 0.8), (0.8, 0.8)):
        smallest = np.linalg.eigvalsh((I + a*Z + b*X) / 4)[0]
        assert np.isclose(smallest, (1 - np.sqrt(a*a + b*b)) / 4)

    # Amplitude-damping worked answer.
    gamma = 0.3
    damping = [np.diag([1, np.sqrt(1-gamma)]), np.array([[0, np.sqrt(gamma)], [0, 0]])]
    assert np.allclose(apply_kraus(I - ZERO, damping), np.diag([gamma, 1-gamma]))
    assert np.allclose(apply_kraus(PLUS, damping),
                       np.array([[1+gamma, np.sqrt(1-gamma)], [np.sqrt(1-gamma), 1-gamma]])/2)
    print("All deterministic identity checks passed.")


def sample_example():
    rng = np.random.default_rng(20261109)
    eta, shots = 0.6, 10000
    ks = luders_operators(eta)
    branches = [k @ PLUS @ k.conj().T for k in ks]
    probs = np.array([np.trace(b).real for b in branches])
    result = rng.choice(2, p=probs)
    conditional = branches[result] / probs[result]  # Never normalize a zero-weight branch.
    print("Sampled outcome:", (1, -1)[result])
    print("Conditional Bloch vector:", [round(float(np.trace(conditional @ p).real), 4) for p in PAULIS])
    r = np.array([0.4, -0.2, 0.6])
    plus_counts = rng.binomial(shots, (1 + eta * r) / 2)
    estimate = (2 * plus_counts / shots - 1) / eta
    print("Tomography target:", r)
    print("Finite-shot estimate with calibrated eta=0.6:", estimate)
    print("Estimated Bloch length:", np.linalg.norm(estimate))


if __name__ == "__main__":
    check_examples()
    sample_example()
