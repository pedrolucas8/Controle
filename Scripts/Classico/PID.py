import matplotlib.pyplot as plt
import numpy as np
import control as ct

# Ativar o modo interativo do matplotlib
plt.ioff()

# Paleta de cores personalizada
cp = {
    'red': (1.0, 0.349, 0.369, 1.0),
    'green': (0.541, 0.788, 0.149, 1.0),
    'blue': (0.098, 0.510, 0.769, 1.0),
    'lred': (1.0, 0.588, 0.6, 1.0),
    'lgreen': (0.722, 0.894, 0.443, 1.0),
    'lblue': (0.369, 0.706, 0.918, 1.0),
    'orange': (1.0, 0.506, 0.227, 1.0),
    'yellow': (1.0, 0.792, 0.227, 1.0),
    'pink': (1.0, 0.349, 0.611, 1.0),
    'purple': (0.416, 0.298, 0.576, 1.0),
    'turquoise': (0.098, 0.761, 0.769, 1.0),
    'brown': (0.576, 0.380, 0.298, 1.0)
}

# Definição dos coeficientes do numerador e denominador da função de transferência fornecida
numerador = [-0.6862,  -159.0263, 1534.9293,  6268.1563] # [0,0] vel_u - profundor
# numerador = [ 0.0813,     0.9793,    6.3050,   -12.3500] # [0,1] vel_u - tração
# numerador = [-7.4350, -2832.7300, -631.1412, -2593.9991] # [1,0] vel_w - profundor
# numerador = [ 0     ,     5.1411,    0.1551,     4.9117] # [1,1] vel_w - tração

denominador = [1, 8.746, 116.2, 22.21, 76.22]


# Criação da função de transferência fornecida
G = ct.tf(numerador, denominador)
# print(f"Função de Transferência: {G}")

# Definição dos ganhos
K_p = 0.2328
K_i = 0
K_d = 0

# Cálculo do tempo integral e derivativo
T_i = K_p / (K_i+1e-17)
T_d = K_d / (K_p+1e-17)

print(f'Kp = {K_p}, Ki = {K_i}, Kd = {K_d}')
print(f"T_i: {T_i}, T_d: {T_d}")

s = ct.TransferFunction.s

# Função de transferência do controlador PID
# G_c_PID = K_p + K_i/s + K_d*s
# print(f"Controlador PID: {G_c_PID}")
G_c_PID = (0.0165*s**2+0.1404*s+0.2987)/s

# Função de transferência em malha fechada com controlador PID
G_PID = ct.feedback(G_c_PID * G)
# print(f"Malha Fechada com PID: {G_PID}")

# Diagrama de Bode para o controlador PID
plt.figure()
ct.bode_plot(G_c_PID, omega=np.linspace(0.1, 100, 1000), color=cp['red'], dB=True, Hz=True)
plt.suptitle('Diagrama de Bode do Controlador PID')
plt.show()

# Diagrama de Bode para o sistema em malha fechada com controlador PID
plt.figure()
ct.bode_plot(G_PID, omega=np.linspace(0.1, 100, 1000), color=cp['purple'], dB=True, Hz=True)
plt.suptitle('Diagrama de Bode do Sistema em Malha Fechada com PID')
plt.show()

# Simulação da resposta a degrau do sistema em malha fechada com controlador PID
t, y_PID = ct.step_response(G_PID, T=np.linspace(0, 10, 1000))
plt.figure()
plt.plot(t, y_PID, label='PID', color=cp['red'])
plt.xlabel('Tempo (s)')
plt.ylabel('Resposta')
plt.title('Resposta a Degrau do Sistema em Malha Fechada com PID')
plt.grid()
plt.legend()
plt.show()