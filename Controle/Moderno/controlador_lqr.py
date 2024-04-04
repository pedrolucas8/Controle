from ..bibliotecas import *
from ..structtype import structtype


def controlador_lqr(A, B1, B2, C, D, Q_LQ, R_LQ):
    """Síntese do controlador linear quadrático

    Argumentos:
        sys_malha_aberta (sys): sistema de malha aberta
        A (matriz): Matriz de estados
        B2 (matriz): Matriz de entradas de controle
        B2 (matriz): Matriz de entradas de distúrbio
        C (matriz): Matriz de observacao
        D (matriz): Matriz de alimentação direta
    Calcula:
        K (2D array (or matrix)) - Matriz de ganho
        S (2D array (or matrix)) - Solução da Equação de Riccati
        P (1D array) - Autovalores do sistemas de malha fechada
    Retorna:
        LQR (struct): struct com as informações do projeto
    """

    K_LQ, S, P_LQ = ct.lqr(A, B2, Q_LQ, R_LQ)

    F_LQ = A - np.matmul(B2, K_LQ)
    C_LQ = C - np.matmul(D, K_LQ)

    # B0 = np.zeros(B.shape)
    D0 = np.zeros(D.shape)

    sys_mf_LQ = ct.ss(F_LQ, B1, C_LQ, D0)

    LQR = structtype(
        Polos=P_LQ,
        Ganhos=K_LQ,
        F=F_LQ,
        Q=Q_LQ,
        R=R_LQ,
        sys_mf=sys_mf_LQ,
    )
    return LQR
