"""Controle Morderno

Retorna:
    sist: struct com todas as informações sobre o sistema
"""

from Controle import *
from Controle.Moderno import *

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
    sist.Controlador = structtype() 
    # ALOCAÇÃO DE POLOS
    polos = [
        np.array([-0.5 + 2j, -0.5 - 2j, -30 + 5j, -30 - 5j]),
        np.array([-0.5 + 4j, -0.5 - 4j, -25 - 1.5j, -25 + 1.5j]),
        np.array([-0.5 + 1j, -0.5 - 1j, -4.5 + 6j, -4.5 - 6j]),
        np.array([-0.1500 + 0.8133j, -0.1500 - 0.8133j, -25 + 1.9713j, -25 - 1.9713j]),
        np.array([-2, -4, -3 + 6j, -3 - 6j]),
    ]
    sist.Controlador.Alocacao = structtype()
    for i in range(len(polos)):
        lab = f"P{i+1}"
        val = controlador_alocacao_polos(polos[i], A, B2, C, D)
        sist.Controlador.Alocacao.SetAttr(lab,val)

    # LINEAR QUADRÁTICO
    Q_LQ = np.array([
        0.05,  # penaliza u
        0.2,  # penaliza w
        0.08,  # penaliza q
        1,  # penaliza theta
    ])
    R_LQ = np.array([
        1,  # penaliza eta
        0.1  # penaliza tau
    ])
    sist.Controlador.LQR = structtype()
    sist.Controlador.LQR.P = controlador_lqr(sys_malha_aberta, A, B2, C, D, np.diag(Q_LQ),np.diag(R_LQ))



    # ========== SÍNTESE DO OBSERVADOR ========== %
    sist.Observador = structtype() 
    # ALOCAÇÃO DE POLOS
    P = np.array([-10 + 10j, -10 - 10j, -20, -30])
    sist.Observador.Alocacao = structtype()
    sist.Observador.Alocacao.P = observador_alocacao_polos(P, A, C)

    # LINEAR QUADRÁTICO
    Qo = 10 * np.identity(Q_LQ.shape[0])  # minimizar o erro
    Ro = np.identity(R_LQ.shape[0])
    sist.Observador.LQR = structtype()
    sist.Observador.LQR.P = observador_lqr(sys_malha_aberta, A, C, Qo,Ro)
    
