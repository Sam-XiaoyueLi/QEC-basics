"""Original conceptual schematics; no measured device data. Run from repo root."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse

OUT = Path(__file__).parent / 'assets'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'svg.fonttype': 'none'})
BLUE, RED, INK, GREEN = '#2563eb', '#dc2626', '#172b4d', '#0f766e'
fig, axs = plt.subplots(3, 1, figsize=(13, 13.5))
fig.subplots_adjust(top=.945, bottom=.045, left=.035, right=.985, hspace=.25)
fig.suptitle('Three physical pictures of quantum hardware', fontsize=23, color=INK)

def setup(ax, title):
    ax.set(xlim=(0,13), ylim=(0,4)); ax.set_aspect('equal'); ax.axis('off')
    ax.text(.1,3.7,title,fontsize=18,weight='bold',color=INK)

def txt(ax,x,y,s,**kw):
    kw.setdefault('color', INK)
    ax.text(x,y,s,**kw)
def arrow(ax,a,b,color=INK): ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color=color,lw=2))

ax=axs[0]; setup(ax,'1  Superconducting: an engineered quantum circuit on a cold chip')
ax.add_patch(Rectangle((.15,.8),5.5,2.2,facecolor='#f1f5f9',edgecolor='#94a3b8'))
for x,label in [(1.45,'Qubit A'),(4.3,'Qubit B')]:
    ax.add_patch(Rectangle((x-.7,1.5),.55,.8,facecolor=BLUE))
    ax.add_patch(Rectangle((x+.15,1.5),.55,.8,facecolor=BLUE))
    ax.plot([x-.15,x+.15],[1.9,1.9],color=INK,lw=2)
    ax.plot([x-.08,x+.08],[1.81,1.99],color=INK,lw=2)
    ax.plot([x-.08,x+.08],[1.99,1.81],color=INK,lw=2)
    txt(ax,x,1.18,label,ha='center')
    arrow(ax,(x,2.9),(x,2.35),RED)
txt(ax,2.9,3.14,'Microwave controls',ha='center',color=RED)
ax.plot([2.15,3.6],[1.9,1.9],color=GREEN,lw=4)
txt(ax,2.87,2.13,'Coupling',ha='center',fontsize=11)
txt(ax,2.9,.46,'Pads + junction form the qubit circuit',ha='center')
txt(ax,8.2,2.88,'Josephson junction\nConceptual cross-section',ha='center',fontsize=12,weight='bold')
for x,w,c in [(6.4,1.7,BLUE),(8.1,.18,'#f59e0b'),(8.28,1.7,BLUE)]:
    ax.add_patch(Rectangle((x,1.72),w,.68,facecolor=c))
txt(ax,7.2,1.45,'Superconductor',ha='center',fontsize=10)
txt(ax,9.2,1.45,'Superconductor',ha='center',fontsize=10)
arrow(ax,(8.19,1.03),(8.19,1.7))
txt(ax,8.19,.78,'Thin insulating barrier',ha='center',fontsize=11)
for y,l in [(1.42,'|0⟩'),(2.05,'|1⟩'),(2.56,'|2⟩')]:
    ax.plot([10.5,11.55],[y,y],color=INK,lw=2); txt(ax,11.65,y,l,va='center')
txt(ax,11.2,3.03,'Circuit levels',ha='center',fontsize=11)
txt(ax,11.2,.69,'Use 0 and 1;\navoid leakage to 2',ha='center',fontsize=11)

ax=axs[1]; setup(ax,'2  Trapped ions: charged atoms suspended above electrodes in vacuum')
ax.add_patch(Rectangle((.3,.85),7,1.9,facecolor='#f8fafc',edgecolor='#94a3b8',ls='--'))
for x in [.5,1.55,2.6,3.65,4.7,5.75,6.8]:
    ax.add_patch(Rectangle((x,.87),.7,.35,facecolor='#94a3b8'))
for x in [1.6,3.4,5.2]: ax.add_patch(Circle((x,1.95),.13,facecolor=BLUE))
ax.annotate('',xy=(5.1,2.3),xytext=(1.7,2.3),arrowprops=dict(arrowstyle='<->',color=GREEN,lw=2))
txt(ax,3.4,2.49,'Collective motion mediates a gate',ha='center',fontsize=11)
arrow(ax,(.65,3.05),(3.3,2.02),RED); txt(ax,.3,3.1,'Laser control',color=RED,fontsize=11)
txt(ax,3.65,.5,'Electric fields confine the ions; ions do not sit on the metal',ha='center',fontsize=11)
txt(ax,8.1,3.02,'QCCD variant: move ions to gate zones',fontsize=13,weight='bold')
for x,label in [(8.2,'Storage'),(10.6,'Gate zone')]:
    ax.add_patch(Rectangle((x,1.4),1.85,1,facecolor='#eff6ff',edgecolor=BLUE))
    txt(ax,x+.925,1.1,label,ha='center',fontsize=11)
ax.add_patch(Circle((8.9,1.9),.12,facecolor=BLUE))
for x in [11.15,11.8]: ax.add_patch(Circle((x,1.9),.12,facecolor=BLUE))
arrow(ax,(9.15,1.9),(10.45,1.9),GREEN)
txt(ax,10.2,.5,'Qubit = internal atomic states, not the position',ha='center',fontsize=11)

ax=axs[2]; setup(ax,'3  Neutral atoms: uncharged atoms held in focused laser traps in vacuum')
for y in [1.25,2.05,2.85]:
    for x in [1,1.8,2.6,3.4]:
        ax.add_patch(Ellipse((x,y),.45,.64,facecolor='#fee2e2',edgecolor='#fca5a5'))
        ax.add_patch(Circle((x,y),.08,facecolor=BLUE))
txt(ax,2.2,.65,'Optical tweezer array',ha='center')
arrow(ax,(4,2.9),(3.55,2.85),RED); txt(ax,4.02,2.91,'Focused laser trap',fontsize=11,color=RED)
arrow(ax,(4.1,1.55),(6.4,1.55),GREEN)
txt(ax,5.25,1.95,'Move selected atoms',ha='center',fontsize=11)
for x in [7.15,8.3]:
    ax.add_patch(Ellipse((x,1.55),.45,.64,facecolor='#fee2e2',edgecolor='#fca5a5'))
    ax.add_patch(Circle((x,1.55),.09,facecolor=BLUE))
    ax.add_patch(Circle((x,1.55),.62,fill=False,edgecolor=GREEN,ls='--',lw=2))
ax.annotate('',xy=(8.15,1.55),xytext=(7.3,1.55),arrowprops=dict(arrowstyle='<->',color=GREEN,lw=2))
txt(ax,7.8,2.7,'Rydberg excitation enables\nstrong interactions for a gate',ha='center',fontsize=11)
txt(ax,7.8,.55,'Dashed halos symbolize interactions,\nnot literal electron trajectories',ha='center',fontsize=10)
for y,l in [(1.3,'|0⟩'),(1.85,'|1⟩'),(2.95,'|r⟩')]:
    ax.plot([10.3,11.3],[y,y],color=INK,lw=2); txt(ax,11.45,y,l,va='center')
arrow(ax,(10.75,1.97),(10.75,2.83),RED)
txt(ax,11,.55,'Store in 0 and 1;\nuse r during entangling',ha='center',fontsize=11)
fig.text(.5,.017,'Original conceptual schematics • not to scale • layouts and encodings vary by device',ha='center',fontsize=11,color=INK)
fig.savefig(OUT/'platform-schematics.png',dpi=160)
fig.savefig(OUT/'platform-schematics.svg')
svg_path = OUT/'platform-schematics.svg'
svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines()) + '\n')
plt.close(fig)
print('Saved platform-schematics.png and .svg')
