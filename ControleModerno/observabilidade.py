# importando as bibliotecas necessárias
from bibliotecas import *
from struct_dict import *


def observabilidade(resultado, A, C):
    # A - matriz da planta do sistema
    # C - matriz de saida do sistema

    # == Analise da Observalidade == #

    # Calculo da matriz OB = [C^T, A^T*C^T, ..., A^(n-1)^T*C^T]

    OB = cmat.obsv(A, C)

    posto_OB = np.linalg.matrix_rank(OB)

    num_linhas, _ = np.shape(A)
    if posto_OB == num_linhas:
        print(
            f"O sistema é observável: ordem do sistema: {num_linhas} = posto(OB) = {posto_OB}"
        )
        observavel = True
    else:
        print(
            f"O sistema não é observável: ordem do sistema: {num_linhas} != posto(OB) = {posto_OB}"
        )
        observavel = False

    resultado = Struct(resultado, "Observabilidade", "OB", OB)
    resultado = Struct(resultado, "Observabilidade", "observavel", observavel)
    resultado = Struct(resultado, "Observabilidade", "posto", posto_OB)
    return resultado


if __name__ == "__main__":
    A = np.array(
        [
            [-0.2655, -0.1235, 0.8388, -9.7925],
            [-1.4412, -3.7332, 15.2192, 0.5863],
            [-0.3795, -6.3157, -4.7475, 0],
            [0, 0, 1, 0],
        ]
    )
    C = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])

    resultado = dict()
    resultado = observabilidade(resultado, A, C)
    print(resultado["Observabilidade"]["OB"])
