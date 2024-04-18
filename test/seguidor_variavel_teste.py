# Exemplo do slide do Décio (nossa função)

import plotly
from Controle import *
from Controle.Moderno import *

# Seguidor de sinal variante no tempo
A = np.matrix([[0,1],[-1,0]])
B1 = np.matrix([[1,0],[0,1]])
B2 = np.matrix([[0],[1]])
C = np.matrix([1,0])
D = np.matrix([0])
Aw = np.matrix([[0,1], [-100,0]]) # -> senoide w=10
Ar = np.matrix([[0,1], [-1,0]]) # -> senoide w=1
C1 = np.matrix([1,0]) # -> C_barra

v = [-1+1j,-1-1j]
K = scipy.signal.place_poles(A, B2, v, method="YT", maxiter=30).gain_matrix

seguidor = seguidor_variavel(A, B1, B2, C, D, K, Ar, C1)
Ke = seguidor.Kex

Ax = np.zeros((2,2))
Ao = np.vstack((
    np.hstack((Aw,Ax)),
    np.hstack((Ax,Ar))
)) # [Aw Ax;Ax Ar]
Ay = np.hstack((B1, B2@K))-B2@Ke
# Ay = np.hstack((Ay, np.zeros((2,1))))
AT = np.vstack((
        np.hstack((A-B2@K, Ay)),
        np.hstack((np.zeros((4,2)), Ao))
)) # -> A_barra
xTo = np.matrix([1,0,1,0,1,0]).transpose()
sys = ct.ss(AT,xTo,AT,xTo)
(y,T) = cmat.step(sys,30)

import matplotlib.pyplot as plt

plt.plot(T,y[:,0].flatten())
yref = [ np.cos(1*t) for t in T]
plt.plot(T,yref)
plt.title("Posição")
plt.grid()
plt.show()

plt.plot(T,y[:,1].flatten())
yref = [ -np.sin(1*t) for t in T]
plt.plot(T,yref)
plt.title("Velocidade")
plt.grid()
plt.show()