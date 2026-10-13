"""Reproduce the Gross-code teaching figures and algebraic checks.

Run from Notebooks: .venv/bin/python qec_knowledge_base/gross-code/build_examples.py
Requires NumPy, Matplotlib, and Stim. This does not certify the distance lower bound
and does not simulate noisy 144-qubit syndrome-extraction circuits.
"""
from pathlib import Path
import json
import os
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "gross-code-mpl"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import stim
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
ELL, M, N = 12, 6, 144
A = [(3, 0), (0, 1), (0, 2)]
B = [(0, 3), (1, 0), (2, 0)]
COLORS = {"L": "#007ab5", "R": "#e5a000", "X": "#ef6092", "Z": "#00ac86"}
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def index(register, i, j):
    return (72 if register == "R" else 0) + (i % ELL) * M + j % M


def vector(left, right=()):
    v = 0
    for register, terms in [("L", left), ("R", right)]:
        for i, j in terms:
            v ^= 1 << index(register, i, j)
    return v


def rows(left_offsets, right_offsets):
    return [vector([(i + a, j + b) for a, b in left_offsets],
                   [(i + a, j + b) for a, b in right_offsets])
            for i in range(ELL) for j in range(M)]


HX = rows(A, B)
HZ = rows([(-i, -j) for i, j in B], [(-i, -j) for i, j in A])


def dot(a, b):
    return (a & b).bit_count() % 2


def insert(v, basis):
    while v:
        p = v.bit_length() - 1
        if p in basis:
            v ^= basis[p]
        else:
            basis[p] = v
            return True
    return False


def span_basis(rs):
    basis = {}
    for v in rs:
        insert(v, basis)
    return basis


def nullspace(rs):
    """RREF over GF(2), then one solution per free column."""
    reduced = list(rs)
    pivots = []
    r = 0
    for c in range(N):
        candidate = next((j for j in range(r, len(reduced)) if (reduced[j] >> c) & 1), None)
        if candidate is None:
            continue
        reduced[r], reduced[candidate] = reduced[candidate], reduced[r]
        for j in range(len(reduced)):
            if j != r and (reduced[j] >> c) & 1:
                reduced[j] ^= reduced[r]
        pivots.append(c)
        r += 1
    answers = []
    for free in sorted(set(range(N)) - set(pivots)):
        v = 1 << free
        for p, row in zip(pivots, reduced):
            if dot(row, v):
                v ^= 1 << p
        answers.append(v)
    assert all(dot(row, v) == 0 for row in rs for v in answers)
    return answers


def quotient_basis(stabilizers, kernel, seed):
    basis = span_basis(stabilizers)
    answer = []
    for v in [seed] + kernel:
        if insert(v, basis):
            answer.append(v)
    return answer


# Equations (64)-(67) in Cross et al., arXiv:2407.18393v2.
X1 = vector([(0, 1), (1, 5), (2, 2), (2, 4), (3, 1), (3, 2),
             (4, 1), (4, 2), (9, 3), (10, 0), (11, 0), (11, 3)],
            [(0, 2), (1, 1), (1, 5), (6, 0)])
Z1 = vector([(2, 3), (2, 5), (3, 0), (3, 3), (3, 4), (3, 5)],
            [(1, 3), (1, 5), (2, 0), (2, 4), (3, 2), (3, 4)])
NX, NZ = nullspace(HZ), nullspace(HX)
LX, LZ = quotient_basis(HX, NX, X1), quotient_basis(HZ, NZ, Z1)
assert len(LX) == len(LZ) == 12
for i in range(12):
    j = next(j for j in range(i, 12) if dot(LX[i], LZ[j]))
    LZ[i], LZ[j] = LZ[j], LZ[i]
    for j in range(i + 1, 12):
        if dot(LX[j], LZ[i]):
            LX[j] ^= LX[i]
        if dot(LX[i], LZ[j]):
            LZ[j] ^= LZ[i]
assert LX[0] == X1 and LZ[0] == Z1
assert all(dot(x, z) == (i == j) for i, x in enumerate(LX) for j, z in enumerate(LZ))
assert all(dot(x, z) == 0 for x in HX for z in HZ)
assert all(dot(x, z) == 0 for x in LX for z in HZ)
assert all(dot(z, x) == 0 for z in LZ for x in HX)


