import numpy as np
from .structtype import structtype


def def_sistema(sist):
    # Matriz de estados. x = [u, w, q, theta]'
    A = np.array(
        [
            [-0.2655, -0.1235, 0.8388, -9.7925],
            [-1.4412, -3.7332, 15.2192, 0.5863],
            [-0.3795, -6.3157, -4.7475, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )

    # # Matriz de entrada de disturbios
    B1 = np.array(([-0.1235, 0.0], [-3.7332, -1.0], [-6.3157, 0.0], [0.0, 0.0]))

    # Matriz de entradas de controle
    B2 = np.array([[-0.6862, 0.0813], [-7.4350, 0.0], [-183.7447, 0.3455], [0.0, 0.0]])

    # Matriz de observacao y = [u, w]'
    C = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]])

    # Matriz de alimentação direta
    D1 = np.zeros((np.shape(C)[0], np.shape(B1)[1]))
    D2 = np.zeros((np.shape(C)[0], np.shape(B2)[1]))

    # Nome das variáveis
    estados = [
        "Vel. Horizontal (u)",
        "Vel. Vertical (w)",
        "Taxa Arfagem (q)",
        "Ang. Atitude (theta)",
    ]
    controle = ["Def. Profundor (eta)", "Tração (tau)"]
    perturbacoes = ["Vel. vertical (Ugust)", "Acel. vertical (U'gust)"]
    saidas = ["Vel. Horizontal (u)", "Vel. Vertical (w)"]

    # Salva o resultado
    sist.sistema = structtype(
        A=A,
        B1=B1,
        B2=B2,
        C=C,
        D1=D1,
        D2=D2,
        estados=estados,
        controle=controle,
        perturbacoes=perturbacoes,
        saidas=saidas,
    )
