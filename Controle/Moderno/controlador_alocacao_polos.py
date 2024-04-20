from ..bibliotecas import *
from ..structtype import structtype


def controlador_alocacao_polos(A, B1, B2, C, D, P1):
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

    O método de alocação manual requer a escolha dos polos para o
    cálculo direto dos termos da matriz de ganhos K. Para os sistemas MIxO, a
    matriz não é única e é necessário outros requisitos numéricos (por padrão lstsq)
    """

    K1 = scipy.signal.place_poles(A, B2, P1, method="YT", maxiter=30)
    K1 = K1.gain_matrix

    F1 = A - np.matmul(B2, K1)
    C1 = C - np.matmul(D, K1)

    # B0 = np.zeros(B2.shape)
    D0 = np.zeros(D.shape)

    sys_mf1 = ct.ss(F1, B1, C1, D0)

    Alocacao = structtype(
        Polos=P1,
        Ganhos=K1,
        F=F1,
        sys_mf=sys_mf1,
    )
    return Alocacao