def support(v):
    return [{"register": "L" if q < 72 else "R", "i": (q % 72) // M,
             "j": q % M, "column": q} for q in range(N) if (v >> q) & 1]


def as_array(rs):
    return np.array([[(r >> q) & 1 for q in range(N)] for r in rs], dtype=np.uint8)


def save(fig, name):
    fig.savefig(ASSETS / (name + ".png"), dpi=180, bbox_inches="tight", facecolor="white")
    svg_path = ASSETS / (name + ".svg")
    fig.savefig(svg_path, bbox_inches="tight", facecolor="white")
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
    plt.close(fig)


def grid(ax, title):
    ii, jj = np.meshgrid(range(ELL), range(M))
    ax.scatter(ii, jj, s=18, color="#d7dfe5")
    ax.set(xticks=range(ELL), yticks=range(M), xlim=(-.6, 11.6), ylim=(-.6, 5.6),
           xlabel="i (mod 12)", ylabel="j (mod 6)", title=title)
    ax.grid(alpha=.15)
    ax.set_aspect("equal")


# A genuine toric drawing: four short edges and two extra edges at every vertex.
def location(register, i, j):
    offsets = {"X": (0, 0), "L": (0, -3), "R": (-3, 0), "Z": (-3, -3)}
    di, dj = offsets[register]
    return ((2 * i + di) % 24, (2 * j + dj) % 12)


# A check at the cut's lower-left corner makes both periodic seams visible.
# Split a wrapped edge at the boundary instead of drawing a spurious line
# across the interior of the cut-open torus.
fig = plt.figure(figsize=(16, 8))
ax = fig.add_axes([.045, .17, .66, .72])
left, right, bottom, top = -.5, 23.5, -.5, 11.5
for i in range(24):
    ax.plot([i, i], [bottom, top], color="#dbe2e8", lw=.65, zorder=0)
for j in range(12):
    ax.plot([left, right], [j, j], color="#dbe2e8", lw=.65, zorder=0)
for register in ["L", "R", "X", "Z"]:
    points = np.array([location(register, i, j) for i in range(ELL) for j in range(M)])
    ax.scatter(points[:, 0], points[:, 1], color=COLORS[register],
               marker="o" if register in "LR" else "s", s=19, alpha=.42)
# Blue boundaries are identified with each other; purple boundaries likewise.
for x in [left, right]:
    ax.plot([x, x], [bottom, top], color="#275dad", lw=2.2, zorder=1)
for y in [bottom, top]:
    ax.plot([left, right], [y, y], color="#8c55ad", lw=2.2, zorder=1)
ax.text(11.5, 12.1, "top ↔ bottom (purple seam)", ha="center", color="#8c55ad", fontsize=11)
ax.text(11.5, -1.25, "left ↔ right (blue seam)", ha="center", color="#275dad", fontsize=11)
origin = (0, 0)
ox, oy = location("X", *origin)
label_positions = {"x³": (7.1, 9.5), "y": (1.1, 10.7), "y²": (1.7, 1.2),
                   "y³": (18.2, 6.8), "x": (20.0, .8), "x²": (3.3, .15)}
