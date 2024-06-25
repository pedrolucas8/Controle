import matplotlib.pyplot as plt
import numpy as np
import control as ct

# Definição dos coeficientes do numerador e denominador da função de transferência fornecida
numerador = [-0.6862,  -159.0263, 1534.9293,  6268.1563] # [0,0] vel_u - profundor
# numerador = [ 0.0813,     0.9793,    6.3050,   -12.3500] # [0,1] vel_u - tração
# numerador = [-7.4350, -2832.7300, -631.1412, -2593.9991] # [1,0] vel_w - profundor
# numerador = [ 0     ,     5.1411,    0.1551,     4.9117] # [1,1] vel_w - tração

denominador = [1, 8.746, 116.2, 22.21, 76.22]
G = ct.tf(numerador, denominador)

print(f'zeros = {G.zeros()}')

Ks = np.linspace(0,.03, num=10000)
# rlist, klist = ct.rlocus(G,Ks)
rlist, klist = ct.rlocus(G)

plt.grid()
plt.ylim(-15,15)
plt.xlim(-12,12)
plt.show()