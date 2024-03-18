import numpy as np
import math


def matriz_transicao_forcante(A, dt=0.1, k=5):
    """Cálculo da mamtriz de transição e do termo forçante para o sistema

    phi(dt) = e^[Adt]

    Args:
        A (matriz): matriz de estados do sistema
        dt (decimal, opicional): intervalo de tempo. Defaults to 0.001.
        k (inteiro, opicional): quantidades de termos da série a ser calculada. Defaults to 4.

    Returns:
        Phi: matriz de transição
        Gamma: matriz do termo forçante
    """
    Phi = np.zeros(shape=np.shape(A))
    Gamma = np.zeros(shape=np.shape(A))

    for i in range(k):
        Phi += (A**i * dt**i) / math.factorial(i)
        Gamma += (A**i * dt**i) / math.factorial(i + 1)
    Gamma *= dt

    return Phi, Gamma


def simulacao_degrau_transicao_forcante(Phi, Gamma, B, x0=None, dt=0.1, n=20):
    """Simulação de uma entrada degrau utilizando as matrizes de transição e do termo forçante

    Observação:
        Para pegar a primeira saída usa-se: x[0, :]
        Para pegar a n-ésima saída usa-se: x[n, :]

    Args:
        Phi (matriz): matriz de transição
        Gamma (matriz): matriz do termo forçante
        B (matriz): matriz de entradas do sistema
        x0 (matriz coluna, optional): condições iniciais. Defaults to np.array([[0], [0]]).
        dt (decimal, optional): intervalo de tempo. Defaults to 0.001.
        n (inteiro, optional): quantidade de intervalos de tempo. Defaults to 20.

    Returns:
        x: vetor de resposta para cada instante t
        t: vetor de tempo
    """

    # inicializando o vetor de tempo
    t = np.arange(start=0, stop=dt * (n + 1), step=dt)

    # entrada degrau
    u = 1

    # Condições iniciais
    if x0 is None:
        x0 = np.zeros((Phi.shape[0], 1))
    else:
        if x0.shape != (Phi.shape[0], 1):
            raise ValueError("x0 deve ter o mesmo número de linhas que Phi.")
        x[:, 0] = x0.flatten()

    # inicializando o vetor x (qtd. linhas de x0, qtd. colunas de t)
    x = np.zeros((np.shape(x0)[0], len(t)))

    # adicionando as condições iniciais
    x[:, 0] = x0.flatten()

    # cálculo dos valores de x(t) para cada instante de tempo
    for i in range(1, len(t)):
        x[:, i] = np.dot(Phi, x[:, i - 1]) + np.dot(Gamma, B).flatten() * u

    return x, t


if __name__ == "__main__":
    A = np.matrix([[0, 1], [-100, 0]])
    B = np.matrix([[0], [10]])

    p, g = matriz_transicao_forcante(A, dt=0.2, k=4)

    x, t = simulacao_degrau_transicao_forcante(p, g, B, dt=0.2)

    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(t, x[0, :])
    plt.show()
    plt.figure()
    plt.plot(t, x[1, :], c="red")
    plt.show()