wrap_channels = {"x³": "b", "y": "a", "y³": "d", "x": "c"}
for register, offsets, terms in [("L", A, ["x³", "y", "y²"]), ("R", B, ["y³", "x", "x²"])]:
    for (di, dj), term in zip(offsets, terms):
        i, j = di % ELL, dj % M
        px, py = location(register, i, j)
        # Position before applying periodic wrapping in the drawing.
        dx0, dy0 = {"L": (0, -3), "R": (-3, 0)}[register]
        ux, uy = 2 * di + dx0, 2 * dj + dy0
        color, style = COLORS[register], "--" if register == "L" else "-"
        if ux < left:
            t = (left - ox) / (ux - ox)
            exit_point = (left, oy + t * (uy - oy))
            entry_point = (right, exit_point[1])
        elif uy < bottom:
            t = (bottom - oy) / (uy - oy)
            exit_point = (ox + t * (ux - ox), bottom)
            entry_point = (exit_point[0], top)
        else:
            exit_point = entry_point = None
        if exit_point:
            for p0, p1 in [((ox, oy), exit_point), (entry_point, (px, py))]:
                ax.annotate("", xy=p1, xytext=p0,
                            arrowprops=dict(arrowstyle="->", color=color, lw=2.1, linestyle=style), zorder=4)
            letter = wrap_channels[term]
            for point in [exit_point, entry_point]:
                ax.scatter(*point, s=85, facecolors="white", edgecolors=color, lw=1.8, zorder=6, clip_on=False)
                # Matching letters identify the continuation of the same edge.
                dy_label = -.25 if point[1] == bottom else .28 if point[1] == top else .28
                dx_label = -.35 if point[0] == left else .35 if point[0] == right else 0
                ax.text(point[0] + dx_label, point[1] + dy_label, letter,
                        ha="center", va="center", color=color, fontsize=10, fontweight="bold", zorder=7)
        else:
            ax.plot([ox, px], [oy, py], color=color, lw=2.1, ls=style, zorder=4)
        ax.scatter([px], [py], color=color, s=90, edgecolor="white", zorder=5)
        ax.annotate(f"{register}({i},{j}) : {term}", (px, py), xytext=label_positions[term],
                    textcoords="data", fontsize=10, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color="#475569", lw=.8),
                    bbox=dict(facecolor="white", alpha=.95, edgecolor="none", pad=1), zorder=8)
ax.scatter([ox], [oy], color=COLORS["X"], marker="s", s=110, edgecolor="black", zorder=8)
ax.annotate("X check (0,0)", (ox, oy), xytext=(1.7, 3.3),
            arrowprops=dict(arrowstyle="->", color="#334155"), fontsize=11,
            bbox=dict(facecolor="white", edgecolor="none"), zorder=8)
ax.set(xlim=(-1.5, 24.5), ylim=(-1.8, 12.8), xticks=[], yticks=[], aspect="equal")
ax.axis("off")
ax.set_title("Figure 1 · A boundary check on the cut-open torus", pad=16, fontsize=15)
legend = [Line2D([], [], marker="o" if r in "LR" else "s", ls="", color=COLORS[r],
                 label=r + (" data" if r in "LR" else " check")) for r in ["L", "R", "X", "Z"]]
legend += [Line2D([], [], ls="--", color="black", label="A edge"),
           Line2D([], [], color="black", label="B edge")]
fig.legend(handles=legend, loc="lower left", bbox_to_anchor=(.065, .08), ncol=6, fontsize=10)
fig.text(.365, .03, "An edge leaving the rectangle returns at the matching letter on the opposite boundary.",
         ha="center", fontsize=10, color="#475569")
# The adjacent torus visual makes the two boundary identifications concrete.
ax3 = fig.add_axes([.73, .32, .26, .43], projection="3d", computed_zorder=False)
u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 65), np.linspace(0, 2 * np.pi, 33))
major, minor = 2.0, .72
xx = (major + minor * np.cos(v)) * np.cos(u)
yy = (major + minor * np.cos(v)) * np.sin(u)
zz = minor * np.sin(v)
ax3.plot_surface(xx, yy, zz, color="#d7e7ed", alpha=.18, linewidth=0,
                 antialiased=True, shade=False, zorder=1)
ax3.plot_wireframe(xx, yy, zz, rstride=4, cstride=4, color="#9caeb9", lw=.45, alpha=.4, zorder=2)
curve = np.linspace(0, 2 * np.pi, 200)
ax3.plot((major + minor * np.cos(curve)), np.zeros_like(curve), minor * np.sin(curve),
         color="#275dad", lw=3, zorder=3)
ax3.plot((major + minor) * np.cos(curve), (major + minor) * np.sin(curve), np.zeros_like(curve),
         color="#8c55ad", lw=3, zorder=3)
ax3.set_box_aspect((1, 1, .3))
ax3.view_init(elev=62, azim=-58)
ax3.axis("off")
fig.text(.86, .80, "Identify both pairs of boundaries", ha="center", fontsize=12, fontweight="bold")
fig.text(.86, .25, "left + right → cylinder\nthen top + bottom → torus", ha="center", fontsize=11, linespacing=1.8)
fig.text(.86, .14, "The torus depicts connectivity.\nThe chip need not be donut-shaped.",
         ha="center", fontsize=10, color="#475569")
