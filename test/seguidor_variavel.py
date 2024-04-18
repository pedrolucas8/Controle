# Exemplo do slide do Décio (adaptado)

import plotly
from Controle import *
from Controle.Moderno import *

# Seguidor de sinal variante no tempo
A = np.array([[0,1],[-1,0]])
print('polos de sem controle')
print(np.linalg.eig(A)[0])
B1 = np.array([[0],[1]])
B2 = np.array([[0],[1]])
CT = cmat.ctrb(A,B2);
print('posto da matriz de controlabilidade')
print(np.linalg.matrix_rank(CT))
C = np.array([1,0])
D = np.array([0])
Aw = np.array([[0,1], [-100,0]]) # -> senoide w=10
Ar = np.array([[0,1], [-1,0]]) # -> senoide w=1
C1 = np.array([1,0]) # -> C_barra

v = [-1+1j,-1-1j]
print('ganho de realimentaçao')
K = scipy.signal.place_poles(A, B2, v, method="YT", maxiter=30).gain_matrix
F = A-B2@K
F1 = np.linalg.inv(F)
F2 = np.hstack(( B1, A-Ar ))
Ke = 1/(C1@F1@B2) * C1@F1@F2 # -> Kex
Ke = np.matrix(Ke)
Ax = np.zeros((2,2))
Ao = np.vstack((
    np.hstack((Aw,Ax)),
    np.hstack((Ax,Ar))
)) # [Aw Ax;Ax Ar]
Ay = np.hstack((B1, B2@K))-B2@Ke
Ay = np.hstack((Ay, np.zeros((2,1))))
AT = np.vstack((
        np.hstack((A-B2*K, Ay)),
        np.hstack((np.zeros((4,2)), Ao))
)) # -> A_barra
xTo = np.matrix([1,0,1,0,1,0]).transpose()
sys = ct.ss(AT,xTo,AT,xTo)
(y,T) = cmat.step(sys,30)

import matplotlib.pyplot as plt
plt.plot(T,y[:,0].flatten())
yref = [ np.sin(1*t) for t in T]
plt.plot(T,yref)