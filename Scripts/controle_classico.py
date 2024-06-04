"""Controle Clássico

Retorna:
    sist: struct com todas as informações sobre o sistema
"""

from Controle import *
from Controle.Classico import *


def controle_classico(sist):
    # VARIÁVEIS QUE SERÃO USADAS
    A = sist.sistema.A
    B2 = sist.sistema.B2
    B1 = sist.sistema.B1
    C = sist.sistema.C
    D = sist.sistema.D
    sist.Classico = structtype()

    # ========== FUNCÕES DE TRANSFERÊNCIA ========== %
    sist.Classico.TFs = structtype()
    sist.Classico.TFs = funcao_transferencia()

    # ========== SÍNTESE DO CONTROLADOR ========== %


if __name__ == "__main__":
    controle_classico(sist)  # type: ignore
