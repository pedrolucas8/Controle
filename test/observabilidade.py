from Controle.Moderno.observabilidade import *

A = np.array(
    [
        [-0.2655, -0.1235, 0.8388, -9.7925],
        [-1.4412, -3.7332, 15.2192, 0.5863],
        [-0.3795, -6.3157, -4.7475, 0],
        [0, 0, 1, 0],
    ]
)
C = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])

sist = structtype()
sist.Observabilidade = observabilidade(A, C)
print(sist.Observabilidade.OB)
