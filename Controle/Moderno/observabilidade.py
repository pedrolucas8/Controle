from ..bibliotecas import *
from ..structtype import structtype 


def observabilidade(A, C):
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

    Observabilidade = structtype(
        OB = OB,
        observavel = observavel,
        posto = posto_OB
    )
    return Observabilidade
