"""Rebuild the color-code figures with the repository's Python environment.

Stim supplies only the lattice coordinates and face supports. Its memory_xyz
measurement schedule is not the Helios SWAP-superdense extraction circuit.
Run: .venv/bin/python qec_knowledge_base/color-codes/build_figures.py
"""
from pathlib import Path
from itertools import permutations
import math
import os

os.environ.setdefault('MPLCONFIGDIR', '/tmp/qec-color-code-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import stim

OUT = Path(__file__).parent / 'assets'
OUT.mkdir(exist_ok=True)
INK = '#172b4d'
COLORS = ['#db5660', '#46a580', '#548fda']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'text.color': INK, 'svg.hashsalt': 'qec-color-code'})


def lattice(d):
    circuit = stim.Circuit.generated('color_code:memory_xyz', distance=d, rounds=2)
    coords = {q: (v[0], v[1] * math.sqrt(3)/2)
              for q, v in circuit.get_final_qubit_coordinates().items()}
    body = next(op.body_copy() for op in circuit if isinstance(op, stim.CircuitRepeatBlock))
    helpers = {t.value for op in body if op.name == 'MR' for t in op.targets_copy()}
    faces = {a: set() for a in sorted(helpers)}
    for op in body:
        if op.name == 'CX':
            ts = op.targets_copy()
            for a, b in zip(ts[::2], ts[1::2]):
                assert a.value not in helpers and b.value in helpers
                faces[b.value].add(a.value)
    data = set(coords) - helpers
    supports = list(faces.values())
    assert len(data) == (3*d*d+1)//4
    assert len(supports)*2 == len(data)-1
    assert all(len(f) in (4, 6) for f in supports)
    assert all(len(a & b) % 2 == 0 for a in supports for b in supports)
    # Three-colour the face-adjacency graph; no physical ion has a colour.
    colours = {}
    def colour(i):
        if i == len(supports):
            return True
        for c in range(3):
            if all(c != colours[j] for j in range(i) if supports[i] & supports[j]):
                colours[i] = c
                if colour(i+1):
                    return True
        colours.pop(i, None)
        return False
    assert colour(0)
    return {q: coords[q] for q in data}, supports, colours


def polygon(points, face):
    cx = sum(points[q][0] for q in face)/len(face)
    cy = sum(points[q][1] for q in face)/len(face)
    return sorted((points[q] for q in face), key=lambda p: math.atan2(p[1]-cy, p[0]-cx))


def draw(ax, points, faces, colours, labels=None, highlight=(), signs=False, focus=None):
    for i, face in enumerate(faces):
        vertices = polygon(points, face)
        alpha = .27 if focus is None or i == focus else .07
        ax.add_patch(Polygon(vertices, facecolor=COLORS[colours[i]], alpha=alpha, zorder=1))
        ax.add_patch(Polygon(vertices, fill=False, edgecolor=INK, lw=1.5, zorder=2))
        if labels is not None:
            cx = sum(p[0] for p in vertices)/len(vertices)
            cy = sum(p[1] for p in vertices)/len(vertices)
            label = chr(65+i)
            if signs:
                label += '\n' + ('−1' if len(face & set(highlight)) % 2 else '+1')
            ax.text(cx, cy, label, ha='center', va='center', weight='bold', fontsize=12, zorder=3)
    for q, (x,y) in points.items():
        ax.scatter([x], [y], s=280 if labels else 38, c='white',
                   edgecolors=INK, linewidths=1.4, zorder=4)
        if labels:
            ax.text(x, y, str(labels[q]), ha='center', va='center', fontsize=11, zorder=5)
        if q in highlight:
            ax.scatter([x], [y], s=480, facecolors='none', edgecolors='#b45309',
                       linewidths=2.8, zorder=6)
    xs, ys = zip(*points.values())
    ax.set(xlim=(min(xs)-.5,max(xs)+.5), ylim=(min(ys)-.45,max(ys)+.45))
    ax.set_aspect('equal')
    ax.axis('off')


