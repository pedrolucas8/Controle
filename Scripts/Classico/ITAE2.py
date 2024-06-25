import control as ctl
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import differential_evolution

# FT da planta
numerador = [-0.6862,  -159.0263, 1534.9293,  6268.1563] # [0,0] vel_u - profundor
# numerador = [ 0.0813,     0.9793,    6.3050,   -12.3500] # [0,1] vel_u - tração
# numerador = [-7.4350, -2832.7300, -631.1412, -2593.9991] # [1,0] vel_w - profundor
# numerador = [ 0     ,     5.1411,    0.1551,     4.9117] # [1,1] vel_w - tração

denominador = [1, 8.746, 116.2, 22.21, 76.22]
polo_dominante = -0.07206714+0.81344151j
denominador_dominante = [
    1, 
    -np.real(polo_dominante+polo_dominante.conjugate()),
    np.real(polo_dominante*polo_dominante.conjugate())
]

# Criação da função de transferência fornecida
G = ctl.tf(numerador, denominador)

# Critérios de desempenho
# wn = 0.75 # ignd=True ; ig0=True ; Kp = [0.81348011], Ki = [0.41647733], Kd = [1.96811795]
# wn = 2.00  # ignd=True ; ig0=False ; Kp = [-0.00227422], Ki = [-0.00297175], Kd = [0.00247413]
wn = 2. # True False - u prof
# wn = 2.1

ignora_zeros = False
ignora_nao_dominantes = True

"""
tempo de subida
    tr = (1+1.1*zeta+1.4*zeta**2)/wn
tempo de acomodação
    ts = - np.log(f*np.sqrt(1-zeta**2))/(zeta*wn)
    para zeta<<1 e f=0.02:
    ts = 4/(zeta*wn)
tempo de pico
    tp = np.pi/(wn*np.sqrt(1-zeta**2))
sobressinal
    Mp = np.exp( -(zeta*np.pi)/(np.sqrt(1-zeta**2)) )
    zeta = - np.log(Mp)/np.sqrt(np.pi**2+np.log(Mp)**2)
"""

# Função de custo ajustada para penalizar oscilações e valores extremos
"""
    G = num/den
    Gc = Kp + Ki/s + Kd*s
    T = Gc*G/(1+Gc*G)
    T = (Kp + Ki/s + Kd*s)*(b3*s³+b2*s²+b1*s+b0)/(a4*s⁴+a3*s³+a2*s²+a1*s+a0+(Kp + Ki/s + Kd*s)*(b3*s³+b2*s²+b1*s+b0))
    T = ( (b3 Kd)s^5 + (Kp b3+b2 Kd)s^4 + (Kp b2+Ki b3+b1 Kd)s^3 + (Kp b1+Ki b2+b0 Kd)s^2 + (Kp b0+Ki b1)s + (Ki b0)
        /( (a4+b3 Kd)s^5 + (a3+Kp b3+b2 Kd)s^4 + (a2+Kp b2+Ki b3+b1 Kd)s^3 + (a1+Kp b1+Ki b2+b0 Kd)s^2 + (a0+Kp b0+Ki b1)s + (Ki b0))
        
"""
# solução ITAE para denominador de 5o grau
sol_itae = [
    [1,      wn],
    [1, 1.4 *wn,      wn**2],
    [1, 1.75*wn, 2.15*wn**2,     wn**3],
    [1, 2.1 *wn, 3.4 *wn**2, 2.7*wn**3,     wn**4],
    [1, 2.8 *wn, 5.0 *wn**2, 5.5*wn**3, 3.4*wn**4, wn**5],
]

ais = denominador if not ignora_nao_dominantes else denominador_dominante

A = np.zeros((0,3))
b = np.zeros((0,1))
# print(A.shape)
grau = len(ais)-1
bis = [0,0,0,ais[-1]] if ignora_zeros else numerador 
for i in range(grau+1):
    bi  = bis[-1-i+1] if 0<=i-1<len(bis) else 0
    bi1 = bis[-1-i  ] if 0<=i<len(bis) else 0
    bi2 = bis[-1-i+2] if 0<=i-2<len(bis) else 0
    linha = np.matrix([[ bi, bi1, bi2-bis[0]*sol_itae[grau][-1-i] ]])
    # print(A.shape,"  ",linha.shape)
    A = np.vstack([linha,A])
    ai = ais[i+1] if i<grau else 0
    b = np.vstack([ais[0]*sol_itae[grau][-1-i]-ai,b,])

# a4,a3,a2,a1,a0 = denominador
# b3,b2,b1,b0 = numerador
# # b3,b2,b1,b0 = [0,0,0,a0]
# A = np.matrix([
#     [b3,  0, b2-b3*2.8*wn   ],
#     [b2, b3, b1-b3*5.0*wn**2],
#     [b1, b2, b0-b3*5.5*wn**3],
#     [b0, b1,   -b3*3.4*wn**4],
#     [ 0, b0,   -b3*    wn**5],
# ])
# b = np.matrix([
#     [2.8*wn   *a4-a3],
#     [5.0*wn**2*a4-a2],
#     [5.5*wn**3*a4-a1], 
#     [3.4*wn**4*a4-a0], 
#     [    wn**5*a4   ],
# ])

Kp,Ki,Kd = np.linalg.lstsq(A,b,None)[0]


print(f'num = {numerador}')
print(f'den = {denominador}')
print(f'wn={wn}, ig0={ignora_zeros}, ignd={ignora_nao_dominantes}')
print(f'Kp = {Kp}, Ki = {Ki}, Kd = {Kd}')
# Kp *= 0.1
# Ki = 0
# Kd = 0

# Simulação com os parâmetros otimizados
s = ctl.TransferFunction.s
Gc = Kp + Ki/s + Kd*s
L = Gc*G
# Ts = L/(1+L)
Ts = ctl.feedback(L,1)
Ts = Ts/Ts(0)
Gf = ctl.tf(Ts.num[0][0][-1],Ts.num[0][0])
# Gf = ( Ki*b0 )/( (b3*Kd)*s**5 + (Kp*b3+b2*Kd)*s**4 + (Kp*b2+Ki*b3+b1*Kd)*s**3 + (Kp*b1+Ki*b2+b0*Kd)*s**2 + (Kp*b0+Ki*b1)*s + (Ki*b0) )
Gmf = Gf * Ts


Tsim = 100

# Plotar a resposta
plt.figure()
T, yout = ctl.step_response(Gmf, Tsim)
plt.plot(T, yout, 'k-', label="Resposta em Malha Fechada (otimizado)")
plt.grid()
T2 = np.linspace(-0.2, Tsim, 1000)
degrau = np.ones_like(T2)
degrau[T2 < 0] = 0
plt.plot(T2, degrau, 'r-', label="Entrada: Degrau Unitário")
plt.xlabel('Tempo (s)')
plt.ylabel('Resposta')
plt.legend()
plt.show()

# Plotar a resposta
plt.figure()
T, yout = ctl.step_response(Gmf, Tsim)
plt.plot(T, yout, 'k-', label="Com pré-compensador")
plt.grid()
T, yout = ctl.step_response(Ts, Tsim)
plt.plot(T, yout, 'k-', label="Sem pré-compensador")
T2 = np.linspace(-0.2, Tsim, 1000)
degrau = np.ones_like(T2)
degrau[T2 < 0] = 0
plt.plot(T2, degrau, 'r--', label="Entrada: Degrau Unitário")
plt.xlabel('Tempo (s)')
plt.ylabel('Resposta')
plt.legend()
plt.show()