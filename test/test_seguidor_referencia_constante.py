# from Controle import define_sistema
from Controle.Simulacao.seguidor_referencia_constante import (
    seguidor_referencia_constante,
)
from Controle.bibliotecas import *
from Controle.define_sistema import def_sistema
from Controle.structtype import structtype
from Controle.Moderno.controlador_lqr import controlador_lqr
from Scripts.malha_aberta import malha_aberta

sist = structtype()
def_sistema(sist)
malha_aberta(sist)
A = sist.sistema.A
B2 = sist.sistema.B2
B1 = sist.sistema.B1
C = sist.sistema.C
D = sist.sistema.D

Q_LQ = np.array(
    [
        0.05,  # penaliza u
        0.2,  # penaliza w
        0.08,  # penaliza q
        1,  # penaliza theta
    ]
)
R_LQ = np.array([1, 0.1])  # penaliza eta  # penaliza tau

sist.Controlador = structtype()
sist.Controlador.LQR = structtype()
sist.Controlador.LQR.P = controlador_lqr(
    A=A,
    B2=B2,
    B1=B1,
    C=C,
    D=D,
    Q_LQ=np.diag(Q_LQ),
    R_LQ=np.diag(R_LQ),
)

K_ref = sist.Controlador.LQR.P.Ganhos  # matriz de ganho
T = np.arange(0, 20, 0.01)  # vetor de tempo
estado = 0  # indice do estado que você que observar (referência vem da matriz C, neste caso 0 corresponde à vel. horizontal)
ref = 3  # valor da referência (ex. 3 m/s)
SeguidorConstante = seguidor_referencia_constante(
    A=A, B2=B2, C=C, D=D, K_ref=K_ref, T=T, estado=estado, ref=ref
)

t = SeguidorConstante.vetor_tempo
y_seguidor = SeguidorConstante.saida
x_seguidor = SeguidorConstante.saida_estado
ref = SeguidorConstante.valor_referencia
estado = SeguidorConstante.estado_referencia


import matplotlib.pyplot as plt

plt.plot(t, y_seguidor)
plt.plot(t, ref * np.ones(np.shape(t)), "--", label="Referência")
plt.title("Seguidor de Refencia Constante")
plt.grid()
plt.legend()
plt.show()

plt.plot(t, x_seguidor)
plt.plot(t, ref * np.ones(np.shape(t)), "--", label="Referência")
plt.title("Seguidor de Refencia Constante")
plt.grid()
plt.legend()
plt.show()
