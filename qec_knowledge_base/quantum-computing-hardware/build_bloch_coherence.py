from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out = Path(__file__).parent / 'assets'
out.mkdir(exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.fonttype': 'none'})
fig = plt.figure(figsize=(11, 5.2), facecolor='white')
u = np.linspace(0, 2*np.pi, 49)
v = np.linspace(0, np.pi, 25)
sx, sy, sz = np.outer(np.cos(u),np.sin(v)), np.outer(np.sin(u),np.sin(v)), np.outer(np.ones_like(u),np.cos(v))
colors = ['#2563eb', '#0891b2', '#d97706', '#dc2626']
for panel in range(2):
    ax = fig.add_subplot(1,2,panel+1,projection='3d')
    ax.plot_wireframe(sx,sy,sz,rstride=8,cstride=4,color='#cbd5e1',linewidth=.6,alpha=.55)
    ax.plot(np.cos(u),np.sin(u),0*u,color='#94a3b8',lw=.8)
    for direction in [(1.14,0,0),(0,1.14,0),(0,0,1.16)]:
        d=np.array(direction)
        ax.plot([-d[0],d[0]],[-d[1],d[1]],[-d[2],d[2]],color='#94a3b8',lw=.8)
    ax.text(0,0,1.27,r'$|0\rangle$',ha='center',fontsize=13)
    ax.text(0,0,-1.29,r'$|1\rangle$',ha='center',fontsize=13)
    ax.text(1.16,0,0,r'$|+\rangle$',fontsize=12)
    ax.text(0,1.19,0,'y',fontsize=10,color='#64748b')
    times=[0,.65,1.8,4]
    for j,t in enumerate(times):
        if panel==0: x,z=np.exp(-t/2),1-np.exp(-t)
        else: x,z=np.exp(-t),0
        ax.quiver(0,0,0,x,0,z,color=colors[j],linewidth=2.4,arrow_length_ratio=.12)
        ax.scatter([x],[0],[z],color=colors[j],s=22,depthshade=False)
    t=np.linspace(0,6,200)
    if panel==0:
        ax.plot(np.exp(-t/2),0*t,1-np.exp(-t),color='#334155',lw=1.2,ls='--')
        ax.set_title(r'$T_1$: energy relaxation',fontsize=15,pad=0)
        caption='Population relaxes into the ground state.\nThe transverse component also shrinks.'
    else:
        ax.plot(np.exp(-t),0*t,0*t,color='#334155',lw=1.2,ls='--')
        ax.set_title(r'Phase loss contributing to $T_2$',fontsize=15,pad=0)
        caption='Pure phase noise: equal populations remain.\nThe average vector shrinks toward the centre.'
    ax.text2D(.5,-.015,caption,transform=ax.transAxes,ha='center',va='top',fontsize=11,linespacing=1.5)
    ax.set(xlim=(-1.2,1.2),ylim=(-1.2,1.2),zlim=(-1.2,1.2))
    ax.set_box_aspect((1,1,1)); ax.view_init(elev=19,azim=-64); ax.set_axis_off()
handles=[plt.Line2D([0],[0],color=c,lw=3) for c in colors]
fig.legend(handles,['Start','Later','Later','Late'],ncol=4,loc='lower center',bbox_to_anchor=(.5,.005),frameon=False)
fig.subplots_adjust(left=.02,right=.98,top=.92,bottom=.18,wspace=.02)
fig.savefig(out/'bloch-coherence.png',dpi=180,facecolor='white')
fig.savefig(out/'bloch-coherence.svg',facecolor='white')
plt.close(fig)
p=out/'bloch-coherence.svg'
p.write_text('\n'.join(s.rstrip() for s in p.read_text().splitlines())+'\n')
print(out/'bloch-coherence.png')
