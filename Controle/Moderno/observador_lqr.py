from ..bibliotecas import *
from ..structtype import structtype 


def observador_lqr(sys_malha_aberta, A, C, Qo, Ro):
    """Síntese do observador linear quadrático

    Args:
        A (matriz): Matriz de estados
        C (matriz): Matriz de observação
    Calcula:
        K (2D array (or matrix)) - Matriz de ganho
        S (2D array (or matrix)) - Solução da Equação de Riccati
        P (1D array) - Autovalores do sistemas de malha fechada
    Retorna:
        LQR: Struct que guarda todas as informações sobre o sistema
    """
    # C_obs = np.copy(C)
    # Qo = 10 * np.identity(4)  # minimizar o erro
    # Ro = np.identity(2)
    Ko_LQ, So, Po_LQ = ct.lqr(sys_malha_aberta, Qo, Ro)
    Ko_LQ = Ko_LQ.transpose()


    LQR = structtype(
        Polos = Po_LQ,
        Ganhos = Ko_LQ,
        Q = Qo,
        R = Ro,
    )
    return LQR