save(fig, "check-pattern")

# Two shared data sites explain commutation without a dense graph.
fig, axes = plt.subplots(1, 2, figsize=(14, 4.6))
xcheck, zcheck = HX[0], HZ[3 * M + 3]
for ax, register in zip(axes, ["L", "R"]):
    grid(ax, register + " register: X(0,0) versus Z(3,3)")
    for v, color, marker in [(xcheck, COLORS["X"], "o"), (zcheck, COLORS["Z"], "s")]:
        points = [q for q in support(v) if q["register"] == register]
        ax.scatter([q["i"] for q in points], [q["j"] for q in points],
                   marker=marker, s=145, facecolors="none", edgecolors=color, linewidths=2)
    shared = [q for q in support(xcheck & zcheck) if q["register"] == register]
    for q in shared:
        ax.scatter(q["i"], q["j"], s=30, color="#212b36")
        ax.annotate(f"shared {register}({q['i']},{q['j']})", (q["i"], q["j"]),
                    xytext=(12, 12), textcoords="offset points", fontsize=10)
fig.suptitle("Two shared qubits → two minus signs → commuting checks", y=1.03, fontsize=15)
save(fig, "commuting-checks")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, rs, title in zip(axes, [HX, HZ], [r"$H_X=[A\mid B]$", r"$H_Z=[B^T\mid A^T]$"]):
    arr = as_array(rs)
    rr, cc = np.nonzero(arr)
    ax.scatter(cc, rr, s=3, color="#007ab5")
    ax.axvline(71.5, color="#e5a000", lw=1.5)
    ax.set(xlim=(-1, 144), ylim=(72, -1), xlabel="data column: L 0–71 | R 72–143",
           ylabel="check row: 6i+j", title=title + "  (72 × 144, rank 66)")
save(fig, "binary-check-matrices")

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
for row, (v, name) in enumerate([(X1, "logical X₁: weight 16"), (Z1, "logical Z₁: weight 12")]):
    for col, register in enumerate(["L", "R"]):
        ax = axes[row, col]
        grid(ax, name + " — " + register)
        points = [q for q in support(v) if q["register"] == register]
        ax.scatter([q["i"] for q in points], [q["j"] for q in points], s=80, color=COLORS[register])
        if register == "R":
            ax.scatter([1], [5], s=220, facecolors="none", edgecolors="black", linewidths=2)
            ax.annotate("only shared site", (1, 5), xytext=(25, -30), textcoords="offset points",
                        arrowprops=dict(arrowstyle="->"), fontsize=10)
fig.suptitle("A logical pair: zero syndrome, but one shared site makes X₁Z₁ = −Z₁X₁", fontsize=15, y=.99)
fig.subplots_adjust(hspace=.65, wspace=.18, top=.88)
save(fig, "logical-operators")

# Verify the logical measurement gadget as linear maps for all outcome branches.
I = np.eye(2, dtype=complex)
XP = np.array([[0, 1], [1, 0]], complex)
ZP = np.diag([1, -1]).astype(complex)
ZZ = np.kron(np.kron(ZP, ZP), I)
XX = np.kron(np.kron(I, XP), XP)
ZA = np.kron(np.kron(I, ZP), I)
embedding = np.zeros((8, 4), complex)
for c in range(2):
    for t in range(2):
        for a in range(2):
            embedding[4 * c + 2 * a + t, 2 * c + t] = 1 / np.sqrt(2)
target = np.zeros((4, 4), complex)
for c in range(2):
    for t in range(2):
        target[2 * c + (t ^ c), 2 * c + t] = 1
