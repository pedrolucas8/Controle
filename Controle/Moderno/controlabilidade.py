import os
import sys

# Obtém o caminho do diretório raiz do projeto
dir_raiz = os.path.dirname(os.path.abspath(__file__))

# Adiciona o caminho do diretório "Controle" ao sys.path
dir_controle = os.path.join(dir_raiz, "..")
sys.path.append(dir_controle)

# importando as bibliotecas necessárias
from bibliotecas import *
from struct_dict import *


def controlabilidade(resultado, A, B):
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

    resultado = Struct(resultado, "Controlabilidade", "CO", CO)
    resultado = Struct(resultado, "Controlabilidade", "controlavel", controlavel)
    resultado = Struct(resultado, "Controlabilidade", "posto", posto_CO)
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
    # Matriz de entradas de controle
    B2 = np.array([[-0.6862, 0.0813], [-7.4350, 0], [-183.7447, 0.3455], [0, 0]])

    resultado = dict()
    resultado = controlabilidade(resultado, A, B2)
    print(resultado)