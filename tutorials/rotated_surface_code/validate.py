"""Check the concrete supports, schedule and logical maps used in the tutorial.

Run from the repository root: uv run python tutorials/rotated_surface_code/validate.py
This is author validation, not a learner exercise or a distance search.
"""
from itertools import product
import numpy as np
import stim


def checks(d):
    faces = [(x, y, 'X' if (x+y) % 2 == 0 else 'Z')
             for x in range(d-1) for y in range(d-1)]
    for i in range(d-1):
        faces += ([(i, -1, 'Z'), (d-1, i, 'X')] if i % 2 == 0
                  else [(i, d-1, 'Z'), (-1, i, 'X')])
    result = []
    for x, y, kind in faces:
        corners = {'NW': (x,y+1), 'SW': (x,y), 'NE': (x+1,y+1), 'SE': (x+1,y)}
        support = {k: d*b+a for k,(a,b) in corners.items() if 0 <= a < d and 0 <= b < d}
        p = stim.PauliString(d*d)
        for q in support.values(): p[q] = kind
        result.append((kind, support, p))
    return result


def verify_patch(d):
    cs = checks(d)
    ps = [p for _,_,p in cs]
    assert len(ps) == d*d-1
    assert all(p.commutes(q) for p in ps for q in ps)
    lx, lz = stim.PauliString(d*d), stim.PauliString(d*d)
    for i in range(d): lx[i] = 'X'; lz[d*i] = 'Z'
    assert all(p.commutes(lx) and p.commutes(lz) for p in ps)
    assert not lx.commutes(lz)
    # Neither redundant stabilizers nor an unconstrained logical qubit allowed.
    for logical in [lx,lz]:
        stim.Tableau.from_stabilizers(ps+[logical])
    orders = {'X':['NW','SW','NE','SE'], 'Z':['NW','NE','SW','SE']}
    circuit = stim.Circuit()
    for i,(kind,_,_) in enumerate(cs):
        if kind == 'X': circuit.append('H',[d*d+i])
    for layer in range(4):
        used = set()
        for i,(kind,csupport,_) in enumerate(cs):
            q = csupport.get(orders[kind][layer])
            if q is None: continue
            a = d*d+i
            assert q not in used, (d,layer,q)
            used.add(q)
            circuit.append('CX',[a,q] if kind == 'X' else [q,a])
        circuit.append('TICK')
    for i,(kind,_,_) in enumerate(cs):
        if kind == 'X': circuit.append('H',[d*d+i])
    # Check every single Pauli error, both logical bases, and the no-error case.
    errors = [stim.PauliString(d*d)]
    for q in range(d*d):
        for kind in 'XYZ':
            e=stim.PauliString(d*d); e[q]=kind; errors.append(e)
    for logical in [lx,lz]:
        initial = stim.Tableau.from_stabilizers(ps+[logical])
        for error in errors:
            sim = stim.TableauSimulator()
            sim.set_inverse_tableau(initial.inverse())
            sim.do_pauli_string(error)
            sim.do(circuit)
            for i,p in enumerate(ps):
                assert sim.peek_z(d*d+i) == (1 if p.commutes(error) else -1)
    if d == 5:
        e=stim.PauliString(25); e[12]='Z'; e[18]='Z'
        violated=[set(s.values()) for _,s,p in cs if not p.commutes(e)]
        assert violated == [{6,7,11,12},{18,19,23,24}], violated
    print(f'd={d}: supports commute, independent checks, logical algebra, collision-free schedule, exact single-error syndrome extraction PASS')


def verify_cnot():
    I=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1])
    def k(*xs):
        out=np.array([[1.]])
        for x in xs: out=np.kron(out,x)
        return out
    cnot=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    # Register order C,A,T. Columns span all C,T inputs, including coherences.
    prep=np.zeros((8,4))
    for x,y in product(range(2),repeat=2):
        for a in range(2): prep[4*x+2*a+y,2*x+y]=1/np.sqrt(2)
    for a,b,c in product(range(2),repeat=3):
        pzz=(np.eye(8)+(-1)**a*k(Z,Z,I))/2
        pxx=(np.eye(8)+(-1)**b*k(I,X,X))/2
        raw=(pxx@pzz@prep)[[4*x+2*c+y for x,y in product(range(2),repeat=2)]]
        correction=k(np.linalg.matrix_power(Z,b),np.linalg.matrix_power(X,a^c))
        corrected=correction@raw
        overlap=np.vdot(cnot,corrected)/4
        assert np.allclose(corrected,overlap*cnot)
        assert np.isclose(abs(overlap)**2,1/8)
    # The two degree-three zero-phase spiders connected by one wire.
    green=np.zeros((2,2,2)); green[0,0,0]=green[1,1,1]=1
    h=np.array([[1,1],[1,-1]])/np.sqrt(2)
    red=np.einsum('ia,jb,kc,abc->ijk',h,h,h,green)
    zx=np.einsum('aic,bjc->abij',green,red).reshape(4,4)
    assert np.allclose(zx,cnot/np.sqrt(2))
    print('CNOT: all 8 measurement branches and frame updates; ZX spider map PASS')


if __name__ == '__main__':
    for d in [3,5]: verify_patch(d)
    verify_cnot()