branches = []
for u in range(2):
    for v in range(2):
        for w in range(2):
            channel = embedding.copy()
            for observable, outcome in [(ZZ, u), (XX, v), (ZA, w)]:
                channel = (np.eye(8) + (-1) ** outcome * observable) @ channel / 2
            reduced = channel[[4 * c + 2 * w + t for c in range(2) for t in range(2)], :]
            correction = np.kron(np.linalg.matrix_power(ZP, v), np.linalg.matrix_power(XP, u ^ w))
            corrected = correction @ reduced
            amplitude = np.vdot(target, corrected) / np.vdot(target, target)
            residual = float(np.max(np.abs(corrected - amplitude * target)))
            assert residual < 1e-12 and abs(abs(amplitude) ** 2 - 1 / 8) < 1e-12
            branches.append({"u_ZZ": u, "v_XX": v, "w_ZA": w,
                             "Z_control": v, "X_target": u ^ w, "matrix_residual": residual})

fig, ax = plt.subplots(figsize=(13, 5))
ax.set(xlim=(0, 12), ylim=(-.8, 3.2))
ax.axis("off")
for label, y in [("control C", 2.4), ("ancilla A: |+⟩", 1.3), ("target T", .2)]:
    ax.text(0, y, label, va="center")
    ax.plot([2, 11.7], [y, y], color="#334155", lw=1.5)
for x, y0, y1, label in [(3.1, 1.3, 2.4, "measure Z̄C Z̄A\noutcome u"), (5.8, .2, 1.3, "measure X̄A X̄T\noutcome v")]:
    ax.add_patch(Rectangle((x - .9, y0 - .2), 1.8, y1 - y0 + .4, facecolor="#e7f2f8", edgecolor="#007ab5"))
    ax.text(x, (y0 + y1) / 2, label, ha="center", va="center", fontsize=10)
ax.add_patch(Rectangle((7.6, 1.05), 1.5, .5, facecolor="#fce6ee", edgecolor="#ef6092"))
ax.text(8.35, 1.3, "measure Z̄A\noutcome w", ha="center", va="center", fontsize=10)
for y, label in [(2.4, "Z̄Cᵛ"), (.2, "X̄Tᵘ⊕ʷ")]:
    ax.add_patch(Rectangle((10, y - .25), 1.2, .5, facecolor="#fff2cf", edgecolor="#b98500"))
    ax.text(10.6, y, label, ha="center", va="center")
ax.text(6, -.5, "Outcome bits: +1 → 0; −1 → 1. Corrections may be tracked in a Pauli frame.", ha="center")
ax.set_title("An exact CNOT on selected logical qubits, given fault-tolerant joint-parity measurements", pad=16)
save(fig, "measurement-cnot")

# Compile a selected logical CNOT into a concrete ideal physical circuit.
# Both operands are in the SAME Gross block: control logical 1, target logical 2.
# Ancilla 144 is unencoded and 145 measures parities: NOT fault tolerant.
selected = stim.Circuit()
selected.append("RX", [144])
selected.append("R", [145])
z_sites = [q["column"] for q in support(LZ[0])]
x_sites = [q["column"] for q in support(LX[1])]
for q in z_sites + [144]:
    selected.append("CX", [q, 145])
selected.append("M", [145])
selected.append("RX", [145])
for q in x_sites + [144]:
    selected.append("CX", [145, q])
selected.append("MX", [145])
selected.append("M", [144])
for q in z_sites:
    selected.append("CZ", [stim.target_rec(-2), q])
for q in x_sites:
    selected.append("CX", [stim.target_rec(-3), q])
    selected.append("CX", [stim.target_rec(-1), q])


def pauli(v, letter):
    return stim.PauliString("".join(letter if (v >> q) & 1 else "I" for q in range(N)))


independent_x = list(span_basis(HX).values())
independent_z = list(span_basis(HZ).values())
stabilizers = [pauli(h, "X") for h in independent_x] + [pauli(h, "Z") for h in independent_z]
physical_cnot_cases = []
for control_bit in range(2):
    for target_bit in range(2):
        logical_state_stabilizers = [(-1 if (control_bit if i == 0 else target_bit if i == 1 else 0) else 1) * pauli(z, "Z")
                                    for i, z in enumerate(LZ)]
        state = stim.Tableau.from_stabilizers(stabilizers + logical_state_stabilizers)
        sim = stim.TableauSimulator(seed=7)
        sim.set_inverse_tableau(state.inverse())
        sim.do_circuit(selected)
        expected_bits = [control_bit, control_bit ^ target_bit] + [0] * 10
        assert all(sim.peek_observable_expectation(pauli(z, "Z")) == (-1) ** b for z, b in zip(LZ, expected_bits))
        assert all(sim.peek_observable_expectation(s) == 1 for s in stabilizers)
        physical_cnot_cases.append({"input": [control_bit, target_bit], "output": expected_bits[:2]})
