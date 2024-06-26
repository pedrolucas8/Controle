from Controle import *
from Controle.EspacoEstado import *

def malha_aberta(sist):
    A = sist.sistema.A
    # B1 = sist.sistema.B1
    B2 = sist.sistema.B2
    C = sist.sistema.C
    D = sist.sistema.D
    lbl_estados = sist.sistema.estados
    lbl_controle = sist.sistema.controle
    # lbl_perturbacoes = sist.sistema.perturbacoes
    lbl_saidas = sist.sistema.saidas
    
    # ========== ESPAÇO DE ESTADOS ========== %
    # Malha aberta - controle
    sist.sys_malha_aberta = ct.ss(
        A,
        B2,
        C,
        D,
        inputs=lbl_controle,
        outputs=lbl_saidas,
        states=lbl_estados,
    )

    # Malha aberta - perturbações

    # ========== ANÁLISES DO SISTEMA ========== %
    # ANÁLISE DE ESTABILIDADE
    sist.Malha_Aberta = estabilidade(A)
    
    # ANÁLISE DE CONTROLABILIDADE
    sist.Controlabilidade = controlabilidade(A, B2)

    # ANÁLISE DE OBSERVABILIDADE
    sist.Observabilidade = observabilidade(A, C)




if __name__=="__main__":
    malha_aberta(sist) # type: ignore
