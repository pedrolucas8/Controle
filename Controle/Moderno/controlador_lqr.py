from ..bibliotecas import *
from ..structtype import structtype 


def controlador_lqr(sys_malha_aberta, A, B, C, D):
    """Síntese do controlador linear quadrático

    Argumentos:
        sys_malha_aberta (sys): sistema de malha aberta
        A (matriz): Matriz de estados
        B2 (matriz): Matriz de entradas de controle
        C (matriz): Matriz de observacao
        D (matriz): Matriz de alimentação direta
    Calcula:
        K (2D array (or matrix)) - Matriz de ganho
        S (2D array (or matrix)) - Solução da Equação de Riccati
        P (1D array) - Autovalores do sistemas de malha fechada
    Retorna:
        resultado (struct): struct com as informações do projeto
    """
    Q1 = 0.05  # penaliza u
    Q2 = 0.2  # penaliza w
    Q3 = 0.08  # penaliza q
    Q4 = 1  # penaliza theta

    Q_LQ_controlador = np.array(
        [[Q1, 0, 0, 0], [0, Q2, 0, 0], [0, 0, Q3, 0], [0, 0, 0, Q4]]
    )

    R1 = 1  # penaliza eta
    R2 = 0.1  # penaliza tau
    R_LQ_controlador = np.array([[R1, 0], [0, R2]])

    K_LQ, S, P_LQ = ct.lqr(sys_malha_aberta, Q_LQ_controlador, R_LQ_controlador)

    F_LQ = A - B * K_LQ
    sys_mf_LQ = ct.ss(F_LQ, B, C, D)
    LQR = structtype()
    LQR.P = structtype(
        Polos = P_LQ,
        Ganhos = K_LQ,
        F = F_LQ,
        Q = Q_LQ_controlador,
        R = R_LQ_controlador,
        sys_mf = sys_mf_LQ
    )

    return LQR
