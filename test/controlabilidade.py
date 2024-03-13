from Controle.Moderno.controlabilidade import *

A = np.array(
    [
        [-0.2655, -0.1235, 0.8388, -9.7925],
        [-1.4412, -3.7332, 15.2192, 0.5863],
        [-0.3795, -6.3157, -4.7475, 0],
        [0, 0, 1, 0],
    ]
)
# Matriz de entradas de controle
B2 = np.array([[-0.6862, 0.0813], [-7.4350, 0], [-183.7447, 0.3455], [0, 0]])

sist = structtype()
sist.Controlabilidade = controlabilidade(A, B2)
sist.Controlabilidade.Show(printa_valores=True)