def save(fig, name):
    fig.savefig(OUT / (name+'.png'), dpi=180, facecolor='white')
    fig.savefig(OUT / (name+'.svg'), facecolor='white', metadata={'Date': None})
    svg = OUT / (name+'.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
    plt.close(fig)


fig, axes = plt.subplots(1,3,figsize=(12,4.5))
fig.subplots_adjust(left=.02, right=.98, top=.82, bottom=.15, wspace=.10)
fig.suptitle('Triangular honeycomb color codes', fontsize=19, weight='bold', y=.98)
for ax, d in zip(axes, (3,5,7)):
    points, faces, colours = lattice(d)
    draw(ax,points,faces,colours)
    ax.set_title(f'd = {d}  ·  {len(points)} data qubits', fontsize=14, pad=16)
fig.text(.5,.055,'Circles = data qubits     •     Each coloured face supports both an X check and a Z check',
         ha='center',fontsize=12)
save(fig,'triangular-patches')

# Relabel the d=3 lattice to exactly match the README's three check supports.
points, oldfaces, _ = lattice(3)
expected = [{1,2,3,4},{1,2,5,6},{1,3,5,7}]
for perm in permutations(range(1,8)):
    labels = dict(zip(sorted(points),perm))
    mapped = [{labels[q] for q in f} for f in oldfaces]
    if all(f in mapped for f in expected):
        faces = [oldfaces[mapped.index(f)] for f in expected]
        break
else:
    raise AssertionError('No compatible seven-qubit numbering')
assert [{labels[q] for q in f} for f in faces] == expected
colours = {0:0,1:1,2:2}
reverse = {v:q for q,v in labels.items()}

fig, axes = plt.subplots(1,3,figsize=(12,5.0))
fig.subplots_adjust(left=.025,right=.975,top=.79,bottom=.25,wspace=.22)
fig.suptitle('Read the checks on a seven-qubit patch', fontsize=19, weight='bold', y=.97)
draw(axes[0],points,faces,colours,labels=labels,highlight=faces[0],focus=0)
axes[0].set_title('1. Check the four qubits of face A',fontsize=12,pad=14)
draw(axes[1],points,faces,colours,labels=labels,highlight={reverse[1]},signs=True)
axes[1].set_title('2. Apply one physical error: X₁',fontsize=12,pad=14)
logical = {reverse[q] for q in (5,6,7)}
draw(axes[2],points,faces,colours,labels=labels,highlight=logical,signs=True)
axes[2].set_title('3. Apply a logical operator: X₅X₆X₇',fontsize=12,pad=14)
notes = [
    'X check: X₁X₂X₃X₄\nZ check: Z₁Z₂Z₃Z₄',
    'Qubit 1 belongs to A, B and C.\nAll three Z-check signs flip.',
    'Each face meets 0 or 2 errors.\nZ checks pass; logical state changes.'
]
for x, note in zip((.17,.50,.83),notes):
    fig.text(x,.145,note,ha='center',va='center',fontsize=12,linespacing=1.6)
fig.text(.5,.035,'Gold rings mark the qubits acted on. Signs in panels 2–3 are Z-check outcomes, starting from +1.',
         ha='center',fontsize=11)
save(fig,'seven-qubit-checks')

fig, ax = plt.subplots(figsize=(12,4.3))
fig.subplots_adjust(left=.02,right=.98,bottom=.03,top=.95)
ax.set(xlim=(-1.8,8),ylim=(-.9,3.3))
ax.axis('off')
ax.text(3.1,3.0,'Transversal CNOT = seven separate physical CNOTs',
        ha='center',fontsize=18,weight='bold')
for y,name in ((2.05,'Control block'),(.45,'Target block')):
    ax.text(-.65,y,name,ha='right',va='center',fontsize=13,weight='bold')
    ax.plot([-.3,6.3],[y,y],lw=12,color='#e9eef5',solid_capstyle='round',zorder=0)
for i in range(7):
    fault = i==2
    colour = '#b45309' if fault else INK
    ax.plot([i,i],[.45,2.05],color=colour,lw=3 if fault else 1.8)
    ax.scatter([i],[2.05],s=100,c=colour,zorder=4)
    ax.scatter([i],[.45],s=500,facecolors='white',edgecolors=colour,linewidths=1.8,zorder=4)
    ax.text(i,.45,'+',ha='center',va='center',fontsize=23,color=colour,zorder=5)
    ax.text(i,2.35,str(i+1),ha='center',fontsize=12)
    ax.text(i,.05,str(i+1),ha='center',fontsize=12)
ax.text(3.1,-.55,'A fault in pair 3 can affect qubit 3 in both blocks; this gate does not spread it to the other pairs.',
        ha='center',fontsize=12)
save(fig,'transversal-cnot')
print('Validated d=3,5,7 data counts, face weights, even overlaps, three-colouring and README numbering.')
