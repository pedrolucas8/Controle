from matplotlib import style
from Controle import *


def seguidor_referencia_constante(A, B2, C, D, K_ref, T, estado=0, ref=0):

    linha_cima = np.hstack((A, B2))
    linha_baixo = np.hstack((C, D))

    A1 = np.vstack((linha_cima, linha_baixo))
    A2 = np.linalg.inv(A1)

    No = np.vstack((np.zeros((4, 1)), np.ones((2, 1))))
    Nxu = np.matmul(A2, No)

    Nx = Nxu[0:4]
    Nu = Nxu[4::]

    K = np.matmul(K_ref, Nx) + Nu
    B = np.matmul(B2, K)

    sys = ct.ss(A - np.matmul(B2, K_ref), B, C[estado, :], np.zeros((1, 1)))
    y_saida, t, x_saida = cmat.step(sys=sys, T=T, return_x=True)
    y_saida_seguidor = ref * y_saida
    x_saida_seguidor = ref * x_saida

    SeguidorConstante = structtype(
        vetor_tempo=t,
        saida=y_saida_seguidor,
        saida_estado=x_saida_seguidor,
        valor_referencia=ref,
        estado_referencia=estado,
    )

    return SeguidorConstante
