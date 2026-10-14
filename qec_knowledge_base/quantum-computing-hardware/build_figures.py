"""Generate the hardware reference diagrams. Run from the repository root."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse

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
    fig.savefig(OUT/f'{name}.png',dpi=160)
    fig.savefig(OUT/f'{name}.svg')
    p=OUT/f'{name}.svg'
    p.write_text('\n'.join(s.rstrip() for s in p.read_text().splitlines())+'\n')
    plt.close(fig)

fig, ax = plt.subplots(figsize=(12, 5.2))
fig.subplots_adjust(left=.02,right=.98,top=.98,bottom=.04)
ax.set(xlim=(0,12),ylim=(0,5.2)); ax.axis('off')
ax.add_patch(Rectangle((.35,.65),11.3,3.85,facecolor='#f8fafc',edgecolor='#cbd5e1'))
txt(ax,6,4.85,'Transmons, resonators, and couplers on a chip',ha='center',fontsize=18,weight='bold')
line(ax,.7,11.3,4.1,color='#7c3aed')
txt(ax,6,4.3,'Readout line: probe in, measurement signal out',ha='center',fontsize=12,color='#7c3aed')
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
    txt(ax,x+.75,3.1,'Readout resonator',ha='left',fontsize=10,color='#b45309')
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
txt(ax,6.4,1.8,'Superconductor',ha='center',fontsize=11)
txt(ax,8.4,1.8,'Superconductor',ha='center',fontsize=11)
arrow(ax,(7.4,1.25),(7.4,2.05))
txt(ax,7.4,1.02,'Insulating barrier',ha='center',fontsize=12)
txt(ax,7.4,.55,'Coherent Cooper-pair tunnelling',ha='center',fontsize=11)
txt(ax,11.9,3.85,'Circuit levels',ha='center',fontsize=16,weight='bold')
for y,label in [(1.05,'|0⟩'),(2.2,'|1⟩'),(3.05,'|2⟩')]:
    line(ax,10.8,12.6,y); txt(ax,12.75,y,label,va='center',fontsize=14)
arrow(ax,(11.3,1.12),(11.3,2.12),RED)
txt(ax,10.65,1.64,'Drive',ha='right',color=RED,fontsize=11)
txt(ax,11.9,.55,'Unequal gaps select the lowest pair',ha='center',fontsize=11)
save(fig,'superconducting')

fig,ax=panel()
txt(ax,2.7,3.85,'Electromagnetic trap',ha='center',fontsize=16,weight='bold')
for x in [.55,1.55,2.55,3.55,4.55]:
    ax.add_patch(Rectangle((x,1.05),.65,.4,facecolor='#94a3b8'))
for x in [1.3,2.65,4]: ax.add_patch(Circle((x,2.25),.12,facecolor=BLUE))
arrow(ax,(.5,3.15),(2.55,2.3),RED)
txt(ax,.55,3.22,'Laser control',fontsize=11,color=RED)
txt(ax,2.7,.65,'Fields confine charged atoms in vacuum',ha='center',fontsize=11)
txt(ax,7.2,3.85,'Internal qubit levels',ha='center',fontsize=16,weight='bold')
for y,label in [(1.25,'|0⟩'),(2.75,'|1⟩')]:
    line(ax,6.1,7.7,y); txt(ax,7.9,y,label,va='center',fontsize=14)
arrow(ax,(6.65,1.4),(6.65,2.6),RED)
txt(ax,7.2,.6,'Two hyperfine states\nElectron + nuclear angular momenta',ha='center',fontsize=11)
txt(ax,7.1,3.13,'Microwave or Raman drive',ha='center',fontsize=11,color=RED)
txt(ax,11.6,3.85,'Entangling interaction',ha='center',fontsize=16,weight='bold')
for x in [10.5,12.6]: ax.add_patch(Circle((x,2.75),.14,facecolor=BLUE))
arrow(ax,(10.7,2.75),(12.4,2.75),GREEN,both=True)
txt(ax,11.55,2.3,'Shared vibrational mode',ha='center',fontsize=12,color=GREEN)
txt(ax,11.55,1.65,'State-dependent forces\n↓\nJoint phase on the qubits',ha='center',va='center',fontsize=12)
txt(ax,11.55,.6,'QCCD: move ions between gate zones',ha='center',fontsize=11)
save(fig,'trapped-ions')

fig,ax=panel()
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
txt(ax,2.2,.4,'Energy minimum holds the atom',ha='center',fontsize=11)
txt(ax,6.9,3.85,'Rubidium internal states',ha='center',fontsize=16,weight='bold')
for y,label in [(1.05,'|0⟩'),(1.8,'|1⟩'),(3,'|r⟩')]:
    line(ax,5.65,7.25,y); txt(ax,7.45,y,label,va='center',fontsize=14)
txt(ax,6.45,.78,'F = 1, mF = 0',ha='center',fontsize=10)
txt(ax,6.45,1.53,'F = 2, mF = 0',ha='center',fontsize=10)
arrow(ax,(5.35,1.12),(5.35,1.72),RED)
arrow(ax,(6.65,1.9),(6.65,2.9),GREEN)
txt(ax,6.65,2.4,'  Rydberg laser',color=GREEN,fontsize=11)
txt(ax,11.6,3.85,'Rydberg blockade',ha='center',fontsize=16,weight='bold')
line(ax,9.7,11.15,2.05,color='#94a3b8',ls='--')
line(ax,9.7,11.15,3.15,color=GREEN)
txt(ax,11.3,3.15,'|rr⟩',va='center',fontsize=14)
txt(ax,11.3,2.05,'Without interaction',va='center',fontsize=10,color='#64748b')
arrow(ax,(10.8,2.13),(10.8,3.07),GREEN,both=True)
txt(ax,10.45,2.6,'V',ha='right',fontsize=15,color=GREEN)
line(ax,9.7,11.15,1.1)
txt(ax,11.3,1.1,'One Rydberg excitation',va='center',fontsize=10)
arrow(ax,(10.1,1.2),(10.1,1.96),RED)
txt(ax,11.5,.55,'Pair shift detunes the second excitation',ha='center',fontsize=11)
save(fig,'neutral-atoms')
print('Generated hardware diagrams.')
