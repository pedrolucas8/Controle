from ..bibliotecas import *
from ..structtype import structtype 


def controlabilidade(A, B):
    # A - matriz da planta do sistema
    # B - matriz de entrada do sistema

    # == Analise da Controlabilidade == #

    # Calculo da matriz CO = [B, AB, ..., A^(n-1)B]

    CO = cmat.ctrb(A, B)

    posto_CO = np.linalg.matrix_rank(CO)

    num_linhas, _ = np.shape(A)
    if posto_CO == num_linhas:
        print(
            f"O sistema é controlável: ordem do sistema: {num_linhas} = posto(CO) = {posto_CO}"
        )
        controlavel = True
    else:
        print(
            f"O sistema não é controlável: ordem do sistema: {num_linhas} != posto(CO) = {posto_CO}"
        )
        controlavel = False

    Controlabilidade = structtype( 
        CO = CO,
        controlavel = controlavel,
        posto = posto_CO
    )
    return Controlabilidade