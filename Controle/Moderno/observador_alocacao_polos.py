from ..bibliotecas import *
from ..structtype import structtype 


def observador_alocacao_polos(A, C):
    """Síntese do observador atráves da alocação de polos

    Args:
        A (matriz): Matriz de estados
        C (matriz): Matriz de observação
    Calcula:
        K (matriz): Matriz de ganho
    Retorna:
        Alocacao (struct): struct com todas as informações sobre o sistema
    """
    P = np.array([-10 + 10j, -10 - 10j, -20, -30])
    K = scipy.signal.place_poles(
        A.transpose(), C.transpose(), P, method="YT", maxiter=30
    )
    K = K.gain_matrix.transpose()

    Alocacao = structtype()
    Alocacao.P = structtype(
        Polos = P,
        Ganhos = K,
    )
    return Alocacao
