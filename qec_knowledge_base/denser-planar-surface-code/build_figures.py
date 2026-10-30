"""Draw the teaching figures for the denser planar surface-code reference.

Paths show logical connectivity from Low et al., Fig. 10; they are not a
qubit-by-qubit specification of its extraction circuit.
Run from the repository root:
  .venv/bin/python qec_knowledge_base/denser-planar-surface-code/build_figures.py
"""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/qec-denser-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Ellipse
import numpy as np

OUT = Path(__file__).parent / 'assets'
OUT.mkdir(exist_ok=True)
INK, X, Z, TWIST, WALL = '#20324a', '#c74d42', '#286fbc', '#16805b', '#9a78aa'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'text.color': INK, 'svg.hashsalt': 'denser-teaching-2026'})


def save(fig, name):
    fig.savefig(OUT / (name + '.png'), dpi=170, facecolor='white')
    fig.savefig(OUT / (name + '.svg'), facecolor='white', metadata={'Date': None})
    p = OUT / (name + '.svg')
    p.write_text('\n'.join(s.rstrip() for s in p.read_text().splitlines()) + '\n')
    plt.close(fig)


def setup(ax, xlim=(-.7, 9.7), ylim=(-1.0, 5.2)):
    ax.set(xlim=xlim, ylim=ylim, aspect='equal')
    ax.axis('off')


def patch(ax, dense=True):
    width = 9 if dense else 4
    ax.add_patch(Rectangle((0, 0), width, 4, fc='#f4f7fb', ec=INK, lw=1.7))
    points = [(0, 0), (0, 4), (width, 0), (width, 4)]
    if dense:
        points += [(4, 4), (5, 0), (3, 2), (6, 2)]
        ax.plot([3, 6], [2, 2], c=WALL, lw=7, alpha=.48, zorder=2)
    ax.scatter(*zip(*points), s=80, c=TWIST, edgecolors='white', linewidths=.7, zorder=6)


def path(ax, points, color, lw=4.0, **kwargs):
    ax.plot(*zip(*points), color=color, lw=lw, solid_capstyle='round', zorder=4, **kwargs)


def anatomy():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={'width_ratios': [1.2, 1]})
    ax = axs[0]
    setup(ax)
    patch(ax)
    ax.text(4.5, 4.75, 'A changed strip of checks', ha='center', weight='bold', fontsize=15)
    path(ax, [(4.5, 3.8), (4.5, 2.05)], X)
    path(ax, [(4.5, 1.95), (4.5, .2)], Z)
    ax.text(4.85, 3.0, 'X part', color=X)
    ax.text(4.85, .9, 'Z part', color=Z)
    ax.text(4.5, 2.35, 'domain wall', color=WALL, ha='center', fontsize=11)
    for x, text, tx in [(3, 'twist', 1.6), (6, 'twist', 7.4)]:
        ax.annotate(text, xy=(x, 2), xytext=(tx, 1.0), color=TWIST,
                    arrowprops={'arrowstyle': '->', 'color': TWIST}, ha='center')
    ax.text(4.5, -.7, 'One logical path changes from X to Z as it crosses.', ha='center', fontsize=11)
    ax = axs[1]
    setup(ax, (-3, 3), (-2.9, 3.4))
    ax.text(0, 2.9, 'Zoom in: one twist check', ha='center', weight='bold', fontsize=15)
    angles = np.radians([162, 90, 18, -54, -126])
    points = np.column_stack([1.65*np.cos(angles), 1.65*np.sin(angles)])
    for xy in points:
        ax.plot([0, xy[0]], [0, xy[1]], c='#bdc7d3', lw=2)
    for i, ((x,y), p) in enumerate(zip(points, ['X', 'X', 'Y', 'Z', 'Z']), 1):
        c = X if p == 'X' else Z if p == 'Z' else TWIST
        ax.add_patch(Circle((x,y), .35, fc='white', ec=c, lw=2.5))
        ax.text(x,y, f'{p}{i}', color=c, ha='center', va='center', weight='bold')
    ax.text(0, -.1, 'one combined\ncheck', ha='center', va='center', fontsize=11)
    ax.text(0, -2.2, '$S=X_1X_2Y_3Z_4Z_5$', ha='center', fontsize=15)
    ax.text(0, -2.7, 'Five circles = five data qubits', ha='center', fontsize=11)
    fig.subplots_adjust(left=.035, right=.98, top=.95, bottom=.06, wspace=.19)
    save(fig, 'twist-anatomy')


