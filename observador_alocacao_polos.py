import control as ct
import numpy as np
import scipy

from uteis import *


def observador_alocacao_polos(resultado, A, C):
    """Síntese do observador atráves da alocação de polos

    Args:
        resultado (struct): struct com todas as informações sobre o sistema
        A (matriz): Matriz de estados
        C (matriz): Matriz de observação
    Calcula:
        K (matriz): Matriz de ganho
    Retorna:
        resultado (struct): struct com todas as informações sobre o sistema
    """
    P = np.array([-10 + 10j], [-10 - 10j], [-20], [-30])
    K = scipy.signal.place_poles(
        A.transpose(), C.transpose(), P, method="YT", maxiter=30
    )
    K = K.gain_matrix

    resultado = add_subTopico(resultado, "Observador", ["Alocacao", "P", "Polos"], P)
    resultado = add_subTopico(resultado, "Observador", ["Alocacao", "P", "Ganhos"], K)
    return resultado