bell_state = stim.Tableau.from_stabilizers(stabilizers + [pauli(LX[0], "X")] + [pauli(z, "Z") for z in LZ[1:]])
sim = stim.TableauSimulator(seed=11)
sim.set_inverse_tableau(bell_state.inverse())
sim.do_circuit(selected)
assert sim.peek_observable_expectation(pauli(LX[0] ^ LX[1], "X")) == 1
assert sim.peek_observable_expectation(pauli(LZ[0] ^ LZ[1], "Z")) == 1
assert all(sim.peek_observable_expectation(pauli(z, "Z")) == 1 for z in LZ[2:])
assert all(sim.peek_observable_expectation(s) == 1 for s in stabilizers)
(ROOT / "selected_cnot_ideal.stim").write_text(
    "# Ideal logical CNOT 1 -> 2 within one already-encoded Gross block.\n"
    "# Qubits 0..143 are data; 144 is an UNENCODED ancilla; 145 is a check ancilla.\n"
    "# Requires input in the code space. Not a fault-tolerant hardware schedule.\n"
    "# First two measurements return u,v; third returns w.\n"
    "# Record-controlled gates implement the Pauli corrections.\n" + str(selected) + "\n")

# Concrete gauging identity for the twelve sites of Z1, using a path of 11
# auxiliary edge qubits. This illustrates the algebra, NOT distance preservation.
ordered_sites = [q["column"] for q in support(Z1)]
vertex_x = []
vertex_z = []
for t, q in enumerate(ordered_sites):
    edges = 0
    if t > 0:
        edges ^= 1 << (N + t - 1)
    if t < len(ordered_sites) - 1:
        edges ^= 1 << (N + t)
    vertex_x.append(edges)
    vertex_z.append(1 << q)
product_x = product_z = 0
for x, z in zip(vertex_x, vertex_z):
    product_x ^= x
    product_z ^= z
assert product_x == 0 and product_z == Z1
dressings = []
for h in HX:
    parity = 0
    auxiliary_z = 0
    for t, q in enumerate(ordered_sites[:-1]):
        parity ^= (h >> q) & 1
        if parity:
            auxiliary_z ^= 1 << (N + t)
    assert dot(h, Z1) == 0
    assert all((dot(h, z) ^ dot(auxiliary_z, x)) == 0 for x, z in zip(vertex_x, vertex_z))
    dressings.append(auxiliary_z)

fig, ax = plt.subplots(figsize=(12, 3.5))
ax.axis("off")
ax.set(xlim=(-.5, 10.5), ylim=(-1.3, 1.8))
for x, label in [(1, "q₁"), (5, "q₂"), (9, "q₃")]:
    ax.scatter([x], [1], s=170, color=COLORS["L"])
    ax.text(x, 1.35, label, ha="center")
for x, label in [(3, "e₁"), (7, "e₂")]:
    ax.scatter([x], [0], s=150, color=COLORS["R"])
    ax.text(x, -.4, label + ": initialize |0⟩", ha="center")
for x, edge in [(1, 3), (5, 3), (5, 7), (9, 7)]:
    ax.plot([x, edge], [1, 0], color="#94a3b8", lw=2, zorder=0)
for x, label in [(1, "Q₁ = Zq₁ Xe₁"), (5, "Q₂ = Zq₂ Xe₁ Xe₂"), (9, "Q₃ = Zq₃ Xe₂")]:
    ax.text(x, -.95, label, ha="center", fontsize=11)
ax.set_title("How auxiliary checks reveal only a product: Q₁ Q₂ Q₃ = Zq₁ Zq₂ Zq₃", pad=18)
save(fig, "parity-measurement")

