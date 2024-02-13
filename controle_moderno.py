"""Controle Morderno

Retorna:
    resultado: struct com todas as informações sobre o sistema
"""

from bibliotecas import *


def controle_moderno(resultado):
    # VARIÁVEIS QUE SERÃO USADAS
    A = resultado["A"]
    B2 = resultado["B2"]
    C = resultado["C"]
    D = resultado["D"]
    sys_malha_aberta = resultado["sys_malha_aberta"]

    # ANÁLISE DE ESTABILIDADE
    resultado = estabilidade(resultado, A)

    # ANÁLISE DE CONTROLABILIDADE
    resultado = controlabilidade(resultado, A, B2)

    # ANÁLISE DE OBSERVABILIDADE
    resultado = observabilidade(resultado, A, C)

    # ========== SÍNTESE DO CONTROLADOR ========== %
    # ALOCAÇÃO DE POLOS
    resultado = controlador_alocacao_polos(resultado, A, B2, C, D)
    # LINEAR QUADRÁTICO
    resultado = controlador_lqr(resultado, sys_malha_aberta, A, B2, C, D)

    # ========== SÍNTESE DO OBSERVADOR ========== %
    # ALOCAÇÃO DE POLOS
    resultado = observador_alocacao_polos(resultado, A, C)

    # # LINEAR QUADRÁTICO
    # resultado = observador_lqr(resultado, A, C)

    return resultado
