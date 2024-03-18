from Controle.matriz_transicao_forcante import * 

A = np.matrix([[0, 1], [-100, 0]])
B = np.matrix([[0], [10]])

dt = .2
p, g = matriz_transicao_forcante(A, dt=dt, k=4)
x, t = simulacao_degrau_transicao_forcante(p, g, B, dt=dt, u0=1*np.pi/180)

import matplotlib.pyplot as plt

plt.figure()
plt.plot(t, x[0, :])
plt.show()
plt.figure()
plt.plot(t, x[1, :], c="red")
plt.show()