# A reproducible noiseless Z-basis codeword outcome, with one injected X error.
ideal = HX[0] ^ HX[5] ^ HX[12] ^ HX[38]
error = 1 << index("R", 1, 5)
measured = ideal ^ error
syndrome = [i for i, h in enumerate(HZ) if dot(h, measured)]
candidates = [q for q in range(N) if [i for i, h in enumerate(HZ) if dot(h, 1 << q)] == syndrome]
assert candidates == [index("R", 1, 5)]
assert all(dot(z, ideal) == 0 for z in LZ)
assert dot(Z1, measured) == 1 and dot(Z1, measured ^ error) == 0
report = {
    "construction": {"ell": ELL, "m": M, "n": N, "A": A, "B": B,
                     "column_order": "L:6i+j; R:72+6i+j", "row_order": "6i+j"},
    "rank_HX": len(span_basis(HX)), "rank_HZ": len(span_basis(HZ)),
    "kernel_dimension_HX": len(NZ), "kernel_dimension_HZ": len(NX), "k": len(LX),
    "row_weights_HX": sorted(set(r.bit_count() for r in HX)),
    "row_weights_HZ": sorted(set(r.bit_count() for r in HZ)),
    "column_weights_HX": sorted(set(as_array(HX).sum(axis=0).tolist())),
    "column_weights_HZ": sorted(set(as_array(HZ).sum(axis=0).tolist())),
    "commutation_matrix_nonzeros": int(np.count_nonzero(as_array(HX) @ as_array(HZ).T % 2)),
    "logical_overlap_matrix": [[dot(x, z) for z in LZ] for x in LX],
    "logical_pairs": [{"logical_index": i + 1, "X_weight": x.bit_count(), "Z_weight": z.bit_count(),
                       "X_support": support(x), "Z_support": support(z)} for i, (x, z) in enumerate(zip(LX, LZ))],
    "distance_evidence": {"verified_upper_bound": 12, "local_lower_bound_certification": "not performed",
                          "source_for_exact_distance": "Bravyi et al., arXiv:2308.07915v2 Table 3 and Section 6"},
    "CNOT_gadget_branches": branches,
    "selected_physical_CNOT": {
        "control_logical_index": 1, "target_logical_index": 2,
        "control_Z_support": support(LZ[0]), "target_X_support": support(LX[1]),
        "extra_qubits": 2, "quantum_two_qubit_CNOTs": len(z_sites) + len(x_sites) + 2,
        "computational_basis_cases": physical_cnot_cases,
        "Bell_pair_XX_ZZ_expectations": [1, 1], "spectator_logical_Zs_preserved": True,
        "all_original_stabilizers_preserved": True,
        "fault_tolerance": "not claimed; unencoded ancilla, no extraction or fault-tolerant parity measurement"},
    "illustrative_path_measurement": {
        "data_sites": support(Z1), "auxiliary_edge_qubits": 11,
        "product_of_vertex_checks_equals_Z1": product_z == Z1 and product_x == 0,
        "all_dressed_X_checks_commute_with_vertex_checks": True,
        "dressed_X_check_weights": sorted(set(h.bit_count() + e.bit_count() for h, e in zip(HX, dressings))),
        "distance_preservation": "not claimed; this path is an algebraic teaching example"},
    "readout": {"ideal_outcome_ones": support(ideal), "injected_X_error": support(error),
                "syndrome_check_coordinates": [[i // M, i % M] for i in syndrome],
                "single_error_candidates": candidates, "raw_logical_Z1_bit": dot(Z1, measured),
                "corrected_logical_Z1_bit": dot(Z1, measured ^ error)},
}
(ROOT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
np.savetxt(ROOT / "H_X.csv", as_array(HX), fmt="%d", delimiter=",")
np.savetxt(ROOT / "H_Z.csv", as_array(HZ), fmt="%d", delimiter=",")
print(json.dumps({"ranks": [report["rank_HX"], report["rank_HZ"]], "k": len(LX),
                  "logical_pair_weights": [[x.bit_count(), z.bit_count()] for x, z in zip(LX, LZ)],
                  "commutation_nonzeros": report["commutation_matrix_nonzeros"],
                  "verified_CNOT_branches": len(branches), "readout_syndrome": report["readout"]["syndrome_check_coordinates"]}))
