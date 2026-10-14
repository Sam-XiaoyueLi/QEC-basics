"""Generate the hardware reference diagrams. Run from the repository root."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
from matplotlib.text import Text

OUT = Path(__file__).parent / 'assets'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'svg.fonttype': 'none'})
BLUE, RED, INK, GREEN = '#2563eb', '#dc2626', '#172b4d', '#0f766e'

def panel():
    fig, ax = plt.subplots(figsize=(14,4.4))
    fig.subplots_adjust(left=.02,right=.98,top=.98,bottom=.03)
    ax.set(xlim=(0,14),ylim=(0,4.2))
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

def txt(ax,x,y,s,**kw):
    kw.setdefault('color',INK)
    ax.text(x,y,s,**kw)

def arrow(ax,a,b,color=INK,both=False):
    ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='<->' if both else '->',color=color,lw=2))

def line(ax,x1,x2,y,color=INK,**kw):
    ax.plot([x1,x2],[y,y],color=color,lw=2,**kw)

def save(fig,name):
    # A shared canvas width and type scale keep page figures consistent.
    width, height = fig.get_size_inches()
    fig.set_size_inches(12, min(height * 12 / width, 4.8))
    for label in fig.findobj(Text):
        old = label.get_fontsize()
        label.set_fontsize(20 if old >= 18 else 18 if label.get_fontweight() == 'bold' else 16 if old >= 14 else 14)
    fig.savefig(OUT/f'{name}.png',dpi=120)
    fig.savefig(OUT/f'{name}.svg')
    p=OUT/f'{name}.svg'
    p.write_text('\n'.join(s.rstrip() for s in p.read_text().splitlines())+'\n')
    plt.close(fig)

fig, ax = plt.subplots(figsize=(12, 5.2))
fig.subplots_adjust(left=.02,right=.98,top=.98,bottom=.04)
ax.set(xlim=(0,12),ylim=(0,5.2)); ax.axis('off')
ax.add_patch(Rectangle((.35,.65),11.3,3.85,facecolor='#f8fafc',edgecolor='#cbd5e1'))
txt(ax,6,4.85,'Chip components',ha='center',fontsize=18,weight='bold')
line(ax,.7,11.3,4.1,color='#7c3aed')
txt(ax,6,4.3,'Readout line: probe in, signal out',ha='center',fontsize=12,color='#7c3aed')
for x,label in [(3,'A'),(9,'B')]:
    for offset in [-.7,.15]:
        ax.add_patch(Rectangle((x+offset,1.65),.55,.7,facecolor=BLUE))
    line(ax,x-.15,x+.15,2)
    ax.plot([x-.08,x+.08],[1.9,2.1],color=INK,lw=2)
    ax.plot([x-.08,x+.08],[2.1,1.9],color=INK,lw=2)
    txt(ax,x,1.32,f'Transmon {label}',ha='center',fontsize=12)
    # Resonator end near the qubit and opposite end near the readout line.
    ax.plot([x+.35,x+.35,x-.35,x-.35,x+.35,x+.35,x-.35,x-.35,x+.35,x+.35],
            [2.45,2.65,2.65,2.9,2.9,3.15,3.15,3.4,3.4,3.95],color='#d97706',lw=2.5)
    txt(ax,x+.75,3.1,'Readout\nresonator',ha='left',fontsize=10,color='#b45309')
    ax.plot([x-.95,x-.95,x-.77],[.85,1.75,1.85],color=RED,lw=2)
    arrow(ax,(x-.95,.7),(x-.95,1.2),RED)
    txt(ax,x-.95,.38,'Control line',ha='center',fontsize=11,color=RED)
ax.add_patch(Rectangle((5.6,1.65),.8,.7,facecolor='#ccfbf1',edgecolor=GREEN,lw=2))
ax.plot([3.8,5.6],[2,2],color=GREEN,lw=2,ls='--')
ax.plot([6.4,8.2],[2,2],color=GREEN,lw=2,ls='--')
txt(ax,6,2,'Coupler',ha='center',va='center',fontsize=10,color=GREEN)
txt(ax,6,2.65,'Sets the A–B interaction',ha='center',fontsize=12,color=GREEN)
save(fig,'chip-layout')

fig,ax=panel()
txt(ax,2.5,3.85,'Transmon circuit',ha='center',fontsize=16,weight='bold')
# Capacitor and Josephson junction connect the same two nodes.
line(ax,1.2,3.8,3); line(ax,1.2,3.8,1.2)
ax.plot([1.2,1.2],[3,2.2],color=INK,lw=2)
ax.plot([1.2,1.2],[1.95,1.2],color=INK,lw=2)
line(ax,.75,1.65,2.2,BLUE); line(ax,.75,1.65,1.95,BLUE)
ax.plot([3.8,3.8],[3,1.2],color=INK,lw=2)
ax.add_patch(Rectangle((3.65,1.96),.3,.3,facecolor='white',edgecolor=INK,lw=2))
ax.plot([3.65,3.95],[1.96,2.26],color=INK,lw=2)
ax.plot([3.65,3.95],[2.26,1.96],color=INK,lw=2)
txt(ax,.65,2.05,'C',ha='right',color=BLUE,fontsize=16)
txt(ax,4.05,2.1,'JJ',color=INK,fontsize=14)
txt(ax,2.5,.65,'Capacitor ∥ junction',ha='center',fontsize=13)
arrow(ax,(2.5,3.6),(2.5,3.05),RED)
txt(ax,2.5,3.65,'Microwave drive',ha='center',fontsize=11,color=RED)
txt(ax,7.5,3.85,'Josephson junction',ha='center',fontsize=16,weight='bold')
for x,w,c in [(5.5,1.8,BLUE),(7.3,.2,'#f59e0b'),(7.5,1.8,BLUE)]:
    ax.add_patch(Rectangle((x,2.1),w,.7,facecolor=c))
txt(ax,7.4,3.15,'Two superconductors',ha='center',fontsize=11)
arrow(ax,(7.4,1.25),(7.4,2.05))
txt(ax,7.4,1.02,'Insulating barrier',ha='center',fontsize=12)
txt(ax,7.4,.55,'Cooper-pair tunnelling',ha='center',fontsize=11)
txt(ax,11.9,3.85,'Circuit levels',ha='center',fontsize=16,weight='bold')
for y,label in [(1.05,'|0⟩'),(2.2,'|1⟩'),(3.05,'|2⟩')]:
    line(ax,10.8,12.6,y); txt(ax,12.75,y,label,va='center',fontsize=14)
arrow(ax,(11.3,1.12),(11.3,2.12),RED)
txt(ax,10.65,1.64,'Drive',ha='right',color=RED,fontsize=11)
txt(ax,11.9,.2,'Unequal gaps\nselect the lowest pair',ha='center',fontsize=11)
save(fig,'superconducting')

fig,ax=panel()
txt(ax,2.7,3.85,'Electromagnetic trap',ha='center',fontsize=16,weight='bold')
for x in [.55,1.55,2.55,3.55,4.55]:
    ax.add_patch(Rectangle((x,1.05),.65,.4,facecolor='#94a3b8'))
for x in [1.3,2.65,4]: ax.add_patch(Circle((x,2.25),.12,facecolor=BLUE))
arrow(ax,(.5,3.15),(2.55,2.3),RED)
txt(ax,.55,3.22,'Laser control',fontsize=11,color=RED)
txt(ax,2.7,.35,'Electric fields hold ions\nin vacuum',ha='center',fontsize=11)
txt(ax,7.2,3.85,'Internal qubit levels',ha='center',fontsize=16,weight='bold')
for y,label in [(1.25,'|0⟩'),(2.75,'|1⟩')]:
    line(ax,6.1,7.7,y); txt(ax,7.9,y,label,va='center',fontsize=14)
arrow(ax,(6.65,1.4),(6.65,2.6),RED)
txt(ax,7.2,.6,'Hyperfine states\nElectron + nuclear spins',ha='center',fontsize=11)
txt(ax,7.1,3.13,'Microwave or\nRaman drive',ha='center',fontsize=11,color=RED)
txt(ax,11.6,3.85,'Entangling interaction',ha='center',fontsize=16,weight='bold')
for x in [10.5,12.6]: ax.add_patch(Circle((x,2.75),.14,facecolor=BLUE))
arrow(ax,(10.7,2.75),(12.4,2.75),GREEN,both=True)
txt(ax,11.55,2.3,'Shared vibrational mode',ha='center',fontsize=12,color=GREEN)
txt(ax,11.55,1.65,'State-dependent forces\n↓\nJoint phase on the qubits',ha='center',va='center',fontsize=12)
txt(ax,11.55,.6,'Transport to\ngate zones',ha='center',fontsize=11)
save(fig,'trapped-ions')

fig, ax = plt.subplots(figsize=(9,4.4))
fig.subplots_adjust(left=.02,right=.98,top=.98,bottom=.03)
ax.set(xlim=(0,9),ylim=(0,4.2))
ax.set_aspect('equal')
ax.axis('off')
txt(ax,2.25,3.85,'Optical tweezer',ha='center',fontsize=16,weight='bold')
ax.add_patch(Ellipse((2.2,2.85),.5,.85,facecolor='#fee2e2',edgecolor='#fca5a5'))
ax.add_patch(Circle((2.2,2.85),.075,facecolor=BLUE))
txt(ax,2.2,2.25,'Atom at the laser focus',ha='center',fontsize=11)
import numpy as np
position=np.linspace(.6,3.8,150)
potential=1.65-.8*np.exp(-((position-2.2)/.65)**2)
ax.plot(position,potential,color=GREEN,lw=2)
ax.add_patch(Circle((2.2,.95),.07,facecolor=BLUE))
arrow(ax,(1.05,1.7),(1.55,1.25),GREEN)
arrow(ax,(3.35,1.7),(2.85,1.25),GREEN)
txt(ax,2.2,.4,'Potential well\nholds the atom',ha='center',fontsize=11)
txt(ax,6.9,3.85,'Internal states',ha='center',fontsize=16,weight='bold')
for y,label in [(1.05,'|0⟩'),(1.8,'|1⟩'),(3,'|r⟩')]:
    line(ax,5.65,7.25,y); txt(ax,7.45,y,label,va='center',fontsize=14)
txt(ax,6.45,.78,'F = 1, mF = 0',ha='center',fontsize=10)
txt(ax,6.45,1.53,'F = 2, mF = 0',ha='center',fontsize=10)
arrow(ax,(5.35,1.12),(5.35,1.72),RED)
arrow(ax,(6.65,1.9),(6.65,2.9),GREEN)
txt(ax,6.65,2.4,'  Rydberg laser',color=GREEN,fontsize=11)
save(fig,'neutral-atoms')

fig, ax = plt.subplots(figsize=(12,6.2))
fig.subplots_adjust(left=.02,right=.98,top=.98,bottom=.02)
ax.set(xlim=(0,12),ylim=(0,6.2))
ax.axis('off')
txt(ax,6,5.9,'Rydberg blockade',ha='center',fontsize=19,weight='bold')
for left,blocked in [(0,False),(6,True)]:
    center=left+3
    title='A is not excited' if not blocked else 'A is in a Rydberg state'
    txt(ax,center,5.35,title,ha='center',fontsize=14,weight='bold')
    for x,label,color in [(left+1.9,'A',GREEN if blocked else BLUE),(left+4.0,'B',BLUE)]:
        ax.add_patch(Circle((x,4.85),.16,facecolor=color))
        txt(ax,x,4.4,label,ha='center',va='center',fontsize=12,weight='bold')
    if blocked:
        arrow(ax,(left+2.2,4.85),(left+3.7,4.85),GREEN,both=True)
        txt(ax,center,3.9,'Interaction shifts B’s level',ha='center',fontsize=11,color=GREEN)
    else:
        txt(ax,center,3.9,'No Rydberg interaction',ha='center',fontsize=11)
    x1,x2=left+1.0,left+3.65
    low,normal,shifted=1.25,2.65,3.5
    line(ax,x1,x2,low)
    txt(ax,x2+.12,low,'B: |1⟩',va='center',fontsize=12)
    if blocked:
        line(ax,x1,x2,normal,color='#94a3b8',ls='--')
        line(ax,x1,x2,shifted,color=GREEN)
        txt(ax,x2+.12,shifted,'B: |r⟩',va='center',fontsize=12,color=GREEN)
        arrow(ax,(x2-.18,normal+.04),(x2-.18,shifted-.04),GREEN,both=True)
        txt(ax,x2+.12,normal,'Original level',va='center',fontsize=10,color='#64748b')
    else:
        line(ax,x1,x2,normal,color=GREEN)
        txt(ax,x2+.12,normal,'B: |r⟩',va='center',fontsize=12,color=GREEN)
    arrow(ax,(left+1.75,low+.08),(left+1.75,normal-.06),RED)
    txt(ax,left+1.98,1.95,'Same laser\ndrive energy',va='center',fontsize=11,color=RED)
    if blocked:
        ax.plot([left+1.63,left+1.87],[normal-.17,normal+.07],color=RED,lw=2)
        ax.plot([left+1.63,left+1.87],[normal+.07,normal-.17],color=RED,lw=2)
    result='Laser matches → B can be excited' if not blocked else 'Laser misses → excitation suppressed'
    txt(ax,center,.65,result,ha='center',fontsize=12,weight='bold',color=GREEN if not blocked else RED)
txt(ax,6,.16,'|1⟩: stored state     |r⟩: Rydberg state',ha='center',fontsize=11)
save(fig,'rydberg-blockade')
print('Generated hardware diagrams.')