def loops():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.0))
    for ax in axs:
        setup(ax, (-.3, 9.3), (-1.0, 5.1))
        ax.add_patch(Rectangle((0, 0), 9, 4, fc='#f4f7fb', ec=INK, lw=1.6))
    ax = axs[0]
    ax.text(4.5, 4.6, 'Loop around an ordinary region', ha='center', weight='bold', fontsize=14)
    ax.add_patch(Ellipse((4.5, 2), 5.4, 2.5, fill=False, ec=Z, lw=3.5))
    ax.add_patch(Ellipse((4.5, 2), 2.9, 1.4, fill=False, ec=Z, lw=2, ls='--'))
    ax.add_patch(Circle((4.5, 2), .25, fc='none', ec=Z, lw=1.8, ls='--'))
    ax.annotate('', xy=(3.65,2), xytext=(2.2,2), arrowprops={'arrowstyle':'->','color':INK,'lw':1.7})
    ax.text(4.5, -.65, 'Can be removed using local checks.\nIts value is already fixed by those checks.', ha='center', fontsize=11)
    ax = axs[1]
    ax.text(4.5, 4.6, 'Loop around a pair of twists', ha='center', weight='bold', fontsize=14)
    ax.plot([3,6], [2,2], c=WALL, lw=7, alpha=.48)
    ax.scatter([3,6], [2,2], s=95, c=TWIST, zorder=5)
    ax.add_patch(Ellipse((4.5, 2), 5.4, 2.5, fill=False, ec=Z, lw=3.5))
    ax.text(4.5, .42, 'Z loop', color=Z, ha='center')
    ax.text(4.5, -.65, 'Local checks leave this value free: +1 or −1.\nIt can label a stored logical bit.', ha='center', fontsize=11)
    fig.subplots_adjust(left=.03, right=.98, top=.98, bottom=.12, wspace=.16)
    save(fig, 'why-the-loop-matters')


def logical_pairs():
    fig, axs = plt.subplots(2, 2, figsize=(12, 7.3))
    ax=axs[0,0]
    setup(ax, (-.8, 4.8), (-1, 5.1)); patch(ax, False)
    path(ax, [(1.4,0),(1.4,4)], X)
    path(ax, [(0,2.1),(4,2.1)], Z)
    ax.text(2,4.65,'Ordinary patch: one pair', ha='center', weight='bold',fontsize=14)
    ax.text(.3,3.0,'flip',color=X); ax.text(2.5,2.35,'read',color=Z)
    ax.text(2,-.7,'One independent logical qubit', ha='center',fontsize=11)
    for ax in [axs[0,1], axs[1,0], axs[1,1]]:
        setup(ax);patch(ax)
    ax=axs[0,1]
    ax.text(4.5,4.7,'Shared rectangle: left pair',ha='center',weight='bold',fontsize=14)
    path(ax, [(1,0),(1,4)],X)
    path(ax, [(0,.15),(5,.15)],Z)
    ax.text(1.3,3.15,'flip 1',color=X);ax.text(2.7,.55,'read 1',color=Z)
    ax.text(4.5,-.65,'Change qubit 1; leave qubits 2 and 3 alone.',ha='center',fontsize=11)
    ax=axs[1,0]
    ax.text(4.5,4.7,'Same rectangle: right pair',ha='center',weight='bold',fontsize=14)
    path(ax,[(4,3.85),(9,3.85)],X)
    path(ax,[(8,0),(8,4)],Z)
    ax.text(5,3.25,'flip 2',color=X);ax.text(6.6,.6,'read 2',color=Z)
    ax.text(4.5,-.65,'Change qubit 2; leave qubits 1 and 3 alone.',ha='center',fontsize=11)
    ax=axs[1,1]
    ax.text(4.5,4.7,'Same rectangle: extra loop pair',ha='center',weight='bold',fontsize=14)
    # A mixed path: unlike Pauli labels at the top crossing, same labels below.
    ax.add_patch(Ellipse((4.5,2),5.2,2.5,fill=False,ec=Z,lw=3.5,zorder=3))
    path(ax,[(3.5,4),(3.5,2)],X)
    path(ax,[(3.5,2),(5.6,.8),(5.6,0)],Z,ls='--')
    ax.text(.1,.45,'read 3:\nZ loop',color=Z,fontsize=11)
    ax.text(6.95,3.0,'flip 3:\nX then Z',color=X,fontsize=11)
    # Actual topological intersection at x=3.5 with the ellipse.
    ytop=2+1.25*np.sqrt(1-((-1)/2.6)**2)
    ax.scatter([3.5],[ytop],marker='*',s=250,c='#f0ad35',edgecolors=INK,lw=.6,zorder=7)
    ax.text(4.5,-.65,'The mixed path flips the loop value.',ha='center',fontsize=11)
    fig.text(.5,.025,'Red = physical X along a path. Blue = physical Z. Green dots = twists, including boundary junctions.\nThe three rectangle panels show different operators on ONE shared patch; local checks are omitted.',ha='center',fontsize=10.5)
    fig.subplots_adjust(left=.045,right=.97,top=.96,bottom=.14,wspace=.18,hspace=.19)
    save(fig,'three-logical-pairs')


if __name__ == '__main__':
    anatomy(); loops(); logical_pairs()
