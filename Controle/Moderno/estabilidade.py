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


def estabilidade(resultado, A):
    # A - matriz da planta do sistema
    polos, _ = np.linalg.eig(A)  # polos = autovalores de A
    if any(polos > 0):
        print("O sistema é instável: pelo menos um autovalor de A é maior que 0.")
        estavel = False
    else:
        print("O sistema é estável: nenhum autovalor de A é maior que 0.")
        estavel = True

    resultado = Struct(resultado, "Malha_Aberta", "polos", polos)
    resultado = Struct(resultado, "Malha_Aberta", "estavel", estavel)

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

    resultado = dict()

    resultado = estabilidade(resultado, A)
    print(resultado)
