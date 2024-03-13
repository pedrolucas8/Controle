from Controle.Moderno.controlador_alocacao_polos import *

A = np.array(
    [
        [-0.2655, -0.1235, 0.8388, -9.7925],
        [-1.4412, -3.7332, 15.2192, 0.5863],
        [-0.3795, -6.3157, -4.7475, 0],
        [0, 0, 1, 0],
    ]
)
B2 = np.array([[-0.6862, 0.0813], [-7.4350, 0], [-183.7447, 0.3455], [0, 0]])
(_, colunas_B2) = np.shape(B2)

C = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
(linhas_C, _) = np.shape(C)

D = np.zeros((linhas_C, colunas_B2))

sist = structtype()
sist.Controlador = structtype()
sist.Controlador.Alocacao = controlador_alocacao_polos(A, B2, C, D)
print(sist.Controlador.Alocacao.P2.Ganhos)