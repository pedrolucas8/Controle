"""Controle Morderno

Retorna:
    resultado: struct com todas as informações sobre o sistema
"""

from .Moderno import *

def controle_moderno(sist):
    # VARIÁVEIS QUE SERÃO USADAS
    A  = sist.sistema.A
    B2 = sist.sistema.B2
    C  = sist.sistema.C
    D  = sist.sistema.D
    sys_malha_aberta = sist.sys_malha_aberta

    # ANÁLISE DE ESTABILIDADE
    sist.Malha_Aberta = estabilidade(A)
    
    # ANÁLISE DE CONTROLABILIDADE
    sist.Controlabilidade = controlabilidade(A, B2)

    # ANÁLISE DE OBSERVABILIDADE
    sist.Observabilidade = observabilidade(A, C)

    # ========== SÍNTESE DO CONTROLADOR ========== %
    # ALOCAÇÃO DE POLOS
    sist = controlador_alocacao_polos(sist, A, B2, C, D)
    # LINEAR QUADRÁTICO
    sist = controlador_lqr(sist, sys_malha_aberta, A, B2, C, D)

    # ========== SÍNTESE DO OBSERVADOR ========== %
    # ALOCAÇÃO DE POLOS
    sist = observador_alocacao_polos(sist, A, C)

    # LINEAR QUADRÁTICO
    sist = observador_lqr(sist, sys_malha_aberta, A, C)
