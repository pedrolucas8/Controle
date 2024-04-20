import numpy as np
import control as ct
import control.matlab as cmat


Ww = 2*np.pi / 5
A = np.matrix([[0,1], [-Ww**2,0]]) # -> senoide w=10
B = np.matrix([[0],[Ww]])
C = np.matrix([[1,0],[0,1]])
D = np.matrix([[0],[0]])

sys = ct.ss(A,B,C,D)

import matplotlib.pyplot as plt


(y,T) = cmat.step(sys,30)
plt.plot(T,y[:,0].flatten())
plt.show()

(y,T) = cmat.impulse(sys,30)
plt.plot(T,y[:,0].flatten())
plt.plot(T,y[:,1].flatten())
plt.show()

(y,T) = cmat.initial(sys,30,X0=B)
plt.plot(T,y[:,0].flatten())
plt.show()

"""
x' = Ax + Bu
sX = AX + BU
(sI-A)X = BU
X = (sI-A)⁻¹BU
u(t) degrau -> U(s) = u0/s
X = (sI-A)⁻¹B u0
X = b (-1/as + 1/a(s-a)) u0
x = b/a (e^(at)-1) u0
"""