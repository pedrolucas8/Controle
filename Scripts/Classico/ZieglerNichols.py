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

PID=0 # 0:P , 1:PI , 2:PID

T = 50 # tempo máximo
w = 10e4 # frequência máxima





# Criação da função de transferência fornecida
G = ct.tf(numerador, denominador)

rlist, klist = ct.rlocus(G,plot=False)
Kcrit = np.inf
Pcrit = np.inf
for i in range(rlist.shape[1]):
    A = np.sign(np.real(rlist[:,i]))
    ii = next( (j for j,v in enumerate(A) if np.sign(v)!=np.sign(A[0])) , -1)
    if ii>=0 and klist[ii]<Kcrit:
        print(ii)
        # Kcrit = ( klist[ii] + klist[ii-1] )/2
        Kcrit = klist[ii]
        jj = np.argmin(abs(np.real(rlist[ii,:])))
        # wd = ( np.imag(rlist[ii,jj]) + np.imag(rlist[ii-1,jj]) )/2
        wd = np.imag(rlist[ii,jj])
        Pcrit = 2*np.pi/abs(wd)
print(f'Kcrit = {Kcrit} , Pcrit = {Pcrit} s')

if np.isinf(Kcrit):
    print("Método não aplicável para este sistema")


# Definição dos ganhos
if PID==0: # P
    K_p = .5*Kcrit; Ti = np.inf; Td = 0 
    K_i = 0; K_d = 0
elif PID==1: # PI
    K_p = .45*Kcrit; Ti = Pcrit/1.2; Td = 0 
    K_i = K_p/Ti; K_d = 0
elif PID==2: # PID
    K_p = .60*Kcrit; Ti = .5*Pcrit; Td = 0.125*Pcrit 
    K_i = K_p/Ti; K_d = K_p*Td


print(f'Kp = {K_p}, Ki = {K_i}, Kd = {K_d}')
print(f"T_i: {T_i}, T_d: {T_d}")

s = ct.TransferFunction.s

Gc = K_p + K_i/s + K_d*s
Gmf = ct.feedback(Gc * G)
Gcrit = ct.feedback(Kcrit * G)

# Resposta crítica
t, y_PID = ct.step_response(Gcrit, T=np.linspace(0, T, 1000))
plt.figure()
plt.plot(t, y_PID, color=cp['red'])
plt.xlabel('Tempo (s)')
plt.ylabel('Resposta')
plt.title('Resposta a Degrau para Kcrit')
plt.grid()
plt.legend()
plt.show()

# Diagrama de Bode para o controlador PID
plt.figure()
ct.bode_plot(Gc, omega=np.linspace(0.1, w, 1000), color=cp['red'], dB=True, Hz=True)
plt.suptitle('Diagrama de Bode do Controlador PID')
plt.show()


# Diagrama de Bode para o sistema em malha fechada com controlador PID
plt.figure()
ct.bode_plot(Gmf, omega=np.linspace(0.1, w, 1000), color=cp['purple'], dB=True, Hz=True)
plt.suptitle('Diagrama de Bode do Sistema em Malha Fechada com PID')
plt.show()

# Simulação da resposta a degrau do sistema em malha fechada com controlador PID
t, y_PID = ct.step_response(Gmf, T=np.linspace(0, T, 1000))
plt.figure()
plt.plot(t, y_PID, label='PID', color=cp['red'])
plt.xlabel('Tempo (s)')
plt.ylabel('Resposta')
plt.title('Resposta a Degrau do Sistema em Malha Fechada com PID')
plt.grid()
plt.legend()
plt.show()