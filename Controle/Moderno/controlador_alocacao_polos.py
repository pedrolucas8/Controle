from ..bibliotecas import *
from ..structtype import structtype


def controlador_alocacao_polos(A, B1, B2, C, D, P1):
    # Alocação de polos para o controlador
    # Ref: Capitulo 10 do livro Flight Dynamics Principles (Cook)
    # [P1, K1] = alocacao_Cook(A, B);

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
