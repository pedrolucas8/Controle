from ..bibliotecas import *
from ..structtype import structtype 


def controlador_alocacao_polos(P1, A, B, C, D):
    # Alocação de polos para o controlador
    # Ref: Capitulo 10 do livro Flight Dynamics Principles (Cook)
    # [P1, K1] = alocacao_Cook(A, B);
    
    K1 = scipy.signal.place_poles(A, B, P1, method="YT", maxiter=30)
    K1 = K1.gain_matrix
    F1 = A - np.matmul(B, K1)
    sys_mf1 = ct.ss(F1, B, C, D)

    Alocacao = structtype(
        Polos = P1,
        Ganhos = K1,
        F = F1,
        sys_mf = sys_mf1,
    )
    return Alocacao
