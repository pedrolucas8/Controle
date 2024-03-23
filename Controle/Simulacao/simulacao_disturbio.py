from Controle import *


def simulacao_disturbio(sys, K, T, W):
    """Simulação no tempo do sistema dado uma 'entrada' de distúrbio

    Args:
        sys (sistema): sistema a ser simulado, malha aberta ou malha fechada
        K (matriz): matriz de ganho, se houver
        T (vetor): vetor de tempo (deve ser definido anteriormente)
        W (matriz): matriz de entrada de distúrbio para a simulação [deve ter dimensão 2 X len(T)]

    Returns:
        Simulacao: informações sobre a simulação feita
    """
    y_saida, _, x_saida = cmat.lsim(sys, W, T)
    u = np.matmul(-K, np.transpose(x_saida))  # entrada de controle dado o distúrbio

    Simulacao = structtype(
        entrada_disturbio=W,
        entrada_controle=u,
        saida_estados=x_saida,
        saida_observada=y_saida,
        sistema=sys,
    )

    return Simulacao
