from ..bibliotecas import *
from ..structtype import structtype


def controlador_lqr(A, B1, B2, C, D, Q_LQ, R_LQ):
    """Síntese do controlador linear quadrático

    Argumentos:
        A (matriz): Matriz de estados
        B1 (matriz): Matriz de entradas de distúrbio
        B2 (matriz): Matriz de entradas de controle
        C (matriz): Matriz de observacao
        D (matriz): Matriz de alimentação direta
    Calcula:
        K (2D array (or matrix)) - Matriz de ganho
        S (2D array (or matrix)) - Solução da Equação de Riccati
        P (1D array) - Autovalores do sistemas de malha fechada
    Retorna:
        LQR (struct): struct com as informações do projeto
    """

    """
    Sistema
        x' = A x + B1 xw + B2 u
        y  = C x + D u
    Assumindo que todo o vetor de estado possa ser obtido das medidas
    Ex: C é inversível e D=0; ou estado obtido por um observador
    A atuação de controle é dada por
        u = - K x
        x' = A x + B1 xw - B2 K x
        x' = (A - B2 K) x + B1 xw
    Ignorando o termo dos distúrbios
        x' = (A - B2 K) x
        x' = F x
    A estabilidade do sistema depende dos autovalores (polos) da matriz F.
    Esses polos podem ser alocados pelo designer através da matriz K

    O método de alocação Linear Quadratic Regulator (LQR) utiliza a teoria de
    controle ótimo para calcular a matriz de ganhos a partir de pesos relativos
    para atuação e estado.
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
