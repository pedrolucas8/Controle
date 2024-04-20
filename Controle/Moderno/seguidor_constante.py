from ..bibliotecas import *
from ..structtype import structtype


def seguidor_constante(A, B1, B2, C, D, K):

    """
    Sistema
        x' = A x + B1 xw + B2 u
        y  = C x + D u
    Em regime permanente
        0   = A xrp + B2 urp + B1 xw 
        yrp = C xrp + D  urp
    Deseja-se que a medida siga uma referência
        yrp = xr
    E o controle compense o erro de regime permanente
        u = urp - K (x-xrp)
    É razoável assumir que
        xrp = Nx xr -> Nx tamanho (nx, ny)
        urp = Nu xr -> Nu tamanho (nu, ny)
    Voltando para a equação de regime permanente
        0 xr = A Nx xr + B2 Nu xr + B1 xw 
        I xr = C Nx xr + D  Nu xr
    Ignorando o termo dos distúrbios, 
    para um caso não trivial (xr!=0)
        A Nx + B2 Nu = 0
        C Nx + D  Nu = I
    Ou seja
        Lambda Nxu = RHS
    Resolvendo para Nxu, obtemos a nova dinâmica
        x' = (A - B2 K) x + B2 (Nu + K Nx) xr + B1 xw
        y  = (C - D  K) x + D  (Nu + K Nx) xr
    """

    nx = A.shape[1]
    nu = B2.shape[1]
    ny = C.shape[0]
    
    linha_cima = np.hstack((A, B2))
    linha_baixo = np.hstack((C, D))

    Lambda = np.vstack((linha_cima, linha_baixo))
    RHS = np.vstack((np.zeros((nx, ny)), np.identity(ny)))
    Nxu = np.linalg.solve(Lambda,RHS)

    Nx = Nxu[:nx,:]
    Nu = Nxu[-nu:,:]

    N = K@Nx + Nu

    F  = A - B2@K
    Br = B2@N
    Cr = C - D@K
    Dr = D@N

    sys_mf1 = ct.ss(F, Br, Cr, Dr)

    Seguidor = structtype(
        Ganhos = K,
        F = F,
        Nx = Nx,
        Nu = Nu,
        sys_mf=sys_mf1,
    )
    return Seguidor
