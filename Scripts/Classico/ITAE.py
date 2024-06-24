import control as ctl
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import differential_evolution

# FT da planta
# numerador = [-0.6862, -159.0263, 1534.9293, 6268.1563] # [0,0] vel_u - profundor
numerador = [0.0813, 0.9793, 6.305, -12.35] # [0,1] vel_u - tração
# numerador = [-7.4350, -2832.7300, -631.1412, -2593.9991] # [1,0] vel_w - profundor
# numerador = [0, 5.1411, 0.1551, 4.9117] # [1,1] vel_w - tração

denominador = [1, 8.746, 116.2, 22.21, 76.22]

# Criação da função de transferência fornecida
P_s = ctl.tf(numerador, denominador)

# Função de custo ajustada para penalizar oscilações e valores extremos
def itae_cost(params):
    Kp, Ki, Kd = params
    s = ctl.TransferFunction.s
    C_s = Kp + Ki / s + Kd * s
    G_s = ctl.series(C_s, P_s)
    G1_s = ctl.feedback(G_s, 1, sign=-1)
    Tsim = 30 # tempo total
    Tnum = 30 # pontos analisados
    T, yout = ctl.step_response(G1_s, Tsim, T_num=Tnum)
    error = 1 - yout  # Assume entrada de degrau unitário
    itae = np.trapz(T * np.abs(error), T)
    return itae

# Limites para os parâmetros PID
bounds = [(0.001, 50), (0.001, 50), (0.001, 50)]

# Otimização dos parâmetros PID usando Differential Evolution
result = differential_evolution(itae_cost, bounds, strategy='best1bin', maxiter=20)
Kp_opt, Ki_opt, Kd_opt = result.x

print(f'Parâmetros otimizados: Kp = {Kp_opt}, Ki = {Ki_opt}, Kd = {Kd_opt}')

# Simulação com os parâmetros otimizados
s = ctl.TransferFunction.s
C_s_opt = Kp_opt + Ki_opt / s + Kd_opt * s
G_s_opt = ctl.series(C_s_opt, P_s)
G1_s_opt = ctl.feedback(G_s_opt, 1, sign=-1)

Tsim = 50
T, yout = ctl.step_response(G1_s_opt, Tsim)

# Plotar a resposta
plt.figure()
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