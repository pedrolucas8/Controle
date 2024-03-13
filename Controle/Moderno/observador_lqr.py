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


def observador_lqr(resultado, sys_malha_aberta, A, C):
    """Síntese do observador linear quadrático

    Args:
        resultado (struct): struct que guarda todas as informações sobre o sistema
        A (matriz): Matriz de estados
        C (matriz): Matriz de observação
    Calcula:
        K (2D array (or matrix)) - Matriz de ganho
        S (2D array (or matrix)) - Solução da Equação de Riccati
        P (1D array) - Autovalores do sistemas de malha fechada
    Retorna:
        resultado: Struct que guarda todas as informações sobre o sistema
    """
    C_obs = np.copy(C)
    Qo = 10 * np.identity(4)  # minimizar o erro
    Ro = np.identity(2)
    Ko_LQ, So, Po_LQ = ct.lqr(sys_malha_aberta, Qo, Ro)
    Ko_LQ = Ko_LQ.transpose()

    resultado = Struct(resultado, "Observador", ["LQR", "P", "Polos"], Po_LQ)
    resultado = Struct(resultado, "Observador", ["LQR", "P", "Ganhos"], Ko_LQ)
    resultado = Struct(resultado, "Observador", ["LQR", "P", "Q"], Qo)
    resultado = Struct(resultado, "Observador", ["LQR", "P", "R"], Ro)

    return resultado


if __name__ == "__main__":
    Qo = 10 * np.identity(4)
    Ro = np.identity(2)
    print(Qo)
    print(Ro)
